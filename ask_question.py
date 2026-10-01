import ollama

from src.retrieval.retriever import search_documents


question = input(
    "\nAsk a question about the document: "
)


# Search the vector database
results = search_documents(
    question
)


documents = results["documents"][0]

metadatas = results["metadatas"][0]


# Combine retrieved chunks
context = "\n\n".join(
    documents
)


prompt = f"""
You are a document question-answering system.

Answer the user's question using ONLY the
information provided in the context.

Do not invent information.

Context:
{context}

Question:
{question}

Answer:
"""


response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)


answer = response["message"]["content"]


print("\nAnswer:")
print(answer)


# Display source information
print("\nSource Information:")

for metadata in metadatas:

    print(
        "Document:",
        metadata.get(
            "source",
            "Unknown"
        )
    )

    print(
        "Page:",
        metadata.get(
            "page",
            "Unknown"
        )
    )

    print(
        "Chunk:",
        metadata.get(
            "chunk",
            "Unknown"
        )
    )

    print()