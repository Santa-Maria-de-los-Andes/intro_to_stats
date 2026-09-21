# -*- coding: utf-8 -*-
"""
Traduce al espanol los encabezados y los generos de spotify.csv (Spotify
Tracks Dataset, 114,000 filas x 21 columnas, 114 generos x 1000 pistas
c/u). Mismo patron que Weeks 1-2/translate_to_spanish.py y
Weeks 3-4/translate_to_spanish.py: dict de encabezados + dict de valores
categoricos, `.map(...).fillna(original)` como red de seguridad para
cualquier valor no listado.

Se conservan sin traducir: `track_id`, `artists`, `album_name`,
`track_name` (nombres propios), y las features de audio que ya son
terminos universales/prestamos ("tempo" es la misma palabra en espanol e
ingles). La columna `Unnamed: 0` (indice posicional duplicado de pandas,
sin valor analitico) se descarta -- no es un dato, es un artefacto de
exportacion del CSV original.

Los 114 generos se tradujeron nombre por nombre: los que ya son nombres de
genero reconocidos como tales en espanol (rock, pop, jazz, house, techno,
death-metal, hip-hop, k-pop...) se mantienen en su forma internacional
-- traducirlos literalmente (ej. "hip-hop" -> "salto de cadera") sonaria
artificial y no es como se llaman de verdad en espanol. Los que son
palabras descriptivas en ingles (children, chill, happy, party, sad,
sleep, study...) o gentilicios (brazil, british, french, indian...) si se
tradujeron, porque esos SI cambian de idioma en el habla real.

Requiere: pandas (pip install pandas)

Salida: spotify_es.csv
"""

import pandas as pd

SPOTIFY_HEADERS_ES = {
    "track_id": "ID_Pista",
    "artists": "Artistas",
    "album_name": "Álbum",
    "track_name": "Nombre_Cancion",
    "popularity": "Popularidad",
    "duration_ms": "Duracion_ms",
    "explicit": "Explicito",
    "danceability": "Bailabilidad",
    "energy": "Energia",
    "key": "Tono",
    "loudness": "Volumen",
    "mode": "Modo",
    "speechiness": "Habla",
    "acousticness": "Acustica",
    "instrumentalness": "Instrumentalidad",
    "liveness": "En_Vivo",
    "valence": "Valencia",
    "tempo": "Tempo",
    "time_signature": "Compas",
    "track_genre": "Genero",
}

GENRE_ES = {
    "acoustic": "Acústico",
    "afrobeat": "Afrobeat",
    "alt-rock": "Rock Alternativo",
    "alternative": "Alternativa",
    "ambient": "Ambiental",
    "anime": "Anime",
    "black-metal": "Black Metal",
    "bluegrass": "Bluegrass",
    "blues": "Blues",
    "brazil": "Brasil",
    "breakbeat": "Breakbeat",
    "british": "Británica",
    "cantopop": "Cantopop",
    "chicago-house": "House de Chicago",
    "children": "Infantil",
    "chill": "Relajante",
    "classical": "Clásica",
    "club": "Club",
    "comedy": "Comedia",
    "country": "Country",
    "dance": "Baile",
    "dancehall": "Dancehall",
    "death-metal": "Death Metal",
    "deep-house": "Deep House",
    "detroit-techno": "Techno de Detroit",
    "disco": "Disco",
    "disney": "Disney",
    "drum-and-bass": "Drum and Bass",
    "dub": "Dub",
    "dubstep": "Dubstep",
    "edm": "EDM",
    "electro": "Electro",
    "electronic": "Electrónica",
    "emo": "Emo",
    "folk": "Folk",
    "forro": "Forró",
    "french": "Francesa",
    "funk": "Funk",
    "garage": "Garage",
    "german": "Alemana",
    "gospel": "Gospel",
    "goth": "Gótica",
    "grindcore": "Grindcore",
    "groove": "Groove",
    "grunge": "Grunge",
    "guitar": "Guitarra",
    "happy": "Feliz",
    "hard-rock": "Rock Duro",
    "hardcore": "Hardcore",
    "hardstyle": "Hardstyle",
    "heavy-metal": "Heavy Metal",
    "hip-hop": "Hip-Hop",
    "honky-tonk": "Honky-Tonk",
    "house": "House",
    "idm": "IDM",
    "indian": "India",
    "indie": "Indie",
    "indie-pop": "Indie Pop",
    "industrial": "Industrial",
    "iranian": "Iraní",
    "j-dance": "J-Dance",
    "j-idol": "J-Idol",
    "j-pop": "J-Pop",
    "j-rock": "J-Rock",
    "jazz": "Jazz",
    "k-pop": "K-Pop",
    "kids": "Para Niños",
    "latin": "Latina",
    "latino": "Latino",
    "malay": "Malaya",
    "mandopop": "Mandopop",
    "metal": "Metal",
    "metalcore": "Metalcore",
    "minimal-techno": "Techno Minimal",
    "mpb": "MPB",
    "new-age": "New Age",
    "opera": "Ópera",
    "pagode": "Pagode",
    "party": "Fiesta",
    "piano": "Piano",
    "pop": "Pop",
    "pop-film": "Pop de Películas",
    "power-pop": "Power Pop",
    "progressive-house": "Progressive House",
    "psych-rock": "Rock Psicodélico",
    "punk": "Punk",
    "punk-rock": "Punk Rock",
    "r-n-b": "R&B",
    "reggae": "Reggae",
    "reggaeton": "Reggaetón",
    "rock": "Rock",
    "rock-n-roll": "Rock and Roll",
    "rockabilly": "Rockabilly",
    "romance": "Romántica",
    "sad": "Triste",
    "salsa": "Salsa",
    "samba": "Samba",
    "sertanejo": "Sertanejo",
    "show-tunes": "Musical de Teatro",
    "singer-songwriter": "Cantautor",
    "ska": "Ska",
    "sleep": "Para Dormir",
    "songwriter": "Compositor",
    "soul": "Soul",
    "spanish": "En Español",
    "study": "Para Estudiar",
    "swedish": "Sueca",
    "synth-pop": "Synth-Pop",
    "tango": "Tango",
    "techno": "Techno",
    "trance": "Trance",
    "trip-hop": "Trip-Hop",
    "turkish": "Turca",
    "world-music": "Música del Mundo",
}


def build_spotify_es(src="spotify.csv", dst="spotify_es.csv"):
    df = pd.read_csv(src)

    unmapped = set(df["track_genre"].unique()) - set(GENRE_ES)
    if unmapped:
        raise ValueError(f"Generos sin traduccion en GENRE_ES: {sorted(unmapped)}")

    df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed:")])
    df["track_genre"] = df["track_genre"].map(GENRE_ES).fillna(df["track_genre"])
    df = df.rename(columns=SPOTIFY_HEADERS_ES)
    df.to_csv(dst, index=False, encoding="utf-8-sig")
    print(f"Escrito {dst} ({len(df)} filas, {len(df.columns)} columnas)")


if __name__ == "__main__":
    build_spotify_es()
