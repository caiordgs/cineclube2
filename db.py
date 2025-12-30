import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "Variáveis de ambiente SUPABASE_URL e SUPABASE_KEY não configuradas"
    )

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def carregar_filmes():
    resp = supabase.table("sugestoes_filmes") \
        .select("*") \
        .order("created_at") \
        .execute()

    return resp.data or []


def salvar_filme(titulo, diretor, pessoa, poster, data_lancamento):
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
    return supabase.table("filmes_sorteados").insert({
        "titulo": titulo,
        "diretor": diretor,
        "pessoa": pessoa,
        "poster": poster,
        "data_lancamento": data_lancamento
    }).execute()

def salvar_review(
    filme_sorteado_id,
    autor,
    comentario,
    nota
):
    supabase.table("reviews_filmes").insert({
        "filme_sorteado_id": filme_sorteado_id,
        "autor": autor,
        "comentario": comentario,
        "nota": nota
    }).execute()

def carregar_filmes_sorteados():
    resp = supabase.table("filmes_sorteados_br") \
        .select("*") \
        .order("data_sorteio_br", desc=True) \
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


