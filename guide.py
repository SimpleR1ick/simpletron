import discord
from discord.ext import commands
from config.settings import BOT_TOKEN, GUILD_ID

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logado como: {bot.user}")
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("Servidor não encontrado.")
        await bot.close()
        return

    # 1. Encontrar a categoria BOTS & TESTES
    category = discord.utils.get(guild.categories, name="⚙️ BOTS & TESTES")
    if not category:
        print("Criando categoria ⚙️ BOTS & TESTES...")
        category = await guild.create_category("⚙️ BOTS & TESTES")

    # 2. Configurar permissões (apenas leitura para @everyone)
    everyone_role = guild.default_role
    bot_role = discord.utils.get(guild.roles, name="Bots")

    overwrites = {
        everyone_role: discord.PermissionOverwrite(send_messages=False, view_channel=True, add_reactions=True),
    }
    if bot_role:
        overwrites[bot_role] = discord.PermissionOverwrite(send_messages=True, view_channel=True, embed_links=True)

    # 3. Criar ou obter o canal #guia-comandos
    channel_name = "guia-comandos"
    channel = discord.utils.get(category.text_channels, name=channel_name)
    if not channel:
        print(f"Criando canal #{channel_name}...")
        channel = await category.create_text_channel(channel_name, overwrites=overwrites)
    else:
        print(f"Canal #{channel_name} já existe. Atualizando mensagens...")
        # Limpar mensagens antigas se houver
        try:
            await channel.purge(limit=10)
        except Exception:
            pass

    # 4. Criar o Embed com o guia completo
    embed = discord.Embed(
        title="📖 Central de Comandos — Simple AI 🤖",
        description=(
            "Bem-vindo ao **Simple AI**, o assistente multifuncional do **The Simple Place**!\n"
            "Abaixo você encontra todos os comandos disponíveis e como utilizá-los. "
            "Para executar qualquer comando, basta digitar `/` no canal <#comandos>.\n\u200b"
        ),
        color=discord.Color.blue()
    )

    embed.add_field(
        name="⚔️ /times",
        value=(
            "**O que faz:** Divide os membros conectados na chamada de voz em 2 equipes equilibradas.\n"
            "**Como usar:** Entre na sala de voz com seus amigos e digite `/times` no chat.\n"
            "*(Opcional: você pode especificar outro canal de voz como argumento)*.\n\u200b"
        ),
        inline=False
    )

    embed.add_field(
        name="🎮 /oquejogar e /adicionarjogo",
        value=(
            "**`/oquejogar`:** Acaba com a indecisão do grupo sorteando um jogo da roleta.\n"
            "**`/adicionarjogo <nome>`:** Adiciona um novo jogo à lista de opções da roleta.\n"
            "*Exemplo:* `/adicionarjogo Lethal Company`\n\u200b"
        ),
        inline=False
    )

    embed.add_field(
        name="🗣️ /quote (Caderno de Pérolas)",
        value=(
            "**`/quote add <@autor> <frase>`:** Salva uma frase engraçada ou absurda dita por alguém.\n"
            "**`/quote random`:** Sorteia e exibe uma pérola histórica registrada no servidor.\n"
            "**`/quote listar`:** Mostra o total de pérolas salvas no servidor.\n"
            "*Exemplo:* `/quote add @amigo eu juro que não fui eu`\n\u200b"
        ),
        inline=False
    )

    embed.add_field(
        name="🎁 /jogosgratis",
        value=(
            "**O que faz:** Busca promoções ativas de jogos 100% gratuitos para PC (Steam, Epic Games, etc.).\n"
            "**Automático:** O bot também monitora e posta novidades a cada 2 horas no canal <#jogos-gratis>.\n\u200b"
        ),
        inline=False
    )

    embed.add_field(
        name="🧠 /perguntar",
        value=(
            "**O que faz:** Faz uma pergunta direta para a inteligência artificial do Google Gemini.\n"
            "**Como usar:** `/perguntar <sua dúvida>` ou marcando `@Simple AI` em qualquer mensagem.\n\u200b"
        ),
        inline=False
    )

    embed.add_field(
        name="🎬 Corretor Automático de Links (Embed Fixer)",
        value=(
            "Não precisa de comando! Ao postar links do **Twitter/X**, **TikTok**, **Instagram Reels** ou **Reddit**, "
            "o bot automaticamente gera o player para assistir o vídeo direto no Discord.\n\u200b"
        ),
        inline=False
    )

    embed.set_footer(text="The Simple Place • Use sempre o canal #comandos para interagir com o bot!")

    await channel.send(embed=embed)
    print("Guia enviado com sucesso!")
    await bot.close()

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
