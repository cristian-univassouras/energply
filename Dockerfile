FROM python:3.10-slim

WORKDIR /app

# Copia o arquivo requirements.txt (onde você vai colocar aquela lista) e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código do seu projeto para dentro do contêiner
COPY . .

# Comando para rodar o servidor FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]