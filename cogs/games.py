import random
import datetime
import discord
from discord import app_commands
from discord.ext import commands
from config.settings import GAMES_FILE
from utils.storage import load_json, save_json

DEFAULT_GAMES = [
    "Valorant", "Counter-Strike 2", "League of Legends", 
    "Rocket League", "Minecraft", "Overwatch 2", 
    "Lethal Company", "Terraria", "GTA V", "Among Us"
]

class GamesCog(commands.Cog, name="Jogos e Sorteios"):
    """Comandos para jogatinas, sorteios de times e escolha de jogos."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _split_teams(self, target, author_voice, guild, canal=None):
        target_channel = canal
        if not target_channel and author_voice:
            target_channel = author_voice.channel
        if not target_channel:
            target_channel = discord.utils.get(guild.voice_channels, name="Jogatina")

        if not target_channel or not target_channel.members:
            msg = "⚠️ Não há ninguém conectado no canal de voz para dividir times! Conecte-se a uma sala primeiro."
            if hasattr(target, "response"):
                await target.response.send_message(msg, ephemeral=True)
            else:
                await target.send(msg)
            return

        members = [m.display_name for m in target_channel.members if not m.bot]
        if len(members) < 2:
            msg = f"É necessário pelo menos 2 pessoas na sala **{target_channel.name}** para formar times! (Atualmente: {len(members)})"
            if hasattr(target, "response"):
                await target.response.send_message(msg, ephemeral=True)
            else:
                await target.send(msg)
            return

        random.shuffle(members)
        half = len(members) // 2
        team_a = members[:half]
        team_b = members[half:]

        embed = discord.Embed(
            title=f"⚔️ Sorteio de Equipes — {target_channel.name}",
            color=discord.Color.orange(),
            timestamp=datetime.datetime.now()
        )
        embed.add_field(name="🔵 Time Azul", value="\n".join([f"• {p}" for p in team_a]) if team_a else "Vazio", inline=True)
        embed.add_field(name="🔴 Time Vermelho", value="\n".join([f"• {p}" for p in team_b]) if team_b else "Vazio", inline=True)
        embed.set_footer(text=f"Total de {len(members)} jogadores divididos")

        if hasattr(target, "response"):
            await target.response.send_message(embed=embed)
        else:
            await target.send(embed=embed)

    @app_commands.command(name="times", description="Divide os amigos presentes na chamada de voz em 2 times equilibrados")
    @app_commands.describe(canal="Canal de voz (opcional, padrão: seu canal atual ou 'Jogatina')")
    async def cmd_times(self, interaction: discord.Interaction, canal: discord.VoiceChannel = None):
        await self._split_teams(interaction, interaction.user.voice, interaction.guild, canal)

    @commands.command(name="times", help="Divide times via prefixo !st times")
    async def prefix_times(self, ctx: commands.Context, canal: discord.VoiceChannel = None):
        await self._split_teams(ctx, ctx.author.voice, ctx.guild, canal)

    async def _pick_game(self, target):
        games = load_json(GAMES_FILE, DEFAULT_GAMES)
        chosen = random.choice(games)
        embed = discord.Embed(
            title="🎮 O que vamos jogar hoje?",
            description=f"A roleta da indecisão escolheu: **{chosen}**!",
            color=discord.Color.teal()
        )
        embed.set_footer(text="Use /adicionarjogo ou !st adicionarjogo para incluir novos jogos")
        if hasattr(target, "response"):
            await target.response.send_message(embed=embed)
        else:
            await target.send(embed=embed)

    @app_commands.command(name="oquejogar", description="Sorteia qual jogo o grupo vai jogar quando ninguém decide")
    async def cmd_oquejogar(self, interaction: discord.Interaction):
        await self._pick_game(interaction)

    @commands.command(name="oquejogar", help="Sorteia um jogo via prefixo !st oquejogar")
    async def prefix_oquejogar(self, ctx: commands.Context):
        await self._pick_game(ctx)

    async def _add_game(self, target, nome: str):
        games = load_json(GAMES_FILE, DEFAULT_GAMES)
        if nome.lower() in [g.lower() for g in games]:
            msg = f"O jogo **{nome}** já está na lista!"
            if hasattr(target, "response"):
                await target.response.send_message(msg, ephemeral=True)
            else:
                await target.send(msg)
            return
        games.append(nome.strip())
        save_json(GAMES_FILE, games)
        msg = f"✅ O jogo **{nome}** foi adicionado à roleta! Total de jogos salvos: {len(games)}."
        if hasattr(target, "response"):
            await target.response.send_message(msg)
        else:
            await target.send(msg)

    @app_commands.command(name="adicionarjogo", description="Adiciona um novo jogo à lista de opções da roleta")
    @app_commands.describe(nome="Nome do jogo")
    async def cmd_adicionarjogo(self, interaction: discord.Interaction, nome: str):
        await self._add_game(interaction, nome)

    @commands.command(name="adicionarjogo", help="Adiciona um jogo via prefixo !st adicionarjogo <nome>")
    async def prefix_adicionarjogo(self, ctx: commands.Context, *, nome: str):
        await self._add_game(ctx, nome)

async def setup(bot: commands.Bot):
    await bot.add_cog(GamesCog(bot))
