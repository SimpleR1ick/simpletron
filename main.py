import asyncio
from pathlib import Path
import discord
from discord.ext import commands
from config.settings import BOT_TOKEN, GUILD_ID

# Configuração de Intents
intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True
intents.message_content = False  # Ative após habilitar 'Message Content Intent' no Developer Portal

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("=" * 55)
    print(f"Simple AI Online: {bot.user} (ID: {bot.user.id})")
    
    if GUILD_ID:
        guild = discord.Object(id=GUILD_ID)
        try:
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
            print(f"Slash Commands sincronizados no servidor {GUILD_ID} ({len(synced)} comandos).")
        except Exception as e:
            print(f"Erro ao sincronizar comandos com a guilda: {e}")
    else:
        synced = await bot.tree.sync()
        print(f"Slash Commands sincronizados globalmente ({len(synced)} comandos).")

    print("Bot 100% pronto e escalável com Cogs!")
    print("=" * 55)

async def load_cogs():
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

async def main():
    async with bot:
        await load_cogs()
        await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except discord.errors.PrivilegedIntentsRequired:
        print("\n" + "=" * 60)
        print("⚠️ AVISO: O 'Message Content Intent' não está ativado no Discord Developer Portal.")
        print("Iniciando sem ele...")
        print("=" * 60 + "\n")
        bot.intents.message_content = False
        asyncio.run(main())
