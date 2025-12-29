import discord
from discord import app_commands
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # comando slash /ping
    @app_commands.command(name="ping", description="Responde com pong")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("pong")

# função que o "loader" do bot chamará para adicionar o cog
async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))