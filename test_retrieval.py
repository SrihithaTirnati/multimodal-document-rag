from src.retrieval.retriever import add_document, search_documents


# Add a test document
add_document(
    "test2",
    "Invoice INV-002 has a total amount of $500",
    {"type": "invoice"}
)


# Search for the document
results = search_documents(
    "What is the invoice total?"
)


# Display the results
print("\nSearch Results:")
print(results)