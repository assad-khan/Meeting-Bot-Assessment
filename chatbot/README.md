Here’s a complete `README.md` file for your **Meeting Bot Assessment** project — formatted professionally with clear technical documentation and a concise breakdown of all required sections.

---

## ✅ `README.md`

```markdown
# 🧠 Meeting Bot - AI Transcript Assistant

This project is an AI-powered meeting assistant that processes uploaded meeting transcripts and enables users to chat with it for summaries, decisions, action items, participants, and follow-up contextual questions. It supports session-level memory and prompt intent routing to intelligently handle user queries.

---

## 📌 Overview

This solution provides:

- 📄 **Transcript analysis** using vector search and semantic retrieval.
- 🔁 **Prompt routing** to handle summaries, participants, action items, and general questions.
- 🧠 **Context-aware follow-up answers** via session-level memory.
- 🧭 **Conversation tracing and logging** for debugging and observability.
- 🧾 **Clean modular design** for easy extensibility and maintainability.

The system uses LangChain, FAISS, and OpenAI's models to enable semantic understanding and interactive conversation over meeting content.

---

## 🧩 How Each Module Works

### `server.py`
- Flask server that handles two API endpoints:
  - `POST /upload`: Stores the meeting transcript in session.
  - `POST /chat`: Routes user messages to `engine.py` and returns the AI-generated response.
- Manages `session_id`-based in-memory session tracking and chat history.

### `chatbot/engine.py`
- Main logic for:
  - Transcript summarization
  - Prompt classification (routing)
  - Vector search over transcript
  - Action item and participant extraction
  - Conversational memory for follow-up queries
- Uses:
  - `LangChain` for building LLM chains
  - `FAISS` for vector-based retrieval
  - `ConversationBufferMemory` for memory persistence

### Logging/Tracing
- All user messages, intents, and responses are logged with timestamps.
- Error handling with clear messages and traceback logging.
- Supports integration with LangSmith (optional).

---

## 🔁 Prompt Routing Logic

User prompts are classified into four categories using simple keyword-based routing:

| Intent         | Trigger Keywords                              | Action Taken                             |
|----------------|------------------------------------------------|------------------------------------------|
| `summary`      | "summarize", "summary", "recap"                | Calls `summarize_transcript()`           |
| `participants` | "participants", "attendees", "who attended"    | Calls `extract_participants()`           |
| `actions`      | "action items", "tasks", "to-do", "assigned"   | Calls `extract_action_items()`           |
| `chat`         | Anything else                                  | Runs through `ConversationalRetrievalChain` for follow-up or QA |

Routing logic is handled via a `classify_intent()` function which returns the intent and dynamically selects the appropriate handler.

---

## 🧠 System Architecture

### 🖼️ Diagram (Text-based)

```

\[Frontend UI]
↓ (via HTTP)
\[Flask Backend - server.py]
↓
\[Chat Engine - engine.py]
├── Transcript Summary       → LLMChain (summarize)
├── Participant Extraction   → LLMChain (participants)
├── Action Item Extraction   → LLMChain (actions)
└── Conversational QA        → ConversationalRetrievalChain
├── Memory            → ConversationBufferMemory
└── Retrieval         → FAISS (vector store per session)

```

### 🔧 Workflow

1. **Transcript Upload**: Stored in session and embedded for retrieval.
2. **User Sends Query**: Routed based on intent (summary, participants, actions, or general).
3. **Response Generation**:
   - For structured queries → LLMChain prompt templates
   - For chat/follow-up → LangChain memory + retriever chain
4. **History Update**: User message and bot response added to session memory.
5. **Logs**: Logged with timestamp and session ID for debugging.

---

## 📂 Folder Structure

```

meeting-bot/
├── chatbot/
│   └── engine.py         # Main AI engine logic (you implemented this)
├── server.py             # Flask backend with endpoints
├── frontend/             # Chat UI (provided)
├── requirements.txt      # Required Python dependencies
└── README.md             # You're reading this!

````

---

## ✅ Dependencies

Be sure to install:

```txt
langchain
openai
faiss-cpu
````

---

## 🔐 Environment Variables

To keep your OpenAI API key secure and configurable, create a `.env` file in the project root:

```
touch .env
```

Inside `.env`, add:

```env
OPENAI_API_KEY="your_openai_api_key_here

---

## 🧪 Sample Prompts to Try

* "Summarize the meeting"
* "Who participated?"
* "What are the action items?"
* "What did I just ask you?"
* "What were the key decisions made?"


"


