import pymupdf


def load_pdf(file_path):

    document = pymupdf.open(file_path)

    pages = []


    for page_number, page in enumerate(document):

        # Extract normal PDF text
        text = page.get_text().strip()


        # Convert page into an image
        pixmap = page.get_pixmap()

        image_bytes = pixmap.tobytes("png")


        # Count words in extracted text
        words = text.split()


        # Decide whether OCR is needed
        #
        # If the PDF contains enough readable words,
        # use the original PDF text.
        #
        # If there is almost no readable text,
        # use OCR.

        needs_ocr = len(words) < 5


        pages.append({

            "page_number": page_number + 1,

            "text": text,

            "image": image_bytes,

            "needs_ocr": needs_ocr

        })


    document.close()


    return pages