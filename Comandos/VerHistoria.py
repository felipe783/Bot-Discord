from typing import Optional
from loader import * 
import discord
from discord import app_commands
from discord.ext import commands

class VerHistoria(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ver_historia", description="Veja a história!")
    async def historia(self, interaction: discord.Interaction):
        db = load_db() 
        historia = ",".join(db["historia"])
        await interaction.response.send_message(f"A historia ficou assim:{historia}",ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(VerHistoria(bot))