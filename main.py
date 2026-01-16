import discord
from discord.ext import commands 
from discord.ext import tasks
from datetime import datetime
import pytz
import os
from pathlib import Path
from dotenv import load_dotenv
from loader import * 

# carrega .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

class Teste(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True 
        super().__init__(command_prefix="!", intents=intents)
        self.db = None
        
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

#vai checar a cada 1 minuto
@tasks.loop(minutes=1)
async def Historias_diaria():
    #print("Iniciou os DEF Historias Diarias")
    await bot.wait_until_ready()
    canal_erros = bot.get_channel(1457546195655332193) #Erros
    canal_historia = bot.get_channel(1456028679967867156) #Historias
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
        await canal_erros.send(f"Deu erro pra zerar o Json \n**{e}**")

@bot.event 
async def on_ready():
    #print("Iniciou o ON_READY")
    Historias_diaria.start()
    #Criar um canal so pra ADM com os bagulho dos codigos
    try:
        Guild_Id = 1120406626881515655
        guild = bot.get_guild(Guild_Id)
        cargo = guild.get_role(1120416496049463366)

        if(discord.utils.get(guild.text_channels, name="comandos-bot-teste")): #achou
            canal=discord.utils.get(guild.text_channels, name="comandos-bot-teste")
            print(f"Canal achado {canal.mention}")
        else: #Não achou
            overwrites={ #Vc literalmente sobre escreve oq o canal vai fazer(Permissões,quem ve,etc.....)
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                cargo: discord.PermissionOverwrite(
                    view_channel = True,
                    send_messages = True,
                    read_message_history = True
                )
            }
            canal = await guild.create_text_channel(
                name="comandos-bot-teste",
                overwrites = overwrites
            )
            print(f"canal criado {canal.mention}")
    except Exception as e:
        print(f"Deu erro pra achar o canal:{e}")
    print("Reload ta on✅")
    canal_id2 = 1455213213670182912 #Inicio 
    canal_inicio = bot.get_channel(canal_id2)
    #Carregando o JSON no "bot.db"
    '''
    try: 
        bot.db = load_db() 
        if not isinstance (bot.db,dict):
            bot.db("historia:",[])
        Historias_diaria.start()
    except Exception as e:
        await canal_erros.send(f"Deu erro pra Zerar o Json {e}") 
    '''
    print(f"O {bot.user} logou")
    await canal_inicio.send("O Monstro Chegou🔥😎") #Mandar mensagem de inicio 
    
bot.run(TOKEN)