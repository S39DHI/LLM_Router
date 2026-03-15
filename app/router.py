# def route_model(complexity: str) -> str:
#     if complexity == "simple":
#         return "gpt-4o-mini"
#     elif complexity == "medium":
#         return "gpt-4.1"
#     else:
#         return "gpt-4.1"

# Better way to make this function is below and this make easy to add more models and aslo !DD!


MODEL_ROUTING = {
    "simple": "gpt-4o-mini",
    "medium": "gpt-4.1",
    "complex": "gpt-4.1"
}

def route_model(complexity: str) -> str:
    if complexity not in MODEL_ROUTING:
        raise ValueError(f"Invalid complexity: {complexity}")
    return MODEL_ROUTING[complexity]
