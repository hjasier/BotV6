import asyncio
import platform
import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.app_commands import Choice
from typing import List
import os
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()
cluster = MongoClient(os.getenv('MONGO_URL'))
db = cluster["database"]
usersdb = db["usuarios"]


class Events(commands.Cog, name="events"):
    def __init__(self, client):
        self.client = client

        @client.event
        async def on_member_join(member):
            print(f'Nuevo miembro --> {member.name}')
            if usersdb.count_documents({"_id": member.id}) == 0:
                userdata = {
                    '_id':member.id,
                    'name':member.name,
                    'xp':0,
                    'level':0,
                    'mensajes_hoy':0,
                    'tiempo_en_llamada':{
                        '2023':0
                    },
                    'cur_msgs':0,
                    'last_vc':0,
                    'personalización_rank':['#FFFFFF','#FFFFFF','#FFFFFF',0,'https://media.discordapp.net/attachments/1048018114161426493/1058422571994976327/image.png',0]   
                }
                usersdb.insert_one(userdata)



async def setup(bot):
    await bot.add_cog(Events(bot))
