from typing import Optional
from loader import * 
import discord
from discord import app_commands
from discord.ext import commands

class historia(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="historia", description="Crie uma história!")
    @app_commands.describe(texto="Escreva uma frase e eu irei juntar com as outras ja escritas😎✍️")
    async def historia(self, interaction: discord.Interaction, texto: Optional[str] = None):
        texto = texto or ""
        db = load_db() 

        db["historia"].append(texto) #ele procura no db a variavel texto
        save_db(db)
        await interaction.response.send_message(f"A historia ficou assim:{",".join(db["historia"])}")

async def setup(bot: commands.Bot):
    await bot.add_cog(historia(bot))