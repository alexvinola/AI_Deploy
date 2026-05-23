# AI Deploy

## Español

Microservicio de clasificación de tickets de soporte técnico construido como proyecto de aprendizaje para practicar el ciclo completo de despliegue de sistemas de IA: desde el código hasta producción con Docker, Kubernetes y CI/CD.

Forma parte de mi transición de Full Stack Developer a AI Engineer, y representa la capa de infraestructura de los agentes construidos en [AI Workflows](https://github.com/alexvinola/ai-workflows). El objetivo no es el microservicio en sí, sino aprender a empaquetar, orquestar y desplegar automáticamente un sistema basado en LLMs.

El agente usa tool use (L3 de la escalera de AI Workflows) para consultar el historial de incidencias y el estado de los servicios antes de clasificar un ticket, devolviendo severidad, área y acción recomendada en formato JSON.

### Qué se practica aquí

- **Docker** — empaquetar el agente como contenedor reproducible
- **Kubernetes** — orquestar el despliegue en un cluster local (Docker Desktop)
- **GitHub Actions** — automatizar el build y despliegue en cada push a main
- **FastAPI** — exponer el agente como microservicio HTTP
- **CI/CD para IA** — el mismo pipeline que se usa en producción para modelos y agentes

### Stack

- **FastAPI** — API HTTP que expone el agente como microservicio
- **Anthropic Claude** — LLM con tool use para clasificación inteligente
- **Docker** — empaquetado y portabilidad
- **Kubernetes** — orquestación y despliegue (cluster local con Docker Desktop)
- **GitHub Actions + act** — CI/CD automatizado en local

### Endpoints

```
GET  /health    → estado del servicio
POST /classify  → clasifica un ticket de soporte
```

### Uso rápido

```bash
curl -X POST http://localhost:8000/classify \
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
│       └── deploy.yml   ← CI/CD
└── Dockerfile
```

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
- **GitHub Actions** — automating build and deployment on every push to main
- **FastAPI** — exposing the agent as an HTTP microservice
- **CI/CD for AI** — the same pipeline used in production for models and agents

### Stack

- **FastAPI** — HTTP API exposing the agent as a microservice
- **Anthropic Claude** — LLM with tool use for intelligent classification
- **Docker** — packaging and portability
- **Kubernetes** — orchestration and deployment (local cluster with Docker Desktop)
- **GitHub Actions + act** — automated CI/CD locally

### Endpoints

```
GET  /health    → service health check
POST /classify  → classifies a support ticket
```

### Quick start

```bash
curl -X POST http://localhost:8000/classify \
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
│       └── deploy.yml   ← CI/CD
└── Dockerfile
```

### Environment variables

```
ANTHROPIC_API_KEY=sk-ant-...
```