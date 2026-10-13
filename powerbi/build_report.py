"""Genera el reporte PBIR de SMA_Tareas_Master (paginas + visuales).

Edita las paginas aqui y vuelve a correr `python build_report.py`; no edites a mano
los visual.json de SMA_Tareas_Master.Report/definition/pages (se borran y regeneran).
El modelo semantico (SMA_Tareas_Master.SemanticModel) NO lo toca este script.
"""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).parent / "SMA_Tareas_Master.Report" / "definition"
SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition"
M = "_Medidas"

# ── tema "DataNest" (oscuro, morado / naranja / dorado) ──────────────
PAGE_BG, CARD_BG, CARD_ALT, BORDER = "#0E0E12", "#17171D", "#1D1D25", "#2A2A33"
TEXT, TEXT_2, TEXT_3 = "#FFFFFF", "#9A9AA5", "#6B6B76"
# ORANGE #DB6C14 (antes #E8761A) pasa la prueba de luminosidad sobre CARD_BG y, junto al morado, los chequeos de daltonismo.
# Reglas (REPORT_SPEC §4): morado = dato principal, gris TEXT_3 = contexto, naranja solo para "bajo" / "Desaprobo".
PURPLE, ORANGE, GOLD, INDIGO = "#8B5CF6", "#DB6C14", "#F2C14E", "#4F46A5"
# Escala divergente de notas y tasas: naranja = bajo, neutro en 55 (umbral real de aprobado), morado = alto
LOW, MID, HIGH = ORANGE, "#2A2A33", "#7C3AED"
THEME_NAME = "DataNest"


def solid(color):
    return {"solid": {"color": color}}


THEME = {
    "name": THEME_NAME,
    "dataColors": [PURPLE, ORANGE, GOLD, INDIGO, "#C4B5FD", "#B45309", "#A78BFA", "#FCD34D"],
    "foreground": TEXT, "foregroundNeutralSecondary": TEXT_2, "foregroundNeutralTertiary": TEXT_3,
    "background": CARD_BG, "backgroundLight": CARD_ALT, "backgroundNeutral": BORDER,
    "tableAccent": PURPLE, "hyperlink": "#A78BFA", "visitedHyperlink": "#C4B5FD",
    "good": PURPLE, "neutral": GOLD, "bad": ORANGE,
    "maximum": HIGH, "center": MID, "minimum": LOW, "null": TEXT_3,
    "textClasses": {
        "title": {"fontFace": "Segoe UI Semibold", "fontSize": 12, "color": TEXT},
        "header": {"fontFace": "Segoe UI Semibold", "fontSize": 12, "color": TEXT},
        "callout": {"fontFace": "Segoe UI Semibold", "fontSize": 26, "color": TEXT},
        "label": {"fontFace": "Segoe UI", "fontSize": 10, "color": TEXT_2},
    },
    "visualStyles": {
        "*": {"*": {
            "background": [{"show": True, "color": solid(CARD_BG), "transparency": 0}],
            "border": [{"show": True, "color": solid(BORDER), "radius": 12}],
            "dropShadow": [{"show": False}],
            "padding": [{"top": 12, "bottom": 12, "left": 14, "right": 14}],
            "title": [{"show": True, "fontColor": solid(TEXT), "fontSize": 12, "fontFamily": "Segoe UI Semibold"}],
            # "Mostrar como tabla" en todos los visuales: ningun valor depende solo del tooltip
            "visualHeader": [{"background": solid(CARD_BG), "border": solid(BORDER), "foreground": solid(TEXT_2),
                              "showSeeDataLayoutToggleButton": True}],
            "categoryAxis": [{"labelColor": solid(TEXT_2), "titleColor": solid(TEXT_2), "showAxisTitle": False,
                              "gridlineShow": False}],
            "valueAxis": [{"labelColor": solid(TEXT_2), "titleColor": solid(TEXT_2), "showAxisTitle": False,
                           "gridlineShow": True, "gridlineColor": solid(BORDER), "gridlineStyle": "dashed"}],
            "legend": [{"show": True, "position": "TopRight", "labelColor": solid(TEXT_2)}],
            "dataPoint": [{"defaultColor": solid(PURPLE)}],
            "labels": [{"color": solid(TEXT)}],
        }},
        "page": {"*": {
            "background": [{"color": solid(PAGE_BG), "transparency": 0}],
            "outspace": [{"color": solid(PAGE_BG), "transparency": 0}],
        }},
        "card": {"*": {
            "labels": [{"color": solid(TEXT), "fontSize": 26, "fontFamily": "Segoe UI Semibold"}],
            "categoryLabels": [{"show": True, "color": solid(TEXT_2), "fontSize": 10}],
        }},
        "textbox": {"*": {
            "background": [{"show": False}], "border": [{"show": False}], "title": [{"show": False}],
        }},
        "slicer": {"*": {
            "header": [{"fontColor": solid(TEXT_2), "background": solid(CARD_BG)}],
            "items": [{"fontColor": solid(TEXT), "background": solid(CARD_ALT)}],
            "padding": [{"top": 6, "bottom": 6, "left": 10, "right": 10}],
        }},
        "tableEx": {"*": {
            "grid": [{"gridVertical": False, "gridHorizontal": True, "gridHorizontalColor": solid(BORDER), "rowPadding": 6}],
            "columnHeaders": [{"fontColor": solid(TEXT_2), "backColor": solid(CARD_BG)}],
            "values": [{"fontColorPrimary": solid(TEXT), "backColorPrimary": solid(CARD_BG),
                        "fontColorSecondary": solid(TEXT), "backColorSecondary": solid(CARD_ALT)}],
            "total": [{"fontColor": solid(TEXT), "backColor": solid(CARD_ALT)}],
        }},
        "pivotTable": {"*": {
            "grid": [{"gridVertical": False, "gridHorizontal": True, "gridHorizontalColor": solid(BORDER), "rowPadding": 6}],
            "columnHeaders": [{"fontColor": solid(TEXT_2), "backColor": solid(CARD_BG)}],
            "rowHeaders": [{"fontColor": solid(TEXT), "backColor": solid(CARD_BG)}],
            "values": [{"fontColorPrimary": solid(TEXT), "backColorPrimary": solid(CARD_BG),
                        "fontColorSecondary": solid(TEXT), "backColorSecondary": solid(CARD_ALT)}],
            "total": [{"fontColor": solid(TEXT), "backColor": solid(CARD_ALT)}],
        }},
    },
}


# ── referencias a campos ─────────────────────────────────────────────
def col(table, prop):
    return ("Column", table, prop)


def meas(prop, table=M):
    return ("Measure", table, prop)


def named(ref, display):
    """Mismo campo con otro encabezado en la tabla/visual."""
    return ref[:3] + (display,)


def field(ref):
    kind, table, prop = ref[:3]
    return {kind: {"Expression": {"SourceRef": {"Entity": table}}, "Property": prop}}


