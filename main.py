import os
import json
from pathlib import Path
from dotenv import load_dotenv

import discord
from discord.ext import commands

# carrega .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

class Teste(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        # se precisar ler mensagens (não necessário para slash commands) habilite message_content:
        # intents.message_content = True
        super().__init__(command_prefix=".", intents=intents)
        self.db = None
        self.config = {}

    async def setup_hook(self):
        # Carrega DB
        try:
            self.Carregar_DB()
            print("Json conectado com sucesso🔥")
        except Exception as e:
            print("Erro ao carregar DB:", e)

        # Carrega dinamicamente todos os cogs em ./Comandos
        comandos_path = Path("Comandos")
        if comandos_path.exists() and comandos_path.is_dir():
            for file in comandos_path.glob("*.py"):
                # ignora arquivos privados / __init__.py
                if file.name.startswith("_"):
                    continue
                module = f"Comandos.{file.stem}"
                try:
                    await self.load_extension(module)
                    print(f"Carregado cog: {module}")
                except Exception as e:
                    print(f"Falha ao carregar {module}: {e}")
        else:
            print("Pasta 'Comandos' não encontrada. Verifique a estrutura do projeto.")

        # Sincroniza a tree de comandos (global)
        try:
            await self.tree.sync()
            print("Comandos sincronizados (tree.sync) ✅")
        except Exception as e:
            print("Falha ao sincronizar comandos da tree:", e)

    def Carregar_DB(self):
        try:
            with open("Data-Base/Data.json", "r", encoding="utf-8") as f:
                self.db = json.load(f)
        except FileNotFoundError as e:
            print(f"O Arquivo não foi encontrado😭 com o caminho:{e.filename}")
        except Exception as e:
            print("Erro ao abrir/parsear o JSON:", e)

bot = Teste()

@bot.event
async def on_ready():
    print(f"{bot.user} logado com sucesso!")
    # Exemplo: enviar mensagem a um canal específico (garanta que o bot está no servidor e o ID está correto)
    canal_id = 1455213213670182912
    canal = bot.get_channel(canal_id)
    if canal:
        try:
            await canal.send("O Monstro Chegou🔥😎")
        except Exception as e:
            print("Não consegui enviar mensagem no canal:", e)
    else:
        print(f"Canal {canal_id} não encontrado no cache. Verifique se o bot está no servidor.")

bot.run(TOKEN)