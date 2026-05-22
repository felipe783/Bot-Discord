from typing import Optional
from loader import * 
import discord
from .historia_group import historia_group


@historia_group.command(name="ver_historia", description="Veja a Historia!")
async def historia(interaction: discord.Interaction):
    db = load_db()
    historia = ", ".join(db["historia"])
    await interaction.response.send_message(
        f"A historia ficou assim: {historia}",
        ephemeral=True
    )

async def setup(bot):
    pass
