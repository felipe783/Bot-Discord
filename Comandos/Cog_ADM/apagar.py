import discord
from discord import app_commands
from discord.ext import commands
from loader import * 

DB = load_db()
#O apagar ta funcionando
class apagar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # comando slash /ping
    @app_commands.default_permissions(administrator=True)
    @app_commands.command(name="apagar", description="Apagar as historias antes do tempo")
    async def ping(self, interaction: discord.Interaction):
        # checa cargo
        Id_cargo= 1120416496049463366
        if not any(role.id == Id_cargo for role in interaction.user.roles):
            await interaction.response.send_message(
                "❌ Tu não tem cargo pra isso não, fi 😎aa",
                ephemeral=True
            )
            return
        
        db = load_db() 
        historia_list = db.get("historia", []) 
        canal_historia = self.bot.get_channel(DB["ID_Historia"][0])
        try: 
            if not isinstance (db,dict): 
                db("historia:",[])
            if historia_list:  
                texto = ", ".join(str(x) for x in historia_list if x is not None and x !="") 
                await canal_historia.send(f"\nHistória antiga:{texto}\nHistorias zeradas🔥\n||@everyone||")
                #Zerar o json
                db["historia"] = []
                save_db(db)
            else:
                await canal_historia.send("Sem histórias pra zerar.😭")
        except Exception as e:
            print(f"Deu erro pra Zerar o Json {e}")
        
        await interaction.response.send_message("Historias apagadas",ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(apagar(bot))