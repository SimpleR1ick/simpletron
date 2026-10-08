import re
import discord
from discord.ext import commands

EMBED_REPLACEMENTS = [
    # Twitter / X
    (re.compile(r"https?://(?:www\.)?(?:twitter\.com|x\.com)/([a-zA-Z0-9_]+/status/\d+)"), r"https://fxtwitter.com/\1"),
    # Instagram Reels & Posts
    (re.compile(r"https?://(?:www\.)?instagram\.com/(reel|p)/([a-zA-Z0-9_-]+)"), r"https://ddinstagram.com/\1/\2"),
    # TikTok
    (re.compile(r"https?://(?:www\.|vm\.|vt\.)?tiktok\.com/([a-zA-Z0-9_/@-]+)"), r"https://vxtiktok.com/\1"),
    # Reddit
    (re.compile(r"https?://(?:www\.)?reddit\.com/r/([a-zA-Z0-9_]+/comments/[a-zA-Z0-9_]+)"), r"https://rxddit.com/r/\1"),
]

class MediaCog(commands.Cog, name="Mídia e Embeds"):
    """Correção automática de links de redes sociais para exibição de vídeo."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        content = message.content
        replaced_urls = []
        for pattern, replacement in EMBED_REPLACEMENTS:
            matches = pattern.findall(content)
            if matches:
                new_content = pattern.sub(replacement, content)
                if new_content != content:
                    replaced_urls.append(new_content)
                    break

        if replaced_urls:
            fixed_link = replaced_urls[0]
            try:
                await message.edit(suppress=True)
            except Exception:
                pass
            await message.channel.send(f"🎬 **Preview corrigido para {message.author.mention}:**\n{fixed_link}")

async def setup(bot: commands.Bot):
    await bot.add_cog(MediaCog(bot))
