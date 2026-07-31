from backend.utils import extract_pdf_text
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from config import model

import faiss
import numpy as np

# Load embedding model only once

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def load_policy(pdf_file):

    """Extract text from a policy PDF,
    split it into chunks,
    and generate embeddings."""

    text = extract_pdf_text(pdf_file)

    #Check if any readable text was extracted
    if not text or not text.strip():
        raise ValueError(
            "The uploaded PDF contains no readable text."
        )
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)

    #Check if any chunks were created
    if len(chunks) == 0:
        raise ValueError(
            "No text chunks could be created from the uploaded PDF."
        )

    embeddings = embedding_model.encode(chunks)

    return chunks, embeddings


def create_index(embeddings):

    """Create a FAISS vector index from document embeddings."""

    if len(embeddings) == 0:
        raise ValueError(
            "No embeddings available to create the vector index."
        )
    
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(
        np.array(embeddings).astype("float32")
    )

    return index


def search_chunks(
    question,
    index,
    chunks,
    top_k=3
):

    """Retrieve the most relevant policy chunks for a question."""
    
    question_embedding = embedding_model.encode(
        [question]
    )

    distances, indices = index.search(
        question_embedding.astype("float32"),
        top_k
    )

    results = [
        chunks[i]
        for i in indices[0]
    ]

    return results

def answer_question(question, index, chunks):

    """Answer a user question using retrieved policy context."""

    # Retrieve the most relevant chunks
    relevant_chunks = search_chunks(
        question,
        index,
        chunks
    )

    # Combine retrieved chunks into context
    context = "\n\n".join(relevant_chunks)

    prompt = f"""
You are an HR Policy Assistant.

Your job is to answer questions ONLY using the provided policy context.

Rules:
1.Answer only from the policy context.
2.Do not make up information.
3.If the answer is not found in the policy, reply:
"I couldn't find this information in the uploaded policy."
4.Provide a clear, professional answer in complete sentences.
5.Keep the answer concise and easy to understand.

Policy Context:
{context}

Question:
{question}
"""
    try:

        response = model.generate_content(prompt)

    except Exception as e:

        raise RuntimeError(
        "Unable to generate a response from Gemini."
        ) from e

    return response.text, relevant_chunks