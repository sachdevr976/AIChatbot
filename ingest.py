import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

# 1️⃣ Check PDF exists
pdf_path = "data/iqra_prospectus.pdf"
if not os.path.exists(pdf_path):
    print("❌ PDF not found:", pdf_path)
    exit()

# 2️⃣ Load PDF
print("📄 Loading PDF...")
loader = PyPDFLoader(pdf_path)
documents = loader.load()
print(f"✅ Loaded {len(documents)} pages")

# 3️⃣ Split documents into chunks
print("✂️ Splitting documents into chunks...")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
docs = splitter.split_documents(documents)
print(f"✅ Total chunks created: {len(docs)}")

# 4️⃣ Initialize embeddings
print("🔗 Creating embeddings...")
embeddings = OllamaEmbeddings(model="llama2")

# 5️⃣ Build FAISS vector store with progress
print("🗄️ Building FAISS vector store...")
doc_embeddings = []
for i, doc in enumerate(docs, 1):
    emb = embeddings.embed_documents([doc.page_content])
    doc.metadata['embedding'] = emb[0]
    doc_embeddings.append(doc)
    if i % 10 == 0 or i == len(docs):
        print(f"Processed {i}/{len(docs)} chunks...")

vectorstore = FAISS.from_documents(doc_embeddings, embeddings)

# 6️⃣ Save vector store locally
print("💾 Saving vector store locally...")
vectorstore.save_local("vectorstore")

print("🎉 Vector store created successfully!")
