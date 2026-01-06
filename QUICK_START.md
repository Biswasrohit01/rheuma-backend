# 🚀 RheumaLens Backend - Quick Start

## ✅ Server Status
The server should now be running! Check the new PowerShell window that opened.

## 🔗 **TEST YOUR API HERE:**

### Main Links:
- **📚 API Documentation (Swagger UI):** http://localhost:8000/docs
- **📖 Alternative Docs (ReDoc):** http://localhost:8000/redoc  
- **❤️ Health Check:** http://localhost:8000/health
- **🏠 Root Endpoint:** http://localhost:8000

---

## ⚙️ **REQUIRED: Supabase Setup**

### 1️⃣ Create Database Table

**Link:** https://supabase.com/dashboard/project/bsdrmxzjpvakoqyqktju/sql/new

**SQL to Run:**
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

### 2️⃣ Create Storage Bucket

**Link:** https://supabase.com/dashboard/project/bsdrmxzjpvakoqyqktju/storage/buckets

**Steps:**
1. Click "New bucket"
2. Name: `scans`
3. Make it **Public**
4. Click "Create bucket"

---

## 🧪 **How to Test the Upload Endpoint**

### Option 1: Using Swagger UI (Easiest)
1. Go to: http://localhost:8000/docs
2. Find `/api/v1/upload` endpoint
3. Click "Try it out"
4. Upload an image file
5. For `patient_data`, enter: `{"patient_name": "John Doe", "age": 45}`
6. Click "Execute"

### Option 2: Using cURL
```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -F "file=@your_image.jpg" \
  -F 'patient_data={"patient_name": "John Doe", "age": 45}'
```

### Option 3: Using Postman
- Method: POST
- URL: http://localhost:8000/api/v1/upload
- Body: form-data
  - `file`: [Select File]
  - `patient_data`: `{"patient_name": "John Doe", "age": 45}`

---

## 📋 **API Endpoints**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| POST | `/api/v1/upload` | Upload scan image |
| GET | `/api/v1/patients` | Get all scans |

---

## 🛠️ **Troubleshooting**

If the server didn't start:
```bash
.\venv\Scripts\Activate.ps1
python main.py
```

If you get errors:
- Make sure the database table exists
- Make sure the storage bucket exists
- Check that `.env` file has correct credentials






