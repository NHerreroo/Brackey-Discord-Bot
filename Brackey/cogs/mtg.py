from discord.ext import commands
import requests

class MTG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def card(self, ctx, *, nombre):
        url = "https://api.scryfall.com/cards/named"
        params = {"fuzzy": nombre}

        r = requests.get(url, params=params)

        if r.status_code != 200:
            await ctx.send("❌ No encontré esa carta")
            return

        carta = r.json()

        if "image_uris" in carta:
            await ctx.send(carta["image_uris"]["large"])
        else:
            await ctx.send(carta["card_faces"][0]["image_uris"]["large"])

async def setup(bot):
    await bot.add_cog(MTG(bot))