def projection(ref):
    table, prop = ref[1], ref[2]
    p = {"field": field(ref), "queryRef": f"{table}.{prop}", "nativeQueryRef": prop}
    if len(ref) > 3:
        p["displayName"] = ref[3]
    return p


def lit(value):
    if isinstance(value, bool):
        v = "true" if value else "false"
    elif isinstance(value, (int, float)):
        v = f"{value}D"
    else:
        v = f"'{value}'"
    return {"expr": {"Literal": {"Value": v}}}


# ── constructores de visuales ────────────────────────────────────────
_counter = {"n": 0}


def text_or_measure(value):
    """Texto fijo, o una medida (tupla de meas()) para titulos que dependen de los filtros."""
    return {"expr": field(value)} if isinstance(value, tuple) else lit(value)


def qref(ref):
    return f"{ref[1]}.{ref[2]}"


def visual(vtype, x, y, w, h, roles, title=None, sort=None, objects=None, subtitle=None, filters=None, extra=None):
    _counter["n"] += 1
    name = f"v{_counter['n']:03d}"
    v = {"visualType": vtype}
    if roles:
        query = {"queryState": {role: {"projections": [projection(r) for r in refs]} for role, refs in roles.items()}}
        if sort:
            ref, direction = sort
            query["sortDefinition"] = {"sort": [{"field": field(ref), "direction": direction}], "isDefaultSort": True}
        v["query"] = query
    if objects:
        v["objects"] = objects
    vco = {}
    if title:
        vco["title"] = [{"properties": {"show": lit(True), "text": text_or_measure(title)}}]
    if subtitle:
        vco["subTitle"] = [{"properties": {"show": lit(True), "text": text_or_measure(subtitle),
                                           "fontColor": solid_lit(TEXT_2), "fontSize": lit(9)}}]
    if vco:
        v["visualContainerObjects"] = vco
    if extra:
        v.update(extra)
    v["drillFilterOtherVisuals"] = True
    out = {
        "$schema": f"{SCHEMA}/visualContainer/1.4.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "z": _counter["n"] * 1000, "width": w, "height": h, "tabOrder": _counter["n"] * 1000},
        "visual": v,
    }
    if filters:
        out["filterConfig"] = {"filters": [dict(f, name=f"{name}f{i}") for i, f in enumerate(filters)]}
    return out


def textbox(text, x, y, w, h, size="18pt", color=TEXT, bold=True):
    _counter["n"] += 1
    style = {"fontSize": size, "color": color}
    if bold:
        style["fontWeight"] = "bold"
    return {
        "$schema": f"{SCHEMA}/visualContainer/1.4.0/schema.json",
        "name": f"v{_counter['n']:03d}",
        "position": {"x": x, "y": y, "z": _counter["n"] * 1000, "width": w, "height": h, "tabOrder": _counter["n"] * 1000},
        "visual": {
            "visualType": "textbox",
            "objects": {"general": [{"properties": {"paragraphs": [
                {"textRuns": [{"value": text, "textStyle": style}]}
            ]}}]},
        },
    }


def card(ref, x, y, w=205, h=95, title=None):
    return visual("card", x, y, w, h, {"Values": [ref]}, title=title)


def headline(ref, x, y, w, h=50, size=16, color=TEXT):
    """Tarjeta sin rotulo para un texto dinamico (titular que cambia con los filtros)."""
    objects = {
        "labels": [{"properties": {"fontSize": lit(size), "color": solid_lit(color)}}],
        "categoryLabels": [{"properties": {"show": lit(False)}}],
    }
    return visual("card", x, y, w, h, {"Values": [ref]}, objects=objects)


def slicer(ref, x, y, w=180, h=55):
    objects = {"data": [{"properties": {"mode": lit("Dropdown")}}]}
    # Mismo grupo en todas las paginas = segmentadores sincronizados
    sync = {"syncGroup": {"groupName": ref[2], "fieldChanges": True, "filterChanges": True}}
    return visual("slicer", x, y, w, h, {"Values": [ref]}, objects=objects, extra=sync)


def back_button(x, y, w=45, h=40):
    _counter["n"] += 1
    return {
        "$schema": f"{SCHEMA}/visualContainer/1.4.0/schema.json",
        "name": f"v{_counter['n']:03d}",
        "position": {"x": x, "y": y, "z": _counter["n"] * 1000, "width": w, "height": h, "tabOrder": _counter["n"] * 1000},
        "visual": {
            "visualType": "actionButton",
            "objects": {"icon": [{"properties": {"shapeType": lit("back"), "lineColor": solid_lit(TEXT)},
                                  "selector": {"id": "default"}}]},
            "visualContainerObjects": {"visualLink": [{"properties": {"show": lit(True), "type": lit("Back")}}],
                                       "title": [{"properties": {"show": lit(False)}}]},
        },
    }


# ── formato: colores por serie, etiquetas, lineas constantes, filtros ─
def solid_lit(color):
    return {"solid": {"color": lit(color)}}


def series_colors(pairs):
    """[(medida, color)] -> dataPoint con un color fijo por serie."""
    return {"dataPoint": [{"properties": {"fill": solid_lit(c)}, "selector": {"metadata": qref(r)}} for r, c in pairs]}


def labels_only(show_ref, hide_refs):
    """Etiquetas de datos solo en la serie principal (REPORT_SPEC §4)."""
    return {"labels": [{"properties": {"show": lit(True)}}]
            + [{"properties": {"showSeries": lit(True)}, "selector": {"metadata": qref(show_ref)}}]
            + [{"properties": {"showSeries": lit(False)}, "selector": {"metadata": qref(r)}} for r in hide_refs]}


def ref_line(obj, value, label, color=TEXT_2):
    """Linea constante (obj = y1AxisReferenceLine / xAxisReferenceLine). value puede ser numero o medida."""
    return {obj: [{"properties": {
        "show": lit(True), "value": text_or_measure(value), "displayName": lit(label),
        "lineColor": solid_lit(color), "style": lit("dashed"), "width": lit(1),
        "dataLabelShow": lit(True), "dataLabelColor": solid_lit(color),
    }, "selector": {"id": "1"}}]}


def fill_by_measure(color_ref):
    """Color de barra tomado de una medida que devuelve un hex (formato por valor de campo)."""
    return {"dataPoint": [{"properties": {"fill": {"solid": {"color": {"expr": field(color_ref)}}}},
                           "selector": {"data": [{"dataViewWildcard": {"matchingOption": 1}}]}}]}


def back_by_measure(value_ref, color_ref):
    """Fondo de celda tomado de una medida que devuelve un hex (tablas y matrices)."""
    return {"values": [{"properties": {"backColor": {"solid": {"color": {"expr": field(color_ref)}}}},
                        "selector": {"data": [{"dataViewWildcard": {"matchingOption": 1}}], "metadata": qref(value_ref)}}]}


