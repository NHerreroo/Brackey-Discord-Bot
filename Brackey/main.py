import discord
from discord.ext import commands
import config
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Cog cargado: {filename}")


async def main():
    async with bot:
        await load_cogs()
        await bot.start(config.TOKEN)

asyncio.run(main())
