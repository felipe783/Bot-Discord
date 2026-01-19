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
            for file in comandos_path.rglob("*.py"):
                if file.name.startswith("_"):
                    continue
                relative_path = file.relative_to(comandos_path)
                module = f"Comandos.{relative_path.with_suffix('').as_posix().replace('/', '.')}"
                try:
                    await self.load_extension(module)
                    print(f"Carregado cog: {module}")
                except Exception as e:
                    print(f"Falha ao carregar {module}: {e}")
        else:
            print("Pasta 'Comandos' não encontrada. Verifique a estrutura do projeto.")
            
async def setup(bot: commands.Bot):
    await bot.add_cog(ReloadCog(bot))