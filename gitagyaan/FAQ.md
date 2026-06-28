# ❓ Frequently Asked Questions (FAQ)

## General Questions

### Q1: What is this project?
**A:** This is an AI-powered Question-Answering system for the Bhagavad Gita (Chapter 1, first 15 slokas). It uses Google Gemini 2.0 Flash AI to provide accurate answers based on semantic search through the verses.

### Q2: Do I need to know programming to use it?
**A:** No! Once installed, just run the app and use the web interface. Installation requires basic command-line knowledge, but we provide step-by-step instructions.

### Q3: Is it free to use?
**A:** Yes! The Google Gemini API has a free tier that's more than sufficient for personal use. The API key is already configured.

### Q4: How accurate are the answers?
**A:** Very accurate! The system retrieves relevant slokas using AI-powered semantic search and generates answers strictly based on the retrieved context. It won't make up information.

### Q5: Can I use this offline?
**A:** Partially. After the first run (which requires internet to build the index), the FAISS search works offline. However, answering questions requires an internet connection for the Gemini API.

---

## Installation Questions

### Q6: What operating systems are supported?
**A:** Windows 10/11, macOS, and Linux (Ubuntu, Debian, Fedora, etc.). WSL (Windows Subsystem for Linux) is also supported.

### Q7: What Python version do I need?
**A:** Python 3.8 or higher. We recommend Python 3.10+ for best performance.

### Q8: How much disk space does it need?
**A:** About 300 MB total:
- Python libraries: ~200-300 MB
- Application: ~1 MB
- Generated files: ~100 KB

### Q9: How long does installation take?
**A:** 2-5 minutes, depending on your internet speed.

### Q10: Can I install it in a virtual environment?
**A:** Yes! Recommended for isolation:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Usage Questions

### Q11: How do I start the application?
**A:** 
- **Windows**: Double-click `run_app.bat` or run `streamlit run app.py`
- **Mac/Linux**: Run `./run_app.sh` or `streamlit run app.py`

### Q12: Why is the first run so slow?
**A:** The first run (1-2 minutes) generates embeddings for all 15 slokas and builds the FAISS index. This only happens once. Subsequent runs take 2-3 seconds.

### Q13: How do I ask questions?
**A:** Simply type your question in plain English in the text box and click "Get Answer". Examples:
- "Who is speaking in the first sloka?"
- "What did Bhishma do?"

### Q14: Can I ask questions in other languages?
**A:** Currently, only English questions are supported. The slokas are in English translation.

### Q15: How many slokas are covered?
**A:** The first 15 slokas of Chapter 1 (Arjuna Vishada Yoga) of the Bhagavad Gita.

---

## Technical Questions

### Q16: What AI model is used?
**A:** 
- **Answer Generation**: Google Gemini 2.0 Flash
- **Embeddings**: Google text-embedding-004 (768 dimensions)

### Q17: What is FAISS?
**A:** FAISS (Facebook AI Similarity Search) is a library for efficient similarity search. It helps find the most relevant slokas for your question by comparing vector embeddings.

### Q18: How does the semantic search work?
**A:** 
1. Each sloka is converted to a 768-dimensional vector (embedding)
2. Your question is also converted to a vector
3. FAISS finds the 3 most similar sloka vectors
4. These slokas are sent to Gemini as context for answering

### Q19: Can I change the number of retrieved slokas?
**A:** Yes! Open `app.py` and change the `TOP_K` variable (default: 3).

### Q20: Where is the data stored?
**A:** 
- Source data: `gita_slokas.json`
- Index files: `faiss_index.bin` and `sloka_mapping.pkl` (generated)
- No query history is stored

---

## Performance Questions

### Q21: How fast are queries?
**A:** Typically 2-5 seconds per query:
- FAISS search: < 0.01 seconds
- API calls: 2-4 seconds

### Q22: Is there a query limit?
**A:** The Gemini API has rate limits (free tier: 15 queries per minute). For personal use, this is more than enough.

### Q23: Can I make it faster?
**A:** 
- Use a faster internet connection
- Reduce `TOP_K` (fewer slokas = smaller context = faster)
- The FAISS part is already optimized

### Q24: Does it cache answers?
**A:** Not currently, but this would be a great future enhancement!

---

## Error & Troubleshooting

### Q25: "Module not found" error?
**A:** Run `pip install -r requirements.txt` to install all dependencies.

### Q26: "Port 8501 already in use"?
**A:** Another Streamlit app is running. Close it or use a different port:
```bash
streamlit run app.py --server.port 8502
```

