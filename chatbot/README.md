# 🧠 Meeting Bot - AI Transcript Assistant

An AI-powered assistant that processes meeting transcripts and allows users to chat with it to get summaries, decisions, action items, participants, and follow-up contextual answers. The system supports session-level memory, prompt intent routing, and semantic search to intelligently handle user queries.

---

## 📌 Features

* 📄 **Transcript Analysis**: Vector search and semantic retrieval of uploaded transcripts.
* 🔁 **Prompt Routing**: Handles summaries, participants, tasks, and general follow-ups.
* 🧠 **Context-Aware Responses**: Maintains session memory for coherent conversations.
* 🔭 **Tracing and Logging**: Logs conversations, intents, and system behavior.
* 🗞 **Modular Design**: Clean architecture for extensibility and maintenance.

---

## 🤩 Modules Overview

### `server.py`

* Flask backend with two main endpoints:

  * `POST /upload`: Uploads and stores meeting transcript per session.
  * `POST /chat`: Handles chat messages and routes them to the AI engine.
* Manages sessions and stores in-memory chat history.

### `chatbot/engine.py`

* Core AI engine:

  * Transcript summarization
  * Intent classification and routing
  * Vector search using FAISS
  * Action item and participant extraction
  * Conversational memory
* Uses:

  * `LangChain` for LLM workflows
  * `FAISS` for fast vector similarity search
  * `ConversationBufferMemory` for memory tracking

---

## 🔁 Prompt Routing Logic

Prompts are classified using keyword-based logic:

| Intent         | Trigger Keywords                             | Action                           |
| -------------- | -------------------------------------------- | -------------------------------- |
| `summary`      | "summarize", "summary", "recap"              | `summarize_transcript()`         |
| `participants` | "participants", "attendees", "who attended"  | `extract_participants()`         |
| `actions`      | "action items", "tasks", "to-do", "assigned" | `extract_action_items()`         |
| `chat`         | Anything else                                | `ConversationalRetrievalChain()` |

Handled using a `classify_intent()` function that routes queries accordingly.

---

## 🧠 System Architecture

### 🖼️ Architecture Diagram (Text Format)

```
[Frontend UI]
     ↓
[Flask Backend - server.py]
     ↓
[Chat Engine - engine.py]
├── Transcript Summary        → LLMChain
├── Participant Extraction    → LLMChain
├── Action Item Extraction    → LLMChain
└── Conversational QA         → ConversationalRetrievalChain
    ├── Memory                → ConversationBufferMemory
    └── Retrieval             → FAISS Vector Store
```

---

## ⚙️ Workflow

1. **Upload Transcript**: Sent via `/upload`, stored in session, and embedded for retrieval.
2. **User Query**: Sent via `/chat`, classified by intent.
3. **Response Generation**:

   * Structured prompts → routed to specific LLMChains.
   * General questions → handled by retriever + memory chain.
4. **Session Memory**: Maintains conversation history.
5. **Logging**: All interactions are logged for observability and debugging.

---

## 📂 Project Structure

```
meeting-bot/
├── chatbot/
│   └── engine.py         # AI engine logic
├── server.py             # Flask API server
├── frontend/             # Chat UI
│   └── index.html         
│   └── scripts.js        
│   └── style.css       
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## ✅ Installation

Install required Python packages:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Setup

Add your OpenAI API key inside `.env`:

```env
OPENAI_API_KEY="your_openai_api_key_here"
```

---

## 🧪 Sample Prompts to Try

* "Summarize the meeting"
* "Who participated?"
* "What are the action items?"
* "What decisions were made?"
* "What did I just ask you?"
