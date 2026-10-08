import asyncio
from pathlib import Path
import discord
from discord.ext import commands
from config.settings import BOT_TOKEN, GUILD_ID

def create_bot(enable_message_content: bool = True, enable_members: bool = True) -> commands.Bot:
    intents = discord.Intents.default()
    intents.guilds = True
    intents.voice_states = True
    intents.members = enable_members
    intents.message_content = enable_message_content

    bot = commands.Bot(
        command_prefix=commands.when_mentioned_or("!st ", "!st"),
        intents=intents,
        case_insensitive=True,
        help_command=None
    )

    @bot.event
    async def on_ready():
        print("=" * 55)
        print(f"Simple AI Online: {bot.user} (ID: {bot.user.id})")
        
        # Sincroniza globalmente para que todos os servidores onde o bot está recebam os comandos
        try:
            global_synced = await bot.tree.sync()
            print(f"Slash Commands sincronizados globalmente ({len(global_synced)} comandos).")
        except Exception as e:
            print(f"Erro ao sincronizar comandos globalmente: {e}")

        if GUILD_ID:
            guild = discord.Object(id=GUILD_ID)
            try:
                bot.tree.copy_global_to(guild=guild)
                synced = await bot.tree.sync(guild=guild)
                print(f"Slash Commands sincronizados no servidor principal {GUILD_ID} ({len(synced)} comandos).")
            except Exception as e:
                print(f"Erro ao sincronizar comandos com a guilda: {e}")

        status_prefix = "Ativo" if enable_message_content else "Ativo apenas via menção (@Simple AI)"
        status_members = "Ativo" if enable_members else "Desativado (Requer Server Members Intent)"
        print(f"Prefixo !st: {status_prefix}")
        print(f"Monitoramento de Membros: {status_members}")
        print("Bot 100% pronto e escalável com Cogs!")
        print("=" * 55)

    @bot.command(name="ajuda", aliases=["help", "comandos"])
    async def cmd_ajuda(ctx: commands.Context):
        """Exibe a lista de comandos disponíveis via prefixo !st."""
        embed = discord.Embed(
            title="📖 Comandos Alternativos — Simple AI (!st)",
            description=(
                "Quando os comandos de barra (`/`) estiverem indisponíveis, "
                "você pode usar o prefixo **`!st`** ou mencionar **`@Simple AI`** diretamente no chat!\n\u200b"
            ),
            color=discord.Color.blue()
        )
        embed.add_field(name="⚔️ !st times", value="Divide os amigos conectados no canal de voz em 2 equipes.", inline=False)
        embed.add_field(name="🎮 !st oquejogar", value="Sorteia um jogo da roleta do grupo.", inline=False)
        embed.add_field(name="➕ !st adicionarjogo <nome>", value="Adiciona um novo jogo à lista da roleta.", inline=False)
        embed.add_field(name="🗣️ !st quote <add/random/listar>", value="Gerencia e sorteia pérolas do servidor.", inline=False)
        embed.add_field(name="🎁 !st jogosgratis", value="Consulta promoções ativas de jogos grátis para PC.", inline=False)
        embed.add_field(name="🧠 !st perguntar <dúvida>", value="Envia uma pergunta para a IA do Google Gemini.", inline=False)
        embed.add_field(name="🥙 !st kebab", value="Invoca a iguaria cibernética Kebabtech.", inline=False)
        embed.add_field(name="👋 !st boasvindas <ativar/desativar/status/testar>", value="Gerencia a recepção automática para novos membros.", inline=False)
        embed.set_footer(text="Exemplo: !st kebab ou @Simple AI times")
        await ctx.send(embed=embed)

    return bot

async def load_cogs(bot: commands.Bot):
    """Carrega dinamicamente todas as extensões da pasta cogs/."""
    cogs_dir = Path(__file__).parent / "cogs"
    for file in cogs_dir.glob("*.py"):
        if not file.name.startswith("__"):
            extension_name = f"cogs.{file.stem}"
            try:
                await bot.load_extension(extension_name)
                print(f"[Cogs] Módulo carregado: {extension_name}")
            except Exception as e:
                print(f"[Cogs] Erro ao carregar {extension_name}: {e}")

async def run(enable_message_content: bool, enable_members: bool = True):
    bot = create_bot(enable_message_content=enable_message_content, enable_members=enable_members)
    async with bot:
        await load_cogs(bot)
        await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(run(enable_message_content=True, enable_members=True))
    except discord.errors.PrivilegedIntentsRequired:
        print("\n" + "=" * 65)
        print("⚠️ AVISO: 'Message Content' ou 'Server Members' intent não está ativo no Portal.")
        print("Tentando inicializar com fallback de intents...")
        print("=" * 65 + "\n")
        try:
            asyncio.run(run(enable_message_content=False, enable_members=True))
        except discord.errors.PrivilegedIntentsRequired:
            print("\n" + "=" * 65)
            print("⚠️ AVISO: 'Server Members Intent' também não está ativo no Developer Portal!")
            print("Para a recepção de novos membros funcionar, ative 'Server Members Intent' no portal.")
            print("Iniciando em modo seguro (sem monitoramento de entrada de membros)...")
            print("=" * 65 + "\n")
            asyncio.run(run(enable_message_content=False, enable_members=False))

