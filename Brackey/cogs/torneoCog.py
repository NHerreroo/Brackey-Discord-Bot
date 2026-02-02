from random import random

from discord.ext import commands
import requests


# CLASE TORENO (LLEVA LA INFO DEL TORNEO)
class Torneo:
    def __init__(self, nombre, max_participantes):
        self.estado = "Esperando"
        self.nombre = nombre
        self.max_participantes = max_participantes
        self.participantes = []

    def añadir_participante(self, usuario):
        if len(self.participantes) >= self.max_participantes:
            return False
        if usuario in self.participantes:
            return False

        self.participantes.append(usuario)
        return True


    def info(self):
        nombres = [miembro.name for miembro in self.participantes]
        participantes_str = "\n".join(nombres) if nombres else "No hay participantes aún."

        return (

            f"🏆 {self.nombre}\n"
            f"👥 Participantes: {len(self.participantes)}/{self.max_participantes}\n"
            f"Estado: {self.estado}\n"
            f"\n"
            f"Lista usuarios:\n - {participantes_str}\n"

        )


#CLASE ENCARGADA DE COMANDOS
class torneoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.listaTorneos = []

    # Crear el torneo
    @commands.command()
    async def createTournament(self, ctx, max_participantes: int, *, nombre):
        torneo = Torneo(nombre, max_participantes)
        self.listaTorneos.append(torneo)

        await ctx.send(
            f"🏆 Torneo **{nombre}** creado "
            f"(máx {max_participantes} jugadores)"
        )

    # Unirse al torneo
    @commands.command()
    async def joinTournament(self, ctx, *, nombre):
        torneo = next(
            (t for t in self.listaTorneos if t.nombre == nombre),None)
        if torneo is None:
            await ctx.send("❌ No existe ese torneo")
            return

        if torneo.añadir_participante(ctx.author):
            await ctx.send(f"✅ {ctx.author.mention} se ha unido a **{nombre}**")
        else:
            await ctx.send("❌ El torneo está lleno o ya estás dentro")

    # Info torneo
    @commands.command()
    async def tournamentInfo(self, ctx, *, nombre):
        torneo = next(
            (t for t in self.listaTorneos if t.nombre == nombre),None)

        if torneo is None:
            await ctx.send("❌ No existe ese torneo")
            return

        await ctx.send(torneo.info())


    @commands.command()
    async def listTournaments(self, ctx):
        torneos = [torneo.nombre for torneo in self.listaTorneos]
        listaTorneos = "\n - ".join(torneos) if torneos else "No hay torneos aún."
        await ctx.send(
            f"Lista Torneos:\n - {listaTorneos}\n"
        )


    @commands.command()
    async def startTournament(self, ctx, *, nombre):
        torneo = next(
            (t for t in self.listaTorneos if t.nombre == nombre), None)

        if torneo is None:
            await ctx.send("❌ No existe ese torneo")
            return

        if len(torneo.participantes) < 4:
            await ctx.send("❌ No hay suficientes jugadores para empezar (mínimo 4)")
            return

        jugadores = torneo.participantes.copy()
        random.shuffle(jugadores)

        grupos = [jugadores[i:i + 4] for i in range(0, len(jugadores), 4)]

        mensaje = f"🏆 **{torneo.nombre}** ha comenzado!\n\n"

        for i, grupo in enumerate(grupos, start=1):
            nombres = ", ".join(jugador.mention for jugador in grupo)
            mensaje += f"**Grupo {i}:** {nombres}\n"

        torneo.estado = "En progreso"
        await ctx.send(mensaje)


async def setup(bot):
    await bot.add_cog(torneoCog(bot))

