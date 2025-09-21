import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()  # loads keys from .env

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
