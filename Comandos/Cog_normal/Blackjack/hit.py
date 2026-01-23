import discord
from discord import app_commands
from discord.ext import commands
import Estados.estados_Blackjack as estados_Blackjack
from datetime import timedelta

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
        user_id = interaction.user.id

        if user_id not in estados_Blackjack.jogos: #Garante que ele ta em um Jogo
            await interaction.response.send_message("Tu nem começou um jogo😭",ephemeral=True)
            return

        jogo = estados_Blackjack.jogos[user_id]
        jogo["doubledown"] = False #Ele não pode dar DoubleDown
        duracao = jogo.get("duracao")

        carta = jogo["baralho"].pop()
        jogo["mao"].append(carta)
        cartaD = jogo["baralho"].pop()
        jogo["dealer"].append(cartaD)

        pontos = calcular_pontos(jogo["mao"])
        dealerP = calcular_pontos(jogo["dealer"])

        if dealerP < 17: #Dealer é obrigado a comprar quando é menor que 17
            dealerP = calcular_pontos(jogo["dealer"])
        else:
            if pontos > 21:
                await interaction.response.send_message(
                    f"💥 Estourou!\nCartas: {formatar_mao(jogo['mao'])}\n"
                    f"Pontos: **{pontos}**"
                )
                await interaction.user.timeout(timedelta(minutes=duracao), reason="Muito ruim no Blackjack")
                del estados_Blackjack.jogos[user_id]
                return
            if dealerP > 21: #O dealer tem uma pequena vantagem(A casa sempre ganha😎🔥)
                await interaction.response.send_message(
                    f"O Dealer estourou💥\n"
                    f"A mesa ganhou,você teve sorte dessa vez...🔥"
                )
                del estados_Blackjack.jogos[user_id]
            else:
                await interaction.response.send_message(
                    f"🃏 Nova carta:{formatar_mao(jogo['mao'])}\n"
                    f"📊 Pontos: **{pontos}**"
                )
        
async def setup(bot):
    await bot.add_cog(hit(bot))