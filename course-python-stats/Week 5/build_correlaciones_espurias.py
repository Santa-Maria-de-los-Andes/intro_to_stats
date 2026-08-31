"""
Semana 5: Causalidad -- genera correlaciones_espurias.html

Recrea (en espanol, para proyectar en clase) los ejemplos clasicos de
"spurious correlations" de tylervigen.com que inspiraron el articulo de
Plotly (https://plotlygraphs.medium.com/spurious-correlations-56752fcffb69).

Datos reales tomados del paquete R `spuriouscorrelations`
(github.com/pachadotdev/spuriouscorrelations), que preserva los datasets
originales de tylervigen.com via Internet Wayback Machine.

Diseno de los graficos: en vez del grafico de doble eje Y del sitio
original (que la guia de dataviz de este proyecto marca como el
anti-patron #1 -- "la alineacion de las dos escalas es arbitraria, asi que
el grafico inventa una correlacion que no esta en los datos"), cada par se
estandariza (z-score) a un solo eje compartido. El efecto visual de "estas
dos lineas se mueven juntas" se mantiene intacto (el r real es asi de
alto), pero sin el truco de escalas arbitrarias -- lo cual es, de hecho,
una leccion extra util para Semana 5: hasta un grafico "honesto" puede
sentirse causal.

Este script es de un solo tema (claro), a proposito -- es un recurso para
proyectar en un aula, no una app con preferencia de tema del usuario.
"""

import base64
import os

import numpy as np
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# Logo institucional (SMA), embebido como data URI para que el HTML final
# siga siendo un solo archivo, sin dependencias externas en el aula.
# ---------------------------------------------------------------------------
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_LOGO_PATH = os.path.join(_SCRIPT_DIR, "..", "..", "shared", "icono SMA.png")


