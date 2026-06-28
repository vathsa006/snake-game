# 🚀 Quick Start Guide

## ⚡ Get Started in 3 Steps

### Step 1: Install Dependencies (2 minutes)

Open Command Prompt (Windows) or Terminal (Mac/Linux) and navigate to the project folder:

```bash
cd d:\NLP\GitaGyaan
```

Install all required libraries:

```bash
pip install -r requirements.txt
```

### Step 2: Verify Setup (30 seconds)

Run the test script to ensure everything is working:

```bash
python test_setup.py
```

You should see all green checkmarks ✅

### Step 3: Launch the App (10 seconds)

Start the Streamlit application:

```bash
streamlit run app.py
```

Your browser will automatically open to `http://localhost:8501`

---

## 🎯 First Time Use

**On the first run**, the app will take 1-2 minutes to:
- Initialize Gemini API
- Generate embeddings for all 15 slokas
- Build the FAISS index
- Save the index to disk

**You'll see a progress bar** during this process.

**After the first run**, the app will start in 2-3 seconds because the index is cached!

---

## 💡 Try These Example Questions

Copy and paste these into the app:

1. **Who is speaking in the first sloka?**
2. **What did Duryodhana tell Drona?**
3. **Name three warriors from the Pandava side**
4. **Who blew the conchshell called Panchajanya?**
5. **What is the name of Bhima's conchshell?**
6. **How does Duryodhana compare the two armies?**
7. **What did Bhishma do after Duryodhana's speech?**

---

## 🔧 Troubleshooting

### Can't install libraries?
Try upgrading pip first:
```bash
python -m pip install --upgrade pip
```

### Port already in use?
Use a different port:
```bash
streamlit run app.py --server.port 8502
```

### API not working?
Check your internet connection. The API key is already configured.

---

## 📖 Need More Help?

Check the full **README.md** for detailed documentation.

---

**Happy Questioning! 🙏**
