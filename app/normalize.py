import re


def normalize(text: str) -> str:
    """
    Normalize input text to reduce trivial rule bypass:
    - lowercase
    - collapse whitespace
    - strip leading/trailing spaces
    """
    t = text.lower()
    t = re.sub(r"\s+", " ", t).strip()
    return t
