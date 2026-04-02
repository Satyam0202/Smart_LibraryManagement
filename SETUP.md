# Setup Guide - Library Management System

Complete step-by-step guide to set up the Library Management System on your local machine.

---

## 📋 Prerequisites

### System Requirements
- **OS**: Windows 10/11, macOS, or Linux
- **RAM**: 2GB minimum
- **Storage**: 500MB free space
- **Network**: Local network access to localhost

### Required Software

#### 1. Python 3.7 or Higher
**Windows:**
- Download from https://www.python.org/downloads/
- During installation: ✅ Check "Add Python to PATH"
- Verify: Open CMD and run `python --version`

**macOS:**
```bash
brew install python3
python3 --version
```

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version
```

#### 2. C++ Compiler

**Windows (MinGW):**
- Download from https://www.mingw-w64.org/
- Add to PATH environment variable
- Verify: Open CMD and run `g++ --version`

**macOS (Xcode):**
```bash
xcode-select --install
g++ --version
```

**Linux:**
```bash
sudo apt install build-essential
g++ --version
```

#### 3. Git (Optional but Recommended)
```bash
# Windows, macOS, Linux
# Download from https://git-scm.com/
git --version
```

#### 4. Modern Web Browser
- Google Chrome (recommended)
- Mozilla Firefox
- Microsoft Edge
- Safari

---

## 🚀 Installation Steps

### Step 1: Clone or Download Repository

**Using Git:**
```bash
git clone https://github.com/yourusername/library-management.git
cd library
```

**Or Download ZIP:**
1. Click "Code" → "Download ZIP"
2. Extract to desired location
3. Open terminal in extracted folder

### Step 2: Verify Project Structure

```
library/
├── app.py
├── library.cpp
├── requirements.txt
├── README.md
├── templates/
│   └── dashboard.html
├── static/
└── *.csv files (will be created)
```

### Step 3: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Your terminal should now show `(venv)` prefix.

### Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install Flask==2.3.0
```

Verify:
```bash
pip list
# Should show Flask, Werkzeug, Jinja2, etc.
```

### Step 5: Compile C++ Code

**Windows:**
```bash
g++ -o library.exe library.cpp
```

**macOS/Linux:**
```bash
g++ -o library library.cpp
# Then update app.py line 13: subprocess.run(['./library', ...])
```

Verify:
```bash
# Windows
library.exe get_books

# macOS/Linux
./library get_books
```

Should display book list.

### Step 6: Run Flask Application

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Step 7: Access in Browser

Open your browser and go to:
```
http://localhost:5000
```

You should see the Login page.

---

## 🔐 First Time Setup

### Create Default Credentials

The system comes with one default user:

**Username:** `admin`  
**Password:** `admin123`

### Login & Initialize

1. Open http://localhost:5000
2. Click "Login"
3. Enter admin/admin123
4. Click "Dashboard"
5. Add some members and books to test

---

## 🧪 Testing Installation

### Test 1: Backend Connectivity
```bash
# In the library folder
python -c "
import subprocess
result = subprocess.run(['library.exe', 'get_books'], capture_output=True, text=True)
lines = [l for l in result.stdout.split('\n') if '|' in l]
print(f'✅ Connected! Found {len(lines)} books')
"
```

### Test 2: Flask Server
```bash
# Terminal window
python app.py

# In another terminal
curl http://localhost:5000
# Should return HTML content
```

### Test 3: Database Files
```bash
# Check if CSV files exist
ls -la *.csv

# Should show:
# - library.csv (books)
# - members.csv (members)
# - issued_books.csv (issuance tracking)
# - activity.csv (activity log)
# - users.csv (authentication)
```

### Test 4: Browser Functionality
1. Open http://localhost:5000
2. Login with admin/admin123
3. Navigate to Books tab
4. Add a test book
5. Navigate to Members tab
6. Add a test member
7. Issue a book to the member
8. Verify in Issued Books tab

---

## 🐛 Troubleshooting

### Issue: "python: command not found"
**Solution:**
- Windows: Reinstall Python and check "Add Python to PATH"
- macOS/Linux: Use `python3` instead of `python`

### Issue: "g++ is not recognized"
**Solution:**
- Windows: Install MinGW and add to PATH
- Edit system environment: `Control Panel → System → Environment Variables`
- Add C++ compiler path to PATH

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:**
```bash
# Make sure virtual environment is activated
pip install flask

# Or reinstall all dependencies
pip install -r requirements.txt
```

### Issue: "library.exe not found"
**Solution:**
```bash
# Recompile C++ code
g++ -o library.exe library.cpp

# Verify compilation worked
library.exe get_books
# Should display books
```

### Issue: "Address already in use"
**Solution:**
```bash
# Another Flask instance is running
# Kill it and restart:

# Windows (Command Prompt as admin)
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or change Flask port in app.py line 430:
# app.run(debug=True, port=5001)
```

