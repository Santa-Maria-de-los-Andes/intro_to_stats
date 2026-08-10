"""
Traduce al espanol los encabezados y ciertos valores de:
  - athlete_events.csv  (deporte, evento, pais/equipo, temporada verano/invierno)
  - vgsales.csv         (genero)

Se conservan sin traducir: nombres de personas (atletas), nombres de juegos,
y nombres de marca (plataforma, editor/publisher, equipo/club cuando no es
un pais reconocible).

Requiere: pandas, pycountry, babel  (pip install pandas pycountry babel)

Salida:
  athlete_events_es.csv
  vgsales_es.csv
"""

import re
import pandas as pd
import pycountry
from babel import Locale

ES = Locale("es")

# ---------------------------------------------------------------------------
# 1. athlete_events.csv
# ---------------------------------------------------------------------------

ATHLETE_HEADERS_ES = {
    "ID": "ID",
    "Name": "Nombre",
    "Sex": "Sexo",
    "Age": "Edad",
    "Height": "Altura",
    "Weight": "Peso",
    "Team": "Equipo",
    "NOC": "CON",
    "Games": "Juegos",
    "Year": "Año",
    "Season": "Temporada",
    "City": "Ciudad",
    "Sport": "Deporte",
    "Event": "Evento",
    "Medal": "Medalla",
}

SPORT_ES = {
    "Aeronautics": "Aeronautica",
    "Alpine Skiing": "Esqui Alpino",
    "Alpinism": "Alpinismo",
    "Archery": "Tiro con Arco",
    "Art Competitions": "Competiciones de Arte",
    "Athletics": "Atletismo",
    "Badminton": "Badminton",
    "Baseball": "Beisbol",
    "Basketball": "Baloncesto",
    "Basque Pelota": "Pelota Vasca",
    "Beach Volleyball": "Voley Playa",
    "Biathlon": "Biatlon",
    "Bobsleigh": "Bobsleigh",
    "Boxing": "Boxeo",
    "Canoeing": "Piraguismo",
    "Cricket": "Criquet",
    "Croquet": "Croquet",
    "Cross Country Skiing": "Esqui de Fondo",
    "Curling": "Curling",
    "Cycling": "Ciclismo",
    "Diving": "Saltos",
    "Equestrianism": "Hipica",
    "Fencing": "Esgrima",
    "Figure Skating": "Patinaje Artistico",
    "Football": "Futbol",
    "Freestyle Skiing": "Esqui Estilo Libre",
    "Golf": "Golf",
    "Gymnastics": "Gimnasia",
    "Handball": "Balonmano",
    "Hockey": "Hockey sobre Cesped",
    "Ice Hockey": "Hockey sobre Hielo",
    "Jeu De Paume": "Juego de Palma",
    "Judo": "Judo",
    "Lacrosse": "Lacrosse",
    "Luge": "Luge",
    "Military Ski Patrol": "Patrulla Militar de Esqui",
    "Modern Pentathlon": "Pentatlon Moderno",
    "Motorboating": "Motonautica",
    "Nordic Combined": "Combinada Nordica",
    "Polo": "Polo",
    "Racquets": "Raquetas",
    "Rhythmic Gymnastics": "Gimnasia Ritmica",
    "Roque": "Roque",
    "Rowing": "Remo",
    "Rugby": "Rugby",
    "Rugby Sevens": "Rugby Siete",
    "Sailing": "Vela",
    "Shooting": "Tiro",
    "Short Track Speed Skating": "Patinaje de Velocidad en Pista Corta",
    "Skeleton": "Skeleton",
    "Ski Jumping": "Salto de Esqui",
    "Snowboarding": "Snowboard",
    "Softball": "Softbol",
    "Speed Skating": "Patinaje de Velocidad",
    "Swimming": "Natacion",
    "Synchronized Swimming": "Natacion Sincronizada",
    "Table Tennis": "Tenis de Mesa",
    "Taekwondo": "Taekwondo",
    "Tennis": "Tenis",
    "Trampolining": "Trampolin",
    "Triathlon": "Triatlon",
    "Tug-Of-War": "Tiro de la Cuerda",
    "Volleyball": "Voleibol",
    "Water Polo": "Waterpolo",
    "Weightlifting": "Halterofilia",
    "Wrestling": "Lucha",
}

