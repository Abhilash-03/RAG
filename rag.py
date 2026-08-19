import os
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from google import genai

load_dotenv() # Load environment variables from .env file

llm = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# 1. Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="company_knowledge")

question = input("Ask a question about the company: ")

question_embedding = model.encode([question])

results = collection.query(
    query_embeddings = question_embedding.tolist(),
    n_results = 2
)

documents = results['documents'][0]
print("\n--- Retrieved Documents ---")
for i, document in enumerate(documents):
    print(f"\nDocument {i + 1}:")
    print(document)

context = "\n\n".join(documents)

prompt = f"""
You are a helpful assistant.

Answer the user's question using only the provided context.

If the answer cannot be found in the context, say that you don't have enough information.

Context:
{context}

Question:
{question}
"""

response = llm.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print("\n--- LLM Response ---")
print(response.text)