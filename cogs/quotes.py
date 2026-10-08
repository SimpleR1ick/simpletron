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

    async def _add_quote(self, target, autor_display_name: str, autor_avatar_url: str, frase: str, added_by_name: str):
        quotes = load_json(QUOTES_FILE, [])
        new_quote = {
            "author_name": autor_display_name,
            "quote": frase.strip(),
            "added_by": added_by_name,
            "date": datetime.datetime.now().strftime("%d/%m/%Y")
        }
        quotes.append(new_quote)
        save_json(QUOTES_FILE, quotes)

        embed = discord.Embed(
            title="📝 Nova Pérola Registrada!",
            description=f'"{frase}"',
            color=discord.Color.gold()
        )
        if autor_avatar_url:
            embed.set_author(name=autor_display_name, icon_url=autor_avatar_url)
        else:
            embed.set_author(name=autor_display_name)
        embed.set_footer(text=f"Adicionado por {added_by_name} • Total de pérolas: {len(quotes)}")
        if hasattr(target, "response"):
            await target.response.send_message(embed=embed)
        else:
            await target.send(embed=embed)

    async def _random_quote(self, target):
        quotes = load_json(QUOTES_FILE, [])
        if not quotes:
            msg = "Nenhuma frase registrada ainda! Use `/quote add` ou `!st quote add` para adicionar a primeira."
            if hasattr(target, "response"):
                await target.response.send_message(msg, ephemeral=True)
            else:
                await target.send(msg)
            return

        item = random.choice(quotes)
        embed = discord.Embed(
            title="🗣️ Pérola do Servidor",
            description=f'**"{item["quote"]}"**\n\n— *{item["author_name"]}* ({item["date"]})',
            color=discord.Color.purple()
        )
        embed.set_footer(text=f"Registrado por {item.get('added_by', 'Alguém')}")
        if hasattr(target, "response"):
            await target.response.send_message(embed=embed)
        else:
            await target.send(embed=embed)

    async def _list_quotes(self, target):
        quotes = load_json(QUOTES_FILE, [])
        msg = f"📚 Temos atualmente **{len(quotes)}** pérolas salvas no servidor! Use `/quote random` ou `!st quote random` para ver uma." if quotes else "O caderno de pérolas está vazio."
        if hasattr(target, "response"):
            await target.response.send_message(msg, ephemeral=True)
        else:
            await target.send(msg)

    @quotes_group.command(name="add", description="Adiciona uma frase engraçada ao caderno de pérolas")
    @app_commands.describe(autor="Quem disse essa frase?", frase="Qual foi a frase dita?")
    async def cmd_quote_add(self, interaction: discord.Interaction, autor: discord.Member, frase: str):
        await self._add_quote(interaction, autor.display_name, autor.display_avatar.url, frase, interaction.user.display_name)

    @quotes_group.command(name="random", description="Sorteia uma frase histórica dita no servidor")
    async def cmd_quote_random(self, interaction: discord.Interaction):
        await self._random_quote(interaction)

    @quotes_group.command(name="listar", description="Lista o total de frases salvas")
    async def cmd_quote_list(self, interaction: discord.Interaction):
        await self._list_quotes(interaction)

    @commands.group(name="quote", invoke_without_command=True, help="Comandos de pérolas via prefixo !st quote")
    async def prefix_quote(self, ctx: commands.Context):
        await self._random_quote(ctx)

    @prefix_quote.command(name="add", help="Adiciona uma pérola: !st quote add @amigo frase")
    async def prefix_quote_add(self, ctx: commands.Context, autor: discord.Member, *, frase: str):
        await self._add_quote(ctx, autor.display_name, autor.display_avatar.url, frase, ctx.author.display_name)

    @prefix_quote.command(name="random", help="Sorteia uma pérola: !st quote random")
    async def prefix_quote_random(self, ctx: commands.Context):
        await self._random_quote(ctx)

    @prefix_quote.command(name="listar", help="Lista total de pérolas: !st quote listar")
    async def prefix_quote_list(self, ctx: commands.Context):
        await self._list_quotes(ctx)

async def setup(bot: commands.Bot):
    await bot.add_cog(QuotesCog(bot))
