import asyncio
import platform
import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.app_commands import Choice
from discord.ui import Button
from typing import List
import os

class EncuestaCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.encuestas_activas = {}

    

    @commands.hybrid_command(name="encuesta",description="Crea una encuesta")           
    @app_commands.describe(titulo="Titulo de la encuesta")
    async def encuesta(self, ctx: Context, *, titulo: str, opción1: str = None , opción2: str = None,opción3: str = None,opción4: str = None,opción5: str = None,opción6: str = None,opción7: str = None,opción8: str = None,opción9: str = None,opción10: str = None):
        opciones = [opción1, opción2, opción3, opción4, opción5, opción6, opción7, opción8, opción9, opción10]
        opciones = [opcion for opcion in opciones if opcion is not None]
        embed=discord.Embed(title=f"{titulo}")

        buttons = []
        for opcion in opciones:
            embed.add_field(name=f"{opcion}", value="🟪      0%", inline=False)
            buttons.append(Button(label=opcion, custom_id=f"opcion_{opcion}"))

        embed.set_footer(text="Numero de votos 0")
        await ctx.send(embed=embed)
        

        
           




    
async def setup(client):
    await client.add_cog(EncuestaCog(client))
