import os
import json
import discord
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional
from loader import * 
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta

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

bot = Teste()

@bot.event
async def on_ready():
    #Falar no terminal ce conseguiu carregar o Json 
    try:
        bot.db = load_db()
        if not isinstance(bot.db, dict):
            bot.db = {"historia": [], "reset": datetime.now().strftime("%Y-%m-%d")}
        if "historia" not in bot.db:
            bot.db["historia"] = []
        if "reset" not in bot.db:
            bot.db["reset"] = datetime.now().strftime("%Y-%m-%d")
        print("JSON Carregado 🔥😎")
    except Exception as e:
        print(f"Erro no load do JSON {e}")   
        bot.db = {"historia": [], "reset": datetime.now().strftime("%Y-%m-%d")} 
    print(f"{bot.user} logado com sucesso!")
    
    #Falar que iniciou e as historias
    canal_id = 1456028679967867156 #Historias
    canal_id2 = 1455213213670182912 #Inicio
    
    canal_historia = bot.get_channel(canal_id)
    canal_inicio = bot.get_channel(canal_id2)

    try:
        reset_str = bot.db.get("reset", "")
        try:
            last_reset_date = datetime.strptime(reset_str, "%Y-%m-%d").date()
        except Exception:
            # se o formato estiver inválido, considera que não precisa resetar agora
            last_reset_date = datetime.now().date()

        hoje = datetime.now().date()
        dias_passados = (hoje - last_reset_date).days

        if dias_passados >= 1:
            # Há mais de um dia desde o último reset -> zera a historia
            historia_list = bot.db.get("historia", [])
            if historia_list:
                # monta texto filtrando valores nulos/vazios e convertendo para str
                texto = ", ".join(str(x) for x in historia_list if x is not None and x != "")

                # envia a história antiga e confirma o reset
                if canal_historia:
                    await canal_historia.send(f"\nHistória antiga: {texto}\nHistórias zeradas 🔥😎\n||@everyone||")
                # zera e atualiza data de reset
                bot.db["historia"] = []
                bot.db["reset"] = hoje.strftime("%Y-%m-%d")
                save_db(bot.db)
                print("Histórias zeradas e Data atualizada no JSON.")
            else:
                # não havia história para zerar
                if canal_historia:
                    await canal_historia.send("Sem histórias pra zerar.😭")
                # atualiza a data de reset mesmo sem história (para não reenviar todo inicio)
                bot.db["reset"] = hoje.strftime("%Y-%m-%d")
                save_db(bot.db)
                print("Nenhuma história para zerar. Data de reset atualizada no JSON.")
        else:
            # Menos de um dia desde o último reset — apenas envia a mensagem de inicialização como antes
            historia_list = bot.db.get("historia", [])
            if historia_list:
                texto=', '.join(str(x) for x in historia_list if x is not None and x != "")
            else:
                texto = "Sem nenhuma historia"
            if canal_historia:
                await canal_historia.send(f"A Historia do dia {last_reset_date}: {texto}\n||@everyone||")
            if canal_inicio:
                await canal_inicio.send("O Monstro Chegou🔥😎")
    except Exception as e:
        print("Erro ao processar lógica de reset/ envio de mensagens:", e)

bot.run(TOKEN)