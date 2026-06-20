from langchain_community.document_loaders import PyPDFLoader
import os


def load_pdf(file_path: str):
    """
    Loads a PDF file and converts it into LangChain Documents
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    return documents