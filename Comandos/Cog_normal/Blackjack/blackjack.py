import discord
from discord import app_commands
from discord.ext import commands
import random
import Estados.estados_Blackjack as estados_Blackjack

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
    naipes = ["♠️", "♥️", "♦️", "♣️"]
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

def tem_blackjack(mao):
    nome = [c["nome"]for c in mao]
    valor = [c["valor"]for c in mao]
    
    return "Ás" in nome and 10 in valor 
    
class blackjack(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="blackjack",description="Começe a jogar blackjack!")
    async def blackjack(self, interaction:discord.Interaction,aposta : int):
        duracao = aposta
        user_id = interaction.user.id

        if user_id in estados_Blackjack.jogos: #Garante que o user não esteja em um jogo
            await interaction.response.send_message("Tu já esta em um jogo😎",ephemeral=True)
            return
        
        if(duracao <= 0 ):
            await interaction.response.send_message(
                "Aposta ai irmão,aqui so trabalho com números acima de 0 😎🔥"
            )
            return #aqui garante que o codigo para
        
        baralho = criar_baralho()
        dealer = [baralho.pop(),baralho.pop()]
        mao = [baralho.pop(),baralho.pop()]
        
        estados_Blackjack.jogos[user_id]= { #Cada user tem uma "mesa de blackjack"
            "baralho" : baralho,
            "mao": mao,
            "dealer" : dealer,
            "duracao" : duracao,
            "doubledown" : True
        }

        pontos = calcular_pontos(mao)
        if tem_blackjack(mao):
            await interaction.response.send_message(
                f"Os Deus do Blackjack estavam do seu lado {user_id}🙌🙏\n"
                "Você fez Blackjack com:\n"
                f"🃏 Suas cartas:{formatar_mao(mao)}\n"
                f"📊 Pontos: **{pontos}**"
            )
            return #Ele ganhou o blackjack
        else:
            await interaction.response.send_message(
                f"🃏 Suas cartas: {formatar_mao(mao)}\n"
                f"📊 Pontos: **{pontos}**\n"
                f"🃏Cartas do Dealer: {formatar_mao(dealer[:1])}"
            )

async def setup(bot : commands.Bot):
    await bot.add_cog(blackjack(bot))
        