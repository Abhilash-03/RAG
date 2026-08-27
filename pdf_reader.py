import pymupdf as fitz

pdf_path = "./data/proposal.pdf"

# open the PDF file
doc = fitz.open(pdf_path)

print(f"Number of pages: {doc.page_count}")

# Extract text from each page
for page_num, page in enumerate(doc, start=1):
    text = page.get_text()

    print(f"\n======= PAGE {page_num} =======")
    print(text)


# close the PDF
doc.close()