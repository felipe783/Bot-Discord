from typing import Optional
import json
import discord
from discord import app_commands
from discord.ext import commands

class Historia(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # comando slash /historia
    @app_commands.command(name="historia", description="Crie uma história!")
    @app_commands.describe(texto="Escreva uma frase e eu irei juntar as outras ja escritas")
    async def historia(self, interaction: discord.Interaction, texto: Optional[str] = None):
        texto = texto or ""
        dados={
            "Historia": texto
        }
        with open("dados.json", "w", encondig="utf-8") as arquivo:
            json.dump(dados, arquivo,indent=4, ensure_ascii=False)
        await interaction.response.send_message(texto)

async def setup(bot: commands.Bot):
    await bot.add_cog(Historia(bot))