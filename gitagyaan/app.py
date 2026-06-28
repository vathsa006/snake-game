"""
Bhagavad Gita Question-Answering System
Chapter 1 - First 15 Slokas
Uses FAISS for vector search and Google Gemini 2.0 Flash for answer generation
"""

import json
import os
import pickle
import numpy as np
import streamlit as st
import google.generativeai as genai
import faiss
from typing import List, Dict, Tuple
from tqdm import tqdm
import time

# ============================================================================
# CONFIGURATION
# ============================================================================

# Get API key from Streamlit secrets or use default
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    GEMINI_API_KEY = "AIzaSyBnxroL-fIW53EHoi6pbKYIcquzzmBWT1c"

MODEL_NAME = "gemini-2.0-flash"

# Use absolute paths relative to the script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SLOKAS_JSON_PATH = os.path.join(SCRIPT_DIR, "gita_slokas.json")
FAISS_INDEX_PATH = os.path.join(SCRIPT_DIR, "faiss_index.bin")
SLOKA_MAPPING_PATH = os.path.join(SCRIPT_DIR, "sloka_mapping.pkl")
TOP_K = 3

# ============================================================================
# GEMINI API SETUP
# ============================================================================

def initialize_gemini():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        return True
    except Exception as e:
        print(f"Error initializing Gemini API: {e}")
        return False

# ============================================================================
# DATA LOADING
# ============================================================================

def load_slokas(json_path: str) -> List[Dict]:
    try:
        if not os.path.exists(json_path):
            print(f"Error: File not found at {json_path}")
            print(f"Current directory: {os.getcwd()}")
            print(f"Script directory: {SCRIPT_DIR}")
            return []
        
        with open(json_path, 'r', encoding='utf-8') as f:
            slokas = json.load(f)
        print(f"Successfully loaded {len(slokas)} slokas from {json_path}")
        return slokas
    except Exception as e:
        print(f"Error loading slokas: {e}")
        return []

# ============================================================================
# EMBEDDING GENERATION
# ============================================================================

def create_gemini_embedding(text: str, model_name: str = MODEL_NAME) -> np.ndarray:
    try:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document"
        )
        return np.array(result['embedding'], dtype=np.float32)
    except Exception as e:
        return np.zeros(768, dtype=np.float32)

def create_query_embedding(text: str) -> np.ndarray:
    try:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_query"
        )
        return np.array(result['embedding'], dtype=np.float32)
    except Exception as e:
        return np.zeros(768, dtype=np.float32)

# ============================================================================
# FAISS INDEX CREATION
# ============================================================================

def build_faiss_index(slokas: List[Dict]) -> Tuple[faiss.Index, List[Dict]]:
    texts = []
    sloka_mapping = []
    
    for idx, sloka in enumerate(slokas):
        combined_text = f"{sloka['sloka']} {sloka['explanation']}"
        texts.append(combined_text)
        sloka_mapping.append({
            'index': idx,
            'sloka': sloka['sloka'],
            'explanation': sloka['explanation'],
            'qa_pairs': sloka.get('qa_pairs', [])
        })
    
    embeddings = []
    for text in tqdm(texts, desc="Generating embeddings"):
        embedding = create_gemini_embedding(text)
        embeddings.append(embedding)
    
    embeddings_matrix = np.array(embeddings, dtype=np.float32)
    dimension = embeddings_matrix.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_matrix)
    
    return index, sloka_mapping

def load_faiss_index() -> Tuple[faiss.Index, List[Dict]]:
    try:
        index = faiss.read_index(FAISS_INDEX_PATH)
        with open(SLOKA_MAPPING_PATH, 'rb') as f:
            sloka_mapping = pickle.load(f)
        return index, sloka_mapping
    except:
        return None, None

# ============================================================================
# CONTEXT RETRIEVAL
# ============================================================================

