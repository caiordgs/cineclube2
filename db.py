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


def salvar_filme(titulo, diretor, pessoa, poster):
    supabase.table("sugestoes_filmes").insert({
        "titulo": titulo.strip(),
        "diretor": diretor or "Desconhecido",
        "pessoa": pessoa.strip(),
        "poster": poster
    }).execute()


def remover_filme(id_filme):
    supabase.table("sugestoes_filmes") \
        .delete() \
        .eq("id", id_filme) \
        .execute()


def limpar_todos():
    supabase.table("sugestoes_filmes") \
        .delete() \
        .gt("id", 0) \
        .execute()
