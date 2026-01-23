import discord
from discord import app_commands
from discord.ext import commands
import random
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

def criar_baralho():
    naipes = ["♠", "♥", "♦", "♣"]
    valores = {
        "Ás": 11,
        "2": 2, "3": 3, "4": 4, "5": 5,
        "6": 6, "7": 7, "8": 8, "9": 9,
        "10": 10, "J": 10, "Q": 10, "K": 10
    }
    baralho = []
    for naipe in naipes:
          for nome, valor in valores.items():
            baralho.append({
                "nome": nome,
                "naipe": naipe,
                "valor": valor
                })
    random.shuffle(baralho) #Ele ta aleatorizando e colocando no baralho a sequência
    return baralho
    
class blackjack(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="blackjack",description="Começe a jogar blackjack!")
    async def blackjack(self, interaction:discord.Interaction,minutos : int):
        duracao = minutos
        user_id = interaction.user.id
        
        estados.duracao[user_id]=duracao

        baralho = criar_baralho()
        mao = [baralho.pop(),baralho.pop()]
        dealer = [baralho.pop(),baralho.pop()]

        estados.jogos[user_id]= { #Cada user tem uma "mesa de blackjack"
            "baralho" : baralho,
            "mao": mao,
            "dealer" : dealer,
        }

        pontos = calcular_pontos(mao)

        await interaction.response.send_message(
            f"🃏 Suas cartas:{formatar_mao(mao)}\n"
            f"📊 Pontos: **{pontos}**"
        )

async def setup(bot : commands.Bot):
    await bot.add_cog(blackjack(bot))
        