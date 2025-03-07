import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# Load the pre-trained model for embedding generation
model = SentenceTransformer("all-MiniLM-L6-v2")

# Directory containing the scraped data
DATA_DIR = "scraped_data"
DATA_FILE = os.path.join(DATA_DIR, "scraped_content.json")
INDEX_FILE = os.path.join(DATA_DIR, "faiss_index.bin")
METADATA_FILE = os.path.join(DATA_DIR, "metadata.json")

# Load the scraped text data
with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract text content and URLs
documents = list(data.values())
urls = list(data.keys())

# Generate embeddings for each document
print("Generating embeddings...")
embeddings = model.encode(documents, convert_to_numpy=True)

# Create FAISS index
d = embeddings.shape[1]  # Dimension of embeddings
index = faiss.IndexFlatL2(d)  # L2 distance-based index
index.add(embeddings)

# Save the FAISS index
faiss.write_index(index, INDEX_FILE)

# Save metadata mapping for retrieval
metadata = {i: urls[i] for i in range(len(urls))}
with open(METADATA_FILE, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=4)

print(f"FAISS index created and saved to {INDEX_FILE}")
