from src.extractors.table_extractor import extract_tables


# PDF containing a table
pdf_path = "documents/table_invoice.pdf"


# Extract tables
tables = extract_tables(pdf_path)


# Display results
print("\nNumber of tables found:", len(tables))

for table in tables:

    print("\n--- Table on Page", table["page_number"], "---")

    for row in table["data"]:
        print(row)
        