import streamlit as st
from PyPDF2 import PdfReader

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_ollama import OllamaLLM
from langchain.chains.question_answering import load_qa_chain

# Page config
st.set_page_config(
    page_title="PDF QA App",
    page_icon="📄"
)

st.title("📄 AI PDF Question Answering App")

pdf = st.file_uploader(
    "Upload PDF",
    type="pdf"
)

if pdf is not None:

    # Read PDF
    pdf_reader = PdfReader(pdf)

    text = ""

    for page in pdf_reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    # ---------------- EXTRACT QUESTIONS ---------------- #

    import re

    questions = re.findall(r'.*?\?', text)

    # Remove duplicates
    questions = list(dict.fromkeys(questions))

    # Sidebar
    st.sidebar.title("📌 Questions in PDF")

    if questions:

        for i, q in enumerate(questions[:50], 1):
            st.sidebar.write(f"{i}. {q}")

    else:
        st.sidebar.write("No questions found.")

    # Split text
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_text(text)

    # Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Vector DB
    knowledge_base = FAISS.from_texts(
        chunks,
        embeddings
    )

    # User Question
    user_question = st.text_input(
        "Ask a question from PDF"
    )

    if user_question:

        docs = knowledge_base.similarity_search(
            user_question
        )

        # Local AI Model
        llm = OllamaLLM(
        model="tinyllama"
        )

        # QA Chain
        chain = load_qa_chain(
            llm,
            chain_type="stuff"
        )

        response = chain.run(
            input_documents=docs,
            question=user_question
        )

        st.subheader("✅ Answer")

        st.write(response)