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
            newUsers = 0
            async for member in guild.fetch_members(limit=150):
                print(member.name)
                if not member == client.user and not member.bot and (usersdb.count_documents({"_id":member.id}) == 0):#Para que no se guarden los datos de los bots ni repetidos
                    newUsers += 1
                    print(member.name)
                    usersdb.insert_one({
                        '_id':member.id,
                        'name':member.name,
                        'tag':member.discriminator,
                        'xp':0,
                        'level':0,
                        'mensajes_hoy':0,
                        'tiempo_en_llamada':0,
                        'cur_msgs':0,
                        'personalización_rank':['#FFFFFF','#FFFFFF','#FFFFFF',0,'https://media.discordapp.net/attachments/1048018114161426493/1058422571994976327/image.png',0]})
            await ctx.send(f"se han creado {newUsers} users nuevos y se han actualizado 0 users")      
            
        @client.command()
        async def act_inf_users(ctx):
            return
            guild = ctx.guild
            ctx.message.delete()
            async for member in guild.fetch_members(limit=150):
                print(member.name)
                if not member == client.user and not member.bot:#Para que no se guarden los datos de los bots ni repetidos
                    usersdb.update_one({'_id':member.id},{"$set":{'personalización_rank':['#FFFFFF','#FFB730','#FFFFFF',0,'https://media.discordapp.net/attachments/1048018114161426493/1058422571994976327/image.png',1]}})
                     

        @client.command()
        async def act_inf_users2(ctx):
            return
            guild = ctx.guild
            ctx.message.delete()
            cusers = 0
            async for member in guild.fetch_members(limit=150):
                cusers += 1
                print(member.name)
                if not member == client.user and not member.bot:
                    curData = usersdb.find_one({'_id':member.id})
                    print(curData)
                    usersdb.update_one({'_id':member.id},{"$set":{'tiempo_en_llamada':{'2023':curData['tiempo_en_llamada']}}})
            await ctx.send(f"{cusers} users actualizados")

        @client.command()
        async def act_info_users_error(ctx):
            return
            cusers = []
            for user in usersdb.find():
                if not type(user['tiempo_en_llamada']) is dict:
                    usersdb.update_one({'_id':user['_id']},{"$set":{'tiempo_en_llamada':{'2023':user['tiempo_en_llamada']}}})
                    cusers.append(user['name'])
            await ctx.send(f"{len(cusers)} con error users actualizados {cusers}")



async def setup(client):
    await client.add_cog(gestión_users(client))
