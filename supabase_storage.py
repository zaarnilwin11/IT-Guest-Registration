# Example: Upload file to Supabase Storage
from supabase import create_client, Client
import config

supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_ANON_KEY)
file = open("path/to/localfile", "rb")
supabase.storage.from_(config.SUPABASE_STORAGE_BUCKET).upload("folder/on/supabase/filename.ext", file)
file.close()