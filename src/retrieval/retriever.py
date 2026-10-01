import chromadb

from src.embeddings.embedder import create_embedding


# Create ChromaDB client
client = chromadb.PersistentClient(
    path="chroma_db"
)


# Create or open document collection
collection = client.get_or_create_collection(
    name="documents"
)


def split_text(
    text,
    chunk_size=500,
    overlap=50
):

    """
    Split a document into overlapping chunks.
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def add_document(
    document_id,
    text,
    metadata=None
):

    # Split document
    chunks = split_text(text)

    for index, chunk in enumerate(chunks):

        chunk_id = (
            document_id
            + "_chunk_"
            + str(index)
        )

        # Create embedding
        embedding = create_embedding(
            chunk
        )

        # Copy metadata
        chunk_metadata = {
            **(metadata or {}),
            "chunk": index,
            "total_chunks": len(chunks)
        }

        # Store chunk
        collection.add(
            ids=[chunk_id],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[chunk_metadata]
        )


def search_documents(
    query,
    n_results=3
):

    # Create embedding for question
    query_embedding = create_embedding(
        query
    )

    # Retrieve the most relevant chunks
    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=n_results
    )

    return results


def clear_collection():

    existing_data = collection.get()

    if existing_data["ids"]:

        collection.delete(
            ids=existing_data["ids"]
        )

        print(
            "ChromaDB collection cleared."
        )

    else:

        print(
            "ChromaDB collection was already empty."
        )