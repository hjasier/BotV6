import requests
from bs4 import BeautifulSoup
import asyncio
import json
import os
import platform
import random
import sys
import aiosqlite
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from cogs.server_mining import mod_suggestion_formatter
from cogs.emojis import procesarEmoji
from cogs.euskaraldia import check_mahi_language
from cogs.levels import process_level_system
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.app_commands import Choice
import re
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
cluster = MongoClient(os.getenv('MONGO_URL'))

db = cluster["database"]
usersdb = db["usuarios"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True



client = Bot(command_prefix=commands.when_mentioned_or('.'), intents=intents, help_command=None)


#-------------------------------------------------------------
#PARA SINCRONIZAR LOS COMANDOS DE BARRA ESTABLECER ESTO EN TRUE
sync_comandos = True
#-------------------------------------------------------------







@client.event
async def on_ready():
    print(f"¡Si ves esto {client.user.name} esta online! ")
    print("-----------------------------------")
    if sync_comandos:
        print("Sincronizando los comandos slash, esto puede tardar bastante...")
        await client.tree.sync(guild=discord.Object(id=718522569820602468))
        await client.tree.sync()
    else:
        print('Los comandos slash no están siendo sincronizados')






test = {'1156154783124688928': {'_id': 1156154783124688928, 'titulo': 'asdfasdf', 'opciones': ['sadf', 'asdf'], 'respuestas': {'0': [404342594940960779], '1': []}, 'author': 404342594940960779, 'chnnl': 718522569820602471}, '1156164781984731207': {'_id': 1156164781984731207, 'titulo': 'asdf', 'opciones': ['asdfa'], 'respuestas': {'0': [404342594940960779]}, 'author': 404342594940960779, 'chnnl': 718522569820602471}}



print(test[1156154783124688928])


#client.run(TOKEN)