SEASON_ES = {"Summer": "Verano", "Winter": "Invierno"}

MEDAL_ES = {"Gold": "Oro", "Silver": "Plata", "Bronze": "Bronce"}

# --- Event translation -----------------------------------------------------
# Every Event string starts with its Sport name (verified against the data),
# e.g. "Judo Men's Extra-Lightweight" -> Sport="Judo".
# The remainder is translated with Men's/Women's/Mixed + a word/phrase glossary.
# Terms not found in the glossary (mostly historical French shooting/art terms
# and proper-noun boat/class names) are left as-is.

PHRASE_ES = {
    "Four-In-Hand": "Tiro de Cuatro",
    "Cross-Country": "Campo a Traves",
    "Muzzle-Loading": "Avancarga",
    "Small-Bore": "Calibre Pequeno",
    "Rapid-Fire": "Tiro Rapido",
    "Bore-Rifle": "Rifle de Calibre",
    "Light-Flyweight": "Peso Mosca Ligero",
    "Light-Heavyweight": "Peso Semipesado",
    "Light-Middleweight": "Peso Medio Ligero",
    "Light-Welterweight": "Peso Welter Ligero",
    "Half-Heavyweight": "Semipesado",
    "Half-Lightweight": "Semiligero",
    "Half-Middleweight": "Semimedio",
    "Middle-Heavyweight": "Medio Pesado",
    "Super-Heavyweight": "Super Pesado",
    "Extra-Lightweight": "Extra Ligero",
    "Two-Man": "Dos Hombres",
    "Three-Day": "Tres Dias",
    "A-Class": "Clase A",
    "B-Class": "Clase B",
    "C-Class": "Clase C",
    "All-Around": "Concurso Completo",
    "Greco-Roman": "Grecorromana",
}

