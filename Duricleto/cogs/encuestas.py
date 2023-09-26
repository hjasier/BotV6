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
import json

encuestas_activas = {}

ruta = "/home/bot/BotV6/Duricleto/cogs/archivos/encuestas.json"

async def updateEmbed(ctx):
    encuesta = encuestas_activas[ctx.message.id]
    
    embed=discord.Embed(title=f"{encuesta['titulo']}")

    total = sum([len(encuesta['respuestas'][vts]) for vts in encuesta['respuestas']])
    print(f"Total --> {total}")
    
    for opc in encuesta['opciones']:
        porcentaje = (len(encuesta['respuestas'][encuesta['opciones'].index(opc)])/total)*100
        prtj = "🟪" * round(porcentaje/10)
        
        embed.add_field(name=f"{opc}", value=f"{prtj}      {porcentaje}%", inline=False)
    await ctx.message.edit(embed=embed)
    embed.set_footer(text=f"Numero de votos {total}")
    
    
        
class EncuestaCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        


    def loadEncuestas():
        global encuestas_activas
        try:
            with open(ruta, 'r') as archivo:
                encuestas_activas = json.load(archivo)
        except FileNotFoundError:
            encuestas_activas = {}
    
    
    
    def updateLocalFile():
        global encuestas_activas
        try:
            with open(ruta, 'w') as archivo:
                json.dump(encuestas_activas, archivo, indent=4)
        except Exception as e:
            print(f"Error al actualizar el archivo: {str(e)}")


    @commands.hybrid_command(name="encuesta",description="Crea una encuesta")           
    @app_commands.describe(titulo="Titulo de la encuesta")
    async def encuesta(self, ctx: Context, *, titulo: str, opción1: str = None , opción2: str = None,opción3: str = None,opción4: str = None,opción5: str = None,opción6: str = None,opción7: str = None,opción8: str = None,opción9: str = None,opción10: str = None):
        opciones = [opción1, opción2, opción3, opción4, opción5, opción6, opción7, opción8, opción9, opción10]
        opciones = [opcion for opcion in opciones if opcion is not None]
        embed=discord.Embed(title=f"{titulo}")

        for opcion in opciones:
            embed.add_field(name=f"{opcion}", value="🟪      0%", inline=False)

        embed.set_footer(text="Numero de votos 0")
        encuesta_id = (titulo.replace(" ",""))[:15]



        class Selector(discord.ui.View):
            @discord.ui.select(
                placeholder = "Envia tu respuesta 📨",
                min_values = 1, 
                max_values = 1, 
                options = [discord.SelectOption(label=option) for option in opciones]
            )
            async def select_callback(self, select, interaction):
               t = select.data['values'][0]
               user_id = select.user.id
               enc_id = (t.replace(" ",""))[:15]
               

               encuesta = encuestas_activas[embedmsg.id]
               
               opcIndex = encuesta['opciones'].index(t)
                
               for opc in range(len(encuesta['opciones'])):
                    try:
                        if opc in encuesta['respuestas']:
                            if user_id in encuesta['respuestas'][opc]:
                                encuesta['respuestas'][opc].remove(user_id)
                        else:
                            encuesta['respuestas'][opc] = []
                    except:
                        pass
               encuesta['respuestas'][opcIndex].append(user_id)
               await updateEmbed(select)
                
               print(encuestas_activas)
               await select.response.defer()   

                
        embedmsg = await ctx.send(embed=embed , view=Selector())
        
        encuesta = {
            '_id':embedmsg.id,
            'titulo':titulo,
            'opciones':opciones,
            'respuestas':{},
            'author':ctx.author.id,
        }
        global encuestas_activas
        encuestas_activas[embedmsg.id] = encuesta
        
                
           




    
async def setup(client):
    await client.add_cog(EncuestaCog(client))
