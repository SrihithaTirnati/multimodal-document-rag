import ollama
import json
import re


def extract_document_information(text):

    prompt = f"""
You are a document information extraction system.

Your job is ONLY to extract information explicitly present
in the document.

Extract these two fields:

1. Invoice number
2. Total amount

IMPORTANT RULES:

- Extract the invoice number ONLY from a line that explicitly
  identifies itself as an invoice number.
- Valid examples include:
  "Invoice Number: INV-123"
  "Invoice No: INV-123"
  "Invoice #: INV-123"
- Do NOT use item names as the invoice number.
- Do NOT use table headers as the invoice number.
- Do NOT use table rows as the invoice number.
- Do NOT use "TABLE DATA" as the invoice number.
- Do NOT calculate the total.
- Do NOT add or multiply table values.
- Do NOT invent values.
- Copy the explicitly stated total from the document.
- If a field is not explicitly present, return an empty string.

Document text:

{text}

Return ONLY valid JSON.

Use exactly this format:

{{
    "invoice_number": "",
    "total": ""
}}

Do not add explanations.
Do not add markdown.
Do not add extra fields.
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


    result = response["message"]["content"].strip()


    # Try normal JSON parsing
    try:

        return json.loads(result)

    except json.JSONDecodeError:

        print("\n⚠️ LLM returned invalid JSON.")
        print("Raw LLM response:")
        print(result)


    # Remove markdown code fences
    repaired_result = result.replace(
        "```json",
        ""
    ).replace(
        "```",
        ""
    ).strip()


    # Add missing closing brace
    if (
        repaired_result.startswith("{")
        and not repaired_result.endswith("}")
    ):

        repaired_result += "}"


    # Try repaired JSON
    try:

        return json.loads(repaired_result)

    except json.JSONDecodeError:

        print("\n⚠️ JSON repair also failed.")


    # Regex fallback
    invoice_match = re.search(
        r'"invoice_number"\s*:\s*"([^"]*)"',
        result
    )

    total_match = re.search(
        r'"total"\s*:\s*"([^"]*)"',
        result
    )


    invoice_number = ""

    total = ""


    if invoice_match:

        invoice_number = invoice_match.group(1)


    if total_match:

        total = total_match.group(1)


    return {
        "invoice_number": invoice_number,
        "total": total
    }