### Q27: "API key invalid" error?
**A:** The API key might have expired. Get a new one from [Google AI Studio](https://makersuite.google.com/app/apikey) and update it in `app.py`.

### Q28: "Failed to load index"?
**A:** Delete `faiss_index.bin` and `sloka_mapping.pkl`, then restart. The app will rebuild them.

### Q29: Blank screen on launch?
**A:** 
- Check console for errors
- Ensure all files are in the same folder
- Try `python test_setup.py` to diagnose

### Q30: "No answer returned"?
**A:** 
- Check your internet connection
- The question might be too vague—try being more specific
- Check console for API errors

---

## Data & Content Questions

### Q31: Where does the sloka data come from?
**A:** The data is from standard English translations of the Bhagavad Gita, formatted into JSON.

### Q32: Can I add more slokas?
**A:** Yes! Edit `gita_slokas.json` to add more slokas (follow the existing format), then delete the index files and restart the app.

### Q33: Can I use this for other chapters?
**A:** Yes! Add slokas from other chapters to `gita_slokas.json`. The system will automatically index them.

### Q34: Is Sanskrit text included?
**A:** Not in the current version, but you can add it to the JSON file.

### Q35: Are the translations accurate?
**A:** The translations are from standard English versions. Multiple interpretations exist; this uses commonly accepted translations.

---

## API & Authentication

### Q36: Do I need my own API key?
**A:** No, an API key is already configured. But you can get your own from [Google AI Studio](https://makersuite.google.com/app/apikey) for higher rate limits.

### Q37: Is my data sent to Google?
**A:** Yes, questions and context are sent to Google Gemini API for processing. No data is stored by the app locally.

### Q38: Can I use a different AI model?
**A:** Yes! Modify the `MODEL_NAME` variable in `app.py`. Options: `gemini-pro`, `gemini-1.5-flash`, etc.

### Q39: What if the API is down?
**A:** You'll get an error message. Wait and try again. Check [Google Cloud Status](https://status.cloud.google.com/) for updates.

### Q40: How many API calls does one query make?
**A:** Two calls:
1. Embedding generation (query)
2. Answer generation (Gemini)

---

## Customization Questions

### Q41: Can I change the UI colors?
**A:** Yes! Streamlit supports themes. Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF6B35"
backgroundColor = "#FFF8F0"
```

### Q42: Can I add more features?
**A:** Absolutely! The code is well-documented. Ideas:
- Add audio narration
- Export to PDF
- Multi-language support
- Query history

### Q43: Can I deploy this online?
**A:** Yes! Use Streamlit Cloud, Heroku, or AWS. Remember to use environment variables for the API key in production.

### Q44: Can I modify the prompt?
**A:** Yes! Edit the `ask_gemini()` function in `app.py` to customize the prompt sent to Gemini.

### Q45: Can I use this for other texts?
**A:** Yes! Just replace `gita_slokas.json` with your own data (follow the same format).

---

## Advanced Questions

### Q46: What's the embedding dimension?
**A:** 768 dimensions (Google text-embedding-004 model).

### Q47: What distance metric does FAISS use?
**A:** L2 (Euclidean) distance via `IndexFlatL2`.

### Q48: Can I use GPU acceleration?
**A:** Yes! Install `faiss-gpu` instead of `faiss-cpu`:
```bash
pip install faiss-gpu
```

### Q49: How is context formatted?
**A:** Retrieved slokas are formatted as:
```
Sloka 1:
Verse: [verse text]
Explanation: [explanation]
```

### Q50: Can I integrate this with other apps?
**A:** Yes! You can use the core functions (`retrieve_context`, `ask_gemini`) as an API or library.

---

## Future Enhancements

### Q51: Will you add more chapters?
**A:** This is a demonstration project. You can easily add more chapters by editing the JSON file!

### Q52: Will you add audio?
**A:** Great idea! Consider contributing or forking the project to add this feature.

### Q53: Can I contribute?
**A:** This is open for enhancement! Feel free to fork and improve.

### Q54: Will you add chat history?
**A:** Not currently implemented, but would be a great addition using Streamlit session state.

### Q55: Will you support other languages?
**A:** Currently English-only. Multi-language support would require translated sloka data.

---

## Best Practices

### Q56: What makes a good question?
**A:** 
- ✅ Specific: "Who blew the Panchajanya conch?"
- ❌ Vague: "Tell me about sounds"

### Q57: How can I get better answers?
**A:** 
- Be specific
- Reference elements from the slokas
- Ask one thing at a time

### Q58: Should I delete the index files?
**A:** Only if:
- You added/changed slokas
- The index is corrupted
- You want to rebuild from scratch

### Q59: How do I backup my setup?
**A:** Just copy the entire `GitaGyaan` folder. Everything is self-contained.

### Q60: Can I run multiple instances?
**A:** Yes, but use different ports:
```bash
streamlit run app.py --server.port 8502
```

---

## Contact & Support

### Q61: Where can I report bugs?
**A:** Check the console output and review the troubleshooting section in README.md.

### Q62: Is there a user community?
**A:** This is a standalone project. Feel free to share and discuss with others!

### Q63: Can I use this for commercial purposes?
**A:** Check Google's Gemini API terms of service for commercial use restrictions.

### Q64: Who created this?
**A:** This was created as an AI-powered educational tool for spiritual seekers and AI enthusiasts.

### Q65: How can I learn more about the Bhagavad Gita?
**A:** This app is a great start! For deeper study, consult traditional commentaries and teachers.

---

**Still have questions? Check README.md or INSTALLATION.md for more details! 🙏**
