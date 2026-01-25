import discord
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

@blackjack_group.command(name="double_down",description="Dobre a aposta,e compre mais uma carta!")
async def double_down(self, interaction:discord.Interaction):
    #Verifica pro cara estar em um Jogo
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
    
    aposta = jogo.get("aposta")
    aposta = aposta * 2 #O Doubledown dobra o valor

    #Cada um recebe mais uma carta
    carta = jogo["baralho"].pop()
    jogo["mao"].append(carta)
    cartaD = jogo["baralho"].pop()
    jogo["dealer"].append(cartaD)

    pontos = calcular_pontos(jogo["mao"])
    dealerP = calcular_pontos(jogo["dealer"])

    #Nenhum deles tem o Blackjack por eu ja filtrar no inicio
    if pontos == 21 and dealerP == 21: #Empate
        await interaction.response.send_message(
                f"Deu empate😤\n" 
                f"O {interaction.user.mention} deu azar do **Dealer** ser melhor que ele😎🔥"
        )
    else: 
        if pontos > 21: #Estourou User
            await interaction.response.send_message(
                "Tu é muito ruim no Blackjack😤\n"
                "Aqui so os fortes sobrevivem🔥,use esse tempo pra ficar menos pior🙏"
                f"🃏 Sua mão:{formatar_mao(jogo['mao'])}\n"
                f"📊 Pontos: **{pontos}**"
            )
            await interaction.user.timeout(timedelta(minutes=aposta), reason="Muito ruim no Blackjack")
        else:
            if dealerP > 21:  #Dealer estourou
                await interaction.response.send_message(
                f"O Dealer estourou💥\n"
                f"A mesa ganhou,dessa sorte dessa vez...🔥"
            )
            else:
                if dealerP == 21: #Dealer 21
                    await interaction.response.send_message(
                       "O **Delaer** foi melhor que todos💥🔥"
                       "Ele bateu 21\n"
                       f"{interaction.user.mention} use esse tempo pra ficar menos pior😎"
                    )
                    await interaction.user.timeout(timedelta(minutes=aposta), reason="Muito ruim no Blackjack")
                else:
                    if pontos == 21: #User 21
                        await interaction.response.send_message(
                            "Você teve sorte dessa vez🥶\n"
                            "Agradeça ao Dealer🙏🙌 por te dar um **21** \n"
                            f"🃏 Sua mão:{formatar_mao(jogo['mao'])}\n"
                            f"📊 Pontos: **{pontos}**"
                        )  
                    else:
                        if pontos > dealerP:
                            await interaction.response.send_message(
                            "Você teve sorte dessa vez🥶\n"
                            "Agradeça ao Dealer🙏🙌,por você ter mais pontos que ele \n"
                            f"🃏 Sua mão:{formatar_mao(jogo['mao'])}\n"
                            f"📊 Pontos: **{pontos}**"
                            )  
                        else: #Dealer ganhou
                            await interaction.response.send_message(
                            "O Dealer não mostrou piedade😭\n"
                            f"{interaction.user.mention} foi amassado,use esse tempo para ficar menos pior🥶\n"
                            )  
                            await interaction.user.timeout(timedelta(minutes=aposta), reason="Muito ruim no Blackjack")
    #Depois de tudo deleta o user_id do cara
    del estados_Blackjack.jogos[user_id]