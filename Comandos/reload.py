from pathlib import Path
import discord
from discord import app_commands
from discord.ext import commands

class ReloadCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.default_permissions(administrator=True)
    @app_commands.command(name="reload", description="Da reload nos comandos")
    async def reloadcog(self, interaction: discord.Interaction):
        print("sda")

async def setup(bot: commands.Bot):
    await bot.add_cog(ReloadCog(bot))