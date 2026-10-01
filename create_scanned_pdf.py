from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


# Create a high-resolution image
image = Image.new(
    "RGB",
    (1700, 2200),
    "white"
)

draw = ImageDraw.Draw(image)


# Use a larger font
font_path = "C:/Windows/Fonts/arial.ttf"

title_font = ImageFont.truetype(
    font_path,
    80
)

text_font = ImageFont.truetype(
    font_path,
    45
)


# Invoice title
draw.text(
    (150, 150),
    "INVOICE",
    fill="black",
    font=title_font
)


# Invoice information
draw.text(
    (150, 350),
    "Invoice Number: INV-SCAN-001",
    fill="black",
    font=text_font
)

draw.text(
    (150, 450),
    "Customer: Test Customer",
    fill="black",
    font=text_font
)


# Item information
draw.text(
    (150, 650),
    "Item: Laptop",
    fill="black",
    font=text_font
)

draw.text(
    (150, 750),
    "Quantity: 1",
    fill="black",
    font=text_font
)

draw.text(
    (150, 850),
    "Price: $800",
    fill="black",
    font=text_font
)


# Total
draw.text(
    (150, 1050),
    "Total: $800",
    fill="black",
    font=text_font
)


# Save image
image_path = "documents/scanned_invoice.png"

image.save(
    image_path,
    dpi=(300, 300)
)


# Create PDF containing the image
pdf_path = "documents/scanned_invoice.pdf"

pdf = canvas.Canvas(
    pdf_path,
    pagesize=letter
)

pdf.drawImage(
    image_path,
    0,
    0,
    width=letter[0],
    height=letter[1]
)

pdf.save()


print("OCR-friendly scanned PDF created!")
print(pdf_path)