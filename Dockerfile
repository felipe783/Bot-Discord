# Usa imagem leve do Python
FROM python:3.12-slim

# Cria pasta do app no container
WORKDIR /app

# Copia requirements primeiro (pra aproveitar cache do Docker)
COPY requirements.txt .

# Instala as libs do pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do bot pro container
COPY . .

# Expõe porta se precisar (opcional)
# EXPOSE 8080

# Comando pra rodar o bot
CMD ["python", "main.py"]
