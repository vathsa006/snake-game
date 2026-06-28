# 📿 Bhagavad Gita Gyan - AI Chatbot

A modern AI-powered chatbot for exploring Bhagavad Gita Chapter 1 (first 15 slokas) using **Google Gemini 2.0 Flash**, **FAISS vector search**, and **Streamlit**.

## 🌟 Features

- **💬 Chatbot Interface**: Modern conversational UI with persistent chat history
- **🎨 Message Bubbles**: Clean chat design with user (orange) and AI (green) messages
- **📚 Comprehensive Sidebar**: Instructions, examples, and tips always available
- **🧠 Intelligent Answers**: Combines retrieved context with AI knowledge for comprehensive responses
- **🔍 Semantic Search**: FAISS vector search finds the most relevant verses
- **⚡ Fast Performance**: Cached FAISS index for quick responses
- **🌓 Dark Mode**: Full support for both light and dark themes
- **📱 Wide Layout**: Full-screen experience for comfortable reading

## 🛠️ Technology Stack

- **Google Gemini 2.0 Flash**: LLM for answer generation and embeddings
- **FAISS**: Facebook AI Similarity Search for efficient vector retrieval
- **Streamlit**: Modern web application framework
- **Python 3.8+**: Core programming language

## 📋 Prerequisites

- Python 3.8 or higher
- Internet connection (for Gemini API calls)
- Windows, macOS, or Linux

## 🚀 Installation

### Step 1: Clone or Download
Download this project to your local machine.

### Step 2: Install Dependencies

Open your terminal/command prompt and navigate to the project folder:

```bash
cd d:\NLP\GitaGyaan
```

Install all required libraries:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install google-generativeai
pip install faiss-cpu
pip install streamlit
pip install numpy
pip install pandas
pip install tqdm
```

### Step 3: Verify Files

Make sure you have these files in your project folder:
- `app.py` - Main application file
- `gita_slokas.json` - Slokas data (15 slokas from Chapter 1)
- `requirements.txt` - Python dependencies

## ▶️ Running the Application

### Start the Streamlit App

Run this command in your terminal:

```bash
streamlit run app.py
```

### Access the Web Interface

Your default browser should automatically open. If not, navigate to:

```
http://localhost:8501
```

### First Run

On the first run, the system will:
1. Initialize the Gemini API
2. Load the slokas from JSON
3. Generate embeddings for all slokas (takes 1-2 minutes)
4. Build and save the FAISS index

This process creates two files:
- `faiss_index.bin` - FAISS index for fast search
- `sloka_mapping.pkl` - Mapping of indices to sloka data

**Subsequent runs will be much faster** as these files are reused!

## 💡 How to Use the Chatbot

### Getting Started

1. **Check the Sidebar** 📚
   - Read the instructions
   - Review example questions
   - Check out pro tips
   - Learn about the system

2. **Start Chatting** 💬
   - Type your question in the input field at the bottom
   - Click "🔍 Ask Question" to submit
   - Watch as your question appears in an orange bubble
   - See the AI's answer appear in a green bubble

3. **Continue the Conversation** 🔄
   - Ask follow-up questions
   - Scroll up to review previous answers
   - All Q&A pairs remain visible in your session

4. **Clear When Needed** 🗑️
   - Click "Clear Chat" to start fresh
   - Perfect for switching topics

### Example Conversation

```
You (🟠): Who is Drona?

AI (🟢): Drona (Dronacharya) is the royal guru who taught 
         archery and warfare to both the Pandavas and Kauravas. 
         He is one of the greatest warriors and teachers in 
         the Mahabharata, and the father of Ashwatthama...

You (🟠): Who is Sanjaya?

AI (🟢): Sanjaya is King Dhritarashtra's charioteer and 
         minister. He possesses divine vision granted by 
         sage Vyasa, which allows him to see and narrate 
         the events of the battle...
