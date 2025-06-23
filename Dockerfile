# Imagem base mínima
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files & Ensure Python output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Define diretório de trabalho dentro do container
WORKDIR /app

# Agora copia o resto dos arquivos
COPY . .

# Instala dependências
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --no-cache-dir -e . \
    && apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*


# Expõe porta da API
EXPOSE 8000

# Comando para rodar o servidor FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

