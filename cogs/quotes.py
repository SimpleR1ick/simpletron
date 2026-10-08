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

    @commands.hybrid_group(name="quote", description="Caderno de frases marcantes e pérolas do servidor")
    async def quote(self, ctx: commands.Context):
        """Se chamado apenas como !st quote ou /quote sem subcomando, sorteia uma pérola."""
        if ctx.invoked_subcommand is None:
            await self.quote_random(ctx)

    @quote.command(name="add", description="Adiciona uma frase engraçada ao caderno de pérolas")
    @app_commands.describe(autor="Quem disse essa frase?", frase="Qual foi a frase dita?")
    async def quote_add(self, ctx: commands.Context, autor: discord.Member, *, frase: str):
        quotes = load_json(QUOTES_FILE, [])
        new_quote = {
            "author_name": autor.display_name,
            "quote": frase.strip(),
            "added_by": ctx.author.display_name,
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
        embed.set_footer(text=f"Adicionado por {ctx.author.display_name} • Total de pérolas: {len(quotes)}")
        await ctx.send(embed=embed)

    @quote.command(name="random", description="Sorteia uma frase histórica dita no servidor")
    async def quote_random(self, ctx: commands.Context):
        quotes = load_json(QUOTES_FILE, [])
        if not quotes:
            await ctx.send("Nenhuma frase registrada ainda! Use `/quote add` para adicionar a primeira.", ephemeral=True)
            return

        item = random.choice(quotes)
        embed = discord.Embed(
            title="🗣️ Pérola do Servidor",
            description=f'**"{item["quote"]}"**\n\n— *{item["author_name"]}* ({item["date"]})',
            color=discord.Color.purple()
        )
        embed.set_footer(text=f"Registrado por {item.get('added_by', 'Alguém')}")
        await ctx.send(embed=embed)

    @quote.command(name="listar", description="Lista o total de frases salvas")
    async def quote_list(self, ctx: commands.Context):
        quotes = load_json(QUOTES_FILE, [])
        if not quotes:
            await ctx.send("O caderno de pérolas está vazio.", ephemeral=True)
            return
        await ctx.send(f"📚 Temos atualmente **{len(quotes)}** pérolas salvas no servidor! Use `/quote random` para ver uma.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(QuotesCog(bot))
