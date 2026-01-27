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
        return (
            f"🏆 {self.nombre}\n"
            f"👥 Participantes: {len(self.participantes)}/{self.max_participantes}"
            f"\n"
            f"Estado: {self.estado}\n"
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



async def setup(bot):
    await bot.add_cog(torneoCog(bot))

