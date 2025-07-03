"""
Meeting Bot Engine

This is where candidates implement their AI chatbot logic.
The main function to implement is respond() which takes a user message,
session data, and returns a response.

Session data includes:
- transcript: The uploaded meeting transcript
- chat_history: List of previous messages in the conversation
- session_id: Unique session identifier

Example usage:
    response = respond("What were the main topics discussed?", session_data)
"""

import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.schema import HumanMessage, AIMessage
from langchain.prompts import PromptTemplate
import logging
import time
from dotenv import load_dotenv

load_dotenv() 
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


# In-memory vector store per session
vector_store_cache = {}

# Cache summary per session
session_summary_cache = {}

def get_session_vectorstore(session_id, transcript):
    if session_id in vector_store_cache:
        return vector_store_cache[session_id]

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_text(transcript)
    documents = [Document(page_content=doc) for doc in docs]

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    vector_store_cache[session_id] = vectorstore
    return vectorstore

def format_chat_history(chat_history):
    messages = []
    for entry in chat_history:
        if entry['sender'] == 'user':
            messages.append(HumanMessage(content=entry['content']))
        elif entry['sender'] == 'bot':
            messages.append(AIMessage(content=entry['content']))
    return messages

def summarize_transcript(transcript):
    prompt = PromptTemplate.from_template(
        """
        Summarize the following meeting transcript clearly and concisely:

        {transcript}

        Summary:
        """
    )
    llm = ChatOpenAI(temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(transcript=transcript)

def extract_participants(transcript):
    prompt = PromptTemplate.from_template(
        """
        From the following meeting transcript, list all participants and their roles:

        {transcript}

        Participants:
        """
    )
    llm = ChatOpenAI(temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(transcript=transcript)

def extract_action_items(transcript):
    prompt = PromptTemplate.from_template(
        """
        Extract all action items from this meeting transcript. Include assignee and deadline if available:

        {transcript}

        Action Items:
        """
    )
    llm = ChatOpenAI(temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(transcript=transcript)

def classify_intent(message):
    msg = message.lower()
    if "summarize" in msg:
        return "summary"
    elif "participants" in msg or "attended" in msg or "who were in the meeting" in msg:
        return "participants"
    elif "action items" in msg or "tasks" in msg or "to-do" in msg:
        return "actions"
    else:
        return "chat"

def respond(user_message, session_data):
    """
     Main chatbot response function - IMPLEMENT YOUR AI LOGIC HERE
     Args:
         user_message (str): The user's chat message
         session_data (dict): Session data containing:
             - transcript (str): The uploaded meeting transcript
             - chat_history (list): List of previous messages
             - session_id (str): Unique session identifier
     Returns:
         str: The chatbot's response
     """
    transcript = session_data.get("transcript", "")
    chat_history = session_data.get("chat_history", [])
    session_id = session_data.get("session_id", "")

    logging.info(f"[{session_id}] User message: {user_message}")

    if not transcript:
        logging.warning(f"[{session_id}] No transcript found.")
        return "Please upload a meeting transcript first so I can help you analyze it."

    intent = classify_intent(user_message)
    logging.info(f"[{session_id}] Classified intent: {intent}")

    start_time = time.time()

    try:
        if intent == "summary":
            if session_id not in session_summary_cache:
                session_summary_cache[session_id] = summarize_transcript(transcript)
            response = session_summary_cache[session_id]

        elif intent == "participants":
            response = extract_participants(transcript)

        elif intent == "actions":
            response = extract_action_items(transcript)

        else:
            vectorstore = get_session_vectorstore(session_id, transcript)
            retriever = vectorstore.as_retriever()
            memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
            memory.chat_memory.messages = format_chat_history(chat_history)

            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=ChatOpenAI(temperature=0),
                retriever=retriever,
                memory=memory
            )
            response = qa_chain.run(user_message)

        elapsed = round(time.time() - start_time, 2)
        logging.info(f"[{session_id}] Response time: {elapsed}s")
        logging.info(f"[{session_id}] Bot response: {response}")

        return response

    except Exception as e:
        logging.exception(f"[{session_id}] Error generating response: {str(e)}")
        return "Oops! Something went wrong while processing your request."


