import discord
from discord import app_commands
from discord.ext import commands

class Historia(commands.cog):
    def __init__(self,bot:commands.bot):
        self.bot=bot


async def setup(bot: commands.Bot):
    await bot.add_cog(Historia(bot))