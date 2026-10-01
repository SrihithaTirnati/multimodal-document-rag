
from src.loaders.pdf_loader import load_pdf
from src.extractors.ocr_extractor import extract_text_from_image
from src.extractors.document_extractor import extract_document_information
from src.extractors.table_extractor import (
    extract_tables,
    calculate_table_total
)
from src.validation.validator import validate_invoice_data
from src.review.review_queue import send_to_review
from src.retrieval.retriever import add_document

from PIL import Image
from io import BytesIO
import os


# PDF file
pdf_path = "documents/table_invoice.pdf"


# Load PDF
pages = load_pdf(pdf_path)

print("Number of pages:", len(pages))


# Extract tables from the PDF
tables = extract_tables(pdf_path)

print("\nNumber of tables found:", len(tables))


# Display extracted tables
for table in tables:

    print("\n--- Table on Page", table["page_number"], "---")

    for row in table["data"]:
        print(row)


# Process each page
for page in pages:

    print("\n--- Page", page["page_number"], "---")

    # Normal PDF text extraction
    print("\nNormal PDF text:")
    print(page["text"])

    # Check whether OCR is needed
    print("\nNeeds OCR:", page["needs_ocr"])


    # Choose text for LLM extraction
    if page["needs_ocr"]:

        print("\nRunning OCR...")

        image = Image.open(
            BytesIO(page["image"])
        )

        ocr_text = extract_text_from_image(image)

        print("\nOCR text:")
        print(ocr_text)

        text_for_llm = ocr_text

    else:

        print("\nOCR not required.")

        text_for_llm = page["text"]


    # Add table information to the text
    page_tables = []

    for table in tables:

        if table["page_number"] == page["page_number"]:

            page_tables.append(
                str(table["data"])
            )


    # Calculate table total
    table_total = None

    for table in tables:

        if table["page_number"] == page["page_number"]:

            table_total = calculate_table_total(
                table["data"]
            )

            print(
                "\nCalculated Table Total:",
                table_total
            )


    # Add table information to LLM input
    if page_tables:

        table_text = "\n".join(page_tables)

        text_for_llm = (
            text_for_llm
            + "\n\nTABLE DATA:\n"
            + table_text
        )


    # LLM extraction
    extracted_information = (
        extract_document_information(
            text_for_llm
        )
    )

    print("\nExtracted Information:")
    print(extracted_information)


    # Validation
    validation_result = validate_invoice_data(
        extracted_information,
        table_total
    )

    print("\nValidation Result:")
    print(validation_result)


    # Confidence score
    confidence = validation_result["confidence"]

    print(
        "\nConfidence Score:",
        confidence * 100,
        "%"
    )


    # Decide what to do with the document
    if (
        validation_result["valid"]
        and confidence >= 0.80
    ):

        print(
            "\n✅ Document passed validation."
        )

        print(
            "Document can be stored."
        )


        # ---------------------------------
        # Store validated document in RAG
        # ---------------------------------

        document_id = (
            os.path.basename(pdf_path)
            + "_page_"
            + str(page["page_number"])
        )


        metadata = {
            "source": os.path.basename(pdf_path),
            "page": page["page_number"],
            "invoice_number":
                extracted_information["invoice_number"],
            "confidence": confidence
        }


        # Include source information in the
        # text used to create the embedding

        document_text = (
            "Source document: "
            + os.path.basename(pdf_path)
            + "\n"
            + "Invoice number: "
            + extracted_information["invoice_number"]
            + "\n"
            + text_for_llm
        )


        add_document(
            document_id,
            document_text,
            metadata
        )


        print(
            "\n📚 Document added to ChromaDB."
        )


    else:

        print(
            "\n⚠️ Document requires human review."
        )

        document_name = os.path.basename(
            pdf_path
        )

        review_file = send_to_review(
            document_name,
            str(extracted_information),
            confidence,
            validation_result["errors"]
        )

        print(
            "Review file created:"
        )

        print(review_file)

