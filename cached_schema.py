from sentence_transformers import SentenceTransformer
import chromadb

embedder = SentenceTransformer("paraphrase-MiniLM-L3-v2")
client = chromadb.Client()
collection = client.get_or_create_collection(name="schema")

def get_schema_for_question(question):
    emb = embedder.encode(question).tolist()
    res = collection.query(
        query_embeddings=[emb],
        n_results=2
    )
    return "\n".join(res["documents"][0])


if __name__ == "__main__":
    # Precompute for demo questions
    questions = [
        "How many customers are there?",
        "List customer names and countries",
        "Show total orders"
    ]

    for q in questions:
        print("QUESTION:", q)
        print(get_schema_for_question(q))
        print("-" * 40)
