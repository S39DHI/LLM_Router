def route_model(complexity: str) -> str:
    if complexity == "simple":
        return "gpt-4o-mini"
    elif complexity == "medium":
        return "gpt-4.1"
    else:
        return "gpt-4.1"
