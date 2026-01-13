from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands
import requests


class busca_mod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="busca_mod", description="Busque o nome de um mod")
    async def buscar_mod(self, interaction: discord.Interaction, texto: Optional[str] = None):
        texto = texto or ""
        url = "https://api.modrinth.com/v2/search"
        params = {"query": texto, "limit": 5}
        headers = {"User-Agent": "SeuBotDiscord/1.0"} 
        res = requests.get(url, params=params, headers=headers)
        data = res.json() #Retorna o json com as infos
        hits = data.get("hits", []) #Ce o json tiver "hints" ele pega
        if not hits:
            await interaction.response.send_message(f"Nenhum mod encontrado para '{texto}'.")
            return

        mod = hits[0]  # pega o primeiro resultado
        titulo = mod.get("title", "Sem título")
        desc = mod.get("description", "")
        downloads = mod.get("downloads", 0)
        autor = mod.get("author", "desconhecido")
        slug = mod.get("slug")

        # Cria uma Embed simples com as informações do mod
        embed = discord.Embed(title=titulo, description=desc[:200] + "...", color=0x00ff00)
        embed.add_field(name="Autor", value=autor)
        embed.add_field(name="Downloads", value=str(downloads))
        if slug:
            embed.url = f"https://modrinth.com/project/{slug}"
        await interaction.response.send_message(embed=embed)

        

async def setup(bot: commands.Bot):
    await bot.add_cog(busca_mod(bot))