WORD_ES = {
    "Aerials": "Saltos Acrobaticos", "Air": "Aire", "Allround": "Combinado",
    "Amateurs": "Aficionados", "American": "Americano", "Ancient": "Antiguo",
    "And": "y", "Any": "Cualquier", "Apparatus": "Aparatos",
    "Applied": "Aplicado", "Architectural": "Arquitectonico",
    "Architecture": "Arquitectura", "Arts": "Artes", "Backstroke": "Espalda",
    "Breaststroke": "Braza", "Chamber": "Camara", "Club": "Clava",
    "Sporting": "Deportiva",
    "Balance": "Equilibrio", "Ball": "Pelota", "Balls": "Bolas",
    "Bantamweight": "Peso Gallo", "Bar": "Barra", "Bars": "Barras",
    "Beam": "Barra de Equilibrio", "Birds": "Aves", "Boats": "Botes",
    "Both": "Ambos", "Butterfly": "Mariposa", "Canadian": "Canadiense",
    "Chorus": "Coro", "Championnat": "Campeonato",
    "Championship": "Campeonato", "Class": "Clase", "Climbing": "Trepa de Cuerda",
    "Colors": "Colores", "Combined": "Combinado", "Competition": "Competicion",
    "Compositions": "Composiciones", "Contest": "Concurso",
    "Continental": "Continental", "Course": "Recorrido", "Courts": "Pistas",
    "Covered": "Cubierto", "Coxed": "Con Timonel", "Coxless": "Sin Timonel",
    "Dancing": "Baile", "Decathlon": "Decatlon", "Designs": "Disenos",
    "Dinghy": "Bote", "Disappearing": "Desaparicion", "Discus": "Disco",
    "Distance": "Distancia", "Double": "Doble", "Doubles": "Dobles",
    "Downhill": "Descenso", "Dramatic": "Dramatico", "Drawings": "Dibujos",
    "Dressage": "Doma", "Dueling": "Duelo", "Duet": "Dueto",
    "Dumbbell": "Mancuerna", "Eights": "Ocho", "Epic": "Epica",
    "Event": "Evento", "Events": "Eventos", "Exercise": "Ejercicio",
    "Featherweight": "Peso Pluma", "Feet": "Pies", "Field": "Campo",
    "Figures": "Figuras", "Five": "Cinco", "Floor": "Suelo",
    "Flyweight": "Peso Mosca", "Foil": "Florete", "Folding": "Plegable",
    "For": "Para", "Four": "Cuatro", "Fours": "Cuatro",
    "Free": "Libre", "Freestyle": "Estilo Libre", "Giant": "Gigante",
    "Graphic": "Grafico", "Greek": "Griego", "Group": "Grupo",
    "Hammer": "Martillo", "Hand": "Mano", "Hands": "Manos",
    "Heavyweight": "Peso Pesado", "Heptathlon": "Heptatlon", "High": "Alto",
    "Hill": "Colina", "Hits": "Aciertos", "Horizontal": "Horizontal",
    "Horse": "Caballo", "Hours": "Horas", "Hunter": "Caza",
    "Hurdles": "Vallas", "Ice": "Hielo", "Individual": "Individual",
    "Instrumental": "Instrumental", "Javelin": "Jabalina", "Jump": "Salto",
    "Jumping": "Salto", "Kayak": "Kayak", "Keelboat": "Quilla",
    "Kneeling": "De Rodillas", "Large": "Grande", "Lightweight": "Peso Ligero",
    "Literature": "Literatura", "Long": "Largo", "Lyric": "Lirico",
    "Man": "Hombre", "Marathon": "Maraton", "Mass": "Masiva",
    "Masters": "Maestros", "Medals": "Medallas", "Medley": "Combinado",
    "Men": "Hombres", "Middleweight": "Peso Medio", "Mile": "Milla",
    "Military": "Militar", "Model": "Modelo", "Mountainbike": "Bicicleta de Montana",
    "Moving": "Movil", "Multihull": "Multicasco", "Music": "Musica",
    "National": "Nacional", "Naval": "Naval", "Normal": "Normal",
    "Obstacle": "Obstaculos", "Olympic": "Olimpico", "One": "Uno",
    "Open": "Abierto", "Or": "o", "Orchestra": "Orquesta",
    "Painting": "Pintura", "Paintings": "Pinturas", "Pairs": "Parejas",
    "Parallel": "Paralelas", "Pentathlon": "Pentatlon", "Person": "Persona",
    "Pistol": "Pistola", "Plain": "Sencillo", "Planning": "Planificacion",
    "Plaques": "Placas", "Platform": "Plataforma", "Plunge": "Zambullida",
    "Points": "Puntos", "Pole": "Pertiga", "Pommelled": "Con Arzones",
    "Portable": "Portatil", "Position": "Posicion", "Positions": "Posiciones",
    "Prone": "Tendido", "Pursuit": "Persecucion", "Put": "Lanzamiento",
    "Quadruple": "Cuadruple", "Race": "Carrera", "Relay": "Relevos",
    "Reliefs": "Relieves", "Revolver": "Revolver", "Rifle": "Rifle",
    "Rings": "Anillas", "Road": "Ruta", "Rope": "Cuerda", "Round": "Ronda",
    "Running": "Carrera", "Sabre": "Sable", "Sailors": "Navegantes",
    "Sculls": "Skiff", "Sculpturing": "Escultura", "Shot": "Peso",
    "Side": "Lado", "Single": "Individual", "Singles": "Individuales",
    "Small": "Pequeno", "Solo": "Solo", "Special": "Especial",
    "Sports": "Deportes", "Springboard": "Trampolin", "Sprint": "Esprint",
    "Standing": "De Pie", "Start": "Salida", "Statues": "Estatuas",
    "Steeplechase": "Carrera de Obstaculos", "Sticks": "Palos", "Stone": "Piedra",
    "Style": "Estilo", "Super": "Super", "Swedish": "Sueco",
    "Swinging": "Oscilante", "Synchronized": "Sincronizado", "System": "Sistema",
    "Tandem": "Tandem", "Target": "Blanco", "Team": "Equipo", "Teams": "Equipos",
    "Three": "Tres", "Throw": "Lanzamiento", "Time": "Tiempo", "Ton": "Tonelada",
    "Town": "Ciudad", "Trial": "Prueba", "Triple": "Triple",
    "Two": "Dos", "Under": "Bajo", "Underwater": "Subacuatico",
    "Uneven": "Asimetricas", "Unknown": "Desconocido", "Unlimited": "Ilimitado",
    "Vault": "Salto", "Vaulting": "Volteo", "Vocals": "Vocal",
    "Walk": "Marcha", "Water": "Agua", "Weight": "Peso",
    "Welterweight": "Peso Welter", "Windsurfer": "Windsurf", "With": "Con",
    "Work": "Obra", "Works": "Obras", "Yard": "Yarda", "Yards": "Yardas",
    "epee": "Espada", "foot": "Pie", "kilometres": "Kilometros",
    "laps": "Vueltas", "metres": "Metros", "mile": "Milla", "pound": "Libra",
    "yard": "Yarda", "yards": "Yardas", "and": "y", "a": "a",
}

