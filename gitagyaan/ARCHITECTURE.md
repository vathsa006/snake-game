# 🎨 System Architecture & Flow Diagrams

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
│                      (Streamlit UI)                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Application Logic Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Context    │  │   Embedding  │  │   Answer     │     │
│  │  Retrieval   │  │  Generation  │  │  Generation  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────┬────────────────────────┬───────────────┘
                     │                        │
                     ▼                        ▼
┌──────────────────────────┐    ┌──────────────────────────┐
│    Vector Search Layer   │    │   AI Service Layer       │
│       (FAISS Index)      │    │  (Google Gemini API)     │
└──────────────────────────┘    └──────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                              │
│              (gita_slokas.json - 15 Slokas)                 │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow Diagram

### First Run (Index Creation)

```
START
  │
  ├─→ [1] Load gita_slokas.json
  │         │
  │         ├─→ Parse 15 slokas
  │         └─→ Extract text + explanations
  │
  ├─→ [2] Generate Embeddings
  │         │
  │         ├─→ Combine sloka + explanation
  │         ├─→ Call Gemini text-embedding-004
  │         ├─→ Get 768-dim vectors
  │         └─→ Store in array (15 vectors)
  │
  ├─→ [3] Build FAISS Index
  │         │
  │         ├─→ Create IndexFlatL2
  │         ├─→ Add all vectors
  │         └─→ Index ready for search
  │
  ├─→ [4] Save to Disk
  │         │
  │         ├─→ Save faiss_index.bin
  │         └─→ Save sloka_mapping.pkl
  │
  └─→ [5] Ready for Queries!
```

### Query Processing Flow

```
User Question: "Who blew the conch?"
         │
         ▼
    [1] Create Query Embedding
         │
         ├─→ Send to Gemini text-embedding-004
         └─→ Get 768-dim vector
         │
         ▼
    [2] Search FAISS Index
         │
         ├─→ Find 3 most similar vectors
         ├─→ Calculate L2 distances
         └─→ Retrieve indices [12, 13, 14]
         │
         ▼
    [3] Build Context
         │
         ├─→ Get slokas from mapping
         ├─→ Format as text
         └─→ Combine into context string
         │
         ▼
    [4] Generate Answer
         │
         ├─→ Create prompt with context
         ├─→ Send to Gemini 2.0 Flash
         ├─→ Receive generated answer
         └─→ Extract text
         │
         ▼
    [5] Display to User
         │
         ├─→ Show answer
         └─→ Show retrieved context (optional)
         │
         ▼
      DONE!
```

## 🧩 Component Breakdown

### Component 1: Data Loading
```
┌─────────────────────────────┐
│   load_slokas()             │
├─────────────────────────────┤
│ Input:  JSON file path      │
│ Process: Parse JSON         │
│ Output: List of slokas      │
│ Error:  Handle file errors  │
└─────────────────────────────┘
```

### Component 2: Embedding Generation
```
┌──────────────────────────────────────┐
│   create_gemini_embedding()          │
├──────────────────────────────────────┤
│ Input:  Text string                  │
│ API:    text-embedding-004           │
│ Output: 768-dim numpy array          │
│ Task:   retrieval_document           │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│   create_query_embedding()           │
├──────────────────────────────────────┤
│ Input:  Query string                 │
│ API:    text-embedding-004           │
│ Output: 768-dim numpy array          │
│ Task:   retrieval_query              │
└──────────────────────────────────────┘
```

### Component 3: FAISS Indexing
```
┌──────────────────────────────────────┐
│   build_faiss_index()                │
├──────────────────────────────────────┤
│ Input:  List of slokas               │
│ Process:                             │
│   1. Generate embeddings (all)       │
│   2. Create IndexFlatL2(768)         │
│   3. Add vectors to index            │
│ Output: FAISS index + mapping        │
└──────────────────────────────────────┘
```

### Component 4: Context Retrieval
```
┌──────────────────────────────────────┐
│   retrieve_context()                 │
├──────────────────────────────────────┤
│ Input:  Question string              │
│ Process:                             │
│   1. Embed question                  │
│   2. Search index (top_k=3)          │
│   3. Get sloka data                  │
│   4. Format context                  │
│ Output: Context string               │
└──────────────────────────────────────┘
```

### Component 5: Answer Generation
```
┌──────────────────────────────────────┐
│   ask_gemini()                       │
├──────────────────────────────────────┤
│ Input:  Question + Context           │
│ Model:  gemini-2.0-flash             │
│ Process:                             │
│   1. Build prompt                    │
│   2. Call API                        │
│   3. Extract response                │
│ Output: Generated answer             │
└──────────────────────────────────────┘
```

## 📁 File Structure Tree

