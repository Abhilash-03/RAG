from chunks import chunk_text_line, chunk_text, chunk_text_recursive


with open("data/company_policy.txt", 'r', encoding="utf-8") as file:
    text = file.read()

# chunks = chunk_text(text, chunk_size=120, overlap=40)
# chunks = chunk_text_line(text)
chunks = chunk_text_recursive(text)

print(f"Total chunks created: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i+1} ---"
          f"({len(chunk)} chars) ---")
    print(chunk)