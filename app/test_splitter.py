from rag.loader import load_pdf
from rag.splitter import split_documents

docs = load_pdf("data/sample.pdf")
chunks = split_documents(docs)

print("Pages:", len(docs))
print("Chunks:", len(chunks))
print("\nFirst chunk:\n")
print(chunks[0].page_content)