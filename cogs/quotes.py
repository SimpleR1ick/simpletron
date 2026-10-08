import random
import datetime
import discord
from discord import app_commands
from discord.ext import commands
from config.settings import QUOTES_FILE
from utils.storage import load_json, save_json

class QuotesCog(commands.Cog, name="Caderno de Pérolas"):
    """Comandos para registrar e sortear frases históricas do servidor."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    quotes_group = app_commands.Group(name="quote", description="Caderno de frases marcantes e pérolas do servidor")

    @quotes_group.command(name="add", description="Adiciona uma frase engraçada ao caderno de pérolas")
    @app_commands.describe(autor="Quem disse essa frase?", frase="Qual foi a frase dita?")
    async def cmd_quote_add(self, interaction: discord.Interaction, autor: discord.Member, frase: str):
        quotes = load_json(QUOTES_FILE, [])
        new_quote = {
            "author_id": autor.id,
            "author_name": autor.display_name,
            "quote": frase.strip(),
            "added_by": interaction.user.display_name,
            "date": datetime.datetime.now().strftime("%d/%m/%Y")
        }
        quotes.append(new_quote)
        save_json(QUOTES_FILE, quotes)

        embed = discord.Embed(
            title="📝 Nova Pérola Registrada!",
            description=f'"{frase}"',
            color=discord.Color.gold()
        )
        embed.set_author(name=autor.display_name, icon_url=autor.display_avatar.url)
        embed.set_footer(text=f"Adicionado por {interaction.user.display_name} • Total de pérolas: {len(quotes)}")
        await interaction.response.send_message(embed=embed)

    @quotes_group.command(name="random", description="Sorteia uma frase histórica dita no servidor")
    async def cmd_quote_random(self, interaction: discord.Interaction):
        quotes = load_json(QUOTES_FILE, [])
        if not quotes:
            await interaction.response.send_message("Nenhuma frase registrada ainda! Use `/quote add` para adicionar a primeira.", ephemeral=True)
            return

        item = random.choice(quotes)
        embed = discord.Embed(
            title="🗣️ Pérola do Servidor",
            description=f'**"{item["quote"]}"**\n\n— *{item["author_name"]}* ({item["date"]})',
            color=discord.Color.purple()
        )
        embed.set_footer(text=f"Registrado por {item.get('added_by', 'Alguém')}")
        await interaction.response.send_message(embed=embed)

    @quotes_group.command(name="listar", description="Lista o total de frases salvas")
    async def cmd_quote_list(self, interaction: discord.Interaction):
        quotes = load_json(QUOTES_FILE, [])
        if not quotes:
            await interaction.response.send_message("O caderno de pérolas está vazio.", ephemeral=True)
            return
        await interaction.response.send_message(f"📚 Temos atualmente **{len(quotes)}** pérolas salvas no servidor! Use `/quote random` para ver uma.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(QuotesCog(bot))
