import discord
from discord import app_commands
from discord.ext import commands
import estados

def formatar_mao(mao):
    return " ".join(f"{c['nome']}{c['naipe']}" for c in mao)

def calcular_pontos(mao): 
    total = sum(c["valor"] for c in mao)
    ases = sum(1 for c in mao if c["nome"] == "Ás")

    while total > 21 and ases:
        total -= 10
        ases -= 1

    return total

class hit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hit", description="Comprar mais uma carta")
    async def hit(self, interaction: discord.Interaction):
        duracao = estados.duracao.get(user_id)
        user_id = interaction.user.id

        if user_id not in estados.jogos:
            await interaction.response.send_message("Tu nem começou um jogo😭",ephemeral=True)
            return

        jogo = estados.jogos[user_id]

        carta = jogo["baralho"].pop()
        jogo["mao"].append(carta)

        pontos = calcular_pontos(jogo["mao"])

        if pontos > 21:
            del estados.jogos[user_id]
            await interaction.response.send_message(
                f"💥 Estourou!\nCartas: {formatar_mao(jogo["mao"])}\n"
                f"Pontos: **{pontos}**"
            )
            await interaction.user.timeout(duracao, reason="Muito ruim no blackjack")
        else:
            await interaction.response.send_message(
                f"🃏 Nova carta:{formatar_mao(jogo["mao"])}\n"
                f"📊 Pontos: **{pontos}**"
            )

async def setup(bot):
    await bot.add_cog(hit(bot))