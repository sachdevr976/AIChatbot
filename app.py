import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_core.prompts import PromptTemplate
import os

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="IQRA University Chatbot",
    page_icon="🎓",
    layout="centered"
)

# -------------------------
# Center Logo & Title
# -------------------------
if os.path.exists("logo.png"):
    st.image("logo.png", width=150)

st.markdown(
    "<h2 style='text-align:center;'>🎓 IQRA University AI Chatbot</h2>",
    unsafe_allow_html=True
)

# -------------------------
# Load Vector Store
# -------------------------
embeddings = OllamaEmbeddings(model="llama2")

if not os.path.exists("vectorstore/index.faiss"):
    st.error("❌ Vectorstore not found. Run ingest.py first.")
    st.stop()

vectorstore = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# -------------------------
# LLM
# -------------------------
llm = OllamaLLM(model="llama2")

# -------------------------
# Prompt
# -------------------------
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an AI assistant for IQRA University.
Answer ONLY from the context below.
If the answer is not in the context, say "Information not available in the provided document."

Context:
{context}

Question:
{question}

Answer:
"""
)

# -------------------------
# Chat History
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# -------------------------
# Chat Input (WhatsApp style)
# -------------------------
question = st.chat_input("Ask anything about IQRA University...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # ✅ CORRECT & MODERN WAY
                docs = retriever.invoke(question)

                context = "\n\n".join(d.page_content for d in docs)

                final_prompt = prompt.format(
                    context=context,
                    question=question
                )

                answer = llm.invoke(final_prompt)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
                st.write(answer)

            except Exception as e:
                st.error(f"❌ Error: {e}")
