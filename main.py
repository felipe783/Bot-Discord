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
        super().__init__(command_prefix=".", intents=intents)
        self.db = None
        self.config = {}

    async def setup_hook(self):
        
        #Carregar os Codigos
        comandos_path = Path("Comandos")
        if comandos_path.exists() and comandos_path.is_dir():
            for file in comandos_path.glob("*.py"):
                
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

        #Tenta sincronizar a Tree
        try:
            await self.tree.sync()
            print("Comandos sincronizados (tree.sync) ✅")
        except Exception as e:
            print("Falha ao sincronizar comandos da tree:", e)

bot = Teste()

@bot.event
async def on_ready():
    
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
    
    
    canal_id = 1456028679967867156 #Historias
    canal_id2 = 1455213213670182912 #Inicio
    
    canal_historia = bot.get_channel(canal_id)
    canal_inicio = bot.get_channel(canal_id2)

    try:
        reset_str = bot.db.get("reset", "")
        try:
            last_reset_date = datetime.strptime(reset_str, "%Y-%m-%d").date()
        except Exception:
            
            last_reset_date = datetime.now().date()

        hoje = datetime.now().date()
        dias_passados = (hoje - last_reset_date).days
        #Verificar ce passou 1 dia 
        if dias_passados >= 1:
            
            historia_list = bot.db.get("historia", [])
            if historia_list:
                texto = ", ".join(str(x) for x in historia_list if x is not None and x != "")

                if canal_historia:
                    await canal_historia.send(f"\nHistória antiga: {texto}\nHistórias zeradas 🔥😎\n||@everyone||")

                #Zerar o json
                bot.db["historia"] = []
                bot.db["reset"] = hoje.strftime("%Y-%m-%d")
                save_db(bot.db)
                print("Histórias zeradas e Data atualizada no JSON.")
            else:
                if canal_historia:
                    await canal_historia.send("Sem histórias pra zerar.😭")
                #Atualiza a data do ultimo reset
                bot.db["reset"] = hoje.strftime("%Y-%m-%d")
                save_db(bot.db)
                print("Nenhuma história para zerar. Data de reset atualizada no JSON.")
        #Aqui não zerou as historias
        else:
            historia_list = bot.db.get("historia", []) #Tenta pegar a chave 'historia' dentro de bot.db,se ela não existir ele retorna uma lista vazia,vulgo "[]" 
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