def retrieve_context(question: str, index: faiss.Index, sloka_mapping: List[Dict], top_k: int = TOP_K) -> str:
    try:
        question_embedding = create_query_embedding(question)
        question_embedding = question_embedding.reshape(1, -1)
        distances, indices = index.search(question_embedding, top_k)
        
        context_parts = []
        for i, idx in enumerate(indices[0]):
            sloka_data = sloka_mapping[idx]
            context_parts.append(
                f"Sloka {idx + 1}:\n"
                f"Verse: {sloka_data['sloka']}\n"
                f"Explanation: {sloka_data['explanation']}\n"
            )
        
        return "\n".join(context_parts)
    except Exception as e:
        return ""

# ============================================================================
# GEMINI ANSWER GENERATION
# ============================================================================

def ask_gemini(question: str, context: str, model_name: str = MODEL_NAME) -> str:
    try:
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""You are an expert scholar on the Bhagavad Gita with deep knowledge of Hindu philosophy and the Mahabharata epic.

Your task: Answer the question using the provided context AND your comprehensive knowledge of the Bhagavad Gita and Mahabharata.

Guidelines:
1. Provide DIRECT, CLEAR, and COMPREHENSIVE answers
2. If asked about a character, give their full identity and role
3. Use the context as supporting evidence, but enhance it with your knowledge
4. Be conversational and educational
5. Keep answers concise but complete (2-4 sentences)
6. Don't just describe what's in the slokas - explain WHO, WHAT, WHY clearly

Context from Bhagavad Gita Chapter 1:
{context}

Question: {question}

