def classify_complexity(question: str) -> str:
    words = question.strip().split()
    length = len(words)
    if length < 8:
        return "simple"
    elif length < 20:
        return "medium"
    else:
        return "complex"
