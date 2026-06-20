from rag.loader import load_pdf
from rag.splitter import split_documents
from rag.vectorstore import create_vectorstore


docs = load_pdf("data/sample.pdf")
chunks = split_documents(docs)

vectorstore = create_vectorstore(chunks)

print("Vector DB created successfully!")
print("Total chunks stored:", len(chunks))