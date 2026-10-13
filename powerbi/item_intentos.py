"""Reconstruye la secuencia de intentos por item (REPORT_SPEC.md §2.4) y la deja en CSV para Power BI.

Uso (antes de refrescar el reporte):
    python item_intentos.py

Escribe en powerbi/data/ (ignorada por git: tiene DNIs):
    item_intentos.csv  un renglon por intento de cada item (StudentKey x TareaKey x Item x NumIntento)
    item_resumen.csv   un renglon por StudentKey x TareaKey x Item (PrimerIntentoOK, ResueltoFinal, SegundosCorreccion)

Las tablas ItemIntentos e ItemResumen del modelo leen estos archivos desde el parametro CarpetaDatos.
Se hace en Python y no en Power Query porque el algoritmo recorre los envios en orden con estado
(ultimo item cambiado), algo lento y dificil de mantener en M.

Mantener sincronizado con expressions.tmdl (SubmissionsRaw) y Tareas.tmdl (AliasDNI):
TEST_IDS, ALIAS_DNI y la limpieza de StudentKey / TareaKey tienen que dar las mismas claves que el modelo.
"""
import csv
import re
from pathlib import Path

import requests

URL = "https://uwykikwutjtkpffwmdiq.supabase.co/rest/v1/submissions"
KEY = "sb_publishable_aBG6GD4wn9CgpSE-47fagQ_sNhnzznu"  # clave publica de solo lectura (la de los leaderboards)
OUT = Path(__file__).parent / "data"

TEST_IDS = {"TEST", "INTEGRATION_TEST", "SCRATCH"}
ALIAS_DNI = {  # canonico = DNI del padron (data/padron.csv)
    "7725963": "77257963", "12345": "63074377", "C74HY1XKH": "00000002", "216362172": "00000001",
    "62482920": "62483930", "74771144": "74114477", "00910804": "9108094",
}
EXCLUIDOS = {"Teoria", "Registro"}  # Teoria: una sola respuesta, queda bloqueada. Registro: 1 punto por participar.


def fetch():
    cols = "id,dni,email,curso,notebook,score_breakdown,submitted_at"
    rows, offset = [], 0
    while True:
        page = requests.get(URL, params={"select": cols, "order": "submitted_at.asc,id.asc", "offset": offset, "limit": 1000},
                            headers={"apikey": KEY}, timeout=60).json()
        rows += page
        if len(page) < 1000:
            return rows
        offset += 1000


def tipo(item):
    """Misma clasificacion que la columna Items[Tipo] del modelo."""
    k = item.lower()
    for prefix, t in [("intex", "Integracion"), ("debug", "Debug"), ("ex", "Ejercicio"), ("reto", "Reto (bonus)"),
                      ("refl", "Reflexion"), ("reg", "Registro"), ("mini", "Checkpoint")]:
        if k.startswith(prefix):
            return t
    return "Teoria" if re.match(r"t\d", k) else "Otro"


def clean(rows):
    """Replica SubmissionsRaw: alias de DNI, sin cuentas de prueba, curso por defecto CS_2026."""
    out = []
    for r in rows:
        dni = (str(r["dni"]).strip() if r["dni"] is not None else None)
        email = (str(r["email"]).strip() if r["email"] is not None else None)
        dni = ALIAS_DNI.get(dni, dni)
        alumno = dni if dni else email
        if not alumno or (dni or "").upper() in TEST_IDS or (email or "").upper() in TEST_IDS:
            continue
        curso = r["curso"] or "CS_2026"
        out.append({**r, "StudentKey": f"{curso}|{alumno}", "TareaKey": f"{curso}|{r['notebook']}"})
    return out


def intentos(rows):
    """§2.4: un item tiene un intento cuando aparece por primera vez o cambia su `e` (o su `text`).
    Un envio que no cambia nada se asigna al ultimo item cambiado si ese item aun no tiene el puntaje maximo."""
    pares = {}
    for r in sorted(rows, key=lambda r: (r["submitted_at"], r["id"])):
        pares.setdefault((r["StudentKey"], r["TareaKey"]), []).append(r)

    out = []
    for (sk, tk), envios in pares.items():
        prev, ultimo, n = {}, None, {}
        for r in envios:
            sb = r["score_breakdown"] if isinstance(r["score_breakdown"], dict) else {}
            cambiados = [k for k, v in sb.items()
                         if k not in prev or v.get("e") != prev[k].get("e") or v.get("text") != prev[k].get("text")]
            if cambiados:
                for k in cambiados:
                    n[k] = n.get(k, 0) + 1
                    out.append((sk, tk, k, n[k], r["submitted_at"], sb[k].get("e"), sb[k].get("p")))
                ultimo = cambiados[-1]
            elif ultimo is not None:
                v = prev[ultimo]
                if (v.get("e") or 0) < (v.get("p") or 0):
                    n[ultimo] += 1
                    out.append((sk, tk, ultimo, n[ultimo], r["submitted_at"], v.get("e"), v.get("p")))
            prev = {**prev, **sb}
    return [dict(zip(["StudentKey", "TareaKey", "Item", "NumIntento", "FechaHoraUTC", "Puntos", "PuntosPosibles"], a),
                 Tipo=tipo(a[2])) for a in out if tipo(a[2]) not in EXCLUIDOS]


def resumen(filas):
    from datetime import datetime
    grupos = {}
    for f in filas:
        grupos.setdefault((f["StudentKey"], f["TareaKey"], f["Item"]), []).append(f)
    out = []
    for (sk, tk, item), g in grupos.items():
        g.sort(key=lambda f: f["NumIntento"])
        ok = [(f["Puntos"] or 0) >= (f["PuntosPosibles"] or 0) for f in g]
        seg = None
        if not ok[0] and any(ok):
            i = ok.index(True)
            t = [datetime.fromisoformat(g[j]["FechaHoraUTC"]) for j in (i - 1, i)]
            seg = round((t[1] - t[0]).total_seconds(), 1)
        out.append({"StudentKey": sk, "TareaKey": tk, "Item": item, "Tipo": g[0]["Tipo"], "Intentos": len(g),
                    "PrimerIntentoOK": ok[0], "ResueltoFinal": any(ok), "SegundosCorreccion": seg})
    return out


def write(path, filas, cols):
    path.parent.mkdir(exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for f in filas:
            w.writerow({c: ("" if f[c] is None else f[c]) for c in cols})


def main():
    filas = intentos(clean(fetch()))
    for f in filas:  # UTC sin zona, igual que Envios[FechaHoraUTC]
        f["FechaHoraUTC"] = f["FechaHoraUTC"].replace("Z", "+00:00")
    res = resumen(filas)
    for f in filas:
        f["FechaHoraUTC"] = f["FechaHoraUTC"][:19]
    write(OUT / "item_intentos.csv", filas,
          ["StudentKey", "TareaKey", "Item", "Tipo", "NumIntento", "FechaHoraUTC", "Puntos", "PuntosPosibles"])
    write(OUT / "item_resumen.csv", res,
          ["StudentKey", "TareaKey", "Item", "Tipo", "Intentos", "PrimerIntentoOK", "ResueltoFinal", "SegundosCorreccion"])
    print(f"{len(filas)} intentos y {len(res)} items en {OUT}")


if __name__ == "__main__":
    main()
