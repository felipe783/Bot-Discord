import discord
from discord import app_commands
from discord.ext import commands
import random
import Estados.estados_Blackjack as estados_Blackjack

class double_down(commands.Cog):
    def __init__(self,bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="double_down",description="Dobre a aposta,e compre mais uma carta!")
    async def double_down(self, interaction:discord.Interaction):

        user_id = interaction.user.id
        jogo = estados_Blackjack.jogos[user_id]

        if user_id not in estados_Blackjack.jogos: #Garante que ele ta em um Jogo
            await interaction.response.send_message("Tu nem começou um jogo😭",ephemeral=True)
            return
        if not jogo["doubledown"]:
            await interaction.response.send_message(
                "Double só pode antes de dar HIT 🤓🔥",ephemeral=True
            )
            return

async def setup(bot : commands.Bot):
    await bot.add_cog(double_down(bot))