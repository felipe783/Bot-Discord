from pathlib import Path
import discord
from discord import app_commands
from discord.ext import commands

class ReloadCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.default_permissions(administrator=True)
    @app_commands.command(name="reload", description="Da reload nos comandos")
    async def reloadcog(self, interaction: discord.Interaction):
        ID = 1457546195655332193
        canal = self.bot.get_channel(ID)
        comandos_path = Path("Comandos")
        if comandos_path.exists() and comandos_path.is_dir():
            for file in comandos_path.glob("*.py"):
                if file.name.startswith("_"):
                    continue
                module = f"Comandos.{file.stem}"
                try:
                    await self.bot.reload_extension(module)
                    await canal.send(f"Carregado cog: {module}",ephemeral = True)
                except Exception as e:
                    await  canal.send(f"Falaha ao carregar {module}\nErro:{e}")
        else:
            await  canal.send(f"Pasta 'Comandos' não encontrada")
            
async def setup(bot: commands.Bot):
    await bot.add_cog(ReloadCog(bot))