def _src(ref):
    kind, table, prop = ref[:3]
    return {kind: {"Expression": {"SourceRef": {"Source": "s"}}, "Property": prop}}


def measure_filter(ref, kind, value):
    """Filtro de visual sobre una medida. kind: 0 =, 1 >, 2 >=, 3 <=, 4 <."""
    return {"field": field(ref), "type": "Advanced", "filter": {
        "Version": 2, "From": [{"Name": "s", "Entity": ref[1], "Type": 0}],
        "Where": [{"Condition": {"Comparison": {"ComparisonKind": kind, "Left": _src(ref),
                                                "Right": {"Literal": {"Value": f"{value}L"}}}}}]}}


def in_filter(ref, values):
    return {"field": field(ref), "type": "Categorical", "filter": {
        "Version": 2, "From": [{"Name": "s", "Entity": ref[1], "Type": 0}],
        "Where": [{"Condition": {"In": {"Expressions": [_src(ref)],
                                        "Values": [[{"Literal": {"Value": f"'{v}'"}}] for v in values]}}}]}}


def merge(*dicts):
    out = {}
    for d in dicts:
        for k, v in d.items():
            out.setdefault(k, []).extend(v)
    return out


def gradient(measure_ref, lo=0, mid=55, hi=100):
    """Escala naranja-neutro-morado fija (0 / 55 = aprobado / 100) para una medida en una tabla/matriz."""
    _, table, prop = measure_ref
    return {
        "values": [{
            "properties": {"backColor": {"solid": {"color": {"expr": {"FillRule": {
                "Input": field(measure_ref),
                "FillRule": {"linearGradient3": {
                    "min": {"color": {"Literal": {"Value": f"'{LOW}'"}}, "value": {"Literal": {"Value": f"{lo}D"}}},
                    "mid": {"color": {"Literal": {"Value": f"'{MID}'"}}, "value": {"Literal": {"Value": f"{mid}D"}}},
                    "max": {"color": {"Literal": {"Value": f"'{HIGH}'"}}, "value": {"Literal": {"Value": f"{hi}D"}}},
                    "nullColoringStrategy": {"strategy": {"Literal": {"Value": "'noColor'"}}},
                }},
            }}}}}},
            "selector": {"data": [{"dataViewWildcard": {"matchingOption": 1}}], "metadata": f"{table}.{prop}"},
        }]
    }


def no_totals():
    return {"subTotals": [{"properties": {"rowSubtotals": lit(False), "columnSubtotals": lit(False)}}]}


# ── campos usados ────────────────────────────────────────────────────
CURSO = col("Cursos", "NombreCurso")
GRADO = col("Alumnos", "Grado")
ALUMNO = col("Alumnos", "Nombre")
TAREA = col("Tareas", "NombreTarea")


GRIS = TEXT_3  # contexto: lo que no hay que mirar primero


def header(title):
    # Una sola fila de segmentadores: Tarea, Grado. El curso queda fijo en el filtro del reporte (REPORT_FILTERS)
    return [
        textbox(title, 10, 5, 850, 50),
        slicer(TAREA, 880, 5, 200),
        slicer(GRADO, 1090, 5, 180),
    ]


# ── piezas de la pagina Inicio (estilo del reporte Benchmark: riel izquierdo + franja de KPI) ──
NOTEBOOK = col("Tareas", "NombreCorto")
METRICA = col("Metrica", "Metrica")
GRADE_COLORS = {"3ro": "#2A9FD8", "4to": PURPLE, "5to": "#B8861F"}  # validado (dataviz): CVD y contraste sobre CARD_BG
LOGO = "logo-white-horizontal.png"
RAIL_W = 152
TABLE_W = 700


def _plain(vc, header=False):
    """Sin fondo, borde, sombra ni relleno (piezas que van encima de un panel)."""
    vc = {
        "background": [{"properties": {"show": lit(False)}}],
        "border": [{"properties": {"show": lit(False)}}],
        "dropShadow": [{"properties": {"show": lit(False)}}],
        "padding": [{"properties": {"top": lit(0), "bottom": lit(0), "left": lit(0), "right": lit(0)}}],
        **vc,
    }
    if not header:
        vc["visualHeader"] = [{"properties": {"show": lit(False)}}]
    return vc


def panel(x, y, w, h, color=CARD_BG, radius=12, border=True):
    """Rectangulo de fondo (textbox vacio con fondo), como los paneles del reporte Benchmark."""
    v = textbox("", x, y, w, h)
    v["visual"]["visualContainerObjects"] = {
        "background": [{"properties": {"show": lit(True), "color": solid_lit(color), "transparency": lit(0)}}],
        "border": [{"properties": {"show": lit(border), "color": solid_lit(BORDER), "radius": lit(radius)}}],
        "visualHeader": [{"properties": {"show": lit(False)}}],
    }
    return v


def text(value, x, y, w, h, size=10, color=TEXT_2, bold=False):
    v = textbox(value, x, y, w, h, size=f"{size}pt", color=color, bold=bold)
    v["visual"]["visualContainerObjects"] = _plain({})
    return v


def detail(ref, x, y, w, h=24, size=9, color=TEXT_2, align="left"):
    """Texto dinamico pequeno sin fondo (subtitulo de un KPI)."""
    v = visual("card", x, y, w, h, {"Values": [ref]}, objects={
        "labels": [{"properties": {"fontSize": lit(size), "color": solid_lit(color), "fontFamily": lit("Segoe UI")}}],
        "categoryLabels": [{"properties": {"show": lit(False)}}],
    })
    v["visual"]["visualContainerObjects"] = _plain({"padding": [{"properties": {
        "top": lit(0), "bottom": lit(0), "left": lit(0), "right": lit(0)}}]})
    return v


def kpi(ref, label, detail_ref, x, y, w, h=96):
    """Panel + valor + detalle (franja superior del Benchmark). El panel se crea primero: z menor = queda detras."""
    back = panel(x, y, w, h)
    value = visual("card", x + 10, y + 4, w - 18, 62, {"Values": [ref]}, objects={
        "labels": [{"properties": {"fontSize": lit(24), "color": solid_lit(TEXT), "fontFamily": lit("Segoe UI Semibold")}}],
        "categoryLabels": [{"properties": {"show": lit(False)}}],
    })
    value["visual"]["visualContainerObjects"] = _plain({
        "title": [{"properties": {"show": lit(True), "text": lit(label), "fontColor": solid_lit(TEXT_2),
                                  "fontSize": lit(10), "fontFamily": lit("Segoe UI"), "alignment": lit("left")}}],
        "padding": [{"properties": {"top": lit(4), "bottom": lit(0), "left": lit(4), "right": lit(4)}}],
    })
    return [back, value, detail(detail_ref, x + 14, y + h - 28, w - 22, 22)]