### Issue: "CSV file not found"
**Solution:**
- CSV files are created automatically on first run
- If missing, delete `*.csv` files and restart
- Login to initialize database files

### Issue: Blank Dashboard or Missing Data
**Solution:**
```bash
# Clear browser cache (Ctrl+Shift+Delete in most browsers)
# Or use Incognito/Private window
# Restart Flask server
```

### Issue: "RuntimeError: Click will abort further execution because Python was configured to use ASCII as encoding"
**Solution (macOS/Linux):**
```bash
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
python app.py
```

### Issue: Books/Members not displaying
**Solution:**
1. Stop Flask server (Ctrl+C)
2. Delete CSV files: `rm *.csv`
3. Restart Flask: `python app.py`
4. Add test data manually
5. Check browser console (F12) for JavaScript errors

---

## 📁 Initial Database Setup

### First Run
When you start Flask for the first time:
1. Create users.csv with admin account
2. Create empty library.csv
3. Create empty members.csv
4. Create empty issued_books.csv
5. Create empty activity.csv

### Add Sample Data
Go to Books tab → Click "📖 Add Book" → Add sample books

Or use the endpoint:
```bash
curl -X POST http://localhost:5000/populate_sample_data
```

---

## 🔑 Changing Admin Password

Currently hardcoded. To change:

1. Open `app.py`
2. Find line with `if username == "admin" and password == "admin123"`
3. Change `"admin123"` to your new password
4. Save and restart Flask

### Better: Create New User in CSV

Edit `users.csv`:
```
username,password
admin,newpassword
user1,password1
```

---

## 📋 Environment Variables (Optional)

Create `.env` file (if using python-dotenv):
```
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000
```

Load in app.py:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 💾 Backup Your Data

### Backup Everything
```bash
# Create backup folder
mkdir backup

# Copy all CSV files
cp *.csv backup/

# Or
cp -r library backup_$(date +%Y%m%d)
```

### Backup Script
Create `backup.sh`:
```bash
#!/bin/bash
BACKUP_DIR="backups/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR
cp *.csv $BACKUP_DIR/
echo "✅ Backup created: $BACKUP_DIR"
```

---

## 🔄 Resetting to Factory Defaults

```bash
# Stop Flask server (Ctrl+C)

# Delete all data files
rm *.csv

# Restart Flask
python app.py

# Login with admin/admin123
# Database will reinitialize
```

---

## 📱 Accessing from Other Machines

### On Same Network
1. Find your IP address:
   - Windows: `ipconfig` (look for IPv4)
   - macOS/Linux: `ifconfig` | `hostname -I`

2. From other machine, visit:
   ```
   http://<YOUR_IP>:5000
   ```

### Example
If your IP is `192.168.1.100`:
```
http://192.168.1.100:5000
```

---

## ⚙️ Advanced Configuration

### Change Data Location
In `app.py`, modify CSV file paths:
```python
CSV_BOOKS = "path/to/library.csv"
CSV_MEMBERS = "path/to/members.csv"
CSV_ISSUED = "path/to/issued_books.csv"
CSV_ACTIVITY = "path/to/activity.csv"
```

### Change Flask Port
Edit `app.py` last line:
```python
app.run(debug=True, port=8000)  # Change 5000 to 8000
```

### Enable Production Mode
```python
app.run(debug=False)  # Set to False for production
```

---

## 🚀 Performance Tips

1. **Use SSD**: Data access is faster
2. **Increase Buffer**: Larger CSV buffers for file I/O
3. **Disable Debug**: Set `debug=False` in production
4. **Minimize Browser Extensions**: Can slow JavaScript
5. **Clear Cache Regularly**: Old data can cause issues

---

## 📊 Monitoring

### Check Current Processes
```bash
# Windows
tasklist | findstr python

# macOS/Linux
ps aux | grep python
```

### Monitor File Changes
```bash
# Windows PowerShell
Get-Item *.csv | Select LastWriteTime

# macOS/Linux
ls -l *.csv
```

---

## 🆘 Getting Help

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review [README.md](README.md) FAQ section
3. Check GitHub Issues
4. Contact developer: m4740600@gmail.com

---

## ✅ Verification Checklist

Before considering installation complete:

- [ ] Python installed and accessible
- [ ] Virtual environment created and activated
- [ ] Flask installed (`pip list` shows Flask)
- [ ] C++ compiler installed (`g++ --version` works)
- [ ] C++ code compiled successfully
- [ ] Flask server starts without errors
- [ ] Dashboard loads in browser
- [ ] Can login with admin/admin123
- [ ] Can add books
- [ ] Can add members
- [ ] Can issue books
- [ ] Activity log records operations

---

## 📞 Support

For issues not covered here:

1. Email: m4740600@gmail.com
2. GitHub Issues: https://github.com/yourusername/library-management/issues
3. Check CONTRIBUTING.md for more info

---

**Happy Setting Up!** 🎉

If you found this guide helpful, please consider giving the project a ⭐ on GitHub!
