# Sobre o Arquivo

O `Dockerfile` empacota o bot para rodar em servidor (o README original cita um Ubuntu Server 24.04).
# Funcionalidade

````dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
````

````bash
docker build -t bot-discord .
docker run -d --name bot-discord --env-file .env --restart unless-stopped bot-discord
docker logs -f bot-discord
````

- O `requirements.txt` é copiado antes do código, então mudar só o `.py` não reinstala as dependências.
- O bot só faz conexões de saída (gateway e API do Discord, Modrinth): **nenhuma porta** precisa ser publicada.

> [!warning] Segurança e dados
> - **Não há `.dockerignore`**: o `COPY . .` leva o `.env` (com o token), o `.git` e o `__pycache__` para a imagem. Crie um `.dockerignore`; o comando acima já passa o token por `--env-file .env`, então ele não precisa estar na imagem.
> - `Json/Data.json` fica dentro do container: sem volume (`-v ./Json:/app/Json`), a história se perde ao recriar.
> - Não há `docker-compose.yml`, *healthcheck* nem script de deploy no repositório.
