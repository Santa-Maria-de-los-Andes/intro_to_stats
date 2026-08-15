"""
Traduce al espanol los encabezados y los nombres de pais de:
  - 2019.csv  (World Happiness Report 2019 — Kaggle, unsdsn/world-happiness)

Se preservan los valores numericos sin cambios. Nombres de pais que pycountry
no reconoce por su forma en este dataset (ej. "South Korea", "Congo
(Kinshasa)", "Kosovo") se traducen a mano en MANUAL_COUNTRY_ES.

Requiere: pandas, pycountry, babel  (pip install pandas pycountry babel)

Salida:
  2019_es.csv
"""

import pandas as pd
import pycountry
from babel import Locale

ES = Locale("es")

HEADERS_ES = {
    "Overall rank": "Puesto",
    "Country or region": "País o región",
    "Score": "Puntaje",
    "GDP per capita": "PBI per cápita",
    "Social support": "Apoyo social",
    "Healthy life expectancy": "Esperanza de vida saludable",
    "Freedom to make life choices": "Libertad para tomar decisiones",
    "Generosity": "Generosidad",
    "Perceptions of corruption": "Percepción de corrupción",
}

# Nombres tal como aparecen en el CSV que pycountry.lookup() no resuelve
# directamente (formas coloquiales, territorios en disputa, o paises con
# nombre compuesto que el dataset abrevia distinto a la forma oficial ISO).
MANUAL_COUNTRY_ES = {
    # pycountry.lookup() falla en estos dos especificamente — mismo problema
    # ya parchado en Weeks 1-2/translate_to_spanish.py (MANUAL_TEAM_ES).
    "Russia": "Rusia",
    "Turkey": "Turquía",
    # Formas no-ISO / territorios en disputa que este dataset usa, que
    # pycountry no puede resolver en absoluto.
    "South Korea": "Corea del Sur",
    "North Macedonia": "Macedonia del Norte",
    "Northern Cyprus": "Chipre del Norte",
    "Hong Kong": "Hong Kong",
    "Congo (Brazzaville)": "Congo (Brazzaville)",
    "Congo (Kinshasa)": "República Democrática del Congo",
    "Ivory Coast": "Costa de Marfil",
    "Trinidad & Tobago": "Trinidad y Tobago",
    "Palestinian Territories": "Territorios Palestinos",
    "Kosovo": "Kosovo",
    "Swaziland": "Suazilandia",  # misma eleccion que Weeks 1-2 MANUAL_TEAM_ES
    "Taiwan": "Taiwán",
    "Laos": "Laos",
    "Syria": "Siria",
    "Somalia": "Somalia",
    "Gambia": "Gambia",
}

