import requests
from discord.ext import commands
import config


class generalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hola(self, ctx):
        await ctx.send(f"¡Hola {ctx.author.mention}! 😄")

    @commands.command()
    async def ruling(self, ctx, *, duda):
        await ctx.send("🧑‍⚖️ Consultando reglas...")

        prompt = construir_prompt_simple(duda)

        try:
            respuesta = preguntar_deepseek(prompt)
        except Exception as e:
            await ctx.send("❌ Error consultando el ruling")
            print(e)
            return

        print(respuesta)
        await ctx.send(f"🧑‍⚖️ **Ruling:**\n{respuesta}")



def construir_prompt_simple(duda):
    return f"""
        Eres un juez certificado de Magic: The Gathering.
        Responde en español, de forma clara y concisa, unos 500 Caracteres como maximo.
        Tu respuesta debe basarse en las reglas oficiales del juego.
        Si aplica, cita reglas (603, 704, 903, etc).
        
        Duda del jugador:
        {duda}
        
        Da el ruling correcto y explícalo brevemente.
        """


def preguntar_deepseek(prompt):
    url = "https://api.deepseek.com/chat/completions"

    headers = {
        "Authorization": f"Bearer {config.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()

    return r.json()["choices"][0]["message"]["content"]


async def setup(bot):
    await bot.add_cog(generalCog(bot))
