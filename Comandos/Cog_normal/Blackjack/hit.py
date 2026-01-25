import discord
from discord.ext import commands
import Estados.estados_Blackjack as estados_Blackjack
from datetime import timedelta
from .blackjack_group import blackjack_group

def formatar_mao(mao):
    return " ".join(f"{c['nome']}{c['naipe']}" for c in mao)

def calcular_pontos(mao): 
    total = sum(c["valor"] for c in mao)
    ases = sum(1 for c in mao if c["nome"] == "Ás")

    while total > 21 and ases:
        total -= 10
        ases -= 1

    return total

class hitcog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

@blackjack_group.command(name="hit", description="Comprar mais uma carta")
async def hit(interaction: discord.Interaction):
        user_id = interaction.user.id

        if user_id not in estados_Blackjack.jogos: #Garante que ele ta em um Jogo
            await interaction.response.send_message("Tu nem começou um jogo😭",ephemeral=True)
            return

        jogo = estados_Blackjack.jogos[user_id]
        jogo["doubledown"] = False  #Ele não pode dar DoubleDown
        duracao = jogo.get("aposta")

        carta = jogo["baralho"].pop()
        jogo["mao"].append(carta)
        cartaD = jogo["baralho"].pop()
        jogo["dealer"].append(cartaD)

        pontos = calcular_pontos(jogo["mao"])
        dealerP = calcular_pontos(jogo["dealer"])
        
        jogo["pontos"] = jogo.get("pontos") + pontos
        jogo["pontos_dealer"] = jogo.get("pontos_dealer") + dealerP

        if dealerP < 17: #Dealer é obrigado a comprar quando é menor que 17
            cartaD = jogo["baralho"].pop()
            jogo["dealer"].append(cartaD)
            dealerP = calcular_pontos(jogo["dealer"])
            
        
        if pontos > 21:
            await interaction.response.send_message(
                f"O {interaction.user.mention} é muito ruim  no Blackjack😤\n"
                "Aqui so os fortes sobrevivem🔥,use esse tempo pra ficar menos pior🙏\n"
                f"🃏 Sua mão:{formatar_mao(jogo['mao'])}\n"
                f"📊 Pontos: **{pontos}**"
            )
            del estados_Blackjack.jogos[user_id]
            await interaction.user.timeout(timedelta(minutes=duracao), reason="Muito ruim no Blackjack")
            return
        else:
            if dealerP > 21: #O dealer tem uma pequena vantagem(A casa sempre ganha😎🔥)
                await interaction.response.send_message(
                    f"Mesa do {interaction.user.mention}\n"
                    f"O Dealer estourou💥😭\n"
                    f"A mesa teve sorte dessa vez...🔥"
                )
                del estados_Blackjack.jogos[user_id]
                return
            else:
                await interaction.response.send_message(
                    f"O jogo do {interaction.user.mention}\n"
                    f"🃏 Nova carta:{formatar_mao(jogo['mao'])}\n"
                    f"📊 Pontos: **{pontos}**"
                )

async def setup(bot: commands.Bot):
    await bot.add_cog(hitcog(bot))