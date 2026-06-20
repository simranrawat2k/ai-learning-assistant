from app.rag.retriever import DocumentRetriever
from app.rag.llm import get_llm


def create_rag_chain(chunks):
    """
    Full RAG pipeline:
    Retriever + Prompt + LLM
    """

    retriever_obj = DocumentRetriever(chunks)
    retriever = retriever_obj.get_retriever()

    llm = get_llm()

    def ask_question(question):
        # Step 1: Retrieve context
        docs = retriever.invoke(question)

        context = "\n\n".join([doc.page_content for doc in docs])

        # Step 2: Build prompt
        prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the provided context.

If the answer is not present in the context, reply:

"I could not find that information in the uploaded PDF."

Context:
{context}

Question:
{question}

Answer:
"""

        # Step 3: Get response from LLM
        response = llm.invoke(prompt)
        return {
            "answer": response.content,
            "sources": docs
    
        }



    return ask_question