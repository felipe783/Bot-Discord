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

    #Carregando meu "Data-Base"(Json)
    def carregar_DB(self):
        try:
            with open("Data-Base/Data.json","r",enconding="utf-8") as f:
                self.db=json.load(f)
                print("Json conectado com sucesso🔥")
        except IOError:
            print("Arquivo não encontrado😭")
    
    #Carregando a tree no bot
    async def setup_hook(self):
        await self.tree.sync()
    
bot = Teste()

@bot.event
async def on_ready():
    print(f"O {bot.user} logou com sucesso🔥😎")
    try:
        await bot.tree.sync()
        print("Logado🔥😎")
    except Exception as e:
        print(f"Não deu certo😭 o erro:{e}")    
        
bot.run(TOKEN)