from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


# Output PDF location
pdf_path = "documents/bad_invoice.pdf"


# Create PDF
document = SimpleDocTemplate(
    pdf_path,
    pagesize=letter
)


# Styles
styles = getSampleStyleSheet()


# Invoice information
invoice_number = "INV-BAD-001"

# INTENTIONALLY WRONG TOTAL
total_amount = "$900"


# Table data
data = [
    ["Item", "Quantity", "Price"],
    ["Laptop", "1", "$800"],
    ["Keyboard", "2", "$50"],
    ["Mouse", "1", "$25"],
    ["USB Cable", "3", "$10"]
]


# Create table
table = Table(data)


# Style the table
table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ])
)


# Build document
content = [

    Paragraph(
        "<b>INVOICE</b>",
        styles["Title"]
    ),

    Spacer(1, 20),

    Paragraph(
        f"<b>Invoice Number:</b> {invoice_number}",
        styles["Normal"]
    ),

    Spacer(1, 20),

    table,

    Spacer(1, 20),

    Paragraph(
        f"<b>Total: {total_amount}</b>",
        styles["Normal"]
    )
]


document.build(content)


print("Bad invoice PDF created successfully!")
print(pdf_path)