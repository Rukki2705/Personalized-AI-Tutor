import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from ollama import chat

# Load the pre-trained model for embedding generation
model = SentenceTransformer("all-MiniLM-L6-v2")

# Directory containing the FAISS index and metadata
DATA_DIR = "scraped_data"
INDEX_FILE = os.path.join(DATA_DIR, "faiss_index.bin")
METADATA_FILE = os.path.join(DATA_DIR, "metadata.json")

# Load FAISS index
index = faiss.read_index(INDEX_FILE)

# Load metadata mapping
with open(METADATA_FILE, "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Function to retrieve the most relevant document
def retrieve_documents(query, top_k=3):
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)
    results = [metadata[str(idx)] for idx in indices[0] if str(idx) in metadata]
    return results

# Function to generate a response using Ollama with mistral models
def generate_response(query):
    retrieved_docs = retrieve_documents(query)
    context = "\n".join(retrieved_docs)
    prompt = f"Using the following context, answer the query: {query}\n\nContext:\n{context}"
    
    # Send the request to Ollama
    response = chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    
    # Extract and return the correct content
    if hasattr(response, "message") and hasattr(response.message, "content"):
        return response.message.content
    else:
        return "Error: No content found in model response."
if __name__ == "__main__":
    while True:
        user_query = input("Ask a question (or type 'exit' to quit): ")
        if user_query.lower() == "exit":
            break
        answer = generate_response(user_query)
        print("\nAI Response:\n", answer, "\n")
