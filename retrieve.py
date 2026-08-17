import chromadb
from sentence_transformers import SentenceTransformer

# 1. Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Connect to ChromaDB and retrieve the collection
client = chromadb.PersistentClient(path="./chroma_db")

try:
    collection = client.get_collection(name="company_knowledge")
except Exception:
    print("Collection 'company_knowledge' does not exist. Run ingest.py first.")
    raise SystemExit(1)

# 3. Define the question to retrieve relevant information
# question = "How many days can employees work remotely?"
# question = "Do employees receive health insurance?"
question = "What is the company's policy regarding pets?"

# 4. Create an embedding for the question
question_embedding = model.encode([question])

# 5. Query the collection for relevant documents based on the question embedding
results = collection.query(
    query_embeddings = question_embedding.tolist(),
    n_results = 2
)

# 6. Print the retrieved documents
documents = results['documents'][0]

for i, doc in enumerate(documents):
    print(f"\n--- Result {i+1} ---")
    print(doc)