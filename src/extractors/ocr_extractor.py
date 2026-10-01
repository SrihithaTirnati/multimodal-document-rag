import pytesseract
from PIL import Image


# Tesseract installation path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)

    return text