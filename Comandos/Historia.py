from typing import Optional
from loader import * 
import json
import discord
from discord import app_commands
from discord.ext import commands

class Historia(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # comando slash /historia
    @app_commands.command(name="historia", description="Crie uma história!")
    @app_commands.describe(texto="Escreva uma frase e eu irei juntar com as outras ja escritas😎✍️")
    async def historia(self, interaction: discord.Interaction, texto: Optional[str] = None):
        texto = texto or ""

        self.bot.db["historia"].append(texto)
        save_db(self.bot.db)
        await interaction.response.send_message(f"A historia ficou assim:{",".join(self.bot.db["historia"])}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Historia(bot))