# Sport names can also reappear inside the event remainder (e.g. team-ball
# sports whose only event is named after the sport itself, like
# "Football Men's Football"), so they're translated with the same pass.
_ALL_PHRASES_ES = {**SPORT_ES, **PHRASE_ES}
_PHRASE_RE = re.compile(
    r"\b(" + "|".join(re.escape(k) for k in sorted(_ALL_PHRASES_ES, key=len, reverse=True)) + r")\b"
)
_WORD_RE = re.compile(r"[A-Za-z][A-Za-z']*")


def _translate_remainder(text: str) -> str:
    text = text.replace("Men's", "Masculino")
    text = text.replace("Women's", "Femenino")
    text = text.replace("Mixed", "Mixto")
    text = _PHRASE_RE.sub(lambda m: _ALL_PHRASES_ES[m.group(0)], text)
    return _WORD_RE.sub(lambda m: WORD_ES.get(m.group(0), m.group(0)), text)


def translate_event(sport_en: str, event: str) -> str:
    sport_es = SPORT_ES.get(sport_en, sport_en)
    remainder = event[len(sport_en):]
    return sport_es + _translate_remainder(remainder)


# --- Country/Team translation ----------------------------------------------
# "Team" holds a mix of real countries/historical NOC teams (translated) and
# club/boat/crew names (left as-is, since they are not countries).

MANUAL_TEAM_ES = {
    "Russia": "Rusia", "Turkey": "Turquia", "Great Britain": "Gran Bretana",
    "England": "Inglaterra", "Scotland": "Escocia", "Wales": "Gales",
    "Holland": "Holanda", "Cote d'Ivoire": "Costa de Marfil",
    "Ivory Coast": "Costa de Marfil", "Soviet Union": "Union Sovietica",
    "West Germany": "Alemania Occidental", "East Germany": "Alemania Oriental",
    "Czechoslovakia": "Checoslovaquia", "Serbia and Montenegro": "Serbia y Montenegro",
    "Unified Team": "Equipo Unificado", "United Arab Republic": "Republica Arabe Unida",
    "North Yemen": "Yemen del Norte", "South Yemen": "Yemen del Sur",
    "South Vietnam": "Vietnam del Sur", "Malaya": "Malaya",
    "Individual Olympic Athletes": "Atletas Olimpicos Individuales",
    "Refugee Olympic Athletes": "Atletas Olimpicos Refugiados",
    "Netherlands Antilles": "Antillas Neerlandesas",
    "United States Virgin Islands": "Islas Virgenes de los Estados Unidos",
    "Brunei": "Brunei", "Palestine": "Palestina",
    "Chinese Taipei": "Taipei Chino", "Newfoundland": "Terranova",
    "North Borneo": "Borneo del Norte", "Rhodesia": "Rodesia",
    "Saar": "Sarre", "Guinea Bissau": "Guinea-Bisau",
    "Cape Verde": "Cabo Verde", "Swaziland": "Suazilandia",
    "Timor Leste": "Timor Oriental",
    "West Indies Federation": "Federacion de las Indias Occidentales",
    "Crete": "Creta",
}

