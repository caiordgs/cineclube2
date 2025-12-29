import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def carregar_filmes():
    resp = supabase.table("sugestoes_filmes") \
        .select("*") \
        .order("created_at") \
        .execute()
    return resp.data or []

def salvar_filme(titulo, diretor, pessoa, poster):
    supabase.table("sugestoes_filmes").insert({
        "titulo": titulo,
        "diretor": diretor,
        "pessoa": pessoa,
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
        .neq("id", "") \
        .execute()
