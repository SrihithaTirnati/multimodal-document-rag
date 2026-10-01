import os


REVIEW_FOLDER = "review_queue"


def send_to_review(
    document_name,
    extracted_information,
    confidence,
    errors
):

    # Create review queue folder if it doesn't exist
    os.makedirs(
        REVIEW_FOLDER,
        exist_ok=True
    )


    # Create a review file
    file_path = os.path.join(
        REVIEW_FOLDER,
        document_name + "_review.txt"
    )


    # Save information for human review
    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "DOCUMENT REQUIRES HUMAN REVIEW\n"
        )

        file.write(
            "--------------------------------\n\n"
        )


        file.write(
            "Document:\n"
        )

        file.write(
            document_name
        )

        file.write(
            "\n\n"
        )


        file.write(
            "Confidence:\n"
        )

        file.write(
            str(confidence * 100)
        )

        file.write(
            "%\n\n"
        )


        file.write(
            "Validation Errors:\n"
        )

        if errors:

            for error in errors:

                file.write(
                    "- " + error + "\n"
                )

        else:

            file.write(
                "No validation errors recorded.\n"
            )


        file.write(
            "\nExtracted Information:\n"
        )

        file.write(
            extracted_information
        )


    return file_path