def image(name, x, y, w, h):
    _counter["n"] += 1
    return {
        "$schema": f"{SCHEMA}/visualContainer/1.4.0/schema.json",
        "name": f"v{_counter['n']:03d}",
        "position": {"x": x, "y": y, "z": _counter["n"] * 1000, "width": w, "height": h, "tabOrder": _counter["n"] * 1000},
        "visual": {
            "visualType": "image",
            "objects": {"image": [{"properties": {"sourceFile": {"image": {
                "name": lit(name),
                "url": {"expr": {"ResourcePackageItem": {"PackageName": "RegisteredResources", "PackageType": 1, "ItemName": name}}},
                "scaling": lit("Fit"),
            }}}}]},
            "visualContainerObjects": _plain({}),
        },
    }


def rail_slicer(ref, x, y, w, h, title, mode="Basic", single=False, default=None):
    """Segmentador del riel izquierdo (sincronizado con el resto de paginas por nombre de campo)."""
    objects = {
        "data": [{"properties": {"mode": lit(mode)}}],
        "header": [{"properties": {"show": lit(True), "text": lit(title), "fontColor": solid_lit(TEXT_2),
                                   "fontSize": lit(9), "background": solid_lit(CARD_BG)}}],
        "items": [{"properties": {"fontColor": solid_lit(TEXT), "background": solid_lit(CARD_BG), "fontSize": lit(9)}}],
    }
    if single:
        objects["selection"] = [{"properties": {"strictSingleSelect": lit(True)}}]
    if default:
        # Seleccion inicial guardada en el segmentador
        objects["general"] = [{"properties": {"filter": {"filter": {
            "Version": 2, "From": [{"Name": "s", "Entity": ref[1], "Type": 0}],
            "Where": [{"Condition": {"In": {"Expressions": [_src(ref)], "Values": [[{"Literal": {"Value": f"'{default}'"}}]]}}}],
        }}}}]
    extra = {"syncGroup": {"groupName": ref[2], "fieldChanges": True, "filterChanges": True}}
    v = visual("slicer", x, y, w, h, {"Values": [ref]}, objects=objects, extra=extra)
    v["visual"]["visualContainerObjects"] = _plain({"padding": [{"properties": {
        "top": lit(4), "bottom": lit(4), "left": lit(4), "right": lit(4)}}]}, header=True)
    return v


def series_by_value(ref, colors):
    """Color fijo por valor de la serie (leyenda): el color sigue al grado, no a su posicion."""
    return {"dataPoint": [{"properties": {"fill": solid_lit(c)}, "selector": {"data": [{"scopeId": {"Comparison": {
        "ComparisonKind": 0, "Left": field(ref), "Right": {"Literal": {"Value": f"'{v}'"}}}}}]}}
        for v, c in colors.items()]}


