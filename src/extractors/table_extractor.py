import pymupdf


def extract_tables(file_path):

    document = pymupdf.open(file_path)

    all_tables = []

    for page_number, page in enumerate(document):

        tables = page.find_tables()

        for table in tables.tables:

            table_data = table.extract()

            all_tables.append({
                "page_number": page_number + 1,
                "data": table_data
            })

    document.close()

    return all_tables


def calculate_table_total(table_data):

    total = 0.0

    # Skip the first row because it contains column names
    for row in table_data[1:]:

        quantity = float(row[1])

        price = float(
            row[2].replace("$", "").replace(",", "")
        )

        total = total + (quantity * price)

    return total