```
GitaGyaan/
│
├── 📄 app.py                    # Main application (642 lines)
│   ├── Imports & Configuration
│   ├── Gemini API Setup
│   ├── Data Loading Functions
│   ├── Embedding Functions
│   ├── FAISS Functions
│   ├── Context Retrieval
│   ├── Answer Generation
│   └── Streamlit UI
│
├── 📊 gita_slokas.json          # Data file (15 slokas)
│   └── Structure:
│       ├── sloka (verse text)
│       ├── explanation
│       └── qa_pairs[]
│
├── 📋 requirements.txt          # Dependencies
│   ├── google-generativeai
│   ├── faiss-cpu
│   ├── streamlit
│   ├── numpy
│   ├── pandas
│   └── tqdm
│
├── 🧪 test_setup.py            # Verification script
│   ├── Test imports
│   ├── Test files
│   ├── Test JSON structure
│   └── Test API connection
│
├── 🚀 run_app.bat              # Windows launcher
├── 🚀 run_app.sh               # Unix launcher
│
├── 📖 README.md                # Full documentation
├── 📖 QUICKSTART.md            # Quick start guide
├── 📖 INSTALLATION.md          # Install instructions
├── 📖 PROJECT_SUMMARY.md       # Project overview
├── 📖 ARCHITECTURE.md          # This file
│
├── 🔒 .gitignore               # Git ignore rules
│
└── Generated files (after first run):
    ├── 💾 faiss_index.bin      # FAISS index (~50KB)
    └── 💾 sloka_mapping.pkl    # Index mapping (~50KB)
```

## 🔢 Data Dimensions

### Sloka Count
```
Total Slokas:    15
Chapter:         1 (Arjuna Vishada Yoga)
Average Length:  ~150 words per sloka
```

### Vector Dimensions
```
Embedding Model:     text-embedding-004
Embedding Dimension: 768
Vector Type:         float32
Index Type:          IndexFlatL2 (L2 distance)
```

### Index Statistics
```
Number of Vectors:   15
Vector Size:         768 × 4 bytes = 3,072 bytes each
Total Index Size:    ~46 KB
Mapping Size:        ~50 KB
Total Storage:       ~100 KB
```

## ⚡ Performance Characteristics

### Time Complexity
```
Index Creation:    O(n)        where n = number of slokas
Embedding Gen:     O(1)        per text (API call)
FAISS Search:      O(d × n)    where d = dimension, n = vectors
Answer Gen:        O(1)        per query (API call)
```

### Space Complexity
```
Embeddings:        O(n × d)    15 × 768 = 11,520 floats
FAISS Index:       O(n × d)    Same as embeddings
Sloka Mapping:     O(n)        15 entries
```

### Execution Times
```
First Run:
  - Load JSON:           < 1 second
  - Generate Embeddings: ~30-60 seconds (15 API calls)
  - Build Index:         < 1 second
  - Save Files:          < 1 second
  Total:                 ~1-2 minutes

Subsequent Runs:
  - Load Index:          ~1 second
  - UI Startup:          ~1-2 seconds
  Total:                 ~2-3 seconds

Per Query:
  - Query Embedding:     ~0.5-1 second
  - FAISS Search:        < 0.01 seconds
  - Answer Generation:   ~1-3 seconds
  Total:                 ~2-5 seconds
```

## 🌐 API Call Pattern

### During Index Creation
```
API: text-embedding-004
Calls: 15 (one per sloka)
Data: ~2-3 KB per call
Total: ~30-45 KB upload
```

### During Query
```
Call 1: text-embedding-004 (query embedding)
  - Upload: ~100 bytes (query text)
  - Download: ~3 KB (768 floats)

Call 2: gemini-2.0-flash (answer generation)
  - Upload: ~1-2 KB (prompt + context)
  - Download: ~500-1000 bytes (answer text)
```

## 🎯 State Management

### Streamlit Session State
```
session_state:
  ├── index           (FAISS index object)
  ├── sloka_mapping   (Dict mapping)
  └── [Future: query_history, user_preferences]
```

## 🔐 Security Considerations

```
✅ API Key Management
   - Embedded in code (for demo)
   - Consider environment variables for production

✅ Input Validation
   - Check for empty queries
   - Sanitize user input

✅ Error Handling
   - Try-except blocks throughout
   - Graceful degradation

✅ Data Privacy
   - No local storage of queries
   - HTTPS for all API calls
```

## 🧪 Testing Strategy

```
Unit Tests:
  ├── test_load_slokas()
  ├── test_create_embedding()
  ├── test_faiss_search()
  └── test_answer_generation()

Integration Tests:
  ├── test_full_query_flow()
  └── test_error_handling()

System Tests:
  └── test_setup.py (included)
```

---

## 📊 Metrics Dashboard (Conceptual)

```
┌─────────────────────────────────────────┐
│         System Health Dashboard         │
├─────────────────────────────────────────┤
│ Index Status:        ✅ Loaded          │
│ Slokas Indexed:      15                 │
│ API Status:          ✅ Connected       │
│ Avg Query Time:      3.2s               │
│ Cache Hit Rate:      100%               │
│ Uptime:              99.9%              │
└─────────────────────────────────────────┘
```

---

**This architecture supports fast, accurate, and scalable question-answering! 🚀**