# ── paginas ──────────────────────────────────────────────────────────
def page_inicio():
    """Como le fue a cada grado / alumno en cada notebook (Python 3ro-5to), con la densidad del Resumen del Benchmark:
    6 KPI + matriz alumno x notebook + 6 paneles (en clase vs final, embudo, arrastre, estado por grado, dispersion, contacto)."""
    valor, aprob = meas("Valor metrica"), meas("Aprobado s/ esperado %")
    salir, fuera = meas("Aprobado al salir de clase %"), meas("Trabajó fuera de clase %")
    x0, w0 = RAIL_W + 8, 1280 - RAIL_W - 16  # area de contenido: 160..1272

    # Riel izquierdo: logo, alcance y segmentadores
    vs = [
        panel(0, 0, RAIL_W, 720, radius=0, border=False),
        image(LOGO, 14, 14, RAIL_W - 28, 34),
        text("Estadística", 10, 58, RAIL_W - 20, 26, size=13, color=TEXT, bold=True),
        text("3ro–5to · ruta Python", 10, 82, RAIL_W - 20, 22, size=9),
        rail_slicer(NOTEBOOK, 8, 116, RAIL_W - 16, 60, "NOTEBOOK", mode="Dropdown"),
        rail_slicer(GRADO, 8, 182, RAIL_W - 16, 118, "GRADO"),
        rail_slicer(METRICA, 8, 308, RAIL_W - 16, 232, "MÉTRICA (MATRIZ)", single=True, default="Aprobado %"),
        text("Base = padrón oficial: quien no entregó cuenta como no aprobado. Aprobado = mejor nota ≥ 55. "
             "Min. entre envíos = dentro de una sesión; una pausa de 60+ min abre otra sesión.",
             10, 556, RAIL_W - 20, 150, size=8, color=TEXT_3),
    ]

    # Titular + franja de 6 KPI
    vs.append(detail(meas("Titulo inicio"), x0, 10, w0, 36, size=15, color=TEXT))
    kpis = [
        (aprob, "Aprobado sobre lo esperado", meas("Detalle aprobado")),
        (salir, "Aprobado al salir de clase", meas("Detalle al salir de clase")),
        (fuera, "Trabajó fuera de clase", meas("Detalle fuera de clase")),
        (meas("Tasa de entrega"), "Entrega", meas("Detalle entrega")),
        (meas("Alumnos en riesgo"), "Alumnos en riesgo", meas("Detalle en riesgo")),
        (meas("Sesiones por alumno"), "Sesiones por alumno", meas("Detalle sesiones")),
    ]
    kw = (w0 - 5 * 10) / 6
    for i, (ref, label, det) in enumerate(kpis):
        vs += kpi(ref, label, det, x0 + i * (kw + 10), 54, kw, 96)

    # Izquierda: grado -> alumno por notebook (+ para abrir un grado). Alta en vez de ancha: son 56 alumnos
    mw = 540
    matrix_objects = {
        "values": [{"properties": {"backColor": {"solid": {"color": {"expr": field(meas("Color metrica"))}}},
                                   "fontColor": solid_lit(TEXT), "fontSize": lit(9)},
                    "selector": {"data": [{"dataViewWildcard": {"matchingOption": 0}}], "metadata": qref(valor)}}],
        "rowHeaders": [{"properties": {"showExpandCollapseButtons": lit(True), "fontSize": lit(9)}}],
        "columnHeaders": [{"properties": {"fontSize": lit(8), "wordWrap": lit(True)}}],
        "columnWidth": [{"properties": {"value": lit(54)}, "selector": {"metadata": qref(valor)}}],
        "subTotals": [{"properties": {"rowSubtotals": lit(True), "columnSubtotals": lit(True)}}],
        "grid": [{"properties": {"gridVertical": lit(True), "gridVerticalColor": solid_lit(PAGE_BG), "gridVerticalWeight": lit(2),
                                 "gridHorizontal": lit(True), "gridHorizontalColor": solid_lit(PAGE_BG),
                                 "gridHorizontalWeight": lit(2)}}],
    }
    vs.append(visual("pivotTable", x0, 158, mw, 554,
                     {"Rows": [GRADO, ALUMNO], "Columns": [NOTEBOOK], "Values": [valor]},
                     title=meas("Titulo metrica matriz"),
                     subtitle="Notas y tasas: naranja < 55 · morado ≥ 55. Actividad: más oscuro = menos que el total. "
                              "Celda vacía = no envió (en Aprobado y Entrega cuenta como 0%).",
                     sort=(GRADO, "Ascending"), objects=matrix_objects))

    # Derecha: 3 filas x 2 paneles (como la grilla del Resumen del Benchmark)
    rx, wa = x0 + mw + 10, 322
    xb = rx + wa + 10
    wb = x0 + w0 - xb
    r1, r2, r3, rh = 158, 346, 534, 178
    pasa, desap, falt = meas("Pares aprobados"), meas("Pares desaprobados"), meas("Entregas faltantes")
    si, no = meas("Aprueba si aprobó el anterior %"), meas("Aprueba si no aprobó el anterior %")
    no_legend = {"legend": [{"properties": {"show": lit(False)}}]}
    legend_top = {"legend": [{"properties": {"show": lit(True), "position": lit("TopLeft"), "showTitle": lit(False),
                                             "fontSize": lit(8)}}]}
    vs += [
        # La prueba: en clase casi nadie aprueba; lo que se aprueba, se aprueba despues
        visual("clusteredColumnChart", rx, r1, wa, rh, {"Category": [NOTEBOOK], "Y": [salir, aprob]},
               title="Lo que se aprueba se aprueba después de clase",
               subtitle="Gris: al salir de clase · Morado: al final (sobre lo esperado)",
               sort=(NOTEBOOK, "Ascending"),
               objects=merge(series_colors([(salir, GRIS), (aprob, PURPLE)]), labels_only(aprob, [salir]), no_legend)),
        # En que paso se pierden
        visual("funnel", xb, r1, wb, rh, {"Category": [col("Etapas", "Etapa")], "Y": [meas("Etapa valor")]},
               title="En qué paso se pierden", subtitle="Pares alumno × notebook",
               sort=(col("Etapas", "Etapa"), "Ascending"),
               objects={"dataPoint": [{"properties": {"fill": solid_lit(PURPLE)}}]}),
        # Arrastre: quien no aprueba un notebook rara vez aprueba el siguiente
        visual("clusteredColumnChart", rx, r2, wa, rh,
               {"Category": [NOTEBOOK], "Y": [no, si],
                "Tooltips": [meas("n no aprobó el anterior"), meas("n aprobó el anterior")]},
               title="Quien no aprueba un notebook rara vez aprueba el siguiente",
               subtitle="% que aprueba · Gris: no aprobó el anterior · Morado: sí lo aprobó",
               sort=(NOTEBOOK, "Ascending"),
               objects=merge(series_colors([(no, GRIS), (si, PURPLE)]), labels_only(si, [no]), no_legend)),
        # Que paso con lo esperado, por grado (3 barras: etiquetas permitidas)
        visual("hundredPercentStackedBarChart", xb, r2, wb, rh, {"Category": [GRADO], "Y": [pasa, desap, falt]},
               title="3ro aprueba la mitad que 4to y 5to", subtitle=meas("Nota grupos chicos"),
               sort=(GRADO, "Ascending"),
               objects=merge(series_colors([(pasa, PURPLE), (desap, ORANGE), (falt, GRIS)]),
                             {"labels": [{"properties": {"show": lit(True), "fontSize": lit(8)}}]}, legend_top)),
        # Un punto por alumno
        visual("scatterChart", rx, r3, wa, rh, {"Category": [ALUMNO], "Series": [GRADO], "X": [fuera], "Y": [aprob]},
               title="Quien vuelve a trabajar fuera de clase aprueba más",
               subtitle="Un punto por alumno · asociación, no causa",
               objects=merge(series_by_value(GRADO, GRADE_COLORS), ref_line("y1AxisReferenceLine", 0.5, "mitad"),
                             {"categoryLabels": [{"properties": {"show": lit(False)}}]}, legend_top)),
        # A quien buscar: alumnos en riesgo, el que menos aprobo primero
        visual("tableEx", xb, r3, wb, rh,
               {"Values": [named(ALUMNO, "Alumno"), named(GRADO, "Grado"), named(aprob, "Aprobó"),
                           named(meas("Ultima actividad"), "Último envío")]},
               title="A quién buscar esta semana", subtitle="En riesgo: prom. < 55 o entrega < 50%",
               sort=(aprob, "Ascending"),
               objects=merge(gradient(aprob, 0, 0.55, 1),
                             {"grid": [{"properties": {"rowPadding": lit(1)}}],
                              "columnHeaders": [{"properties": {"fontSize": lit(8)}}],
                              "values": [{"properties": {"fontSize": lit(8)}}]}),
               filters=[measure_filter(meas("Alumnos en riesgo"), 1, 0)]),
    ]
    return "inicio", "Inicio", vs


def page_resumen():
    aprob, salir = meas("Aprobado s/ esperado %"), meas("Aprobado al salir de clase %")
    kpis = [aprob, meas("Tasa de entrega"), meas("Trabajó fuera de clase %"), meas("Alumnos en riesgo")]
    vs = header("Vista general")
    vs.append(headline(meas("Titulo resumen"), 10, 65, 1260, 50))
    vs += [card(k, 10 + i * 317, 122, 307, 95) for i, k in enumerate(kpis)]
    vs += [
        # 1.3 la prueba: en clase casi nadie aprueba; lo que se aprueba, se aprueba despues
        visual("clusteredColumnChart", 10, 227, 620, 483, {"Category": [TAREA], "Y": [salir, aprob]},
               title="Lo que se aprueba se aprueba después de clase",
               subtitle="Gris: aprobado al salir de clase · Morado: aprobado al final (sobre lo esperado)",
               sort=(TAREA, "Ascending"),
               objects=merge(series_colors([(salir, GRIS), (aprob, PURPLE)]), labels_only(aprob, [salir]))),
        # 1.4 el alcance: brecha por grado
        visual("pivotTable", 640, 227, 630, 255, {"Rows": [TAREA], "Columns": [GRADO], "Values": [aprob]},
               title="Aprobado sobre lo esperado, por tarea y grado", sort=(TAREA, "Ascending"),
               objects={**gradient(aprob, 0, 0.55, 1), **no_totals()}),
        headline(meas("Nota grupos chicos"), 640, 487, 630, 36, size=10, color=TEXT_2),
        # 1.5 en que paso se pierden
        visual("funnel", 640, 528, 630, 182, {"Category": [col("Etapas", "Etapa")], "Y": [meas("Etapa valor")]},
               title="En qué paso se pierden (pares alumno × tarea)", sort=(col("Etapas", "Etapa"), "Ascending"),
               objects={"dataPoint": [{"properties": {"fill": solid_lit(PURPLE)}}]}),
    ]
    return "resumen", "Vista general", vs


