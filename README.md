# Multimodal Document RAG

A document processing and retrieval pipeline designed to work with different types of PDF documents, including normal text PDFs, scanned documents, and documents containing tables.

The project combines PDF text extraction, OCR, table extraction, LLM-based information extraction, validation, and retrieval into one workflow. Documents with uncertain or inconsistent results are sent to a human review queue instead of being stored without verification.

## What this project does

The pipeline processes a document in multiple stages:

1. Detects the type of content present in the document.
2. Extracts text directly from text-based PDFs.
3. Uses OCR for scanned documents when required.
4. Extracts structured information such as invoice numbers and totals.
5. Detects and processes tables from PDF documents.
6. Validates extracted information against available document data.
7. Assigns a confidence score to the extracted information.
8. Sends low-confidence or inconsistent results to a human review queue.
9. Stores the processed information for retrieval.
10. Allows users to ask questions about the documents through a RAG-based interface.

## Technologies Used

* Python
* PyMuPDF
* Tesseract OCR
* Ollama
* Large Language Models
* Retrieval-Augmented Generation (RAG)
* PDF table extraction
* Streamlit
* JSON
* Git and GitHub

## Project Structure

```text
multimodal_document_rag/
│
├── documents/
│   └── Input PDF documents
│
├── review_queue/
│   └── Documents requiring human review
│
├── src/
│   ├── extractors/
│   ├── validators/
│   └── retrieval/
│
├── main.py
├── requirements.txt
└── README.md
```

## Extraction and Validation

The extraction stage converts information from different document formats into a structured form.

For example, an invoice can be processed to identify fields such as:

```text
Invoice Number: 12345
Total: 1250.00
```

For documents containing tables, the extracted table data can also be used to calculate and verify totals.

The validation layer compares the extracted information with available document data. When the information does not meet the validation requirements or the confidence is too low, the document is moved to the review queue.

## Human Review

Instead of assuming that every extraction is correct, the system keeps track of confidence and validation results.

Documents with missing fields, inconsistent totals, or low-confidence extraction can be flagged for manual verification.

This is useful for document-processing systems where incorrect information can be more problematic than asking a person to review an uncertain result.

## RAG Pipeline

After processing, document information can be retrieved when a user asks a question.

The general workflow is:

```text
PDF Documents
      |
      v
Document Detection
      |
      +---- Text Extraction
      |
      +---- OCR
      |
      +---- Table Extraction
      |
      v
LLM-based Information Extraction
      |
      v
Validation
      |
      +---- High Confidence --> Store
      |
      +---- Low Confidence --> Human Review
      |
      v
Document Retrieval
      |
      v
Question Answering
```

## Current Status

The project currently supports:

* Text extraction from PDFs
* OCR for scanned documents
* Structured invoice information extraction
* PDF table extraction
* Table total calculation
* Validation of extracted information
* Confidence scoring
* Human review queue
* Local LLM processing with Ollama
* RAG-based document querying

## Future Improvements

Some areas that can be added to the project include:

* Support for more document formats
* Better handling of complex tables
* Improved retrieval and document chunking
* More detailed confidence scoring
* A more complete review interface
* Deployment as a web application
* Support for larger document collections

## Running the Project

Clone the repository and create a Python virtual environment.

```bash
python -m venv venv
```

Activate the environment on Windows:

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Make sure the required local OCR and LLM components are installed before running the project.

Then run the appropriate Python or Streamlit entry point from the project directory.

## Purpose

This project was built to understand how document AI systems can handle information that is not always clean or structured. The main focus is on combining extraction, validation, retrieval, and human review rather than relying on a single extraction method.
