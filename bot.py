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
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
cluster = MongoClient(os.getenv('MONGO_URL'))

db = cluster["database"]
usersdb = db["usuarios"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = Bot(command_prefix=commands.when_mentioned_or('.'), intents=intents, help_command=None)


#-------------------------------------------------------------
#PARA SINCRONIZAR LOS COMANDOS DE BARRA STABLECER ESTO EN TRUE
sync_comandos = False
#-------------------------------------------------------------


@client.event
async def on_ready():
    print(f"¡Si ves esto {client.user.name} esta online! ")
    print("-----------------------------------")
    status_task.start()
    if sync_comandos:
        print("Sincronizando los comandos de barra, esto puede tardar bastante...")
        await client.tree.sync()


@tasks.loop(minutes=1.0)
async def status_task():
    if random.choice([0,1]) == 0:
        await client.change_presence(activity=discord.Game("embarazar a tu mai"))
    else:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a tu mai gemir"))

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user or message.author.bot:
        return
    await client.process_commands(message)




async def load_cogs():
    for filename in os.listdir('/home/disc_bot/BotV6/Duricleto/cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')







asyncio.run(load_cogs())
client.run(TOKEN)
