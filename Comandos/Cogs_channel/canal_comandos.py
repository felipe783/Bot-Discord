import discord
from discord.ext import commands
from discord.utils import get

GUILD_ID = 1120406626881515655
ROLE_ID = 1120416496049463366
CHANNEL_NAME = "comandos-bot-teste"

class ChannelCreator(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._done = False  # garante execução única

    @commands.Cog.listener()
    async def on_ready(self):
        # executa apenas uma vez
        if self._done:
            return
        self._done = True

        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(GUILD_ID)
        cargo = guild.get_role(ROLE_ID)
        existing = discord.utils.get(guild.text_channels, name=CHANNEL_NAME)
        if existing:
            print(f"Canal já existe: {existing.mention}")
            return
        
        overwrites={
            guild.default_role: discord.PermissionOverwrite(view_channel= False)
        }
        if cargo:
            overwrites[cargo] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            )

        try:
            canal = await guild.create_text_channel(
                name=CHANNEL_NAME,
                overwrites=overwrites,
                reason="Canal criado pelo bot de teste"
            )
            print(f"Canal criado: {canal.mention}")
        except Exception as e:
            print(f"Erro ao criar o canal: {e}")   

async def setup(bot: commands.Bot):
    await bot.add_cog(ChannelCreator(bot))