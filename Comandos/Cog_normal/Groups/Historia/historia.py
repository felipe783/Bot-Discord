from typing import Optional
from loader import * 
import discord
from .historia_group import historia_group

@historia_group.command(name="escrever",description="Escreva uma Historia!")
async def historia(
    interaction: discord.Interaction,
    texto: Optional[str] = None
):
    texto = texto or ""
    db = load_db()
    db["historia"].append(texto)
    save_db(db)
    historia_texto = ", ".join(db["historia"])

    await interaction.response.send_message(
        f"A historia ficou assim: {historia_texto}"
    )

async def setup(bot):
    pass