def page_seguimiento():
    nota_clase = meas("Nota en clase (tarea actual)")
    aprob, desaprob = meas("Pares que aprobaron"), meas("Pares que desaprobaron")
    fuera, fuera_curso = meas("Trabajó fuera de clase %"), meas("Trabajó fuera de clase % (curso)")
    vs = header("Seguimiento después de clase")
    vs.append(headline(meas("Titulo countdown"), 10, 65, 1260, 50))
    vs += [
        # 3.2 a quien escribirle: no volvieron (incluye a quienes no entregaron), nota en clase mas baja primero
        visual("tableEx", 10, 122, 500, 588,
               {"Values": [ALUMNO, GRADO, nota_clase, meas("Dias desde ultimo envio")]},
               title="Escríbeles, empezando por la nota en clase más baja",
               subtitle="No volvieron después de clase en la tarea actual · vacío = no envió nada en clase",
               sort=(nota_clase, "Ascending"), objects=gradient(nota_clase),
               filters=[measure_filter(meas("No volvieron"), 0, 1)]),
        # 3.3
        visual("clusteredColumnChart", 520, 122, 750, 290,
               {"Category": [col("Envios", "DiasDesdeClaseEje")], "Y": [aprob, desaprob]},
               title="¿Cuándo vuelven los que aprueban?",
               subtitle="Pares alumno × tarea con envíos ese día · 0 = día de clase",
               sort=(col("Envios", "DiasDesdeClaseEje"), "Ascending"),
               objects=series_colors([(aprob, PURPLE), (desaprob, GRIS)])),
        # 3.4 (3 barras: etiquetas permitidas)
        visual("clusteredColumnChart", 520, 422, 370, 250,
               {"Category": [col("AlumnoTarea", "DiasTrabajadosBanda")], "Y": [meas("Aprobado % (entregados)")]},
               title="Quien trabaja 2 días o más casi siempre aprueba",
               subtitle=meas("n por dias trabajados"),
               sort=(col("AlumnoTarea", "DiasTrabajadosBanda"), "Ascending"),
               objects={"labels": [{"properties": {"show": lit(True)}}]}),
        textbox("Asociación, no causa: los más motivados trabajan más días y también aprueban más.",
                520, 674, 370, 36, size="9pt", color=TEXT_2, bold=False),
        # 3.5 sin resaltar 3ro: la distancia a la linea ya lo muestra
        visual("clusteredBarChart", 900, 422, 370, 288, {"Category": [GRADO], "Y": [fuera]},
               title="Trabajó fuera de clase, por grado", subtitle=meas("Nota grupos chicos"),
               sort=(GRADO, "Ascending"), objects=ref_line("y1AxisReferenceLine", fuera_curso, "Promedio del curso")),
    ]
    return "seguimiento", "Seguimiento", vs


def page_estudiante():
    mejor, mediana = meas("Mejor nota real"), meas("Mediana del grado")
    estado = meas("Estado con icono")
    vs = header("Estudiante")
    vs += [
        back_button(10, 70),
        headline(meas("Titulo estudiante"), 65, 65, 1205, 50),
        # 2.1
        visual("multiRowCard", 10, 122, 300, 108,
               {"Values": [ALUMNO, GRADO, col("Alumnos", "DNI"), meas("Dias desde ultimo envio")]}),
        # 2.2 estado por tarea: icono + texto, el color solo acompana
        visual("pivotTable", 320, 122, 950, 108, {"Rows": [ALUMNO], "Columns": [TAREA], "Values": [estado]},
               title="Estado por tarea", sort=(TAREA, "Ascending"),
               objects={**back_by_measure(estado, meas("Estado color")), **no_totals()}),
        # 2.3 grafico de puntos (lineChart sin linea)
        visual("lineChart", 10, 240, 620, 230, {"Category": [TAREA], "Y": [mejor, mediana]},
               title="Su mejor nota frente a la mediana de su grado", subtitle="Morado: alumno · Gris: mediana del grado",
               sort=(TAREA, "Ascending"),
               objects=merge(series_colors([(mejor, PURPLE), (mediana, GRIS)]),
                             {"lineStyles": [{"properties": {"strokeWidth": lit(0), "showMarker": lit(True),
                                                             "markerSize": lit(8)}}]},
                             ref_line("y1AxisReferenceLine", 55, "Aprobado (55)"))),
        # 2.4
        visual("tableEx", 10, 480, 620, 230,
               {"Values": [TAREA, col("AlumnoTarea", "DiasTrabajados"), col("AlumnoTarea", "FueraDeClaseIcono"),
                           col("AlumnoTarea", "Intentos"), col("AlumnoTarea", "MinutosTotales")]},
               title="Cómo trabajó cada tarea", sort=(TAREA, "Ascending")),
        # 2.5
        visual("clusteredBarChart", 640, 240, 630, 470, {"Category": [col("Items", "Item")], "Y": [meas("Puntos perdidos")]},
               title="Dónde pierde puntos (elige una tarea arriba)", sort=(meas("Puntos perdidos"), "Descending")),
    ]
    return "estudiante", "Estudiante", vs


# Pagina de drill-through: se llega desde cualquier visual con Alumnos[Nombre] (Alumnos, Libro, Seguimiento, Actividad)
DRILLTHROUGH = {
    "estudiante": {
        "visibility": "HiddenInViewMode",
        "pageBinding": {"name": "pbEstudiante", "type": "Drillthrough", "parameters": []},
        "filterConfig": {"filters": [{"name": "dtAlumno", "field": field(ALUMNO), "type": "Categorical",
                                      "howCreated": "Drillthrough"}]},
    }
}


def page_libro():
    vs = header("Libro de notas (mejor intento, %)")
    vs.append(visual(
        "pivotTable", 10, 70, 1260, 640,
        {"Rows": [ALUMNO], "Columns": [TAREA], "Values": [meas("Mejor nota")]},
        title="Mejor nota por alumno y tarea (vacio = no entregado)",
        sort=(ALUMNO, "Ascending"),
        objects={**gradient(meas("Mejor nota")), **no_totals()},
    ))
    return "libro", "Libro de notas", vs


