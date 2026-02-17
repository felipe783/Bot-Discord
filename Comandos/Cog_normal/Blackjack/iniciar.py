import discord
from discord import app_commands
from discord.ext import commands
import random
import Estados.estados_Blackjack as estados_Blackjack
from .blackjack_group import blackjack_group
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
    if not isinstance(mao, list) or len(mao) != 2:
        return False
    nomes = [c.get("nome") for c in mao]
    total = calcular_pontos(mao)
    return "Ás" in nomes and total == 21
    
class iniciarcog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

@blackjack_group.command(name="iniciar",description="Começe a jogar blackjack!")
async def iniciar(interaction:discord.Interaction,aposta : int):
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
        mao_dealer = [baralho.pop(),baralho.pop()]
        mao_user = [baralho.pop(),baralho.pop()]
        
        estados_Blackjack.jogos[user_id]= { #Cada user tem uma "mesa de blackjack"
            "baralho" : baralho,
            "mao": mao_user,
            "dealer" : mao_dealer,
            "aposta" : duracao,
            "doubledown" : True,
            "stand" : True,
            "pontos" : 0,
            "pontos_dealer": 0
        }
        jogo = estados_Blackjack.jogos[user_id]

        pontos_user = calcular_pontos(mao_user)
        pontos_dealer = calcular_pontos(mao_dealer)

        jogo["pontos"] = pontos_user
        jogo["pontos_dealer"] = pontos_dealer

        dealerBlack = False
        userBlack = False

        if tem_blackjack(jogo["dealer"]):
            dealerBlack = True
        if tem_blackjack(mao_user):
            userBlack = True
            
        if userBlack and dealerBlack: #Empatou
            await interaction.response.send_message(
                f"Deu empate😤\n" 
                f"O {interaction.user.mention} deu azar do **Dealer** ser melhor que ele😎🔥"
            )
            del estados_Blackjack.jogos[user_id]
        else:
            if userBlack: #User deu blackjack
                await interaction.response.send_message(
                f"Os Deuses do Blackjack estavam do seu lado {interaction.user.mention}🙌🙏\n"
                "Você fez Blackjack com:\n"
                f"🃏 {formatar_mao(mao_user)}\n"
                )
                del estados_Blackjack.jogos[user_id]
            else:
                if dealerBlack: #Dealer deu blackjack
                   del estados_Blackjack.jogos[user_id]
                   await interaction.response.send_message(
                        "Se renda ao **Dealer** ele fez um blackjack🙏\n"
                        f"Ele amassou  o {interaction.user.mention}🥶 \n"
                        "com um **BlackJack**🔥:\n"
                        f"🃏 {formatar_mao(jogo['dealer'])}\n"
                    ) 
                   await interaction.user.timeout(timedelta(minutes=duracao), reason="Muito ruim no Blackjack")
                else:
                    await interaction.response.send_message(
                        f"O jogo de {interaction.user.mention}:\n"
                        f"🃏 Suas cartas: {formatar_mao(mao_user)}\n"
                        f"📊 Pontos: **{pontos_user}**\n"
                        f"🃏Carta do Dealer: {formatar_mao(mao_dealer[:1])}"
                    )

async def setup(bot: commands.Bot):
    await bot.add_cog(iniciarcog(bot))