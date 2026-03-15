from fastapi import FastAPI
from app.schemas import AskRequest, AskResponse
from app.classifier import classify_complexity
from app.router import route_model
from app.llm_client import ask_llm

app = FastAPI()

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    question = request.question
    complexity = classify_complexity(question)
    model_used = route_model(complexity)
    answer = ask_llm(question, model_used)
    return AskResponse(
        complexity=complexity,
        model_used=model_used,
        answer=answer
    )
