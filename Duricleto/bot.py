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
from cogs.general import calc_dias_desde_7_11_2023
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
    status_task.start()
    if sync_comandos:
        print("Sincronizando los comandos slash, esto puede tardar bastante...")
        await client.tree.sync(guild=discord.Object(id=718522569820602468))
        await client.tree.sync()
    else:
        print('Los comandos slash no están siendo sincronizados')


def checkEmoji(string):
    regex = r":\b\w+\b:"
    coincidencias = re.findall(regex, string)
    return len(coincidencias) > 0




@tasks.loop(minutes=1.0)
async def status_task():
    if random.choice([0,1]) == 0:
        await client.change_presence(activity=discord.Game("embarazar a tu mai"))
    else:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a tu mai gemir"))



@client.event
async def on_message(message: discord.Message):
    if message.author.bot or message.guild is None:
        return
    if message.content.startswith('.'):
        await client.process_commands(message)
    elif checkEmoji(message.content):
        await procesarEmoji(client,message)
    elif message.author == client.user or message.author.bot:
        return
    elif message.channel.id == 1048676891902611496:
        await mod_suggestion_formatter(message)
    elif message.channel.id == 1047817172677840926:
         if not  message.attachments:
            await check_mahi_language(message)
    elif message.guild.id == 1006149775038627860:
        await process_level_system(message)
    elif message.channel.id == 1176064861353017454:
        await calc_dias_desde_7_11_2023(message)
    else:
        await client.process_commands(message)



# Esto carga los archivos en la carpeta cogs
async def load_cogs():
    for filename in os.listdir('/home/bot/BotV6/Duricleto/cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')










asyncio.run(load_cogs())
client.run(TOKEN)