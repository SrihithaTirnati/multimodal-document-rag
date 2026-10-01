import streamlit as st
import os

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
from src.retrieval.retriever import search_documents

from PIL import Image
from io import BytesIO

import ollama


# -----------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------

st.set_page_config(
    page_title="Multimodal Document RAG",
    page_icon="📄",
    layout="wide"
)


# -----------------------------------------
# HEADER
# -----------------------------------------

st.title("📄 Multimodal Document RAG")

st.markdown(
    """
    **Intelligent document processing using OCR, LLM extraction,
    validation, embeddings and Retrieval-Augmented Generation.**
    """
)

st.divider()


# -----------------------------------------
# SIDEBAR
# -----------------------------------------

with st.sidebar:

    st.header("⚙️ Pipeline")

    st.markdown(
        """
        **1.** PDF Upload  
        ↓  
        **2.** Text / OCR Extraction  
        ↓  
        **3.** Table Extraction  
        ↓  
        **4.** LLM Information Extraction  
        ↓  
        **5.** Validation  
        ↓  
        **6.** Confidence Scoring  
        ↓  
        **7.** ChromaDB Retrieval  
        ↓  
        **8.** Question Answering
        """
    )

    st.divider()

    st.info(
        "Low-confidence documents are routed "
        "to the Human Review Queue."
    )


# -----------------------------------------
# DOCUMENT UPLOAD
# -----------------------------------------

st.header("📤 Upload Document")

uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"]
)


if uploaded_file:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )


    documents_folder = "documents"

    os.makedirs(
        documents_folder,
        exist_ok=True
    )


    pdf_path = os.path.join(
        documents_folder,
        uploaded_file.name
    )


    with open(
        pdf_path,
        "wb"
    ) as file:

        file.write(
            uploaded_file.getbuffer()
        )


    # -----------------------------------------
    # PROCESS DOCUMENT
    # -----------------------------------------

    if st.button(
        "⚙️ Process Document",
        type="primary"
    ):

        with st.spinner(
            "Processing document..."
        ):

            pages = load_pdf(
                pdf_path
            )


            tables = extract_tables(
                pdf_path
            )


            total_pages = len(
                pages
            )


            processed_pages = 0

            review_required = False


            # -----------------------------------------
            # PROCESS EACH PAGE
            # -----------------------------------------

            for page in pages:

                page_number = page[
                    "page_number"
                ]


                # -----------------------------------------
                # TEXT OR OCR
                # -----------------------------------------

                if page["needs_ocr"]:

                    image = Image.open(
                        BytesIO(
                            page["image"]
                        )
                    )


                    text_for_llm = (
                        extract_text_from_image(
                            image
                        )
                    )

                else:

                    text_for_llm = page[
                        "text"
                    ]


                # -----------------------------------------
                # TABLE EXTRACTION
                # -----------------------------------------

                page_tables = []

                table_total = None


                for table in tables:

                    if (
                        table["page_number"]
                        == page_number
                    ):

                        page_tables.append(
                            str(
                                table["data"]
                            )
                        )


                        table_total = (
                            calculate_table_total(
                                table["data"]
                            )
                        )


                if page_tables:

                    table_text = "\n".join(
                        page_tables
                    )


                    text_for_llm = (
                        text_for_llm
                        + "\n\nTABLE DATA:\n"
                        + table_text
                    )


                # -----------------------------------------
                # LLM EXTRACTION
                # -----------------------------------------

                extracted_information = (
                    extract_document_information(
                        text_for_llm
                    )
                )


                # -----------------------------------------
                # VALIDATION
                # -----------------------------------------

                validation_result = (
                    validate_invoice_data(
                        extracted_information,
                        table_total,
                        text_for_llm
                    )
                )


                confidence = (
                    validation_result[
                        "confidence"
                    ]
                )


                # -----------------------------------------
                # VALID DOCUMENT
                # -----------------------------------------

                if (
                    validation_result["valid"]
                    and confidence >= 0.80
                ):

                    document_id = (
                        uploaded_file.name
                        + "_page_"
                        + str(page_number)
                    )


                    metadata = {

                        "source":
                            uploaded_file.name,

                        "page":
                            page_number,

                        "invoice_number":
                            extracted_information.get(
                                "invoice_number",
                                ""
                            ),

                        "confidence":
                            confidence
                    }


                    document_text = (

                        "Source document: "
                        + uploaded_file.name
                        + "\n"

                        + "Page: "
                        + str(page_number)
                        + "\n"

                        + "Invoice number: "
                        + extracted_information.get(
                            "invoice_number",
                            ""
                        )
                        + "\n"

                        + text_for_llm
                    )


                    add_document(
                        document_id,
                        document_text,
                        metadata
                    )


                # -----------------------------------------
                # HUMAN REVIEW
                # -----------------------------------------

                else:

                    review_required = True


                    send_to_review(

                        uploaded_file.name,

                        str(
                            extracted_information
                        ),

                        confidence,

                        validation_result[
                            "errors"
                        ]
                    )


                processed_pages += 1


        # -----------------------------------------
        # PROCESSING RESULT
        # -----------------------------------------

        if review_required:

            st.warning(
                "⚠️ Document requires human review."
            )

            st.write(
                "The document failed validation "
                "or had a low confidence score."
            )

        else:

            st.success(
                f"✅ Document processed successfully! "
                f"{processed_pages}/{total_pages} pages processed."
            )


# -----------------------------------------
# QUESTION ANSWERING
# -----------------------------------------

st.divider()

st.header("🔎 Ask Questions")

st.write(
    "Ask a question about the processed documents."
)


question = st.text_input(
    "Your question",
    placeholder="Example: What is the invoice number?"
)


if st.button(
    "🔍 Ask Question",
    type="primary"
):

    if not question:

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Searching documents..."
        ):

            results = search_documents(
                question
            )


            documents = (
                results["documents"][0]
            )


            metadatas = (
                results["metadatas"][0]
            )


            context = "\n\n".join(
                documents
            )


            prompt = f"""
You are a document question-answering system.

Answer the user's question using ONLY
the information in the context.

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


            answer = response[
                "message"
            ][
                "content"
            ]


        # -----------------------------------------
        # ANSWER
        # -----------------------------------------

        st.subheader("💡 Answer")

        st.success(
            answer
        )


        # -----------------------------------------
        # SOURCES
        # -----------------------------------------

        st.subheader(
            "📚 Source Information"
        )


        for metadata in metadatas:

            with st.expander(
                f"📄 {metadata.get('source', 'Unknown')}"
            ):

                st.write(
                    f"**Page:** "
                    f"{metadata.get('page', 'Unknown')}"
                )

                st.write(
                    f"**Chunk:** "
                    f"{metadata.get('chunk', 'Unknown')}"
                )

                st.write(
                    f"**Confidence:** "
                    f"{metadata.get('confidence', 'Unknown')}"
                )