# 🔧 Quick Fix - Python Not Found

## Issue
Windows can't find Python in your PATH.

## Solutions (Try in order)

### Option 1: Use Python Launcher (Recommended)
```bash
# Try this instead of 'python':
py -3 --version

# If that works, use:
cd intelligence-service
py -3 -m venv venv
venv\Scripts\activate
py -3 -m pip install -r requirements.txt
py -3 src/main.py
```

### Option 2: Install Python
1. Visit: https://www.python.org/downloads/
2. Download Python 3.9 or higher
3. **Important:** Check "Add Python to PATH" during installation
4. Restart terminal
5. Run: `python --version`

### Option 3: Use Anaconda (If installed)
```bash
# If you have Anaconda:
conda --version

# Create environment:
cd intelligence-service
conda create -n nhl-game python=3.9
conda activate nhl-game
pip install -r requirements.txt
python src/main.py
```

### Option 4: Find Existing Python
```bash
# Check if Python is in common locations:
dir "C:\Python*" /s /b
dir "C:\Users\rhine\AppData\Local\Programs\Python" /s /b

# Or use Windows search for "python.exe"
```

## After Python Works

Once you can run `python --version`, do:

```bash
cd nhl-simulation-game/intelligence-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

You should see:
```
🏒 NHL Intelligence Service
=============================
Starting server...
✅ Puckcast model loaded successfully
```

Then visit: http://localhost:8000/docs

## Still Stuck?

**Quick test without venv:**
```bash
cd intelligence-service
pip install fastapi uvicorn pandas numpy scikit-learn
python src/main.py
```

⚠️ Not recommended long-term, but gets you running quickly!

## Alternative: Use Docker (Advanced)

If Python is too problematic, I can create a Docker setup that runs everything in a container (no Python install needed on your machine).

Want me to set that up instead?

