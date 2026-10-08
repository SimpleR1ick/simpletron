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

    async def _send_kebab(self, target, user_display_name: str):
        if not KEBAB_IMAGE.exists():
            if hasattr(target, "response"):
                await target.response.send_message("❌ Imagem do kebab não encontrada!", ephemeral=True)
            else:
                await target.send("❌ Imagem do kebab não encontrada!")
            return

        file = discord.File(KEBAB_IMAGE, filename="kebab.png")
        embed = discord.Embed(
            title="🥙 Kebabtech: Diretamente de Night City!",
            description="*O verdadeiro poder do Sandevistan é manter o churrasco girando a 10.000 RPM.*",
            color=discord.Color.from_rgb(255, 175, 55)
        )
        embed.set_image(url="attachment://kebab.png")
        embed.set_footer(text=f"Servido com molho especial para {user_display_name}")

        if hasattr(target, "response"):
            await target.response.send_message(embed=embed, file=file)
        else:
            await target.send(embed=embed, file=file)

    @app_commands.command(name="kebab", description="Kebabtech: o ápice da culinária cibernética de Night City")
    async def cmd_kebab(self, interaction: discord.Interaction):
        await self._send_kebab(interaction, interaction.user.display_name)

    @commands.command(name="kebab", help="Envia o Kebabtech via prefixo !st kebab")
    async def prefix_kebab(self, ctx: commands.Context):
        await self._send_kebab(ctx, ctx.author.display_name)

async def setup(bot: commands.Bot):
    await bot.add_cog(FunCog(bot))
