import discord
from discord.ext import commands
from discord.utils import get
from loader import * 

GUILD_ID = 1120406626881515655
NOME = "historias"
DB = load_db()

class CanalHistoria(commands.Cog):
    def __init__(self , bot:commands.Bot):
        self.bot = bot
        self._done = False

    @commands.Cog.listener()
    async def on_ready(self):
        if self._done:
            return
        self._done = True

        await self.bot.wait_until_ready()

        guild = self.bot.get_guild(GUILD_ID)
        existing = discord.utils.get(guild.text_channels, name = NOME)
        if existing:
            print(f"Canal já esxiste:{existing.mention}")
            return
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(send_messages = False),
            guild.me: discord.PermissionOverwrite(send_messages = True)
        }
        
        try:
            canal = await guild.create_text_channel(
                name=NOME,
                overwrites = overwrites,
                reason = "Canal cria pras historias"
            )

            CANAL_ID = canal.id
            if  "ID_Historia" not in DB:
                DB["ID_Historia"]=[]

            DB["ID_Historia"].append(CANAL_ID)
            save_db(DB)
            
            print(f"Canal historias criado: {canal.mention}")
        except Exception as e:
            print(f"Erro ao criar canal historias: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(CanalHistoria(bot))   
