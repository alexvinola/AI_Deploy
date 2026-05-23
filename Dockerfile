FROM python:3.11-slim

WORKDIR /app

# Instalar uv
RUN pip install uv

# Copiar dependencias
COPY pyproject.toml .
COPY uv.lock .

# Instalar dependencias
RUN uv sync --frozen --no-dev

# Copiar código
COPY app/ ./app/

# Exponer puerto
EXPOSE 8000

# Arrancar
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]