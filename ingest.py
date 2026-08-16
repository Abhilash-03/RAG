import chromadb;
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="company_knowledge")

# Function to chunk text into smaller pieces
def chunk_text(text, chunk_size=300, overlap=80):
    """
    Splits the input text into chunks of specified size with optional overlap.

    Args:
        text (str): The input text to be chunked.
        chunk_size (int): The maximum size of each chunk.
        overlap (int): The number of overlapping characters between chunks.

    Returns:
        list: A list of text chunks.
    """

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

# Read the knowledge text file and chunk it
with open("data/knowledge.txt", 'r', encoding='utf-8') as file:
    text = file.read()

chunks = chunk_text(text)

# Create embeddings for each chunk using the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

embeddings = model.encode(chunks)

# Add the chunks and their embeddings to the ChromaDB collection
collection.add(
    ids=[f"chunk-{i}" for i in range(len(chunks))],
    documents=chunks,
    embeddings=embeddings.tolist(),
    metadatas=[{
        "source": "knowledge.txt",
        "chunk_index": i
    } 
     for i in range(len(chunks))
    ]
)

print(f"Added {len(chunks)} chunks to the ChromaDB collection.")


# Retrieve and print the stored data from the collection
getData = collection.get(include=["documents", "embeddings", "metadatas"])

for id, doc, embedding, metadata in zip(getData["ids"], getData["documents"], getData["embeddings"], getData["metadatas"]):
    print(f"Document: {id} -> {doc}")
    print(f"Embedding: {embedding[:10]}...")  # Print only the first 10 dimensions of the embedding for brevity
    print(f"Metadata: {metadata}")
    print("---")