def _logo_data_uri():
    with open(_LOGO_PATH, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/png;base64,{b64}"


# ---------------------------------------------------------------------------
# Paleta validada (dataviz skill) para las lineas de datos -- categorica,
# slot 1 y slot 2. El resto de la pagina usa una paleta editorial propia
# (ver TOKENS abajo), separada de estos dos colores de serie.
# ---------------------------------------------------------------------------
COLOR_A = "#2a78d6"   # azul -- slot 1
COLOR_B = "#eb6834"   # naranja -- slot 2
CHART_SURFACE = "#fcfcfb"
CHART_GRID = "#e1e0d9"
CHART_AXIS_LINE = "#c3c2b7"
CHART_INK_PRIMARY = "#14171c"
CHART_INK_SECONDARY = "#5b6270"
CHART_INK_MUTED = "#8b909c"

# ---------------------------------------------------------------------------
# Tokens editoriales de la pagina (dossier / caso de investigacion)
# ---------------------------------------------------------------------------
TOKENS = dict(
    page="#eef0f3",
    surface="#fcfcfd",
    ink_primary="#14171c",
    ink_secondary="#5b6270",
    ink_muted="#8b909c",
    hairline="#dde1e7",
    accent="#1c5cab",
    accent_soft="#e8f0fb",
)

# ---------------------------------------------------------------------------
# Datos reales (paquete spuriouscorrelations, snapshot de tylervigen.com)
# Ordenados de menor a mayor |r| -- la presentacion escala en intensidad.
# ---------------------------------------------------------------------------
EJEMPLOS = [
    dict(
        id="cage",
        titulo='"Ahogamientos en piscinas" y "Peliculas de Nicolas Cage"',
        años=list(range(1999, 2010)),
        a_nombre="Personas ahogadas al caer en una piscina",
        a_unidad="personas",
        a_valores=[109, 102, 102, 98, 85, 95, 96, 98, 123, 94, 102],
        b_nombre="Peliculas protagonizadas por Nicolas Cage",
        b_unidad="peliculas",
        b_valores=[2, 2, 2, 3, 1, 1, 2, 3, 4, 1, 4],
        r=0.666,
        pais="Estados Unidos",
    ),
    dict(
        id="missamerica",
        titulo='"Edad de Miss America" y "Asesinatos por vapor y objetos calientes"',
        años=list(range(1999, 2010)),
        a_nombre="Edad de Miss America",
        a_unidad="años",
        a_valores=[24, 24, 24, 21, 22, 21, 24, 22, 20, 19, 22],
        b_nombre="Asesinatos por vapor, objetos calientes",
        b_unidad="casos",
        b_valores=[7, 7, 7, 3, 4, 3, 8, 4, 2, 3, 2],
        r=0.870,
        pais="Estados Unidos",
    ),
    dict(
        id="queso",
        titulo='"Consumo de queso per capita" y "Muertes por enredarse en las sabanas"',
        años=list(range(2000, 2010)),
        a_nombre="Consumo de queso per capita",
        a_unidad="libras/persona",
        a_valores=[29.8, 30.1, 30.5, 30.6, 31.3, 31.7, 32.6, 33.1, 32.7, 32.8],
        b_nombre="Personas muertas al enredarse en sus sabanas",
        b_unidad="personas",
        b_valores=[327, 456, 509, 497, 596, 573, 661, 741, 809, 717],
        r=0.947,
        pais="Estados Unidos",
    ),
    dict(
        id="ciencia",
        titulo='"Gasto de EE.UU. en ciencia y tecnologia" y "Suicidios por ahorcamiento"',
        años=list(range(1999, 2010)),
        a_nombre="Gasto en ciencia, espacio y tecnologia",
        a_unidad="miles de millones USD",
        a_valores=[18.079, 18.594, 19.753, 20.734, 20.831, 23.029, 23.597, 23.584, 25.525, 27.731, 29.449],
        b_nombre="Suicidios por ahorcamiento, estrangulacion y asfixia",
        b_unidad="casos",
        b_valores=[5427, 5688, 6198, 6462, 6635, 7336, 7248, 7491, 8161, 8578, 9000],
        r=0.992,
        pais="Estados Unidos",
    ),
    dict(
        id="margarina",
        titulo='"Tasa de divorcio en Maine" y "Consumo de margarina per capita"',
        años=list(range(2000, 2010)),
        a_nombre="Tasa de divorcio en Maine",
        a_unidad="por cada 1,000 hab.",
        a_valores=[5.0, 4.7, 4.6, 4.4, 4.3, 4.1, 4.2, 4.2, 4.2, 4.1],
        b_nombre="Consumo de margarina per capita",
        b_unidad="libras/persona",
        b_valores=[8.2, 7.0, 6.5, 5.3, 5.2, 4.0, 4.6, 4.5, 4.2, 3.7],
        r=0.992,
        pais="Estados Unidos",
    ),
]


def zscore(valores):
    arr = np.array(valores, dtype=float)
    return list((arr - arr.mean()) / arr.std())


def build_figure(ej):
    z_a = zscore(ej["a_valores"])
    z_b = zscore(ej["b_valores"])

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=ej["años"], y=z_a,
        mode="lines+markers",
        name=ej["a_nombre"],
        line=dict(color=COLOR_A, width=2),
        marker=dict(size=9, color=COLOR_A),
        customdata=ej["a_valores"],
        hovertemplate=(
            f"<b>{ej['a_nombre']}</b><br>"
            "Año %{x}<br>"
            f"%{{customdata}} {ej['a_unidad']}"
            "<extra></extra>"
        ),
    ))
    fig.add_trace(go.Scatter(
        x=ej["años"], y=z_b,
        mode="lines+markers",
        name=ej["b_nombre"],
        line=dict(color=COLOR_B, width=2),
        marker=dict(size=9, color=COLOR_B),
        customdata=ej["b_valores"],
        hovertemplate=(
            f"<b>{ej['b_nombre']}</b><br>"
            "Año %{x}<br>"
            f"%{{customdata}} {ej['b_unidad']}"
            "<extra></extra>"
        ),
    ))

    # Etiquetas directas al final de cada linea (identidad sin depender solo del color)
    fig.add_annotation(
        x=ej["años"][-1], y=z_a[-1], text=ej["a_nombre"],
        showarrow=False, xanchor="left", xshift=10,
        font=dict(size=12, color=COLOR_A), align="left",
    )
    fig.add_annotation(
        x=ej["años"][-1], y=z_b[-1], text=ej["b_nombre"],
        showarrow=False, xanchor="left", xshift=10,
        font=dict(size=12, color=COLOR_B), align="left",
    )

    fig.update_layout(
        title=None,
        showlegend=False,
        plot_bgcolor=CHART_SURFACE,
        paper_bgcolor=CHART_SURFACE,
        margin=dict(l=50, r=190, t=20, b=40),
        height=340,
        font=dict(family="'IBM Plex Sans', system-ui, sans-serif", color=CHART_INK_PRIMARY),
        hovermode="x unified",
        xaxis=dict(
            range=[ej["años"][0] - 0.5, ej["años"][-1] + 0.5],
            dtick=1, tickfont=dict(color=CHART_INK_MUTED, size=12),
            showgrid=True, gridcolor=CHART_GRID, gridwidth=1,
            showline=True, linecolor=CHART_AXIS_LINE, linewidth=1, zeroline=False,
        ),
        yaxis=dict(
            title=dict(text="Desviaciones estandar respecto al promedio", font=dict(color=CHART_INK_SECONDARY, size=12)),
            tickfont=dict(color=CHART_INK_MUTED, size=12),
            showgrid=True, gridcolor=CHART_GRID, gridwidth=1,
            showline=True, linecolor=CHART_AXIS_LINE, linewidth=1, zeroline=False,
        ),
    )
    return fig