```

## 📊 Example Questions

The sidebar includes 10+ example questions like:

- "Who is Drona?"
- "Who is speaking in the first sloka?"
- "What did Duryodhana tell his teacher?"
- "Name three warriors from the Pandava side"
- "Who blew the conchshell called Panchajanya?"
- "What is the name of Bhima's conchshell?"
- "How does Duryodhana compare the two armies?"
- "What did Bhishma do?"
- "Who is Sanjaya?"
- "What is the significance of Kurukshetra?"

## 🔧 Configuration

You can modify these settings in `app.py`:

- **TOP_K**: Number of slokas to retrieve (default: 3)
- **MODEL_NAME**: Gemini model to use (default: "gemini-2.0-flash")
- **GEMINI_API_KEY**: Your Gemini API key (already configured)

## 📁 Project Structure

```
GitaGyaan/
│
├── app.py                    # Main application file
├── gita_slokas.json          # Slokas data (15 slokas)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── faiss_index.bin          # Generated FAISS index (after first run)
└── sloka_mapping.pkl        # Generated sloka mapping (after first run)
```

## 🔑 API Configuration

The Google Gemini API key is already embedded in the code:
- **API Key**: `AIzaSyB23pN4vZIY79K9qmHD_PDDAZq3hDuQxZY`
- **Model**: `gemini-2.0-flash`
- **Embedding Model**: `text-embedding-004`

**Note**: For production use, consider storing the API key in environment variables.

## 🧠 How It Works

1. **Data Loading**: Loads 15 slokas from `gita_slokas.json`

2. **Embedding Generation**: 
   - Each sloka (verse + explanation) is converted to a 768-dimensional vector
   - Uses Google's `text-embedding-004` model

3. **FAISS Indexing**: 
   - Stores all embeddings in a FAISS index
   - Enables fast similarity search

4. **Question Processing**:
   - User question is converted to an embedding
   - FAISS finds the 3 most similar slokas

5. **Answer Generation**:
   - Retrieved slokas are sent to Gemini 2.0 Flash as context
   - Gemini generates a precise answer based only on the context

## 🐛 Troubleshooting

### Issue: "Failed to initialize Gemini API"
- **Solution**: Check your internet connection. The API key is embedded in the code.

### Issue: "File gita_slokas.json not found"
- **Solution**: Ensure `gita_slokas.json` is in the same folder as `app.py`

### Issue: Slow first run
- **Solution**: This is normal! Generating embeddings for 15 slokas takes time. Subsequent runs will be fast.

### Issue: "No module named 'faiss'"
- **Solution**: Install FAISS: `pip install faiss-cpu`

### Issue: Port 8501 already in use
- **Solution**: Stop other Streamlit apps or use: `streamlit run app.py --server.port 8502`

## 📈 Performance

- **First Run**: ~1-2 minutes (building FAISS index)
- **Subsequent Runs**: ~2-3 seconds (loading cached index)
- **Query Response Time**: ~2-5 seconds (depends on API latency)
- **Embedding Dimension**: 768 (Google text-embedding-004)

## 🔮 Future Enhancements

Potential features for upcoming versions:
- ✨ Auto-scroll to latest message
- ⏱️ Timestamps on each message
- 📋 Copy button for AI answers
- 💾 Export chat history (TXT/PDF)
- 🔄 Follow-up question suggestions
- 🔍 Search through chat history
- ✏️ Edit sent questions
- 🔁 Regenerate answers
- 📖 Add all 18 chapters
- 🔊 Audio narration of slokas
- 🌍 Multi-language support

## 📚 Documentation

### Quick Guides
- **QUICKSTART.md** - Get started in 3 steps
- **INSTALLATION.md** - Detailed installation guide
- **CHATBOT_UPDATE_SUMMARY.md** - v2.2 chatbot UI summary
- **CHATBOT_UI_V2.2.md** - Complete chatbot documentation

### Technical Docs
- **ARCHITECTURE.md** - System design and flow
- **PROJECT_SUMMARY.md** - What was built
- **FAQ.md** - Frequently asked questions
- **TESTING_GUIDE.md** - How to test features

### Version History
- **IMPROVEMENTS_V2.md** - v2.0 intelligence updates
- **DARK_MODE_GUIDE.md** - Dark mode implementation
- **DARK_MODE_FIX.md** - Quick dark mode fix

### Navigation
- **INDEX.md** - Master documentation index

## 🎯 Version History

### v2.2 (Current) - Chatbot UI 💬
- Modern chatbot interface with message bubbles
- Persistent chat history in session
- Comprehensive sidebar with instructions
- Wide layout for better experience
- Form-based input with auto-clear
- Clear chat functionality

### v2.1 - Dark Mode Support 🌓
- Full dark mode compatibility
- Transparent backgrounds with rgba()
- Custom theme configuration
- Enhanced visibility

### v2.0 - Intelligence Enhancement 🧠
- Intelligent, comprehensive answers
- Enhanced character descriptions
- Direct responses not limited to context
- Improved UI styling

### v1.0 - Initial Release 🎉
- FAISS vector search
- Gemini API integration
- Basic Streamlit UI
- 15 slokas from Chapter 1

## 📝 License

This project is for educational purposes. The Bhagavad Gita text is in the public domain.

## 🙏 Acknowledgments

- **Bhagavad Gita**: Ancient Indian scripture
- **Google Gemini**: For powerful AI capabilities
- **FAISS**: Facebook AI Research
- **Streamlit**: For the beautiful UI framework

## 📧 Support

For issues or questions, please check the troubleshooting section above.

---

**Made with ❤️ for spiritual seekers and AI enthusiasts**
