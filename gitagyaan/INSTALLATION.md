# 📥 Complete Installation Guide

## For Windows Users 🪟

### Method 1: Double-Click Launch (Easiest!)

1. **Double-click `run_app.bat`**
   - This will automatically:
     - Check Python installation
     - Install missing libraries
     - Launch the application

2. **Wait for browser to open**
   - The app will open at `http://localhost:8501`

That's it! 🎉

### Method 2: Manual Installation

1. **Open Command Prompt** (Win + R, type `cmd`, press Enter)

2. **Navigate to project folder:**
   ```cmd
   cd d:\NLP\GitaGyaan
   ```

3. **Install libraries:**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Run the app:**
   ```cmd
   streamlit run app.py
   ```

---

## For Mac/Linux Users 🍎🐧

### Method 1: Shell Script (Easiest!)

1. **Make the script executable:**
   ```bash
   chmod +x run_app.sh
   ```

2. **Run the script:**
   ```bash
   ./run_app.sh
   ```

3. **Wait for browser to open**
   - The app will open at `http://localhost:8501`

### Method 2: Manual Installation

1. **Open Terminal**

2. **Navigate to project folder:**
   ```bash
   cd /path/to/GitaGyaan
   ```

3. **Install libraries:**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

---

## 📦 What Gets Installed?

The following Python packages will be installed:

| Package | Version | Purpose |
|---------|---------|---------|
| google-generativeai | Latest | Google Gemini API client |
| faiss-cpu | Latest | Vector similarity search |
| streamlit | Latest | Web UI framework |
| numpy | Latest | Numerical computing |
| pandas | Latest | Data manipulation |
| tqdm | Latest | Progress bars |

**Total Size**: ~200-300 MB

**Installation Time**: 2-5 minutes (depends on internet speed)

---

## ✅ Verify Installation

### Option 1: Run Test Script

```bash
python test_setup.py
```

You should see all green checkmarks ✅

### Option 2: Check Manually

```bash
pip list | grep -E "streamlit|faiss|google-generativeai"
```

All three should appear in the list.

---

## 🔧 Troubleshooting

### Problem: "Python is not recognized"

**Solution**: 
- Install Python from [python.org](https://www.python.org/)
- During installation, check "Add Python to PATH"
- Restart your terminal/command prompt

### Problem: "pip is not recognized"

**Solution**:
```bash
python -m ensurepip --upgrade
```

### Problem: "Permission denied" (Mac/Linux)

**Solution**:
```bash
pip3 install --user -r requirements.txt
```

### Problem: FAISS installation fails

**Solution**: Try installing with conda instead:
```bash
conda install -c pytorch faiss-cpu
```

Or use the GPU version:
```bash
pip install faiss-gpu
```

### Problem: Port 8501 already in use

**Solution**: Use a different port:
```bash
streamlit run app.py --server.port 8502
```

### Problem: "Module not found" errors

**Solution**: Reinstall all dependencies:
```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

---

## 🌐 Internet Connection Required

This application requires internet for:
- ✅ Installing dependencies (one-time)
- ✅ Generating embeddings (first run only)
- ✅ Querying Gemini API (every question)

**Note**: After the first run, only API queries need internet.

---

## 💾 Disk Space Requirements

- **Python packages**: ~200-300 MB
- **Application files**: ~1 MB
- **Generated index**: ~100 KB

**Total**: ~300 MB

---

## 🐍 Python Version

- **Minimum**: Python 3.8
- **Recommended**: Python 3.10+
- **Tested on**: Python 3.11

Check your version:
```bash
python --version
```

---

## 🔄 Update Instructions

To update the application:

1. **Pull latest changes** (if using Git)
   ```bash
   git pull
   ```

2. **Update dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Delete old index files** (if structure changed)
   ```bash
   rm faiss_index.bin sloka_mapping.pkl
   ```

4. **Restart the app**

---

## 🗑️ Uninstall Instructions

To completely remove the application:

1. **Delete the project folder**
   ```bash
   rm -rf GitaGyaan
   ```

2. **Uninstall Python packages** (optional)
   ```bash
   pip uninstall google-generativeai faiss-cpu streamlit numpy pandas tqdm -y
   ```

---

## 📱 Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| Windows 10/11 | ✅ Fully Supported | Use `run_app.bat` |
| macOS | ✅ Fully Supported | Use `run_app.sh` |
| Linux (Ubuntu/Debian) | ✅ Fully Supported | Use `run_app.sh` |
| WSL (Windows Subsystem for Linux) | ✅ Supported | Use Linux instructions |

---

## 🔐 Security Notes

- **API Key**: Embedded in code (for convenience)
- **Data**: All processing is done via Google's API
- **Privacy**: No local storage of queries
- **Network**: HTTPS connections only

---

## 🆘 Still Having Issues?

1. **Check Python installation**:
   ```bash
   python --version
   pip --version
   ```

2. **Verify file integrity**:
   ```bash
   python test_setup.py
   ```

3. **Check internet connection**:
   ```bash
   ping google.com
   ```

4. **Review error messages** in the terminal

5. **Consult README.md** for detailed documentation

---

## 🎓 Next Steps

After installation:

1. ✅ Run `python test_setup.py` to verify
2. ✅ Launch the app with `streamlit run app.py`
3. ✅ Try example questions from QUICKSTART.md
4. ✅ Explore the interface
5. ✅ Have fun learning! 🙏

---

**Installation complete? Great! Now check QUICKSTART.md to start using the app! 🚀**