def page_cotejo():
    """Lista de cotejo (CNB, area EPT): alumno x indicador, con las preguntas que evidencian cada indicador.
    El mapeo indicador -> items del autograder vive en la tabla Indicadores del modelo."""
    cotejo, logrado = meas("Cotejo"), meas("Indicador logrado %")
    columna = col("Indicadores", "Columna")
    small = {"columnHeaders": [{"properties": {"fontSize": lit(8), "wordWrap": lit(True)}}],
             "values": [{"properties": {"fontSize": lit(8), "wordWrap": lit(True)}}]}
    vs = header("Lista de cotejo · CNB (EPT)")
    vs += [
        visual("pivotTable", 10, 70, 650, 640, {"Rows": [ALUMNO], "Columns": [columna], "Values": [cotejo]},
               title="Cotejo por alumno (elige un notebook arriba)",
               subtitle="✓ Sí = logró ≥ 60% de los puntos de sus preguntas · ✗ No · – No entregó · … Pendiente · "
                        "? Sin desglose (nota de revisión manual)",
               sort=(ALUMNO, "Ascending"),
               objects=merge(back_by_measure(cotejo, meas("Cotejo color")), no_totals(), small)),
        visual("tableEx", 670, 70, 600, 340,
               {"Values": [named(columna, "Ind."), col("Indicadores", "Indicador"), col("Indicadores", "Capacidad"),
                           col("Indicadores", "Evidencias"), named(logrado, "Logrado")]},
               title="Indicadores y preguntas que los evidencian",
               subtitle="Logrado = sobre los alumnos esperados del padrón (quien no entregó cuenta como No)",
               sort=(columna, "Ascending"), objects=merge(gradient(logrado, 0, 0.55, 1), small)),
        visual("pivotTable", 670, 420, 330, 290, {"Rows": [col("Indicadores", "Capacidad")], "Columns": [GRADO],
                                                  "Values": [logrado]},
               title="Logro por capacidad y grado", subtitle=meas("Nota grupos chicos"),
               sort=(col("Indicadores", "Capacidad"), "Ascending"),
               objects=merge(gradient(logrado, 0, 0.55, 1), no_totals(), small)),
        visual("tableEx", 1010, 420, 260, 290,
               {"Values": [named(ALUMNO, "Alumno"), named(meas("Indicadores logrados"), "Logrados"), named(logrado, "%")]},
               title="A quién apoyar", subtitle="Menos indicadores logrados primero",
               sort=(logrado, "Ascending"), objects=merge(gradient(logrado, 0, 0.55, 1), small)),
    ]
    return "cotejo", "Lista de cotejo", vs


NIVEL_COLORS = {"AD": "#7C3AED", "A": "#4F46A5", "B": "#B45309", "C": ORANGE}  # = medida Nivel color


def page_nivel():
    """Nivel de logro (CNB) por capacidad y competencia: agrupa todos los checks de la lista de cotejo
    (alumno x indicador, todas las tareas vencidas) con mapeo claro y aplica C / B / A / AD sobre el % Si.
    Sin segmentador de tarea: el nivel es del bimestre completo."""
    detalle, color = meas("Nivel de logro detalle"), meas("Nivel color")
    capacidad, competencia = col("Indicadores", "Capacidad"), col("Indicadores", "Competencia")
    nivel = col("Niveles", "Nivel")
    small = {"columnHeaders": [{"properties": {"fontSize": lit(8), "wordWrap": lit(True)}}],
             "values": [{"properties": {"fontSize": lit(8), "wordWrap": lit(True)}}]}
    vs = [textbox("Nivel de logro por capacidad y competencia · CNB", 10, 5, 1060, 50), slicer(GRADO, 1090, 5, 180)]
    sub = ("Agrupa todos los checks de la lista de cotejo de la capacidad (alumno × indicador, notebooks vencidos; "
           "no entregó = No). C < 50% Sí · B 50–69% · A 70–89% · AD ≥ 90%")
    vs += [
        visual("pivotTable", 10, 70, 660, 640, {"Rows": [ALUMNO], "Columns": [capacidad], "Values": [detalle]},
               title="Por capacidad", subtitle=sub, sort=(ALUMNO, "Ascending"),
               objects=merge(back_by_measure(detalle, color), no_totals(), small)),
        visual("pivotTable", 680, 70, 300, 640, {"Rows": [ALUMNO], "Columns": [competencia], "Values": [detalle]},
               title="Por competencia", subtitle="Agrupa los checks de todas sus capacidades",
               sort=(ALUMNO, "Ascending"), objects=merge(back_by_measure(detalle, color), no_totals(), small)),
        visual("hundredPercentStackedBarChart", 990, 70, 280, 300,
               {"Category": [capacidad], "Series": [nivel], "Y": [meas("Alumnos en nivel")]},
               title="Alumnos por nivel", sort=(capacidad, "Ascending"),
               objects=merge(series_by_value(nivel, NIVEL_COLORS),
                             {"labels": [{"properties": {"show": lit(True), "fontSize": lit(8)}}],
                              "legend": [{"properties": {"show": lit(True), "position": lit("TopLeft"),
                                                         "showTitle": lit(False), "fontSize": lit(8)}}],
                              "categoryAxis": [{"properties": {"fontSize": lit(7)}}]})),
        visual("tableEx", 990, 380, 280, 330,
               {"Values": [named(capacidad, "Capacidad"), named(col("Indicadores", "Columna"), "Ind."),
                           col("Indicadores", "Indicador"), col("Indicadores", "Cuenta")]},
               title="Qué se agrupa en cada capacidad", subtitle="Excluido = el vínculo con la capacidad no es claro",
               sort=(capacidad, "Ascending"), objects=small),
    ]
    return "nivel", "Nivel de logro", vs


def page_alumnos():
    cols = [ALUMNO, GRADO, meas("Entregas obligatorias"), meas("Entregas esperadas"), meas("Tasa de entrega"),
            meas("Nota promedio"), meas("Promedio con faltantes en 0"), meas("Nota a tiempo"), meas("Envios"),
            meas("Intentos por entrega"), meas("Logros promedio"), meas("Racha maxima"), meas("Ultimo envio")]
    vs = header("Seguimiento por alumno")
    vs += [
        visual("tableEx", 10, 70, 1260, 400, {"Values": cols}, title="Alumnos (ordenados por promedio con faltantes en 0)",
               sort=(meas("Promedio con faltantes en 0"), "Ascending"), objects=gradient(meas("Promedio con faltantes en 0"))),
        visual("clusteredBarChart", 10, 480, 860, 230, {"Category": [ALUMNO], "Y": [meas("Entregas faltantes")]},
               title="Entregas faltantes por alumno", sort=(meas("Entregas faltantes"), "Descending")),
        card(meas("Alumnos en riesgo"), 880, 480, 390, 110, title="Alumnos en riesgo (prom. < 55 o < 50% entregado)"),
        card(meas("Entregas faltantes"), 880, 600, 390, 110, title="Entregas faltantes"),
    ]
    return "alumnos", "Alumnos", vs


def page_ejercicios():
    item = col("Items", "Item")
    primero, final = meas("% al primer intento"), meas("% resuelto final")
    vs = header("Analisis por ejercicio")
    vs += [
        visual("clusteredColumnChart", 10, 70, 420, 300, {"Category": [col("ItemResumen", "Tipo")], "Y": [primero, final]},
               title="Éxito por tipo de ítem", subtitle="Gris: al primer intento · Morado: resuelto al final",
               sort=(col("ItemResumen", "Tipo"), "Ascending"),
               objects=series_colors([(primero, GRIS), (final, PURPLE)])),
        visual("clusteredColumnChart", 10, 380, 420, 330, {"Category": [item], "Y": [meas("Exito por item %")]},
               title="Items mas dificiles (filtra una tarea)", sort=(meas("Exito por item %"), "Ascending")),
        visual("pivotTable", 440, 70, 830, 640,
               {"Rows": [TAREA, item], "Values": [meas("Alumnos que intentaron"), meas("Exito por item %"), meas("Puntaje perfecto %")]},
               title="Detalle por tarea e item", sort=(TAREA, "Ascending"),
               objects=gradient(meas("Exito por item %"), 0, 0.55, 1)),
    ]
    return "ejercicios", "Ejercicios", vs


