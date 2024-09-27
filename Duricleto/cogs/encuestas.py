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
    for opc in encuesta['opciones']:
        porcentaje = (len(encuesta['respuestas'][str(encuesta['opciones'].index(opc))])/total)*100
        prtj = "🟪" * round(porcentaje/10)
        
        embed.add_field(name=f"{opc}", value=f"{prtj}      {porcentaje}%", inline=False)
    embed.set_footer(text=f"Numero de votos {total}")
    await ctx.message.edit(embed=embed)
    updateLocalFile()
    

async def votar_callback(select, embedmsg, encuestas_activas):
    t = select.data['values'][0]
    user_id = select.user.id
    enc_id = (t.replace(" ",""))[:15]
    encuesta = encuestas_activas[embedmsg.id]
    
    opcIndex = encuesta['opciones'].index(t)
    
    for opc in range(len(encuesta['opciones'])):
        try:
            if str(opc) in encuesta['respuestas']:
                if user_id in encuesta['respuestas'][str(opc)]:
                    encuesta['respuestas'][str(opc)].remove(user_id)
            else:
                encuesta['respuestas'][str(opc)] = []
        except:
            pass
    
    encuesta['respuestas'][str(opcIndex)].append(user_id)
    await updateEmbed(select)
    await select.response.defer()
    
def loadEncuestas():
    global encuestas_activas
    try:
        with open(ruta, 'r') as archivo:
            encuestas_activas = json.load(archivo)
            encuestas_activas = {int(key): value for key, value in encuestas_activas.items()}
    except FileNotFoundError:
        encuestas_activas = {}
loadEncuestas()


def updateLocalFile():
    global encuestas_activas
    try:
        with open(ruta, 'w') as archivo:
            json.dump(encuestas_activas, archivo, indent=4)
    except Exception as e:
        print(f"Error al actualizar el archivo: {str(e)}")
        
class EncuestaCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    

        
    async def reloadEncuestas(self):
        for encuesta in encuestas_activas:
            encuesta = encuestas_activas[encuesta]
            print("Relodeando encuesta ")
            channel = self.client.get_channel(int(encuesta['chnnl']))
            msg = await channel.fetch_message(int(encuesta['_id']))
            
            class Selector(discord.ui.View):
                @discord.ui.select(
                    placeholder = "📨 Elige tu respuesta 📨",
                    min_values = 1, 
                    max_values = 1, 
                    options = [discord.SelectOption(label=option) for option in encuesta['opciones']]
                )
                async def select_callback(self, select, interaction):
                    await votar_callback(select, msg, encuestas_activas)      
            await msg.edit(view=Selector())
            
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.reloadEncuestas()

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
                placeholder = "Elige tu respuesta 📨",
                min_values = 1, 
                max_values = 1, 
                options = [discord.SelectOption(label=option) for option in opciones]
            )
            async def select_callback(self, select, interaction):
               await votar_callback(select, embedmsg, encuestas_activas)

                
        embedmsg = await ctx.send(embed=embed , view=Selector())
        
        encuesta = {
            '_id':embedmsg.id,
            'titulo':titulo,
            'opciones':opciones,
            'respuestas':{},
            'author':ctx.author.id,
            'chnnl':ctx.channel.id
        }
        global encuestas_activas
        encuestas_activas[embedmsg.id] = encuesta
        
        
    @commands.hybrid_command(name="encuestas",description="Lista y pointers a las encuestas")           
    async def encuestas(self,ctx):
        embed = discord.Embed(title="Lista de encuestas activas")
        for enc in encuestas_activas:
            encuesta = encuestas_activas[enc]
            embed.add_field(name='\u200b', value=f'**{encuesta["titulo"]}** ➼ [``[ - Ir -]``](https://discord.com/channels/{encuesta["chnnl"]}/1006149775038627862/{encuesta["_id"]})'  , inline=False)
        
        await ctx.send(embed=embed)
            
        
    @commands.hybrid_command(name="sinoreact",description="Añade :thumbsup: :thumbsdown:  al mensaje anterior")           
    async def sinoreact(self,ctx):
        channel = ctx.channel
        
        # Usar el historial del canal para obtener los últimos dos mensajes
        messages = []
        async for message in channel.history(limit=2):
            messages.append(message)
        
        if len(messages) > 1:
            # El primer mensaje es el comando 'vota', el segundo es el mensaje anterior
            previous_message = messages[1]
            
            # Añadir las reacciones al mensaje anterior
            await previous_message.add_reaction('👍')
            await previous_message.add_reaction('👎')

        else:
            await ctx.send("No se encontró un mensaje anterior.")

                    
           




    
async def setup(client):
    await client.add_cog(EncuestaCog(client))
