from discord import app_commands
from discord.ext import commands

class blackjack(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

blackjack_group = app_commands.Group(
    name="blackjack",
    description="Comandos do Blackjack"
)

async def setup(bot: commands.Bot):
    await bot.add_cog(blackjack(bot))