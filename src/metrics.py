import re


def placeholder_penalty_score(email_text):
    """
    Detect unresolved placeholders in generated emails.

    Returns:
        float: Score between 0.0 and 1.0

        1.0 = No placeholders detected
        0.0 = Many placeholders detected
    """

    placeholder_patterns = [
        # [Customer Name]
        r"\[[^\]]+\]",

        # <customer_name>
        r"<[^>]+>",

        # {customer_name}
        r"\{[^}]+\}",

        # Common template instructions
        r"\b(insert|replace|your)\s+[a-zA-Z ]+\b",
    ]

    count = 0

    for pattern in placeholder_patterns:
        matches = re.findall(
            pattern,
            email_text,
            flags=re.IGNORECASE
        )
        count += len(matches)

    # No placeholders found
    if count == 0:
        return 1.0

    # Apply penalty for each placeholder
    score = max(
        0.0,
        1.0 - (count * 0.20)
    )

    return round(score, 3)


if __name__ == "__main__":

    email_1 = """
    Subject: Order Update

    Dear Customer,

    Your replacement order has been shipped.

    Best regards
    """

    email_2 = """
    Subject: Order Update

    Dear [Customer Name],

    Your replacement order has been shipped.

    Best regards
    """

    email_3 = """
    Subject: Order Update

    Dear [Customer Name],

    Please contact <support_email> if you have questions.

    Best regards,

    [Your Name]
    """

    print("Email 1:", placeholder_penalty_score(email_1))
    print("Email 2:", placeholder_penalty_score(email_2))
    print("Email 3:", placeholder_penalty_score(email_3))