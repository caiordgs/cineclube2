import os
from supabase import create_client
from config.env import ENV, SUPABASE_URL, SUPABASE_KEY
from datetime import date, datetime, timezone


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "SUPABASE_URL / SUPABASE_KEY não carregadas. Verifique o ambiente."
    )

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print(">>> AMBIENTE ATIVO:", ENV)
print(">>> SUPABASE_URL:", SUPABASE_URL)

def carregar_filmes():
    resp = supabase.table("sugestoes_filmes") \
        .select("*") \
        .order("created_at") \
        .execute()

    return resp.data or []


def salvar_filme(titulo, diretor, pessoa, poster, data_lancamento):
    if isinstance(data_lancamento, (datetime, date)):
        data_lancamento = data_lancamento.isoformat()

    supabase.table("sugestoes_filmes").insert({
        "titulo": titulo.strip(),
        "diretor": diretor or "Desconhecido",
        "pessoa": pessoa.strip(),
        "poster": poster,
        "data_lancamento": data_lancamento
    }).execute()

def remover_filme(id_filme):
    supabase.table("sugestoes_filmes") \
        .delete() \
        .eq("id", id_filme) \
        .execute()


def limpar_todos():
    supabase.table("sugestoes_filmes") \
        .delete() \
        .gte("created_at", "1970-01-01") \
        .execute()

def salvar_filme_sorteado(
    titulo,
    diretor,
    pessoa,
    poster,
    data_lancamento
):
    supabase.table("filmes_sorteados").insert(
        {
            "titulo":          titulo,
            "diretor":         diretor,
            "pessoa":          pessoa,
            "poster":          poster,
            "data_lancamento": data_lancamento,
            "data_sorteio":    datetime.now(timezone.utc).isoformat()
        }
    ).execute()


def carregar_filmes_sorteados():
    resp = supabase.table("filmes_sorteados") \
        .select("*") \
        .order("data_sorteio", desc=True) \
        .execute()

    return resp.data or []


def salvar_review(
    filme_sorteado_id,
    autor,
    comentario,
    nota,
    diretor
):
    supabase.table("reviews_filmes").insert({
        "filme_sorteado_id": filme_sorteado_id,
        "autor": autor,
        "comentario": comentario,
        "nota": nota,
        "diretor": diretor
    }).execute()


def carregar_reviews(filme_sorteado_id):
        resp = supabase.table("reviews_filmes") \
            .select("*") \
            .eq("filme_sorteado_id", filme_sorteado_id) \
            .order("created_at", desc=True) \
            .execute()

        return resp.data or []

def carregar_filme_da_semana():
    resp = supabase.table("filmes_sorteados") \
        .select("*") \
        .order("data_sorteio", desc=True) \
        .limit(1) \
        .execute()

    data = resp.data or []
    return data[0] if data else None

def review_ja_existe(filme_sorteado_id, autor):
    resp = supabase.table("reviews_filmes") \
        .select("id") \
        .eq("filme_sorteado_id", filme_sorteado_id) \
        .eq("autor", autor) \
        .execute()

    return bool(resp.data)

def filme_ja_existe(titulo, diretor):
    resp = (
        supabase
        .table("sugestoes_filmes")
        .select("id")
        .eq("titulo", titulo)
        .eq("diretor", diretor)
        .execute()
    )
    return bool(resp.data)



