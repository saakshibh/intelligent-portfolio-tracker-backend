import os
from supabase import create_client, Client

class SupabaseManager: # Added the Class wrapper
    def __init__(self):
        self.url: str = os.environ.get("SUPABASE_URL")
        self.key: str = os.environ.get("SUPABASE_KEY")
        self.supabase: Client = create_client(self.url, self.key)

    def insert_data(self, table_name, data):
        try:
            response = self.supabase.table(table_name).insert(data).execute()
            return response
        except Exception as e:
            print(f"❌ Database Error: {e}")