## Kubernetes Deployment

### 1. Build Docker image

```bash
docker build -t llm-router .
```

### 2. Create Kubernetes Secret

```bash
kubectl create secret generic openai-secret \
  --from-literal=api-key=YOUR_OPENAI_API_KEY
```

### 3. Deploy to Kubernetes

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### 4. Check running pods

```bash
kubectl get pods
```

### 5. Check service

```bash
kubectl get svc
```

### 6. Access API

Visit:
```
http://<node-ip>:<node-port>/docs
```

The service is exposed via NodePort. Use the output from `kubectl get svc` to find the port.
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

Using curl:
```bash
curl -X POST "http://127.0.0.1:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "Explain Kubernetes pods"}'
```

JSON body:
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