Provide a direct, intelligent answer:"""
        
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text
        else:
            return "I couldn't generate an answer. Please try rephrasing your question."
            
    except Exception as e:
        return f"Error calling Gemini API: {e}"

# ============================================================================
# INITIALIZATION
# ============================================================================

def initialize_system():
    if not initialize_gemini():
        st.error("Failed to initialize Gemini API")
        return None, None
    
    slokas = load_slokas(SLOKAS_JSON_PATH)
    if not slokas:
        st.error(f"Failed to load slokas from {SLOKAS_JSON_PATH}")
        return None, None
    
    index, sloka_mapping = build_faiss_index(slokas)
    return index, sloka_mapping

# ============================================================================
# STREAMLIT UI
# ============================================================================

def main():
    st.set_page_config(
        page_title="Bhagavad Gita Gyan",
        page_icon="🕉️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Modern CSS with dark mode support and full responsiveness
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Light Mode Variables */
    :root {
        --bg-primary: #f8fafc;
        --bg-secondary: #ffffff;
        --bg-gradient-start: #667eea;
        --bg-gradient-end: #764ba2;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --border-color: #e2e8f0;
        --shadow-light: rgba(0, 0, 0, 0.1);
        --shadow-medium: rgba(0, 0, 0, 0.15);
        --hover-bg: #f1f5f9;
    }
    
    /* Dark Mode Variables */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --border-color: #334155;
            --shadow-light: rgba(0, 0, 0, 0.3);
            --shadow-medium: rgba(0, 0, 0, 0.5);
            --hover-bg: #334155;
        }
    }
    
    .main {
        background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
        padding: 0 !important;
        min-height: 100vh;
    }
    
    .stApp {
        background: transparent;
    }
    
    /* Header Section - Fully Responsive */
    .header-container {
        background: var(--bg-secondary);
        backdrop-filter: blur(10px);
        padding: clamp(1rem, 3vw, 2rem) clamp(1rem, 4vw, 3rem);
        border-radius: 0 0 clamp(15px, 3vw, 30px) clamp(15px, 3vw, 30px);
        box-shadow: 0 10px 40px var(--shadow-light);
        margin-bottom: clamp(1rem, 3vw, 2rem);
    }
    
    .main-title {
        font-size: clamp(1.5rem, 5vw, 3rem);
        font-weight: 700;
        background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        text-align: center;
        color: var(--text-secondary);
        font-size: clamp(0.9rem, 2.5vw, 1.1rem);
        font-weight: 500;
    }
    
    /* Main Container - Responsive */
    .main-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 0 clamp(1rem, 3vw, 2rem);
        width: 100%;
        box-sizing: border-box;
    }
    
    /* Welcome Screen - Responsive */
    .welcome-box {
        background: var(--bg-secondary);
        padding: clamp(1.5rem, 4vw, 3rem);
        border-radius: clamp(15px, 3vw, 25px);
        text-align: center;
        box-shadow: 0 10px 40px var(--shadow-light);
        margin: clamp(1rem, 3vw, 2rem) auto;
        width: 100%;
        box-sizing: border-box;
    }
    
    .welcome-title {
        font-size: clamp(1.3rem, 4vw, 2rem);
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1rem;
    }
    
    .welcome-text {
        color: var(--text-secondary);
        font-size: clamp(0.9rem, 2.5vw, 1.1rem);
        line-height: 1.8;
    }
    
    .example-questions {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(min(150px, 100%), 1fr));
        gap: clamp(0.5rem, 2vw, 1rem);
        margin-top: clamp(1rem, 3vw, 2rem);
    }
    
    .example-btn {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 2px solid rgba(102, 126, 234, 0.3);
        padding: clamp(0.6rem, 2vw, 0.8rem) clamp(0.8rem, 2vw, 1rem);
        border-radius: 12px;
        color: var(--bg-gradient-start);
        font-weight: 600;
        font-size: clamp(0.8rem, 2vw, 0.9rem);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .example-btn:hover {
        background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Input Section - Fully Responsive */
    .input-container {
        background: var(--bg-secondary);
        border-radius: clamp(15px, 3vw, 25px);
        padding: clamp(1rem, 2.5vw, 1.5rem);
        box-shadow: 0 10px 40px var(--shadow-light);
        margin-bottom: clamp(1rem, 3vw, 2rem);
        margin-top: 0 !important;
        width: 100%;
        box-sizing: border-box;
    }
    
    .stTextArea textarea {
        border: 2px solid var(--border-color) !important;
        border-radius: 15px !important;
        padding: clamp(0.8rem, 2vw, 1rem) !important;
        font-size: clamp(0.9rem, 2vw, 1rem) !important;
        transition: all 0.3s ease !important;
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        resize: vertical !important;
        min-height: 80px !important;
        width: 100% !important;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--bg-gradient-start) !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        background: var(--bg-secondary) !important;
    }
    
    .stButton button {
        background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%) !important;
        color: white !important;
        border: none !important;
        padding: clamp(0.7rem, 2vw, 0.9rem) clamp(1.5rem, 3vw, 2rem) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: clamp(0.9rem, 2vw, 1rem) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s ease !important;
        width: 50% !important;
        margin: 0.5rem auto 0.5rem auto !important;
        display: block !important;
    }
    
    /* Message Bubbles - Fully Responsive */
    .user-message {
        background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
        color: white;
        padding: clamp(0.8rem, 2vw, 1.2rem) clamp(1rem, 2.5vw, 1.5rem);
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        font-size: clamp(0.9rem, 2vw, 1rem);
        line-height: 1.6;
        animation: slideInUp 0.4s ease;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    .ai-message {
        background: var(--bg-secondary);
        color: var(--text-primary);
        padding: clamp(0.8rem, 2vw, 1.2rem) clamp(1rem, 2.5vw, 1.5rem);
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px var(--shadow-light);
        font-size: clamp(0.9rem, 2vw, 1rem);
        line-height: 1.7;
        animation: slideInUp 0.4s ease;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    .typing-indicator {
        background: var(--bg-secondary);
        padding: clamp(0.8rem, 2vw, 1.2rem) clamp(1rem, 2.5vw, 1.5rem);
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px var(--shadow-light);
        display: inline-block;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    .typing-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--bg-gradient-start);
        margin: 0 3px;
        animation: typing 1.4s ease-in-out infinite;
    }
    
    .typing-dot:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-dot:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes typing {
        0%, 60%, 100% {
            transform: translateY(0);
        }
        30% {
            transform: translateY(-10px);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.6;
        }
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%) !important;
    }
    
    /* Form columns - Stack on mobile */
    [data-testid="column"] {
        padding: 0 0.5rem !important;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* header {visibility: hidden;} */
    
    /* Mobile Responsive - Stack columns */
    @media (max-width: 768px) {
        .main-container {
            padding: 0 0.5rem;
        }
        
        .input-container {
            padding: 1rem;
        }
        
        .example-questions {
            grid-template-columns: 1fr;
        }
        
        [data-testid="column"] {
            width: 100% !important;
            padding: 0.25rem 0 !important;
        }
        
        .stButton button {
            margin-top: 0.5rem;
        }
    }
    
    /* Small mobile devices */
    @media (max-width: 480px) {
        .main-title {
            font-size: 1.5rem;
            letter-spacing: 0;
        }
        
        .subtitle {
            font-size: 0.85rem;
        }
        
        .welcome-box {
            padding: 1.5rem 1rem;
        }
        
        .user-message, .ai-message {
            font-size: 0.9rem;
            padding: 0.8rem 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="header-container">
        <div class="main-title">🕉️ Bhagavad Gita Gyan</div>
        <div class="subtitle">Chapter 1: Arjuna Vishada Yoga • Slokas 1-15</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize system
    if 'index' not in st.session_state or 'sloka_mapping' not in st.session_state:
        with st.spinner("Initializing wisdom repository..."):
            index, sloka_mapping = initialize_system()
            if index is None or sloka_mapping is None:
                st.error("System initialization failed")
                return
            st.session_state.index = index
            st.session_state.sloka_mapping = sloka_mapping
    
    # Initialize chat history and processing state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    
    index = st.session_state.index
    sloka_mapping = st.session_state.sloka_mapping
    
    # Main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Welcome message (only if no chat history)
    if not st.session_state.chat_history:
        st.markdown("""
        <div class="welcome-box">
            <div class="welcome-title">🙏 Namaste! Welcome to Bhagavad Gita Gyan</div>
            <div class="welcome-text">
                Ask me anything about Chapter 1 (Slokas 1-15) and receive wisdom from the sacred verses combined with intelligent insights.
            </div>
            <div class="example-questions">
                <div class="example-btn">Who is Drona?</div>
                <div class="example-btn">What is Kurukshetra?</div>
                <div class="example-btn">Tell me about Bhishma</div>
                <div class="example-btn">Who blew conchshells?</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Input section - Always at top
    st.markdown('<div class="input-container">', unsafe_allow_html=True)

    with st.form(key='question_form', clear_on_submit=True):
        question = st.text_area(
            "Ask a question",
            placeholder="Ask your question here... (e.g., Who is Drona? What happened at Kurukshetra?)",
            height=100,
            label_visibility="collapsed",
            disabled=st.session_state.processing
        )

        submit = st.form_submit_button(
            "🔍 Ask Question" if not st.session_state.processing else "⏳ Processing...",
            use_container_width=True,
            disabled=st.session_state.processing
        )

        if st.session_state.chat_history:
            clear = st.form_submit_button(
                "🗑️ Clear",
                use_container_width=True,
                disabled=st.session_state.processing
            )
        else:
            clear = False

    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle clear
    if clear:
        st.session_state.chat_history = []
        st.session_state.processing = False
        st.rerun()
    
    # Handle submit
    if submit and question.strip() and not st.session_state.processing:
        st.session_state.processing = True
        
        # Add user message
        st.session_state.chat_history.append({
            'role': 'user',
            'content': question
        })
        
        # Show user message immediately
        st.markdown(f'<div class="user-message">💭 {question}</div>', unsafe_allow_html=True)
        
        # Show typing indicator
        typing_placeholder = st.empty()
        typing_placeholder.markdown("""
        <div class="typing-indicator">
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
        </div>
        """, unsafe_allow_html=True)
        
        # Get answer
        context = retrieve_context(question, index, sloka_mapping, top_k=TOP_K)
        if context:
            answer = ask_gemini(question, context)
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': answer
            })
        else:
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': "I couldn't find relevant information. Please try rephrasing your question."
            })
        
        # Clear typing indicator
        typing_placeholder.empty()
        
        st.session_state.processing = False
        st.rerun()
    
    # Display chat history (below input)
    if st.session_state.chat_history:
        for i, msg in enumerate(st.session_state.chat_history):
            if msg['role'] == 'user':
                st.markdown(f'<div class="user-message">💭 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="ai-message">🕉️ {msg["content"]}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()