# LLM Router Service

## Project Description
A FastAPI service that receives a user question, classifies its complexity, routes the query to the appropriate LLM model, and returns the answer along with metadata about the routing decision.

## Setup Instructions
1. Clone the repository.
2. Navigate to the `llm-router` directory.
3. Copy `.env.example` to `.env` and add your OpenAI API key.
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API
Start the server from the llm-router directory:
```bash
cd llm-router
uvicorn app.main:app --reload
```

Access interactive docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Example Request
POST `/ask`
```json
{
  "question": "Explain Kubernetes pods"
}
```

## Example Response
```json
{
  "complexity": "simple",
  "model_used": "gpt-4o-mini",
  "answer": "A Kubernetes Pod is the smallest deployable unit..."
}
```

## Routing Logic
- If question length < 8 words → simple → gpt-4o-mini
- If question length < 20 words → medium → gpt-4.1
- Otherwise → complex → gpt-4.1

## System Architecture Overview
```
User Question
↓
Complexity Classifier
↓
Model Router
↓
OpenAI API
↓
Return Response JSON
```

## Kubernetes Deployment
To deploy in Kubernetes, create a Dockerfile and Kubernetes manifests (not included here).