def build_table_html(ej):
    filas = "".join(
        f"<tr><td>{a}</td><td>{x}</td><td>{y}</td></tr>"
        for a, x, y in zip(ej["años"], ej["a_valores"], ej["b_valores"])
    )
    return f"""
    <details class="tabla-datos">
      <summary>Ver datos reales</summary>
      <table>
        <thead>
          <tr><th>Año</th><th>{ej['a_nombre']} ({ej['a_unidad']})</th><th>{ej['b_nombre']} ({ej['b_unidad']})</th></tr>
        </thead>
        <tbody>{filas}</tbody>
      </table>
    </details>
    """


def build_card_html(ej, fig, numero, primero):
    chart_html = fig.to_html(
        full_html=False,
        include_plotlyjs="inline" if primero else False,
        config={"displayModeBar": False, "responsive": True},
    )
    return f"""
    <section class="expediente" id="{ej['id']}">
      <div class="expediente-cabecera">
        <span class="expediente-num">EXPEDIENTE {numero:02d}</span>
        <span class="expediente-pais">{ej['pais']} &middot; {ej['años'][0]}&ndash;{ej['años'][-1]}</span>
      </div>
      <h2>{ej['titulo']}</h2>
      <div class="chart">{chart_html}</div>
      <div class="expediente-pie">
        <div class="r-badge"><span>r</span>{ej['r']:.3f}</div>
        {build_table_html(ej)}
      </div>
    </section>
    """


