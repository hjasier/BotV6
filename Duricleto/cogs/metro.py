import platform
import random
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.app_commands import Choice
from typing import List
import asyncio
import requests        
from pymongo import MongoClient
from dotenv import load_dotenv
import asyncio
import datetime
import os
import string
load_dotenv()
cluster = MongoClient(os.getenv('MONGO_URL'))
db = cluster["database"]
usersdb = db["usuarios"]
metrodb = db["metro"]







def getProxMetros(salida,direcci0n):
    search = f'https://api.metrobilbao.eus/metro/real-time/{salida}/{direcci0n}'
    return requests.get(search)

        
        
#-----------------------------------------------------------------------------------------------------------------        
 
        

class metro(commands.Cog, name="metro"):
    def __init__(self, client):
        self.client = client
        
        
        
        
        
        
        
        
async def setup(client):
    await client.add_cog(metro(client))






