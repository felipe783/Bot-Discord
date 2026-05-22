from discord import app_commands

blackjack_group = app_commands.Group(
    name="blackjack",
    description="Comandos do Blackjack"
)

async def setup(bot):
    pass