import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

#Commita com o TOKEN na env
load_dotenv()  # carrega o .env
TOKEN = os.getenv("DISCORD_TOKEN")

#Permissões que o Bot precisa(ele tem todas as permissões)
intents = discord.Intents.all()
bot = commands.Bot(".", intents=intents)#Esse ponto é como acessa o bot

@bot.event
async def on_ready():
    print("O Teste Chegou😎🔥")

bot.run(TOKEN)