def requires_advisor_approval(credits: int) -> bool:
    """Return whether the credit load exceeds the approval threshold."""
    if type(credits) is not int:
        raise TypeError("credits must be an integer")
    return credits > 30