\# 📄 Multimodal Document RAG



A document question-answering system that can work with \*\*normal PDFs, scanned documents, and tables\*\*.



I built this project to explore how RAG systems can be made more reliable when the documents are messy or difficult to process. Instead of directly sending extracted information to an LLM, the system first validates it and sends uncertain documents for human review.



\## 💡 Why I Built This



Most simple RAG projects assume that the document already contains clean, readable text.



Real-world documents are not always like that.



A PDF might contain:



\* Normal text

\* Scanned pages

\* Tables

\* Incorrect or inconsistent information

\* Different document layouts



So I wanted to build a pipeline that could handle these situations before the information reached the RAG system.



\---



\## 🔄 How It Works



The overall pipeline is:



```text

PDF

&#x20;↓

Text Extraction

&#x20;↓

OCR if needed

&#x20;↓

Table Extraction

&#x20;↓

LLM Information Extraction

&#x20;↓

Validation

&#x20;↓

Confidence Score

&#x20;↓

&#x20;┌─────────────────────┐

&#x20;│                     │

High Confidence    Low Confidence

&#x20;│                     │

&#x20;▼                     ▼

ChromaDB          Human Review

&#x20;│

&#x20;▼

Semantic Retrieval

&#x20;│

&#x20;▼

Llama 3.2

&#x20;│

&#x20;▼

Answer + Source

```



The important part is that \*\*not every document is automatically trusted\*\*.



\---



\## 🧩 Main Features



\### 📄 PDF Processing



The project uses PyMuPDF to read PDF documents and process them page by page.



\### 🔍 OCR for Scanned Documents



If a page does not contain enough extractable text, the system treats it as a possible scanned page and uses \*\*Tesseract OCR\*\* to extract the text from the page image.



\### 📊 Table Extraction



Tables are extracted separately from the document.



For invoice documents, the values from the table can also be used to independently calculate the expected total.



\### 🤖 LLM-Based Extraction



I use \*\*Llama 3.2 through Ollama\*\* to extract structured information such as:



```json

{

&#x20;   "invoice\_number": "INV-123",

&#x20;   "total": "$955"

}

```



The prompt instructs the model to use only information that is actually present in the document.



\### ✅ Independent Validation



The extracted information is then checked separately.



For example, if the LLM says:



```text

Total = $900

```



but the table calculation gives:



```text

Table Total = $955

```



the system detects the mismatch.



\### 📈 Confidence Scoring



The validation results are used to calculate a confidence score.



For example:



```text

Confidence: 67%

```



A low-confidence result is not automatically added to the knowledge base.



\### 👤 Human Review



Documents that fail validation or have low confidence are sent to a \*\*Human Review Queue\*\*.



This creates a human-in-the-loop step instead of allowing an uncertain extraction to continue through the pipeline.



\### 🧠 Embeddings + ChromaDB



Validated document content is split into chunks and converted into embeddings using:



```text

all-MiniLM-L6-v2

```



The embeddings are stored in \*\*ChromaDB\*\*, which is then used for semantic search.



\### 💬 RAG Question Answering



When a user asks a question, the system:



```text

Question

&#x20;  ↓

Create Query Embedding

&#x20;  ↓

Search ChromaDB

&#x20;  ↓

Retrieve Relevant Chunks

&#x20;  ↓

Send Context to Llama 3.2

&#x20;  ↓

Generate Answer

```



The application also shows the document, page, and chunk information used as the source.



\---



\## 🧪 Example



I created an intentionally incorrect invoice to test whether the validation system could catch an error.



The document contains:



```text

Printed Total: $900

```



But calculating the values in the table gives:



```text

Table Total: $955

```



The system detects the mismatch and produces:



```text

Validation: Failed

Confidence: 67%

Human Review: Required

```



This test helped verify that the system does not simply trust the LLM's answer.



\---



\## 🖥️ Streamlit Interface



The project has a simple Streamlit interface where you can:



1\. Upload a PDF.

2\. Process the document.

3\. View whether it passed validation.

4\. Automatically run OCR when required.

5\. Store validated documents.

6\. Send failed documents to human review.

7\. Ask questions about processed documents.

8\. View the source document and page information.



Run the application with:



```bash

streamlit run app.py

```



\---



\## 🛠️ Technologies Used



\* \*\*Python\*\* — Main programming language

\* \*\*PyMuPDF\*\* — PDF processing

\* \*\*Tesseract OCR\*\* — Scanned document extraction

\* \*\*Llama 3.2\*\* — Local LLM

\* \*\*Ollama\*\* — Running the LLM locally

\* \*\*Sentence Transformers\*\* — Text embeddings

\* \*\*all-MiniLM-L6-v2\*\* — Embedding model

\* \*\*ChromaDB\*\* — Vector database

\* \*\*Streamlit\*\* — User interface

\* \*\*ReportLab\*\* — Creating test PDFs



\---



\## 📁 Project Structure



```text

multimodal\_document\_rag/

│

├── documents/

│

├── src/

│   ├── loaders/

│   │   └── pdf\_loader.py

│   │

│   ├── extractors/

│   │   ├── document\_extractor.py

│   │   ├── ocr\_extractor.py

│   │   └── table\_extractor.py

│   │

│   ├── retrieval/

│   │   └── retriever.py

│   │

│   ├── validation/

│   │   └── validator.py

│   │

│   ├── embeddings/

│   │   └── embedder.py

│   │

│   └── review/

│       └── review\_queue.py

│

├── app.py

├── main.py

├── ask\_question.py

├── clear\_database.py

├── requirements.txt

└── README.md

```



\---



\## ⚙️ Running the Project



Create and activate a virtual environment:



```powershell

python -m venv venv

venv\\Scripts\\activate

```



Install the required packages:



```powershell

pip install -r requirements.txt

```



Make sure Ollama is installed and the Llama 3.2 model is available:



```powershell

ollama pull llama3.2

```



Then start the application:



```powershell

streamlit run app.py

```



\---



\## 🔐 Local LLM



One reason I used Ollama for this project was to run \*\*Llama 3.2 locally\*\*.



This means the main LLM pipeline does not depend on an OpenAI API key.



\---



\## 📚 What I Learned



Building this project helped me understand how the different parts of a practical RAG system fit together.



Some of the main concepts I worked with were:



\* PDF processing

\* OCR

\* Table extraction

\* Prompt-based information extraction

\* LLM validation

\* Confidence scoring

\* Human-in-the-loop systems

\* Embeddings

\* Vector databases

\* Semantic search

\* Retrieval-Augmented Generation

\* Local LLMs

\* Streamlit applications



More importantly, I learned that building a useful RAG system is not just about connecting an LLM to a vector database. \*\*The quality of the information going into the system matters just as much as the retrieval step.\*\*



\---



\## 🔮 Future Improvements



Some things I would like to add later:



\* Support for more document types

\* Better handling of complex tables

\* Batch document processing

\* Hybrid keyword + semantic search

\* Retrieval reranking

\* A dedicated human-review dashboard

\* Better confidence calibration

\* More advanced multimodal models



\---



\## 👩‍💻 About



\*\*Srihitha Tirnati\*\*

B.Tech — Electrical and Electronics Engineering

NIT Andhra Pradesh



This project was built as part of my learning journey in \*\*AI, Machine Learning, and Retrieval-Augmented Generation\*\*.



