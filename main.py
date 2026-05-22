import discord
from discord.ext import commands 
from discord.ext import tasks
from datetime import datetime
import pytz
import os
from pathlib import Path
from dotenv import load_dotenv
from loader import * 
import traceback
import asyncio
from Comandos.load_groups import load_all_groups

# carrega .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DB = load_db()
GUILD_ID = 1120406626881515655

class Teste(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True 
        intents.guilds = True
        super().__init__(command_prefix="!", intents=intents)
        self.db = None
        
    async def setup_hook(self):
        
        '''
        #Isso daqui limpa o bot inteiro
        SEU_GUILD_ID = 
        guild = discord.Object(id=SEU_GUILD_ID)
        bot.tree.clear_commands(guild=guild)
        await bot.tree.sync(guild=guild)
        await asyncio.sleep(5)
        await bot.close()
        print("Comandos foram deletados")
        '''
        
        comandos_path = Path("Comandos")
        if comandos_path.exists() and comandos_path.is_dir():
            for file in comandos_path.rglob("*.py"):
                if file.name.startswith("_"):
                    continue
                relative_path = file.relative_to(comandos_path)
                module = f"Comandos.{relative_path.with_suffix('').as_posix().replace('/', '.')}"
                try:
                    if module in self.extensions:
                        await self.reload_extension(module)
                        print(f"Recarregado cog: {module}")
                    else:
                        await self.load_extension(module)
                        print(f"Carregado cog: {module}")
                except Exception as e:
                    print(f"Falha ao carregar {module}: {e}")
        else:
            print("Pasta 'Comandos' não encontrada. Verifique a estrutura do projeto.")

        # Carrega todos os groups automaticamente
        await load_all_groups(self)

        # Tenta sincronizar a Tree
        try:
            await self.tree.sync()
            print("Comandos sincronizados (tree.sync) ✅")
        except Exception as e:
            print("Falha ao sincronizar comandos da tree:", e)
                        
bot = Teste()

#vai checar a cada 1 minuto
@tasks.loop(minutes=1)
async def Historias_diaria():
    #print("Iniciou os DEF Historias Diarias")
    await bot.wait_until_ready()
    
    canal_historia = bot.get_channel(DB["ID_Historia"][0]) #Historias
    agora=datetime.now(pytz.timezone("America/Sao_Paulo"))

    db = load_db()
    if db is None:
        db = {}
    # garante que bot.db exista e aponte para o dict carregado
    bot.db = db

    try:
        if agora.hour==12 and agora.minute==00: #no meio dia vai fazer oq ta dentro do if
            historia_list = db.get("historia", []) #Vai tentar pegar a lista historia,ce ela não existir retorna uma lsita vazia

            if historia_list:  #Se o "historia_list" não ter historia ele não roda
                texto = ", ".join(str(x) for x in historia_list if x is not None and x !="") 
                await canal_historia.send(f"\nHistória antiga:{texto}\nHistorias zeradas🔥\n||@everyone||")
                #Zerar o json
                bot.db["historia"] = []
                save_db(bot.db)
            else:
                await canal_historia.send("Sem histórias pra zerar.😭")
    except Exception as e:  
        print(f"Deu erro pra zerar o Json \n**{e}**")

@bot.event 
async def on_ready():
    Historias_diaria.start()
    canal_id2 = 1455213213670182912 #Inicio 
    canal_inicio = bot.get_channel(canal_id2)
    print(f"O {bot.user} logou")
    await canal_inicio.send("O Monstro Chegou🔥😎") #Mandar mensagem de inicio 
    
bot.run(TOKEN)