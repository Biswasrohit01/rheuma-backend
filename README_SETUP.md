# RheumaLens Backend Setup Guide

## Quick Setup Steps

### 1. Database Table Setup

Go to your Supabase Dashboard → SQL Editor and run:

```sql
CREATE TABLE IF NOT EXISTS scans (
    id BIGSERIAL PRIMARY KEY,
    patient_name TEXT NOT NULL,
    age INTEGER NOT NULL,
    image_url TEXT NOT NULL,
    analysis_result JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Direct Link to SQL Editor:**
https://supabase.com/dashboard/project/bsdrmxzjpvakoqyqktju/sql/new

### 2. Storage Bucket Setup

1. Go to Supabase Dashboard → Storage
2. Click "New bucket"
3. Name: `scans`
4. Make it **Public** (or configure RLS policies)
5. Click "Create bucket"

**Direct Link to Storage:**
https://supabase.com/dashboard/project/bsdrmxzjpvakoqyqktju/storage/buckets

### 3. Start the Server

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start server
python main.py
```

### 4. Test the API

Once the server is running, visit:
- **API Documentation (Swagger UI):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health
- **Root:** http://localhost:8000

### API Endpoints

- **POST** `/api/v1/upload` - Upload scan image
  - Requires: `file` (image) and `patient_data` (JSON string with `patient_name` and `age`)
  
- **GET** `/api/v1/patients` - Get all scans

### Example Upload Request

Using the Swagger UI at http://localhost:8000/docs:
1. Click on `/api/v1/upload`
2. Click "Try it out"
3. Upload an image file
4. For `patient_data`, use: `{"patient_name": "John Doe", "age": 45}`
5. Click "Execute"






