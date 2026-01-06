-- Fix the 'scans' table schema
-- Run this in your Supabase SQL Editor

-- Option 1: If table doesn't exist or you want to recreate it
DROP TABLE IF EXISTS scans CASCADE;

CREATE TABLE scans (
    id BIGSERIAL PRIMARY KEY,
    patient_name TEXT NOT NULL,
    age INTEGER NOT NULL,
    image_url TEXT NOT NULL,
    analysis_result JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Option 2: If table exists and you just need to add the missing column
-- Uncomment these if you want to alter instead of recreate:
-- ALTER TABLE scans ADD COLUMN IF NOT EXISTS analysis_result JSONB;
-- ALTER TABLE scans ADD COLUMN IF NOT EXISTS image_url TEXT;
-- ALTER TABLE scans ADD COLUMN IF NOT EXISTS patient_name TEXT;
-- ALTER TABLE scans ADD COLUMN IF NOT EXISTS age INTEGER;
-- ALTER TABLE scans ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW();

-- Grant permissions (if using RLS)
ALTER TABLE scans ENABLE ROW LEVEL SECURITY;

-- Create a policy to allow all operations (adjust as needed for your security requirements)
CREATE POLICY "Allow all operations on scans" ON scans
    FOR ALL
    USING (true)
    WITH CHECK (true);






