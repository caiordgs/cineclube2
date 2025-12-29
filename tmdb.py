import requests
import os

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

if not TMDB_API_KEY:
    raise RuntimeError("Variável de ambiente TMDB_API_KEY não configurada")

HEADERS = {
    "Authorization": f"Bearer {TMDB_API_KEY}",
    "Accept": "application/json"
}


def buscar_filmes(query):
    url = f"{BASE_URL}/search/movie"

    params = {
        "query": query,
        "language": "pt-BR",
        "include_adult": False,
        "page": 1
    }

    r = requests.get(url, headers=HEADERS, params=params, timeout=10)

    if r.status_code == 200:
        resultados = r.json().get("results", [])
        if resultados:
            return resultados

    params["api_key"] = TMDB_API_KEY
    r = requests.get(url, params=params, timeout=10)

    if r.status_code == 200:
        return r.json().get("results", [])

    return []


def buscar_diretor(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/credits"

    r = requests.get(url, headers=HEADERS, timeout=10)

    if r.status_code != 200:
        r = requests.get(
            url,
            params={"api_key": TMDB_API_KEY},
            timeout=10
        )

    data = r.json() if r.status_code == 200 else {}

    for pessoa in data.get("crew", []):
        if pessoa.get("job") == "Director":
            return pessoa.get("name", "N/A")

    return "N/A"


def poster_url(path):
    if path:
        return f"https://image.tmdb.org/t/p/w300{path}"
    return None
