from sentence_transformers import SentenceTransformer, util

# Load pre-trained embedding model (offline support if pre-downloaded)
model = SentenceTransformer("all-MiniLM-L6-v2")

def search_semantically(query, documents, top_k=5):
    texts = [doc["text"] for doc in documents]
    doc_embeddings = model.encode(texts, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)

    similarities = util.cos_sim(query_embedding, doc_embeddings)[0]
    top_results = similarities.topk(k=top_k)

    results = []
    for score, idx in zip(top_results.values, top_results.indices):
        doc = documents[int(idx)]
        results.append({
            "file": doc["file"],
            "position": doc["position"],
            "text": doc["text"],
            "score": float(score)
        })
    return results
