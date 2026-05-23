# AI Deploy

## Español

Microservicio de clasificación de tickets de soporte técnico construido como proyecto de aprendizaje para practicar el ciclo completo de despliegue de sistemas de IA: desde el código hasta producción con Docker, Kubernetes y CI/CD.

Forma parte de mi transición de Full Stack Developer a AI Engineer, y representa la capa de infraestructura de los agentes construidos en [AI Workflows](https://github.com/alexvinola/ai-workflows). El objetivo no es el microservicio en sí, sino aprender a empaquetar, orquestar y desplegar automáticamente un sistema basado en LLMs.

El agente usa tool use (L3 de la escalera de AI Workflows) para consultar el historial de incidencias y el estado de los servicios antes de clasificar un ticket, devolviendo severidad, área y acción recomendada en formato JSON.

### Qué se practica aquí

- **Docker** — empaquetar el agente como contenedor reproducible
- **Kubernetes** — orquestar el despliegue en un cluster local (Docker Desktop)
- **GitHub Actions** — pipeline de CI/CD con ejecución manual (`workflow_dispatch`)
- **FastAPI** — exponer el agente como microservicio HTTP

### Stack

- **FastAPI** — API HTTP que expone el agente como microservicio
- **Anthropic Claude** — LLM con tool use para clasificación inteligente
- **Docker** — empaquetado y portabilidad
- **Kubernetes** — orquestación y despliegue (cluster local con Docker Desktop)
- **GitHub Actions** — pipeline CI/CD

### Endpoints

```
GET  /health    → estado del servicio
POST /classify  → clasifica un ticket de soporte
```

### Uso rápido

```bash
curl -X POST http://localhost:8080/classify \
  -H "Content-Type: application/json" \
  -d '{"ticket": "Auth service returning 500 errors since 09:15 UTC"}'
```

### Estructura

```
ai-deploy/
├── app/
│   ├── main.py          ← API FastAPI
│   └── classifier.py    ← agente con tool use
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── .github/
│   └── workflows/
│       └── deploy.yml   ← CI/CD manual
└── Dockerfile
```

### Despliegue local

```bash
# 1. Construir la imagen
docker build -t ticket-classifier:latest .

# 2. Crear el secret con la API key
kubectl create secret generic anthropic-secret \
  --from-literal=api-key=sk-ant-...

# 3. Desplegar en Kubernetes
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# 4. Exponer el servicio
kubectl port-forward service/ticket-classifier-service 8080:80
```

### Sobre el pipeline de CI/CD

El workflow de GitHub Actions (`workflow_dispatch`) se ejecuta manualmente desde GitHub → Actions → Run workflow. Incluye los siguientes pasos:

1. ✅ Checkout del código
2. ✅ Setup Python 3.11
3. ✅ Instalación de dependencias con uv
4. ✅ Tests de importación
5. ✅ Build de la imagen Docker
6. ⚠️ Deploy a Kubernetes — **falla en GitHub Actions** porque el runner de GitHub no tiene acceso al cluster de Kubernetes local. En un entorno real con un self-hosted runner instalado en el servidor, este paso funcionaría correctamente. El paso está marcado con `continue-on-error: true` para que el pipeline no se detenga.

### Variables de entorno

```
ANTHROPIC_API_KEY=sk-ant-...
```

---

## English

Support ticket classification microservice built as a learning project to practice the full deployment cycle of AI systems: from code to production with Docker, Kubernetes and CI/CD.

Part of my transition from Full Stack Developer to AI Engineer, representing the infrastructure layer of the agents built in [AI Workflows](https://github.com/alexvinola/ai-workflows). The goal is not the microservice itself, but learning how to package, orchestrate and automatically deploy an LLM-based system.

The agent uses tool use (L3 of the AI Workflows ladder) to query incident history and service status before classifying a ticket, returning severity, area and recommended action in JSON format.

### What is practiced here

- **Docker** — packaging the agent as a reproducible container
- **Kubernetes** — orchestrating the deployment on a local cluster (Docker Desktop)
- **GitHub Actions** — CI/CD pipeline with manual execution (`workflow_dispatch`)
- **FastAPI** — exposing the agent as an HTTP microservice

### Stack

- **FastAPI** — HTTP API exposing the agent as a microservice
- **Anthropic Claude** — LLM with tool use for intelligent classification
- **Docker** — packaging and portability
- **Kubernetes** — orchestration and deployment (local cluster with Docker Desktop)
- **GitHub Actions** — CI/CD pipeline

### Endpoints

```
GET  /health    → service health check
POST /classify  → classifies a support ticket
```

### Quick start

```bash
curl -X POST http://localhost:8080/classify \
  -H "Content-Type: application/json" \
  -d '{"ticket": "Auth service returning 500 errors since 09:15 UTC"}'
```

### Structure

```
ai-deploy/
├── app/
│   ├── main.py          ← FastAPI API
│   └── classifier.py    ← agent with tool use
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── .github/
│   └── workflows/
│       └── deploy.yml   ← manual CI/CD
└── Dockerfile
```

### Local deployment

```bash
# 1. Build the image
docker build -t ticket-classifier:latest .

# 2. Create the secret with the API key
kubectl create secret generic anthropic-secret \
  --from-literal=api-key=sk-ant-...

# 3. Deploy to Kubernetes
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# 4. Expose the service
kubectl port-forward service/ticket-classifier-service 8080:80
```

### About the CI/CD pipeline

The GitHub Actions workflow (`workflow_dispatch`) runs manually from GitHub → Actions → Run workflow. It includes the following steps:

1. ✅ Code checkout
2. ✅ Python 3.11 setup
3. ✅ Dependency installation with uv
4. ✅ Import tests
5. ✅ Docker image build
6. ⚠️ Kubernetes deploy — **fails in GitHub Actions** because the GitHub runner does not have access to the local Kubernetes cluster. In a real environment with a self-hosted runner installed on the server, this step would work correctly. The step is marked with `continue-on-error: true` so the pipeline does not stop.

### Environment variables

```
ANTHROPIC_API_KEY=sk-ant-...
```