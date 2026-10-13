"""Carga a Supabase las notas de la revision manual de notebooks (alumnos cuyo envio no llego a la BD).

Uso:
    python notas_manuales.py                         # vista previa de data/notas_manuales.csv (no escribe nada)
    python notas_manuales.py --enviar                # inserta las filas de la vista previa
    python notas_manuales.py 71234567 nb6 72         # un solo alumno (vista previa); agregar --enviar para insertar
    python notas_manuales.py 71234567 nb6 85% --enviar

data/notas_manuales.csv (ignorada por git: tiene DNIs). Columnas:
    dni, notebook, puntos               obligatorias. `puntos` = puntos core sobre _CORE_MAX, o un porcentaje ("85%")
    nombre, grado                       opcionales: solo hacen falta si el alumno no tiene NINGUN envio en la BD
    fecha                               opcional, hora Peru "2026-10-05 14:30". Por defecto: 1 minuto antes del limite
                                        (examen_final no tiene limite: por defecto la hora en que lo cargas)

Examen final: notebook = examen_final, puntos = nota sobre 20 (ej. 71234567,examen_final,16).
    comentario                          opcional, solo para tu registro (no se sube)

Cada nota se inserta como un envio mas en `submissions` (mismo camino que el autograder, clave anon):
el leaderboard y Power BI ya toman el mejor envio por alumno, asi que no hay que borrar ni editar nada.
Las filas manuales se reconocen por email = "revision_manual". Si el alumno ya tiene en la BD un envio
con igual o mas puntos en ese notebook, la fila se salta (no cambiaria su nota).

Mantener TAREAS sincronizado con Meta en Tareas.tmdl (_CORE_MAX y fecha limite de cada autograder).
"""
import argparse
import ast
import csv
import datetime as dt
import sys
from collections import Counter
from pathlib import Path

import requests

from item_intentos import ALIAS_DNI, KEY, URL

ROOT = Path(__file__).resolve().parent.parent
CSV_DEFAULT = Path(__file__).parent / "data" / "notas_manuales.csv"
CURSO = "STAT_2026"
MARCA = "revision_manual"
PERU = dt.timezone(dt.timedelta(hours=-5))

# notebook -> (_CORE_MAX, fecha limite UTC, autograder del que se leen los niveles)
TAREAS = {
    "nb1_semana1": (101, dt.datetime(2026, 8, 17, 4, 59), "Weeks 1-2/autograder_nb1_semana1.py"),
    "nb1_semana2": (177, dt.datetime(2026, 8, 24, 4, 59), "Weeks 1-2/autograder_nb1_semana2.py"),
    "nb3":         (200, dt.datetime(2026, 8, 31, 4, 59), "Weeks 3-4/autograder_nb3.py"),
    "nb3_lite":    (70,  dt.datetime(2026, 8, 31, 4, 59), "Weeks 3-4/autograder_nb3.py"),
    "nb4":         (60,  dt.datetime(2026, 9, 7, 4, 59),  "Weeks 3-4/autograder_nb4.py"),
    "nb4_lite":    (55,  dt.datetime(2026, 9, 7, 4, 59),  "Weeks 3-4/autograder_nb4.py"),
    "nb5":         (102, dt.datetime(2026, 9, 22, 4, 59), "Week 6/autograder_nb5.py"),
    "nb6":         (87,  dt.datetime(2026, 10, 6, 4, 59), "Week 7/autograder_nb6.py"),
    # Examen en papel: nota vigesimal, sin fecha limite ni autograder (fecha por defecto = ahora).
    "examen_final": (20, None, None),
}

# Niveles CNB para lo que no tiene autograder (umbral %, num, nombre): AD 18-20, A 14-17, B 11-13, C 0-10
_NIVELES_CNB = [(88, 4, "AD"), (68, 3, "A"), (53, 2, "B"), (0, 1, "C")]