_country_cache: dict[str, str | None] = {}


def _country_es(name: str) -> str | None:
    """Return Spanish name for `name` if it's a recognizable country, else None."""
    if name in _country_cache:
        return _country_cache[name]
    result = MANUAL_TEAM_ES.get(name)
    if result is None:
        try:
            alpha2 = pycountry.countries.lookup(name).alpha_2
            result = ES.territories.get(alpha2)
        except LookupError:
            result = None
    _country_cache[name] = result
    return result


def translate_team(team: str) -> str:
    """Translate the country part of a Team value; leave club/boat names as-is."""
    m = re.match(r"^(.*)(-\d+)$", team)
    base, suffix = (m.group(1), m.group(2)) if m else (team, "")
    parts = base.split("/")
    translated_parts = []
    changed = False
    for p in parts:
        es = _country_es(p)
        if es:
            translated_parts.append(es)
            changed = True
        else:
            translated_parts.append(p)
    if not changed:
        return team
    return "/".join(translated_parts) + suffix


def build_athlete_events_es(src="athlete_events.csv", dst="athlete_events_es.csv"):
    df = pd.read_csv(src)

    df["Season"] = df["Season"].map(SEASON_ES).fillna(df["Season"])
    df["Games"] = df["Games"].apply(
        lambda g: re.sub(r"(Summer|Winter)$", lambda m: SEASON_ES[m.group(0)], g)
    )
    sport_en = df["Sport"]
    df["Event"] = [
        translate_event(s, event) for s, event in zip(sport_en, df["Event"])
    ]
    df["Sport"] = sport_en.map(SPORT_ES).fillna(sport_en)
    df["Team"] = df["Team"].apply(translate_team)
    df["Medal"] = df["Medal"].map(MEDAL_ES).fillna(df["Medal"])

    df = df.rename(columns=ATHLETE_HEADERS_ES)
    df.to_csv(dst, index=False, encoding="utf-8-sig")
    print(f"Escrito {dst} ({len(df)} filas)")


# ---------------------------------------------------------------------------
# 2. vgsales.csv
# ---------------------------------------------------------------------------

VGSALES_HEADERS_ES = {
    "Rank": "Puesto",
    "Name": "Nombre",
    "Platform": "Plataforma",
    "Year": "Año",
    "Genre": "Género",
    "Publisher": "Editor",
    "NA_Sales": "Ventas_NA",
    "EU_Sales": "Ventas_EU",
    "JP_Sales": "Ventas_JP",
    "Other_Sales": "Ventas_Otros",
    "Global_Sales": "Ventas_Globales",
}

GENRE_ES = {
    "Action": "Accion", "Adventure": "Aventura", "Fighting": "Lucha",
    "Misc": "Varios", "Platform": "Plataformas", "Puzzle": "Rompecabezas",
    "Racing": "Carreras", "Role-Playing": "Rol", "Shooter": "Disparos",
    "Simulation": "Simulacion", "Sports": "Deportes", "Strategy": "Estrategia",
}


def build_vgsales_es(src="vgsales.csv", dst="vgsales_es.csv"):
    df = pd.read_csv(src)
    df["Genre"] = df["Genre"].map(GENRE_ES).fillna(df["Genre"])
    df = df.rename(columns=VGSALES_HEADERS_ES)
    df.to_csv(dst, index=False, encoding="utf-8-sig")
    print(f"Escrito {dst} ({len(df)} filas)")


if __name__ == "__main__":
    build_athlete_events_es()
    build_vgsales_es()