def page_actividad():
    # REPORT_SPEC §5 pag. 4: no usar la palabra "IA" en esta pagina
    primero, final, n = meas("% al primer intento"), meas("% resuelto final"), meas("Items n")
    minutos, dias = meas("Minutos para corregir (mediana)"), meas("Dias desde ultimo envio")
    vs = header("Actividad y calidad de los ítems")
    vs.append(textbox("Los ítems donde los alumnos se quedan atascados, y quién lleva más de una semana sin actividad",
                      10, 62, 1260, 40, size="13pt", color=TEXT_2, bold=False))
    vs += [
        # 4.1 sin etiquetas en los puntos; el item va en la informacion sobre herramientas y en Ejercicios
        visual("scatterChart", 10, 107, 620, 345,
               {"Category": [TAREA, col("ItemResumen", "Item"), col("ItemResumen", "Tipo")], "X": [primero], "Y": [final],
                "Tooltips": [n]},
               title="Abajo a la izquierda: ítems que pocos aciertan y muchos no terminan",
               subtitle="Un punto por ítem · solo ítems con n ≥ 10",
               objects=merge(ref_line("xAxisReferenceLine", 0.5, "50%"), ref_line("y1AxisReferenceLine", 0.8, "80%"),
                             {"categoryLabels": [{"properties": {"show": lit(False)}}]}),
               filters=[measure_filter(n, 2, 10)]),
        # 4.2 gris = el error muestra el valor esperado
        visual("clusteredBarChart", 640, 107, 630, 345, {"Category": [TAREA], "Y": [minutos]},
               title="Minutos para corregir un ítem (mediana)",
               subtitle="Gris: muestra el valor esperado · Morado: no lo muestra. En las tareas que muestran el valor "
                        "esperado, este tiempo mide copiar el número, no entender el error.",
               sort=(TAREA, "Ascending"), objects=fill_by_measure(meas("Color muestra esperado"))),
        # 4.3
        visual("clusteredColumnChart", 10, 462, 620, 248, {"Category": [TAREA], "Y": [primero, final]},
               title="Las reflexiones casi no se reintentan", subtitle="Gris: al primer intento · Morado: resuelto al final",
               sort=(TAREA, "Ascending"), objects=series_colors([(primero, GRIS), (final, PURPLE)]),
               filters=[in_filter(col("ItemResumen", "Tipo"), ["Reflexion"])]),
        # 4.4
        visual("tableEx", 640, 462, 630, 248,
               {"Values": [ALUMNO, GRADO, dias, meas("Ultima tarea"), meas("Alerta inactividad")]},
               title="Días sin actividad (⚠ = más de 7)", sort=(dias, "Descending")),
    ]
    return "actividad", "Actividad", vs


# Orden final (REPORT_SPEC §5): Vista general · Seguimiento · Libro · Lista de cotejo · Nivel de logro · Alumnos · Estudiante (oculta) · Actividad · Ejercicios
PAGES = [page_inicio, page_resumen, page_seguimiento, page_libro, page_cotejo, page_nivel, page_alumnos, page_estudiante, page_actividad,
         page_ejercicios]


# Alcance fijo de todo el reporte: Estadistica (STAT_2026), ruta Python, 3ro-5to.
# Tareas[Ruta] = "Python" deja fuera CS ("Python (CS)"), Sheets y las rutas Lite.
REPORT_FILTERS = [
    dict(in_filter(col("Tareas", "Ruta"), ["Python"]), name="rfRuta", isLockedInViewMode=True),
    dict(in_filter(col("Alumnos", "Curso"), ["STAT_2026"]), name="rfCurso", isLockedInViewMode=True),
    dict(in_filter(col("Alumnos", "Banda"), ["3ro-5to"]), name="rfBanda", isLockedInViewMode=True),
]


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    pages_dir = ROOT / "pages"
    # Vaciar sin borrar la carpeta en si (OneDrive la bloquea)
    # y tolerar carpetas vacias bloqueadas (OneDrive / Power BI Desktop abierto)
    if pages_dir.exists():
        for f in pages_dir.rglob("*"):
            if f.is_file():
                f.unlink()
        for d in sorted((p for p in pages_dir.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
            shutil.rmtree(d, ignore_errors=True)

    write(ROOT / "version.json", {"$schema": f"{SCHEMA}/versionMetadata/1.0.0/schema.json", "version": "2.0.0"})
    write(ROOT.parent / "StaticResources" / "RegisteredResources" / f"{THEME_NAME}.json", THEME)
    write(ROOT / "report.json", {
        "$schema": f"{SCHEMA}/report/1.2.0/schema.json",
        "themeCollection": {
            "baseTheme": {"name": "CY26SU07", "reportVersionAtImport": "5.75", "type": "SharedResources"},
            "customTheme": {"name": f"{THEME_NAME}.json", "reportVersionAtImport": "5.75", "type": "RegisteredResources"},
        },
        "layoutOptimization": "None",
        "resourcePackages": [
            {"name": "SharedResources", "type": "SharedResources",
             "items": [{"name": "CY26SU07", "path": "BaseThemes/CY26SU07.json", "type": "BaseTheme"}]},
            {"name": "RegisteredResources", "type": "RegisteredResources",
             "items": [{"name": f"{THEME_NAME}.json", "path": f"{THEME_NAME}.json", "type": "CustomTheme"},
                       {"name": LOGO, "path": LOGO, "type": "Image"}]},
        ],
        "filterConfig": {"filters": REPORT_FILTERS},
        "settings": {"useStylableVisualContainerHeader": True, "defaultDrillFilterOtherVisuals": True,
                     "allowChangeFilterTypes": True, "useEnhancedTooltips": True},
    })

    order = []
    for build in PAGES:
        _counter["n"] = 0
        name, display, visuals = build()
        order.append(name)
        write(pages_dir / name / "page.json", {
            "$schema": f"{SCHEMA}/page/1.3.0/schema.json",
            "name": name, "displayName": display, "displayOption": "FitToPage", "height": 720, "width": 1280,
            **DRILLTHROUGH.get(name, {}),
        })
        for v in visuals:
            write(pages_dir / name / "visuals" / v["name"] / "visual.json", v)
    write(pages_dir / "pages.json", {"$schema": f"{SCHEMA}/pagesMetadata/1.0.0/schema.json",
                                     "pageOrder": order, "activePageName": order[0]})
    print(f"{len(order)} paginas generadas en {pages_dir}")


if __name__ == "__main__":
    main()
