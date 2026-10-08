import datetime
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands, tasks
from config.settings import GIVEAWAYS_FILE, GUILD_ID
from utils.storage import load_json, save_json

class GiveawaysCog(commands.Cog, name="Jogos Grátis"):
    """Monitoramento automático e consulta de jogos grátis na Steam/Epic."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.auto_free_games_task.start()

    def cog_unload(self):
        self.auto_free_games_task.cancel()

    async def check_free_games(self, channel: discord.TextChannel = None, send_only_new: bool = True):
        url = "https://www.gamerpower.com/api/giveaways?type=game&platform=pc"
        seen_giveaways = set(load_json(GIVEAWAYS_FILE, []))

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status != 200:
                        return []
                    giveaways = await resp.json()
        except Exception as e:
            print(f"[Giveaways] Erro ao buscar jogos grátis: {e}")
            return []

        new_offers = []
        for item in giveaways[:15]:
            gid = str(item.get("id"))
            if send_only_new and gid in seen_giveaways:
                continue

            seen_giveaways.add(gid)
            new_offers.append(item)

            if channel:
                embed = discord.Embed(
                    title=f"🎁 Jogo Grátis: {item.get('title')}",
                    description=item.get("description", "Aproveite enquanto está de graça!"),
                    url=item.get("open_giveaway_url"),
                    color=discord.Color.green(),
                    timestamp=datetime.datetime.now()
                )
                if item.get("image"):
                    embed.set_image(url=item.get("image"))
                embed.add_field(name="Plataforma", value=item.get("platforms", "PC"), inline=True)
                embed.add_field(name="Preço Normal", value=item.get("worth", "N/A"), inline=True)
                embed.add_field(name="Resgatar", value=f"[Clique aqui para pegar]({item.get('open_giveaway_url')})", inline=False)
                embed.set_footer(text="Simple AI • Jogos Grátis")
                await channel.send(embed=embed)

        save_json(GIVEAWAYS_FILE, list(seen_giveaways))
        return new_offers

    @tasks.loop(hours=2)
    async def auto_free_games_task(self):
        guild = self.bot.get_guild(GUILD_ID)
        if not guild:
            return
        channel = discord.utils.get(guild.text_channels, name="jogos-gratis")
        if channel:
            await self.check_free_games(channel=channel, send_only_new=True)

    @auto_free_games_task.before_loop
    async def before_free_games_loop(self):
        await self.bot.wait_until_ready()

    @app_commands.command(name="jogosgratis", description="Verifica se há novos jogos grátis na Steam/Epic Games no momento")
    async def cmd_jogosgratis(self, interaction: discord.Interaction):
        await interaction.response.defer()
        channel = interaction.channel
        offers = await self.check_free_games(channel=channel, send_only_new=False)
        if not offers:
            await interaction.followup.send("Nenhuma promoção de jogo grátis encontrada no momento.")
        else:
            await interaction.followup.send("Encontrei as ofertas acima para PC!")

    @commands.command(name="jogosgratis", help="Verifica jogos grátis via prefixo !st jogosgratis")
    async def prefix_jogosgratis(self, ctx: commands.Context):
        async with ctx.typing():
            offers = await self.check_free_games(channel=ctx.channel, send_only_new=False)
            if not offers:
                await ctx.send("Nenhuma promoção de jogo grátis encontrada no momento.")
            else:
                await ctx.send("Encontrei as ofertas acima para PC!")

async def setup(bot: commands.Bot):
    await bot.add_cog(GiveawaysCog(bot))