def niveles(autograder):
    """Lee la lista _LEVELS [(umbral, num, nombre), ...] del autograder sin ejecutarlo."""
    if autograder is None:
        return _NIVELES_CNB
    tree = ast.parse((ROOT / "course-python-stats" / autograder).read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "_LEVELS" for t in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError(f"No encontre _LEVELS en {autograder}")


def nivel(pct, levels):
    for umbral, num, nombre in levels:
        if pct >= umbral:
            return num, nombre
    return levels[-1][1], levels[-1][2]


def envios_previos(dni):
    """Todos los envios del alumno (cualquier notebook), incluidos los de DNIs mal escritos que apuntan a este."""
    dnis = [dni] + [mal for mal, bien in ALIAS_DNI.items() if bien == dni]
    r = requests.get(URL, params={"select": "dni,nombre,grado,curso,notebook,earned,submitted_at",
                                  "dni": f"in.({','.join(dnis)})", "order": "submitted_at.asc"},
                     headers={"apikey": KEY}, timeout=30)
    r.raise_for_status()
    return r.json()


def preparar(fila):
    """Valida una fila del CSV y devuelve (payload para insertar o None, mensaje)."""
    dni = ALIAS_DNI.get(fila["dni"].strip(), fila["dni"].strip())
    nb = fila["notebook"].strip()
    if nb not in TAREAS:
        return None, f"notebook '{nb}' desconocido (opciones: {', '.join(TAREAS)})"
    core_max, limite, autograder = TAREAS[nb]

    bruto = fila["puntos"].strip()
    puntos = round(float(bruto[:-1]) / 100 * core_max) if bruto.endswith("%") else int(float(bruto))
    if not 0 <= puntos <= core_max:
        return None, f"puntos {puntos} fuera de rango (0-{core_max} para {nb})"

    previos = envios_previos(dni)
    nombres = [p["nombre"] for p in previos if p.get("nombre")]
    nombre = (fila.get("nombre") or "").strip() or (Counter(nombres).most_common(1)[0][0] if nombres else "")
    grado = (fila.get("grado") or "").strip() or next((p["grado"] for p in reversed(previos) if p.get("grado")), "")
    if not nombre or not grado:
        return None, "sin envios previos en la BD: agrega columnas nombre y grado en el CSV"

    mejor = max((p["earned"] for p in previos if p["notebook"] == nb and (p["curso"] or CURSO) == CURSO), default=None)
    if mejor is not None and mejor >= puntos:
        return None, f"ya tiene {mejor}/{core_max} en la BD (>= {puntos}), nada que hacer"

    if (fila.get("fecha") or "").strip():
        cuando = dt.datetime.strptime(fila["fecha"].strip(), "%Y-%m-%d %H:%M").replace(tzinfo=PERU)
    elif limite is None:
        cuando = dt.datetime.now(dt.timezone.utc)
    else:
        cuando = limite.replace(tzinfo=dt.timezone.utc) - dt.timedelta(minutes=1)

    pct = min(100, round(puntos / core_max * 100))
    lvl_num, lvl_name = nivel(pct, niveles(autograder))
    payload = {
        "email": MARCA, "dni": dni, "nombre": nombre, "grado": grado, "curso": CURSO, "notebook": nb,
        "earned": puntos, "possible": core_max, "pct": pct, "level_num": lvl_num, "level_name": lvl_name,
        "achievements": [], "streak": 0,
        # Sin items: Items / ItemIntentos no inventan intentos por ejercicio para una nota manual.
        "score_breakdown": {},
        "submitted_at": cuando.astimezone(dt.timezone.utc).isoformat(),
    }
    antes = "sin envios" if mejor is None else f"antes {mejor}/{core_max}"
    return payload, f"{nombre} ({grado}) · {nb}: {puntos}/{core_max} = {pct}% · {lvl_name} · {antes}"


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # los nombres de nivel traen emojis; la consola de Windows usa cp1252
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("uno", nargs="*", metavar="DNI NOTEBOOK PUNTOS", help="cargar un solo alumno en vez del CSV")
    ap.add_argument("--csv", type=Path, default=CSV_DEFAULT)
    ap.add_argument("--enviar", action="store_true", help="insertar en Supabase (sin esto solo muestra la vista previa)")
    args = ap.parse_args()

    if args.uno:
        if len(args.uno) != 3:
            ap.error("para un solo alumno: DNI NOTEBOOK PUNTOS")
        filas = [dict(zip(("dni", "notebook", "puntos"), args.uno))]
    else:
        if not args.csv.exists():
            args.csv.parent.mkdir(exist_ok=True)
            args.csv.write_text("dni,notebook,puntos,nombre,grado,fecha,comentario\n", encoding="utf-8")
            sys.exit(f"Cree {args.csv} vacio: llenalo (una fila por alumno x notebook) y vuelve a correr.")
        with open(args.csv, encoding="utf-8-sig", newline="") as f:
            filas = [r for r in csv.DictReader(f) if (r.get("dni") or "").strip()]

    listos = []
    for i, fila in enumerate(filas, 1):
        try:
            payload, msg = preparar(fila)
        except (ValueError, KeyError, requests.RequestException) as ex:
            payload, msg = None, f"error: {ex}"
        print(f"{'OK  ' if payload else 'SKIP'} [{i}] DNI {fila.get('dni', '').strip()} · {msg}")
        if payload:
            listos.append(payload)

    if not listos:
        print("\nNada para insertar.")
        return
    if not args.enviar:
        print(f"\nVista previa: {len(listos)} fila(s). Corre otra vez con --enviar para insertarlas.")
        return
    r = requests.post(URL, json=listos, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}",
                                                 "Content-Type": "application/json", "Prefer": "return=minimal"},
                      timeout=30)
    if r.status_code >= 300:
        sys.exit(f"\nSupabase rechazo el envio ({r.status_code}): {r.text}")
    print(f"\nInsertadas {len(listos)} fila(s). Refresca Power BI (y corre item_intentos.py) para verlas.")


if __name__ == "__main__":
    main()
