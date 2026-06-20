from rag.loader import load_pdf
from rag.splitter import split_documents
from rag.retriever import DocumentRetriever


docs = load_pdf("data/sample.pdf")
chunks = split_documents(docs)

retriever_obj = DocumentRetriever(chunks)
retriever = retriever_obj.get_retriever()

query = "What is this PDF about?"

results = retriever.invoke(query)

print("\nTop Matching Chunks:\n")

for i, r in enumerate(results):
    print(f"\n--- Chunk {i+1} ---")
    print(r.page_content[:300])