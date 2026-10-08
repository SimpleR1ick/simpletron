from pathlib import Path
import discord
from discord import app_commands
from discord.ext import commands

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
KEBAB_IMAGE = ASSETS_DIR / "kebab.png"

class FunCog(commands.Cog, name="Diversão e Memes"):
    """Comandos de diversão, piadas e memes da comunidade."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="kebab", description="Kebabtech: o ápice da culinária cibernética de Night City")
    async def cmd_kebab(self, interaction: discord.Interaction):
        if not KEBAB_IMAGE.exists():
            await interaction.response.send_message("❌ Imagem do kebab não encontrada!", ephemeral=True)
            return

        file = discord.File(KEBAB_IMAGE, filename="kebab.png")
        embed = discord.Embed(
            title="🥙 Kebabtech: Diretamente de Night City!",
            description="*O verdadeiro poder do Sandevistan é manter o churrasco girando a 10.000 RPM.*",
            color=discord.Color.from_rgb(255, 175, 55)
        )
        embed.set_image(url="attachment://kebab.png")
        embed.set_footer(text=f"Servido com molho especial para {interaction.user.display_name}")

        await interaction.response.send_message(embed=embed, file=file)

async def setup(bot: commands.Bot):
    await bot.add_cog(FunCog(bot))
