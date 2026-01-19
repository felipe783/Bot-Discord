import discord
from discord import app_commands
from discord.ext import commands

class ajuda(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot=bot

    @app_commands.command(name="ajuda",description="Explicação dos comandos")
    async def ajuda(self,interaction:discord.Interaction):
        embed = discord.Embed(
            title="📖 Ajuda — Comandos Gerais",
            description="Resumo dos comandos do Bot",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="**Comandos:**",
            value="",
            inline=False
        )
        embed.add_field(
            name="/ping",
            value="O bot ira te responder com um **pong**",
            inline=False
        )
        embed.add_field(
            name="/historia",
            value="O bot ira continuar a **historia** com a frase que voce escrever",
            inline=False
        )
        embed.add_field(
            name="/ver_historia",
            value="Mostra a historia atual",
            inline=False
        )
        embed.add_field(
            name="/buscar_mod",
            value="Procure o mod a sua escolha no Modrinth",
            inline=False
        )

        embed_admin = discord.Embed(
            title="🛡️ Ajuda — Comandos ADM",
            description="Apenas administradores",
            color=discord.Color.red()
        )

        embed_admin.add_field(
            name="/apagar",
            value="Apaga a história atual\n**Somente ADM**",
            inline=False
        )
        embed_admin.add_field(
            name="/reload",
            value="Recarrega todas as COGS\n**Somente ADM**",
            inline=False
        )

        #ephemreal deixa so visto pro cara q chamo
        await interaction.response.send_message(embeds=[embed,embed_admin],ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(ajuda(bot))