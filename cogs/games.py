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

    @app_commands.command(name="times", description="Divide os amigos presentes na chamada de voz em 2 times equilibrados")
    @app_commands.describe(canal="Canal de voz (opcional, padrão: seu canal atual ou 'Jogatina')")
    async def cmd_times(self, interaction: discord.Interaction, canal: discord.VoiceChannel = None):
        target_channel = canal
        if not target_channel and interaction.user.voice:
            target_channel = interaction.user.voice.channel
        if not target_channel:
            target_channel = discord.utils.get(interaction.guild.voice_channels, name="Jogatina")

        if not target_channel or not target_channel.members:
            await interaction.response.send_message(
                "⚠️ Não há ninguém conectado no canal de voz para dividir times! Conecte-se a uma sala primeiro.",
                ephemeral=True
            )
            return

        members = [m.display_name for m in target_channel.members if not m.bot]
        if len(members) < 2:
            await interaction.response.send_message(
                f"É necessário pelo menos 2 pessoas na sala **{target_channel.name}** para formar times! (Atualmente: {len(members)})",
                ephemeral=True
            )
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
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="oquejogar", description="Sorteia qual jogo o grupo vai jogar quando ninguém decide")
    async def cmd_oquejogar(self, interaction: discord.Interaction):
        games = load_json(GAMES_FILE, DEFAULT_GAMES)
        chosen = random.choice(games)
        embed = discord.Embed(
            title="🎮 O que vamos jogar hoje?",
            description=f"A roleta da indecisão escolheu: **{chosen}**!",
            color=discord.Color.teal()
        )
        embed.set_footer(text="Use /adicionarjogo para incluir novos jogos na roleta")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="adicionarjogo", description="Adiciona um novo jogo à lista de opções da roleta")
    @app_commands.describe(nome="Nome do jogo")
    async def cmd_adicionarjogo(self, interaction: discord.Interaction, nome: str):
        games = load_json(GAMES_FILE, DEFAULT_GAMES)
        if nome.lower() in [g.lower() for g in games]:
            await interaction.response.send_message(f"O jogo **{nome}** já está na lista!", ephemeral=True)
            return
        games.append(nome.strip())
        save_json(GAMES_FILE, games)
        await interaction.response.send_message(f"✅ O jogo **{nome}** foi adicionado à roleta! Total de jogos salvos: {len(games)}.")

async def setup(bot: commands.Bot):
    await bot.add_cog(GamesCog(bot))
