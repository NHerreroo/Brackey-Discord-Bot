from random import random

import discord
from discord.ext import commands
import requests


# CLASE TORENO (LLEVA LA INFO DEL TORNEO)
class Torneo:
    def __init__(self, nombre, max_participantes, bracket):
        self.estado = "Esperando"
        self.bracket = bracket
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

            f"🏆  {self.nombre}\n"
            f"👥 Participantes: {len(self.participantes)}/{self.max_participantes}\n"
            f"Bracket: B{self.bracket}\n"
            f"Estado: {self.estado}\n"
            f"\n"
            f"Lista usuarios:\n - {participantes_str}\n"

        )

#CLASE PARA EL BOTON DE JOIN CON UI
class JoinTournamentView(discord.ui.View):
    def __init__(self, torneo):
        super().__init__(timeout=None)
        self.torneo = torneo

    @discord.ui.button(
        label="Unirse al torneo",
        style=discord.ButtonStyle.green,
        emoji="🏆"
    )
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):

        if self.torneo.añadir_participante(interaction.user):
            await interaction.response.send_message(
                f"✅ {interaction.user.mention} se ha unido al torneo",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ El torneo está lleno o ya estás dentro",
                ephemeral=True
            )



class ListTournamentView(discord.ui.View):
    def __init__(self, torneo):
        super().__init__(timeout=None)
        self.torneo = torneo

    @discord.ui.button(
        label="Info",
        style=discord.ButtonStyle.blurple,
        emoji="🏆"
    )
    async def info(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message(
            f"✅ {interaction.user.mention} se ha unido al torneo",
            ephemeral=True
        )




#CLASE ENCARGADA DE COMANDOS --------------------------------------------------------------
class torneoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.listaTorneos = []

    # Crear el torneo
    @commands.command()
    async def createTournament(self, ctx, max_participantes: int, bracket: int, *, nombre):
        torneo = Torneo(nombre, max_participantes, bracket)
        self.listaTorneos.append(torneo)

        embed = discord.Embed(
            title=f"**{nombre}**",
            description=f"MTG Tournament - Bracket {torneo.bracket}",
            color=discord.Color.gold()
        )

        embed.add_field(
            name="👥 Máx. participantes",
            value=str(max_participantes),
            inline=False
        )

        embed.set_footer(text=f"Creado por {ctx.author.name}")

        await ctx.send(
            f"🏆 Torneo creado! \n",
            embed=embed,
            view=JoinTournamentView(torneo)
        )

    # Unirse al torneo de forma manual
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



#MODIFICAR COMANDOS PARA HACERLO POR UI: PODER VER LA LISTA DANDO A BOTON idk estoy harto nah en v mola q  flipas esto soy hacker

async def setup(bot):
    await bot.add_cog(torneoCog(bot))

