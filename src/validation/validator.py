import re


def extract_numeric_amount(value):

    text = str(value)

    text = text.replace(",", "")

    match = re.search(
        r"\d+(?:\.\d+)?",
        text
    )

    if match:
        return float(match.group())

    return None


def extract_printed_total(text):

    match = re.search(
        r"Total\s*:\s*\$?\s*([\d,]+(?:\.\d+)?)",
        text,
        re.IGNORECASE
    )

    if match:

        return float(
            match.group(1).replace(",", "")
        )

    return None


def validate_invoice_data(
    extracted_information,
    table_total=None,
    document_text=""
):

    errors = []

    confidence_points = 0
    total_points = 0

    invoice_number = extracted_information.get(
        "invoice_number",
        ""
    )

    total_points += 1

    if not invoice_number:

        errors.append(
            "Invoice number is missing."
        )

    elif not re.search(
        r"(INV|Invoice|#)",
        str(invoice_number),
        re.IGNORECASE
    ):

        errors.append(
            "Invoice number format looks invalid."
        )

    else:

        confidence_points += 1


    total = extracted_information.get(
        "total",
        ""
    )

    total_points += 1

    numeric_total = None

    if not total:

        errors.append(
            "Total amount is missing."
        )

    else:

        numeric_total = extract_numeric_amount(
            total
        )

        if numeric_total is None:

            errors.append(
                "Total amount is not numeric."
            )

        else:

            confidence_points += 1


    # Compare with table total
    if table_total is not None:

        print(
            "\nTrusted Total from Table:",
            table_total
        )

        total_points += 1

        if numeric_total is None:

            errors.append(
                "Extracted total could not be compared "
                "with the table total."
            )

        elif abs(
            numeric_total - table_total
        ) > 0.01:

            errors.append(
                "Extracted total does not match "
                "the trusted table total."
            )

        else:

            confidence_points += 1


    # Compare with printed total
    printed_total = extract_printed_total(
        document_text
    )

    if printed_total is not None:

        print(
            "\nPrinted Total in Document:",
            printed_total
        )

        total_points += 1

        if numeric_total is None:

            errors.append(
                "Extracted total could not be compared "
                "with the printed total."
            )

        elif abs(
            numeric_total - printed_total
        ) > 0.01:

            errors.append(
                "Extracted total does not match "
                "the printed document total."
            )

        else:

            confidence_points += 1


    if total_points > 0:

        confidence = (
            confidence_points / total_points
        )

    else:

        confidence = 0.0


    confidence = round(
        confidence,
        2
    )


    valid = len(errors) == 0


    return {

        "valid": valid,

        "confidence": confidence,

        "errors": errors

    }