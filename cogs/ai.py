import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from config.settings import GEMINI_API_KEY

class AICog(commands.Cog, name="Inteligência Artificial"):
    """Comandos e interações com a IA Google Gemini."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def query_gemini(self, prompt: str, system_context: str = "") -> str:
        if not GEMINI_API_KEY:
            return (
                "⚠️ Nenhuma chave da API Gemini foi configurada no `.env`!\n"
                "Gere uma chave gratuita em https://aistudio.google.com/ e preencha a variável `GEMINI_API_KEY`."
            )

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"{system_context}\n\nPergunta do usuário: {prompt}" if system_context else prompt}
                    ]
                }
            ]
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=20)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        candidates = data.get("candidates", [])
                        if candidates:
                            text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                            return text.strip() if text else "Não consegui gerar uma resposta."
                        return "Resposta vazia recebida do Gemini."
                    else:
                        error_text = await resp.text()
                        return f"Erro na API do Gemini ({resp.status}): {error_text[:100]}"
        except Exception as e:
            return f"Erro ao contatar o Gemini: {e}"

    @commands.hybrid_command(name="perguntar", aliases=["pergunte"], description="Faça uma pergunta para a inteligência artificial do Gemini")
    @app_commands.describe(pergunta="O que você deseja perguntar?")
    async def perguntar(self, ctx: commands.Context, *, pergunta: str):
        await ctx.defer()
        sys_prompt = "Você é o Simple AI, assistente do servidor 'The Simple Place'. Responda com bom humor, clareza e seja amigável."
        resposta = await self.query_gemini(pergunta, system_context=sys_prompt)
        if len(resposta) > 2000:
            resposta = resposta[:1990] + "..."
        await ctx.send(f"🧠 **Pergunta:** {pergunta}\n\n{resposta}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        # Responder a menções diretas @Simple AI quando não for comando prefixado
        if self.bot.user in message.mentions and not message.mention_everyone and not message.content.startswith("!"):
            clean_content = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
            if clean_content:
                async with message.channel.typing():
                    sys_prompt = "Você é o Simple AI, assistente oficial do servidor 'The Simple Place'. Responda de forma descontraída e bem-humorada em português."
                    reply = await self.query_gemini(clean_content, system_context=sys_prompt)
                    await message.reply(reply[:2000])

async def setup(bot: commands.Bot):
    await bot.add_cog(AICog(bot))
