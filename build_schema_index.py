from sentence_transformers import SentenceTransformer
import chromadb

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Read schema
with open("docs/schema.txt", "r") as f:
    schema_text = f.read()

# Split into chunks (simple)
chunks = schema_text.split("\n\n")

# Create Chroma client
client = chromadb.Client()
collection = client.get_or_create_collection(name="schema")

# Embed and store
for i, chunk in enumerate(chunks):
    embedding = model.encode(chunk).tolist()
    collection.add(
        documents=[chunk],
        embeddings=[embedding],
        ids=[str(i)]
    )

print("Schema indexed successfully")
