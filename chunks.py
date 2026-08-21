
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

# ---- 3. Recursive algorithm to chunk text optimally

def find_best_separator(text, separators):
    """
    Finds the best separator to split the text based on the provided list of separators.

    Args:
        text (str): The input text to be analyzed.
        separators (list): A list of separators to try for splitting.

    Returns:
        str: The best separator found in the text, or None if none are found.
    """

    for sep in separators:
        if sep in text:
            return sep

    return None


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
        separators = ['\n\n', '\n', '. ', '! ', '? ', ', ', ' ']

    text = text.strip() # Remove leading and trailing whitespace    

    if len(text) <= max_length:
        return [text]

    separator = find_best_separator(text, separators)

    # print(f"Using separator: '{repr(separator)}' for chunking.")

    # If no suitable separator is found, return the entire text as a single chunk
    if not separator:
        return [text]

    pieces = text.split(separator)

    chunks = []
    current_chunk = ""

    for piece in pieces:
        piece = piece.strip() # Remove leading and trailing whitespace
        # print(f"Piece length: {len(piece)}")

        if not piece:
            continue

        # case A: piece is TOO LARGE, we need to chunk it recursively
        if len(piece) > max_length:
            # first save whatever we have already accumulated in current_chunk
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""

                # now recursively chunk the overized piece using a smaller separator
                smaller_chunks = chunk_text_recursive(piece, max_length, separators[1:])
                # add those chunks to the main list of chunks
                chunks.extend(smaller_chunks)
        
        # case B: piece fits in the current chunk
        else:
            # if current chunk is empty, start it with this piece.
            if not current_chunk:
                current_chunk = piece

            else:
                # try adding this piece to the curent chunk.
                candidate = (current_chunk + separator + piece)

                # does it fit?
                if len(candidate) <= max_length:
                    current_chunk = candidate
                else:
                    # it doesn't fit, so save the current chunk and start a new one with this piece.
                    chunks.append(current_chunk)
                    current_chunk = piece


    # Save final chunk if it has content
    if current_chunk:
        chunks.append(current_chunk)

    return chunks