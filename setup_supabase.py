"""Setup script to initialize Supabase database table."""
from app.core.database import get_db
from app.core.config import settings

def setup_database():
    """Create the scans table if it doesn't exist."""
    print("=" * 60)
    print("Setting up Supabase Database")
    print("=" * 60)
    
    try:
        supabase = get_db()
        
        # SQL to create the table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS scans (
            id BIGSERIAL PRIMARY KEY,
            patient_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            image_url TEXT NOT NULL,
            analysis_result JSONB NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """
        
        # Try to execute via RPC or direct SQL
        # Note: This requires service role key, not anon key
        # If this fails, user needs to run SQL manually in Supabase dashboard
        try:
            result = supabase.rpc('exec_sql', {'sql': create_table_sql}).execute()
            print("[OK] Table created via RPC")
        except Exception as e:
            # RPC might not be available, so we'll provide manual instructions
            print("[INFO] Cannot create table automatically (requires service role key)")
            print("[INFO] Please run this SQL manually in Supabase Dashboard:")
            print("-" * 60)
            print(create_table_sql)
            print("-" * 60)
        
        # Test connection by trying to query
        try:
            test_result = supabase.table("scans").select("id").limit(1).execute()
            print("[OK] Database connection successful")
            print("[OK] Table 'scans' exists and is accessible")
        except Exception as e:
            print(f"[WARNING] Table might not exist yet: {str(e)}")
            print("[INFO] Please create the table using the SQL above")
        
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"[ERROR] Database setup failed: {str(e)}")
        print("\n[INFO] Please create the table manually in Supabase Dashboard:")
        print("-" * 60)
        print("""
CREATE TABLE IF NOT EXISTS scans (
    id BIGSERIAL PRIMARY KEY,
    patient_name TEXT NOT NULL,
    age INTEGER NOT NULL,
    image_url TEXT NOT NULL,
    analysis_result JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
        """)
        print("-" * 60)
        return False

if __name__ == "__main__":
    setup_database()






