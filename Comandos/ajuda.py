import discord
from discord import app_commands
from discord.ext import commands

class ajuda(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot=bot

    @app_commands.command(name="ajuda",description="Explicação dos comandos")
    async def ajuda(self,interaction:discord.Interaction):
        embed = discord.Embed(
            title="Ajuda",
            description="Resumo dos comandos do Bot",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="**Comandos:**",
            value="",
            inline=False
        )
        embed.add_field(
            name="/Ping",
            value="O bot ira te responder com um **pong**",
            inline=False
        )
        embed.add_field(
            name="/Historia",
            value="O bot ira continuar a **historia** com a frase que voce escrever",
            inline=False
        )
        embed.add_field(
            name="/Ajuda",
            value="é esse que voce ta lendo",
            inline=False
        )
        embed.add_field(
            name="/Apagar",
            value="Apagar a historia no momento que quiser\n** Apenas ADM pode usar **",
            inline=False
        )
        #ephemreal deixa so visto pro cara q chamo
        await interaction.response.send_message(embed=embed,ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(ajuda(bot))