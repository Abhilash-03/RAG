
# BASIC-RAG: Chunks Module
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

# Function to chunk text into smaller pieces based on line breaks

def chunk_text_line(text):
    """
    Splits the input text into chunks based on line breaks.

    Args:
        text (str): The input text to be chunked.

    Returns:
        list: A list of text chunks.
    """

    lines = text.splitlines()

    chunks = []

    for line in lines:
        if line.strip(): # Only add non-empty lines
            chunks.append(line.strip())

    return chunks


def find_best_separator(text, separators):
    """
    Finds the best separator to split the text based on the provided list of separators.

    Args:
        text (str): The input text to be analyzed.
        separators (list): A list of separators to try for splitting.

    Returns:
        str: The best separator found in the text, or an empty string if none are found.
    """

    for sep in separators:
        if sep in text:
            return sep

    return ''

# Recursive algorithm to chunk text optimally
def chunk_text_recursive(text, max_length=150, separators=None):
    """
    Recursively splits the input text into chunks of specified maximum length,
    trying to split at the best possible separator.

    Args:
        text (str): The input text to be chunked.
        max_length (int): The maximum length of each chunk.
        separators (list, optional): A list of separators to try for splitting.

    Returns:
        list: A list of text chunks.
    """

    if separators is None:
        separators = ['\n', '\n\n', '.', '!', '?', ',', ' ', ';', ':']

    if len(text) <= max_length:
        return [text]

    separator = find_best_separator(text, separators)

    pieces = text.split(separator)

    chunks = []

    for piece in pieces:
        if len(piece) <= max_length:
            chunks.append(piece)
        else:
            chunks.extend(chunk_text_recursive(piece, max_length, separators))

    return chunks