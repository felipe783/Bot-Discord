import discord
from discord import app_commands
from discord.ext import commands
import random
import estados

class doubledown(commands.Cog):
    def __init__(self,bot: commands.Bot):
        self.bot = bot