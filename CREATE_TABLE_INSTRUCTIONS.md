# Fix Database Table Schema

## Problem
The `scans` table is missing the `analysis_result` column (and possibly other columns).

## Solution

### Step 1: Open Supabase SQL Editor
Go to: **https://supabase.com/dashboard/project/bsdrmxzjpvakoayqktju/sql/new**

### Step 2: Run This SQL

```sql
-- Drop and recreate the table with correct schema
DROP TABLE IF EXISTS scans CASCADE;

CREATE TABLE scans (
    id BIGSERIAL PRIMARY KEY,
    patient_name TEXT NOT NULL,
    age INTEGER NOT NULL,
    image_url TEXT NOT NULL,
    analysis_result JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS (Row Level Security)
ALTER TABLE scans ENABLE ROW LEVEL SECURITY;

-- Create a policy to allow all operations
-- (Adjust this based on your security needs)
CREATE POLICY "Allow all operations on scans" ON scans
    FOR ALL
    USING (true)
    WITH CHECK (true);
```

### Step 3: Verify
After running the SQL, try uploading a file again at: http://localhost:8000/docs

---

## Alternative: If You Want to Keep Existing Data

If you have data in the table and want to keep it, use this instead:

```sql
-- Add missing columns
ALTER TABLE scans 
    ADD COLUMN IF NOT EXISTS analysis_result JSONB,
    ADD COLUMN IF NOT EXISTS image_url TEXT,
    ADD COLUMN IF NOT EXISTS patient_name TEXT,
    ADD COLUMN IF NOT EXISTS age INTEGER,
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW();

-- Set default for existing rows if needed
UPDATE scans 
SET analysis_result = '{}'::jsonb 
WHERE analysis_result IS NULL;
```






