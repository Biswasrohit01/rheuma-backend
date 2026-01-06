# Troubleshooting: DNS Resolution Error

## Error: `[Errno 11001] getaddrinfo failed`

This error means your computer cannot resolve the Supabase hostname. Here are the solutions:

### Solution 1: Verify Your Supabase URL

1. Go to your Supabase Dashboard: https://supabase.com/dashboard
2. Select your project
3. Go to **Settings** → **API**
4. Copy the **Project URL** - it should look like: `https://xxxxx.supabase.co`
5. Make sure there's NO trailing slash

### Solution 2: Check Network Connectivity

```powershell
# Test if you can reach Supabase
ping supabase.co

# Test DNS resolution
nslookup bsdrmxzjpvakoqyqktju.supabase.co
```

### Solution 3: Check Firewall/Proxy

- If you're on a corporate network, check if Supabase is blocked
- Try using a different network (mobile hotspot)
- Check Windows Firewall settings

### Solution 4: Verify Project Status

1. Go to: https://supabase.com/dashboard/project/bsdrmxzjpvakoqyqktju
2. Make sure the project is **Active** (not paused)
3. Check if the project exists

### Solution 5: Update .env File

Make sure your `.env` file has the correct format (no quotes, no spaces):

```
SUPABASE_URL=https://bsdrmxzjpvakoqyqktju.supabase.co
SUPABASE_KEY=sb_publishable_0lxbHTqeaGKoH__ChW5F3w_zvA6U6yC
```

### Solution 6: Test with Python

Run this to test connectivity:

```python
import socket
import requests

# Test DNS
try:
    ip = socket.gethostbyname("bsdrmxzjpvakoqyqktju.supabase.co")
    print(f"DNS OK: {ip}")
except Exception as e:
    print(f"DNS Failed: {e}")

# Test HTTP connection
try:
    r = requests.get("https://bsdrmxzjpvakoqyqktju.supabase.co", timeout=5)
    print(f"HTTP OK: {r.status_code}")
except Exception as e:
    print(f"HTTP Failed: {e}")
```