PAGE_STYLE = f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,500;0,600;1,500&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap');

  :root {{
    --page: {TOKENS['page']};
    --surface: {TOKENS['surface']};
    --ink-primary: {TOKENS['ink_primary']};
    --ink-secondary: {TOKENS['ink_secondary']};
    --ink-muted: {TOKENS['ink_muted']};
    --hairline: {TOKENS['hairline']};
    --accent: {TOKENS['accent']};
    --accent-soft: {TOKENS['accent_soft']};
    --serie-a: {COLOR_A};
    --serie-b: {COLOR_B};
    color-scheme: light;
  }}

  * {{ box-sizing: border-box; }}

  body {{
    margin: 0;
    background: var(--page);
    color: var(--ink-primary);
    font-family: 'IBM Plex Sans', system-ui, -apple-system, "Segoe UI", sans-serif;
    padding: 48px 20px 72px;
  }}

  .envoltorio {{ max-width: 760px; margin: 0 auto; }}

  .masthead {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding-bottom: 18px;
    margin-bottom: 28px;
    border-bottom: 2px solid var(--accent);
  }}
  .masthead img {{
    height: 46px;
    width: auto;
    display: block;
  }}
  .masthead-tag {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--ink-muted);
    text-align: right;
  }}

  header.hero {{
    text-align: center;
    margin-bottom: 40px;
    padding-bottom: 32px;
    border-bottom: 1px solid var(--hairline);
  }}
  .eyebrow {{
    display: block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 14px;
  }}
  header.hero h1 {{
    font-family: 'Newsreader', Georgia, serif;
    font-weight: 600;
    font-size: 2.6rem;
    line-height: 1.1;
    margin: 0 0 14px;
    text-wrap: balance;
  }}
  header.hero p {{
    color: var(--ink-secondary);
    font-size: 1.05rem;
    line-height: 1.55;
    max-width: 560px;
    margin: 0 auto;
  }}

  .metodo {{
    background: var(--accent-soft);
    border: 1px solid var(--hairline);
    border-radius: 10px;
    padding: 20px 24px;
    margin-bottom: 44px;
    font-size: 0.95rem;
    line-height: 1.6;
    color: var(--ink-secondary);
  }}
  .metodo b {{ color: var(--ink-primary); font-weight: 600; }}
  .metodo b.serie-a {{ color: var(--serie-a); }}
  .metodo b.serie-b {{ color: var(--serie-b); }}

  .expediente {{
    background: var(--surface);
    border: 1px solid var(--hairline);
    border-radius: 14px;
    padding: 26px 26px 20px;
    margin-bottom: 24px;
  }}
  .expediente-cabecera {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 10px;
  }}
  .expediente-num {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    color: var(--accent);
  }}
  .expediente-pais {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: var(--ink-muted);
  }}
  .expediente h2 {{
    font-family: 'Newsreader', Georgia, serif;
    font-weight: 500;
    font-style: italic;
    font-size: 1.28rem;
    line-height: 1.4;
    margin: 0 0 16px;
    text-wrap: balance;
  }}
  .chart {{ overflow-x: auto; }}

  .expediente-pie {{
    display: flex;
    align-items: flex-start;
    gap: 18px;
    margin-top: 14px;
    flex-wrap: wrap;
  }}
  .r-badge {{
    display: flex;
    align-items: baseline;
    gap: 6px;
    font-family: 'IBM Plex Mono', monospace;
    font-variant-numeric: tabular-nums;
    font-weight: 600;
    font-size: 1.05rem;
    color: var(--ink-primary);
    background: var(--page);
    border: 1px solid var(--hairline);
    border-radius: 999px;
    padding: 5px 16px;
    white-space: nowrap;
  }}
  .r-badge span {{ color: var(--ink-muted); font-weight: 500; font-size: 0.85rem; }}

  .tabla-datos {{ font-size: 0.85rem; color: var(--ink-secondary); flex: 1; min-width: 220px; }}
  .tabla-datos summary {{
    cursor: pointer;
    color: var(--ink-muted);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.04em;
  }}
  .tabla-datos[open] summary {{ margin-bottom: 8px; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{
    text-align: left;
    padding: 5px 10px;
    border-bottom: 1px solid var(--hairline);
    font-size: 0.8rem;
    font-variant-numeric: tabular-nums;
  }}
  th {{ color: var(--ink-muted); font-weight: 500; }}
  table {{ display: block; overflow-x: auto; }}

  .cierre {{
    text-align: center;
    margin-top: 44px;
    padding-top: 32px;
    border-top: 1px solid var(--hairline);
  }}
  .cierre p.veredicto {{
    font-family: 'Newsreader', Georgia, serif;
    font-style: italic;
    font-size: 1.3rem;
    color: var(--ink-primary);
    max-width: 520px;
    margin: 0 auto 20px;
    text-wrap: balance;
  }}
  footer {{
    text-align: center;
    color: var(--ink-muted);
    font-size: 0.78rem;
    margin-top: 20px;
  }}
  footer a {{ color: var(--ink-secondary); }}

  @media (max-width: 560px) {{
    header.hero h1 {{ font-size: 2rem; }}
    .expediente {{ padding: 20px 18px 16px; }}
  }}
</style>
"""


def build_page_inner():
    cards = "\n".join(
        build_card_html(ej, build_figure(ej), numero=i + 1, primero=(i == 0))
        for i, ej in enumerate(EJEMPLOS)
    )

    return f"""<title>Correlaciones espurias</title>
{PAGE_STYLE}
<div class="envoltorio">
  <div class="masthead">
    <img src="{_logo_data_uri()}" alt="Logo SMA">
    <span class="masthead-tag">Material de clase &middot; Estadística</span>
  </div>

  <header class="hero">
    <span class="eyebrow">Semana 5 &middot; Chequeo de realidad sobre causalidad</span>
    <h1>Correlaciones espurias</h1>
    <p>Cinco pares de variables reales, casi perfectamente correlacionadas.
    Ninguna de las dos causa la otra.</p>
  </header>

  <div class="metodo">
    <b>Como leer estos graficos:</b> <b class="serie-a">■</b> y <b class="serie-b">■</b>
    estan estandarizadas a la misma escala (desviaciones estandar respecto a su
    propio promedio), asi que comparten <b>un solo eje</b> &mdash; nada de escalas
    infladas para forzar la coincidencia visual. El parecido que ves es real: el
    coeficiente de correlacion (<b>r</b>) de cada par es, de verdad, asi de alto.
    Lo que <b>no</b> es real es cualquier historia de causa y efecto entre las dos.
  </div>

  {cards}

  <div class="cierre">
    <p class="veredicto">"Correlacion no implica causalidad" &mdash; ni siquiera
    cuando r = 0.992.</p>
  </div>

  <footer>
    Datos reales del paquete R <code>spuriouscorrelations</code> (rescate de
    tylervigen.com via Internet Wayback Machine) &mdash; inspirado en el articulo
    <a href="https://plotlygraphs.medium.com/spurious-correlations-56752fcffb69" target="_blank" rel="noopener">
    "Spurious Correlations" de Plotly</a>.
  </footer>
</div>
"""


def main():
    inner = build_page_inner()
    # El bloque <title>/<style> y el contenido visual llegan concatenados en
    # `inner` (formato listo para Artifact); para el archivo standalone los
    # separamos en <head> y <body> respectivamente.
    head_part, _, body_marker = inner.partition('<div class="envoltorio">')
    body_part = '<div class="envoltorio">' + body_marker

    full_html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{head_part}
</head>
<body>
{body_part}
</body>
</html>
"""

    out_path = __file__.replace("build_correlaciones_espurias.py", "correlaciones_espurias.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Escrito: {out_path}")

    # Version "inner" (sin doctype/html/head/body), solo para vista previa como
    # Artifact -- no es un archivo del curso, se escribe fuera de esta carpeta.
    import os
    scratch_dir = os.environ.get("CLAUDE_SCRATCHPAD_DIR", os.path.dirname(out_path))
    inner_path = os.path.join(scratch_dir, "correlaciones_espurias_artifact_preview.html")
    try:
        with open(inner_path, "w", encoding="utf-8") as f:
            f.write(inner)
        print(f"Escrito (vista previa): {inner_path}")
    except OSError:
        pass


if __name__ == "__main__":
    main()
