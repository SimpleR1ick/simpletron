from typing import Tuple, Dict, Any, Optional
import discord
from discord import app_commands
from discord.ext import commands
from config.settings import WELCOME_FILE
from utils.storage import load_json, save_json

class WelcomeCog(commands.Cog, name="Boas-vindas"):
    """Automação de recepção para novos membros nos servidores."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def _get_guild_config(self, guild_id: int) -> Dict[str, Any]:
        data = load_json(WELCOME_FILE, {})
        return data.get(str(guild_id), {"enabled": False, "channel_id": None})

    def _save_guild_config(self, guild_id: int, config: Dict[str, Any]):
        data = load_json(WELCOME_FILE, {})
        data[str(guild_id)] = config
        save_json(WELCOME_FILE, data)

    def _build_welcome_payload(self, member: discord.Member) -> Tuple[str, discord.Embed]:
        """Gera o texto e o embed com a foto ampliada do membro (Estilo 2B)."""
        guild = member.guild
        total = guild.member_count or len(guild.members)

        content = f"👋 Salve {member.mention}!"
        embed = discord.Embed(
            description=(
                f"Seja muito bem-vindo(a) ao **{guild.name}**!\n"
                f"Dá uma passada no chat pra se enturmar. Agora somos **{total} membros**! 🚀"
            ),
            color=discord.Color.from_rgb(88, 101, 242)
        )
        # Foto do membro em destaque (tamanho grande)
        embed.set_image(url=member.display_avatar.url)
        embed.set_footer(
            text=f"{guild.name} • Membro #{total}",
            icon_url=guild.icon.url if guild.icon else None
        )
        return content, embed

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Disparado quando um novo membro entra em qualquer servidor que o bot faz parte."""
        if member.bot:
            return

        config = self._get_guild_config(member.guild.id)
        if not config.get("enabled", False):
            return

        channel_id = config.get("channel_id")
        if not channel_id:
            return

        channel = member.guild.get_channel(channel_id)
        if not channel or not isinstance(channel, discord.TextChannel):
            return

        # Verifica se o bot tem permissão para enviar mensagens no canal
        bot_member = member.guild.me or member.guild.get_member(self.bot.user.id)
        if bot_member:
            perms = channel.permissions_for(bot_member)
            if not perms.send_messages or not perms.embed_links:
                return

        content, embed = self._build_welcome_payload(member)
        try:
            await channel.send(content=content, embed=embed)
        except Exception as e:
            print(f"[Boas-vindas] Erro ao enviar mensagem no servidor {member.guild.name}: {e}")

    @commands.hybrid_group(name="boasvindas", description="Gerencia as mensagens de boas-vindas para novos membros")
    async def boasvindas(self, ctx: commands.Context):
        """Comando base de boas-vindas. Se invocado sem argumentos, exibe o status."""
        if ctx.invoked_subcommand is None:
            await self.welcome_status(ctx)

    @boasvindas.command(name="ativar", description="Ativa as mensagens de boas-vindas no canal selecionado")
    @app_commands.describe(canal="Canal de texto onde os novos membros serão recebidos")
    async def welcome_enable(self, ctx: commands.Context, canal: discord.TextChannel):
        if not ctx.guild:
            await ctx.send("Este comando só pode ser utilizado dentro de um servidor.", ephemeral=True)
            return

        if not ctx.author.guild_permissions.manage_guild and not ctx.author.guild_permissions.administrator:
            await ctx.send("❌ Você precisa da permissão de **Gerenciar Servidor** ou **Administrador** para configurar as boas-vindas.", ephemeral=True)
            return

        self._save_guild_config(ctx.guild.id, {
            "enabled": True,
            "channel_id": canal.id
        })

        embed = discord.Embed(
            title="✅ Boas-vindas Ativadas!",
            description=(
                f"A recepção de novos membros está **ativada** para o servidor **{ctx.guild.name}**!\n\n"
                f"📍 **Canal configurado:** {canal.mention}\n"
                f"🧪 Use `/boasvindas testar` ou `!st boasvindas testar` para ver uma prévia da mensagem."
            ),
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @boasvindas.command(name="desativar", description="Desativa as mensagens de boas-vindas neste servidor")
    async def welcome_disable(self, ctx: commands.Context):
        if not ctx.guild:
            await ctx.send("Este comando só pode ser utilizado dentro de um servidor.", ephemeral=True)
            return

        if not ctx.author.guild_permissions.manage_guild and not ctx.author.guild_permissions.administrator:
            await ctx.send("❌ Você precisa da permissão de **Gerenciar Servidor** ou **Administrador** para desativar as boas-vindas.", ephemeral=True)
            return

        self._save_guild_config(ctx.guild.id, {
            "enabled": False,
            "channel_id": None
        })

        embed = discord.Embed(
            title="🛑 Boas-vindas Desativadas",
            description=f"As mensagens de boas-vindas foram desativadas no servidor **{ctx.guild.name}**.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    @boasvindas.command(name="status", description="Verifica o status atual da automação de boas-vindas")
    async def welcome_status(self, ctx: commands.Context):
        if not ctx.guild:
            await ctx.send("Este comando só pode ser utilizado dentro de um servidor.", ephemeral=True)
            return

        config = self._get_guild_config(ctx.guild.id)
        enabled = config.get("enabled", False)
        channel_id = config.get("channel_id")
        channel = ctx.guild.get_channel(channel_id) if channel_id else None

        embed = discord.Embed(
            title="⚙️ Status das Boas-vindas",
            color=discord.Color.blue()
        )
        embed.add_field(name="🏠 Servidor", value=ctx.guild.name, inline=True)
        embed.add_field(name="📢 Status", value="🟢 Ativado" if enabled else "🔴 Desativado", inline=True)
        embed.add_field(
            name="📍 Canal",
            value=channel.mention if channel else "Nenhum canal configurado",
            inline=False
        )
        embed.set_footer(text=f"Total atual de membros: {ctx.guild.member_count}")
        await ctx.send(embed=embed)

    @boasvindas.command(name="testar", description="Simula o envio da mensagem de boas-vindas com o seu perfil")
    async def welcome_test(self, ctx: commands.Context):
        if not ctx.guild:
            await ctx.send("Este comando só pode ser utilizado dentro de um servidor.", ephemeral=True)
            return

        config = self._get_guild_config(ctx.guild.id)
        channel_id = config.get("channel_id")
        target_channel = ctx.guild.get_channel(channel_id) if channel_id else ctx.channel

        content, embed = self._build_welcome_payload(ctx.author)
        embed.set_author(name="🧪 Simulação de Boas-vindas")

        try:
            await target_channel.send(content=content, embed=embed)
            if target_channel.id != ctx.channel.id:
                await ctx.send(f"✅ Teste enviado com sucesso no canal {target_channel.mention}!", ephemeral=True)
        except discord.Forbidden:
            await ctx.send(f"⚠️ O bot não tem permissão para enviar mensagens em {target_channel.mention}.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(WelcomeCog(bot))
