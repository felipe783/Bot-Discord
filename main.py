import os
import sys
import discord
import json
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# ? Commita com o TOKEN na env
load_dotenv()  # abre o .env e joga as variaveis pro ambiente
TOKEN = os.getenv("DISCORD_TOKEN") # Aqui pega o valor da variavel que eu quero

#Permissões que o Bot precisa(ele tem todas as permissões)
#intents = discord.Intents.all()
#bot = commands.Bot(".", intents=intents) # Esse ponto é como acessa o bot

class Teste(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix=".",intents=intents)
        self.db = None 
        self.config = {}
    #Carregando a tree no bot
    async def setup_hook(self):
        try:
            self.Carregar_DB()
            await self.tree.sync()
            print(f"O {bot.user} logou com sucesso🔥😎")
        except Exception as e:
            print(f"Não deu certo😭 o erro:{e}")  

    #Carregando meu "Data-Base"(Json)
    def Carregar_DB(self):
        try:
            with open("Bot-Discord/Data-Base/Data.json","r",encoding="utf-8") as f:
                self.db=json.load(f)
                print("Json conectado com sucesso🔥")
        except FileNotFoundError as e:
            print(f"O Arquivo não foi encontrado😭 com o caminho:{e.filename}")

bot = Teste()

bot.run(TOKEN)