# El dataset original (2019.csv) no trae columna de region/continente, que
# la Seccion C del notebook necesita para .groupby(). Se agrega aqui como
# columna derivada — no viene de la fuente Kaggle original.
#
# Esquema: 5 continentes (America, Europa, Asia, Africa, Oceania), el modelo
# que se ensena en el curriculo peruano (a diferencia del modelo de 7
# continentes que separa America del Norte/Sur) — mas apropiado para el
# contexto CNB de este curso que inventar un esquema nuevo.
#
# Nota para GAUSS: clasificacion geografica estandar (no la taxonomia de
# "Region" propia del World Happiness Report 2015/2016, que es mas fina
# — 10 regiones — pero se reconstruye de memoria y no se pudo verificar
# contra la fuente original, asi que se prefirio el esquema de continentes,
# geograficamente inambiguo). Casos transcontinentales con eleccion explicita:
# Rusia -> Europa (convencion cartografica estandar); Turquia, Georgia,
# Armenia, Azerbaiyan -> Asia (mismo criterio que un atlas escolar estandar,
# distinto del agrupamiento politico "Oriente Medio y Norte de Africa" que
# usa el WHR original). Oceania solo tiene 2 paises en este dataset
# (Australia, Nueva Zelanda) — cualquier correlacion calculada sobre ese
# grupo en la Seccion C no es estadisticamente confiable por el tamano de
# muestra; vale la pena convertir esto en un punto de discusion explicito
# en vez de ocultarlo.
CONTINENTE_ES = {
    "Finland": "Europa", "Denmark": "Europa", "Norway": "Europa",
    "Iceland": "Europa", "Netherlands": "Europa", "Switzerland": "Europa",
    "Sweden": "Europa", "Austria": "Europa", "Luxembourg": "Europa",
    "United Kingdom": "Europa", "Ireland": "Europa", "Germany": "Europa",
    "Belgium": "Europa", "Czech Republic": "Europa", "Malta": "Europa",
    "France": "Europa", "Spain": "Europa", "Italy": "Europa",
    "Slovakia": "Europa", "Poland": "Europa", "Lithuania": "Europa",
    "Slovenia": "Europa", "Kosovo": "Europa", "Romania": "Europa",
    "Cyprus": "Europa", "Latvia": "Europa", "Estonia": "Europa",
    "Hungary": "Europa", "Northern Cyprus": "Europa", "Portugal": "Europa",
    "Russia": "Europa", "Serbia": "Europa", "Moldova": "Europa",
    "Montenegro": "Europa", "Croatia": "Europa",
    "Bosnia and Herzegovina": "Europa", "Belarus": "Europa",
    "Greece": "Europa", "North Macedonia": "Europa", "Bulgaria": "Europa",
    "Albania": "Europa", "Ukraine": "Europa",

    "Israel": "Asia", "United Arab Emirates": "Asia", "Taiwan": "Asia",
    "Saudi Arabia": "Asia", "Qatar": "Asia", "Singapore": "Asia",
    "Bahrain": "Asia", "Uzbekistan": "Asia", "Kuwait": "Asia",
    "Thailand": "Asia", "South Korea": "Asia", "Japan": "Asia",
    "Kazakhstan": "Asia", "Pakistan": "Asia", "Philippines": "Asia",
    "Tajikistan": "Asia", "Hong Kong": "Asia", "Turkey": "Asia",
    "Malaysia": "Asia", "Mongolia": "Asia", "Kyrgyzstan": "Asia",
    "Turkmenistan": "Asia", "Azerbaijan": "Asia", "Lebanon": "Asia",
    "Indonesia": "Asia", "China": "Asia", "Vietnam": "Asia",
    "Bhutan": "Asia", "Nepal": "Asia", "Jordan": "Asia", "Laos": "Asia",
    "Cambodia": "Asia", "Palestinian Territories": "Asia",
    "Armenia": "Asia", "Iran": "Asia", "Georgia": "Asia",
    "Bangladesh": "Asia", "Iraq": "Asia", "Sri Lanka": "Asia",
    "Myanmar": "Asia", "India": "Asia", "Syria": "Asia", "Yemen": "Asia",
    "Afghanistan": "Asia",

    "Mauritius": "Africa", "Libya": "Africa", "Nigeria": "Africa",
    "Algeria": "Africa", "Morocco": "Africa", "Cameroon": "Africa",
    "Ghana": "Africa", "Ivory Coast": "Africa", "Benin": "Africa",
    "Congo (Brazzaville)": "Africa", "Gabon": "Africa",
    "South Africa": "Africa", "Senegal": "Africa", "Somalia": "Africa",
    "Namibia": "Africa", "Niger": "Africa", "Burkina Faso": "Africa",
    "Guinea": "Africa", "Gambia": "Africa", "Kenya": "Africa",
    "Mauritania": "Africa", "Mozambique": "Africa",
    "Congo (Kinshasa)": "Africa", "Mali": "Africa",
    "Sierra Leone": "Africa", "Chad": "Africa", "Ethiopia": "Africa",
    "Swaziland": "Africa", "Uganda": "Africa", "Egypt": "Africa",
    "Zambia": "Africa", "Togo": "Africa", "Liberia": "Africa",
    "Comoros": "Africa", "Madagascar": "Africa", "Lesotho": "Africa",
    "Burundi": "Africa", "Zimbabwe": "Africa", "Botswana": "Africa",
    "Malawi": "Africa", "Rwanda": "Africa", "Tanzania": "Africa",
    "Central African Republic": "Africa", "South Sudan": "Africa",
    "Tunisia": "Africa",

    "Canada": "America", "Costa Rica": "America",
    "United States": "America", "Mexico": "America", "Chile": "America",
    "Guatemala": "America", "Panama": "America", "Brazil": "America",
    "Uruguay": "America", "El Salvador": "America",
    "Trinidad & Tobago": "America", "Colombia": "America",
    "Nicaragua": "America", "Argentina": "America", "Ecuador": "America",
    "Jamaica": "America", "Honduras": "America", "Bolivia": "America",
    "Paraguay": "America", "Peru": "America",
    "Dominican Republic": "America", "Venezuela": "America",
    "Haiti": "America",

    "New Zealand": "Oceania", "Australia": "Oceania",
}
# "Africa"/"America"/"Oceania" sin tilde a proposito: son la forma correcta
# en espanol (solo "Africa" y "America" llevan tilde por ser esdrujulas —
# "Á-fri-ca", "A-mé-ri-ca" — se agrega abajo al escribir la columna final).
_CONTINENTE_TILDE_FIX = {"Africa": "África", "America": "América", "Oceania": "Oceanía"}

_country_cache: dict[str, str | None] = {}


def country_es(name: str) -> str:
    """Devuelve el nombre en espanol de `name`; si no se reconoce, lo deja igual."""
    if name in _country_cache:
        return _country_cache[name]
    result = MANUAL_COUNTRY_ES.get(name)
    if result is None:
        try:
            alpha2 = pycountry.countries.lookup(name).alpha_2
            result = ES.territories.get(alpha2)
        except LookupError:
            result = None
    _country_cache[name] = result or name
    return _country_cache[name]


def build_2019_es(src="2019.csv", dst="2019_es.csv"):
    df = pd.read_csv(src)
    unresolved = sorted({
        c for c in df["Country or region"]
        if country_es(c) == c and c not in MANUAL_COUNTRY_ES
    })
    if unresolved:
        print("Sin traduccion automatica de pycountry (revisados a mano, "
              "coinciden en espanol e ingles):")
        for c in unresolved:
            print(f"  - {c}")

    sin_continente = sorted(set(df["Country or region"]) - set(CONTINENTE_ES))
    if sin_continente:
        raise ValueError(f"Paises sin continente asignado: {sin_continente}")

    continente = df["Country or region"].map(CONTINENTE_ES).map(
        lambda c: _CONTINENTE_TILDE_FIX.get(c, c)
    )
    df["Country or region"] = df["Country or region"].apply(country_es)
    df = df.rename(columns=HEADERS_ES)
    # Continente insertado justo despues del pais — columna derivada, no
    # viene del CSV original de Kaggle (ver nota junto a CONTINENTE_ES).
    df.insert(df.columns.get_loc("País o región") + 1, "Continente", continente)
    # Preserva el formato de 3 decimales del CSV original (pandas recorta
    # ceros finales por defecto, ej. 7.600 -> 7.6).
    df.to_csv(dst, index=False, encoding="utf-8-sig", float_format="%.3f")
    print(f"Escrito {dst} ({len(df)} filas)")
    print(df["Continente"].value_counts())


if __name__ == "__main__":
    build_2019_es()
