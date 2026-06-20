from rag.loader import load_pdf

docs = load_pdf("data/sample.pdf")

print(len(docs))
print(docs[0].page_content[:300])