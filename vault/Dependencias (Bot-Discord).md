
[**discord.py**](https://discordpy.readthedocs.io/)
Cliente do gateway e da API do Discord: `commands.Bot`, cogs, `app_commands` (slash commands e groups) e `tasks.loop`.
````
pip install discord.py
````

[**requests**](https://requests.readthedocs.io/)
Chamada HTTP à API do Modrinth no `/busca_mod`.
````
pip install requests
````

[**pytz**](https://pypi.org/project/pytz/)
Fuso `America/Sao_Paulo` da tarefa diária.
````
pip install pytz
````

[**dotenv**](https://pypi.org/project/dotenv/)
Pacote que instala o `python-dotenv` (`load_dotenv()` lê o `.env`).
````
pip install dotenv
````

**nest_asyncio**
Listado no `requirements.txt`, mas **não é importado** em nenhum arquivo.


Instalar tudo de uma vez:
````
pip install -r requirements.txt
````

> Nenhuma versão é fixada. O `Dockerfile` usa `python:3.12-slim`.
