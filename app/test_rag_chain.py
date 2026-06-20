from app.rag.loader import load_pdf
from app.rag.splitter import split_documents
from app.rag.chain import create_rag_chain


docs = load_pdf("data/sample.pdf")
chunks = split_documents(docs)

ask = create_rag_chain(chunks)

question = "What is this document about?"

answer = ask(question)

print("\nAI Answer:\n")
print(answer)