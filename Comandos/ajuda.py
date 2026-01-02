import discord
from discord import app_commands
from discord.ext import commands

class Ajuda(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot=breakpoint

    @app_commands.command(name="Ajuda",description="Explicação dos comandos")
    async def ajuda(self,interaction:discord.Interaction):
        await interaction.response.send_message(f"{a}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Ajuda(bot))