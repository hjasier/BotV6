import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.utils import get
from pymongo import MongoClient
import os

#--------------------------------------------------------
TOKEN = os.getenv('DISCORD_TOKEN')
cluster = MongoClient(os.getenv('MONGO_URL'))
usersdb = cluster["database"]["usuarios"]


#--------------------------------------------------------
#Esto habría que importarlo desde el main con una clase y no definirlo en cada archrivo, pero con los cogs es raro


class gestión_users(commands.Cog, name="gestión_users"):
    def __init__(self, client):
        self.client = client

        #Updatear_Base_De_Datos_Usuarios
        @client.command()
        async def updatear_us(ctx):
            return
            guild = ctx.guild
            ctx.message.delete()
            async for member in guild.fetch_members(limit=150):
                print(member.name)
                if not member == client.user or not member.bot:#Para que no se guarden los datos de los bots
                    usersdb.insert_one({
                        '_id':member.id,
                        'name':member.name,
                        'tag':member.discriminator,
                        'xp':0,
                        'level':0,
                        'mensajes_hoy':0,
                        'tiempo_en_llamada':[0,0,0]})
                     




async def setup(client):
    await client.add_cog(gestión_users(client))
