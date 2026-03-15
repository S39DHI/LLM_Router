# LLM Router Service

## Project Description
A FastAPI service that receives a user question, classifies its complexity, routes the query to the appropriate LLM model, and returns the answer along with metadata about the routing decision.

The system is designed to balance **cost and performance** by dynamically selecting the most suitable model based on query complexity.

Tested With:
- Python 3.11
- Docker
- Minikube
- Kubernetes

<p align="center">
  <img src="images/1.png" width="750">
</p>

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Running Locally](#running-locally)
3. [Running with Docker](#running-with-docker)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Routing Logic](#routing-logic)
6. [Example Request and Response](#example-request-and-response)

---

# System Architecture

The service is implemented using multiple modular components. Each component handles a specific responsibility in the routing pipeline.

## System Flow

```
User Question
↓
FastAPI Endpoint (/ask)
↓
Query Classifier
↓
Model Router
↓
OpenAI API
↓
Return Response JSON
```

## Project Structure

```
app/
 ├── main.py
 ├── classifier.py
 ├── router.py
 ├── llm_client.py
 └── schemas.py
```

## FastAPI Entry Point (`main.py`)

This file contains the main API endpoint.

```
POST /ask
```

Responsibilities:
- Receives the user question
- Sends the question to the classifier
- Uses the router to select the appropriate model
- Calls the LLM client
- Returns the final response

---

## Query Classifier (`classifier.py`)

The classifier determines the complexity of the question using **custom heuristics designed in this project**.

Instead of using a machine learning model, a rule-based heuristic approach is implemented that evaluates multiple signals from the question.

The classifier analyzes:

1. **Query length**
2. **Keyword signals**
3. **Multi-part question structure**

Keywords are grouped into different categories:

### Complex Keywords
Example words indicating technical complexity:

```
architecture
distributed
scalable
system
pipeline
microservices
kubernetes
optimization
performance
algorithm
```

### Reasoning Words

```
why
how
explain
analyze
evaluate
```

### Comparison Words

```
compare
difference
vs
versus
```

### Task Words

```
design
build
implement
create
develop
```

### Heuristic Scoring

Each signal increases the classification score.

Example signals:
- Long query
- Multiple keywords detected
- Multi-part questions

Classification result:

```
Score ≤ 1  → Simple
Score ≤ 3  → Medium
Score > 3  → Complex
```

This approach allows building a lightweight classifier without training data.

---

# Running Locally

## 1 Clone Repository

```bash
git clone https://github.com/S39DHI/LLM_Router.git
cd LLM_Router
```

## 2 Create Environment File

```bash
cp .env.example .env
```

Add your API key inside `.env`

```
OPENAI_API_KEY=your_openai_api_key
```

## 3 Install Dependencies

```bash
pip install -r requirements.txt
```

## 4 Run API

```bash
uvicorn app.main:app --reload
```

## 5 Access API

```
http://127.0.0.1:8000/docs
```

FastAPI automatically provides interactive Swagger documentation.

---

# Running with Docker

The project includes a Dockerfile to containerize the FastAPI application.

## Important Note About `.dockerignore`

In production systems, sensitive files such as `.env` should **not be included in the Docker image**.

Therefore `.env` is typically added to `.dockerignore`.

Example `.dockerignore` entry:

```
.env
```

This prevents the API key from being copied into the image.

However, for this assignment the `.env` file may still exist locally for testing.

---

## 1 Build Docker Image

```bash
docker build -t llm-router .
```

Verify image:

```bash
docker images
```

---

## 2 Run Container

Instead of copying the `.env` file into the image, environment variables are passed during runtime.

```bash
docker run -p 8000:8000 --env-file .env llm-router
```

This securely provides the OpenAI API key to the container.

---

## 3 Access API

```
http://localhost:8000/docs
```

---

# Kubernetes Deployment

The project can also be deployed using Kubernetes.

For **local development and testing**, Minikube is used.

In real production environments, Kubernetes clusters can be deployed on cloud providers such as:

- AWS (EKS)
- Google Cloud (GKE)
- Azure (AKS)

---

## 1 Start Minikube

```bash
minikube start
```

---

## 2 Configure Docker for Minikube

This allows Docker images to be built directly inside the Minikube cluster.

```bash
eval $(minikube docker-env)
```

---

## 3 Build Docker Image

```bash
docker build -t llm-router .
```

Verify:

```bash
docker images
```

---

## 4 Create Kubernetes Secret

Store the OpenAI API key securely.

```bash
kubectl create secret generic openai-secret \
  --from-literal=api-key=YOUR_OPENAI_API_KEY
```

Verify:

```bash
kubectl get secrets
```

---

## 5 Deploy Application

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

---

## 6 Check Pods

```bash
kubectl get pods
```

Expected:

```
llm-router-xxxxx   1/1   Running
```

---

## 7 Check Service

```bash
kubectl get svc
```

Example:

```
llm-router-service   NodePort   10.xx.xx.xx   80:31244/TCP
```

---

## 8 Access API

```bash
minikube service llm-router-service
```

Example URL

```
http://192.168.39.103:31244/docs
```

This opens the FastAPI Swagger UI.

<p align="center">
  <img src="images/2.png" width="750">
</p>

---

# Example Request and Response

## Example Request

POST `/ask`

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

---

## Example Response

```json
{
 "complexity": "simple",
 "model_used": "gpt-4o-mini",
 "answer": "A Kubernetes Pod is the smallest deployable unit..."
}
```

---

# Routing Logic

The routing system consists of two main stages:

1. **Complexity Classification**
2. **Model Routing**

---

## Complexity Classification

The classifier evaluates multiple signals from the query.

Signals include:

- Query length
- Reasoning words
- Comparison words
- Task words
- Technical keywords
- Multi-part question structure

Each signal increases the heuristic score.

Classification levels:

```
Score ≤ 1  → Simple
Score ≤ 3  → Medium
Score > 3  → Complex
```

---

## Model Routing

After classification, the router selects the LLM model dynamically.

Current configuration:

```
Simple   → gpt-4o-mini
Medium   → gpt-4.1
Complex  → gpt-4.1
```

The router uses a **mapping-based design**, making it easy to extend.

Example future routing:

```
Simple → cheaper fast model
Medium → balanced model
Complex → high reasoning model
```

This dynamic routing strategy helps reduce cost while maintaining high-quality responses.
