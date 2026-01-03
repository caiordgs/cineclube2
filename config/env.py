import os
from dotenv import load_dotenv

load_dotenv(".env.hml")

ENV = os.getenv("ENV", "homologation")

if ENV == "production":
    load_dotenv(".env.prod", override=True)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
