from app.rag.vectorstore import create_vectorstore


class DocumentRetriever:
    def __init__(self, chunks):
        self.vectorstore = create_vectorstore(chunks)

    def get_retriever(self):
        return self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )