import streamlit as st
import os
import hashlib
import tempfile

from app.rag.loader import load_pdf
from app.rag.splitter import split_documents
from app.rag.chain import create_rag_chain


st.set_page_config(page_title="AI Learning Assistant", layout="centered")

st.title("📚 AI Learning Assistant")
st.write("Upload a PDF and ask questions from it")


# -----------------------------
# CHAT HISTORY
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# FILE HASH
# -----------------------------
def get_file_hash(file_bytes):
    return hashlib.md5(file_bytes).hexdigest()


# -----------------------------
# RAG BUILDER (CACHE SAFE)
# -----------------------------
@st.cache_resource
def setup_rag(file_hash: str, file_path: str):
    print(f"🔄 Building RAG for file: {file_hash}")

    docs = load_pdf(file_path)
    chunks = split_documents(docs)

    return create_rag_chain(chunks)


# -----------------------------
# PDF UPLOAD
# -----------------------------
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

ask = None

if uploaded_file is not None:

    file_bytes = uploaded_file.getvalue()

    file_hash = get_file_hash(file_bytes)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
         tmp.write(file_bytes)
         temp_path = tmp.name

    with st.spinner("Processing PDF..."):
        ask = setup_rag(file_hash, temp_path)
        os.remove(temp_path)
    
    st.session_state.messages = []

    st.success("PDF processed successfully!")


# -----------------------------
# DISPLAY OLD CHAT
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------
# QUESTION INPUT
# -----------------------------
question = st.chat_input("Ask your question")


if ask and question:

    # User message
    with st.chat_message("user"):
        st.markdown(question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # AI response
    with st.spinner("Thinking..."):
        result = ask(question)

    answer = result["answer"]

    with st.chat_message("assistant"):

        st.markdown(answer)

        st.markdown("### 📄 Sources")

        for i, doc in enumerate(result["sources"]):

            page = doc.metadata.get("page")

            if page is not None:
                title = f"Source {i+1} - Page {page + 1}"
            else:
                title = f"Source {i+1}"

            with st.expander(title):
                st.write(doc.page_content)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

elif question and not uploaded_file:
    st.warning("Please upload a PDF first")