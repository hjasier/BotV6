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






test = {0:[3,32],3:33}

for n in test:
    print(n)

t3 = sum([2,32,3,])

print("🟪" * 3)


#client.run(TOKEN)



