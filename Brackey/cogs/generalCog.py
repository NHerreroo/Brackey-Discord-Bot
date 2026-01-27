from discord.ext import commands

class generalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hola(self, ctx):
        await ctx.send(f"¡Hola {ctx.author.mention}! 😄")

async def setup(bot):
    await bot.add_cog(generalCog(bot))
