# Fix Supabase URL Issue

## Problem
The URL `bsdrmxzjpvakoqyqktju.supabase.co` cannot be resolved (DNS error).

## Solution: Get the Correct URL

### Step 1: Open Supabase Dashboard
Go to: **https://supabase.com/dashboard**

### Step 2: Find Your Project
- If you see your project, click on it
- If you don't see a project, you need to create one first

### Step 3: Get the Project URL
1. Click on **Settings** (gear icon in left sidebar)
2. Click on **API** 
3. Look for **Project URL** - it should look like:
   ```
   https://xxxxxxxxxxxxx.supabase.co
   ```
4. **Copy this URL exactly** (no trailing slash)

### Step 4: Verify the Key
In the same API settings page:
- Look for **anon public** key (for client-side)
- Or **service_role** key (for server-side - keep this secret!)

The key format `sb_publishable_...` is correct for newer Supabase projects.

### Step 5: Update .env File
Once you have the correct URL, update your `.env` file:

```
SUPABASE_URL=https://your-actual-project-ref.supabase.co
SUPABASE_KEY=sb_publishable_0lxbHTqeaGKoH__ChW5F3w_zvA6U6yC
```

### Step 6: Restart Server
After updating, restart your FastAPI server.

---

## Alternative: Create a New Project

If the project doesn't exist:
1. Go to https://supabase.com/dashboard
2. Click "New Project"
3. Fill in the details
4. Wait for project to be created
5. Copy the new Project URL and key
6. Update your `.env` file

---

## Quick Test

After updating, test with:
```bash
python test_supabase_connection.py
```






