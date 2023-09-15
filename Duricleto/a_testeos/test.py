from typing import Literal, Union, NamedTuple,List, Union
from enum import Enum
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context

from dotenv import load_dotenv
load_dotenv()
import os
TOKEN = os.getenv('DISCORD_TOKEN')


client = Bot(command_prefix=commands.when_mentioned_or('.'), intents=discord.Intents.default(), help_command=None)



@client.event
async def on_ready():
    await client.tree.sync()


class Fruits(Enum):
    miemoji = 0
    miemoji2 = 1

vars=('tx', 'ty', 'tz')  # plus plenty more
n = 1
for v in vars:
    setattr(Fruits, v, n+1)



@client.tree.command()
@app_commands.describe(fruit='Emoji a elegir')
async def emoja(interaction: discord.Interaction, fruit: Fruits):
    await interaction.response.send_message(repr(fruit))



test = Literal['Buy', 'Sell','resell','test','test2']



@client.tree.command()
@app_commands.describe(action='The action to do in the shop')
async def shop(interaction: discord.Interaction, action: test):
    await interaction.response.send_message(f'Action: {action}\n')






client.run("ODIyNTUzMDU2NDk4NTQ4Nzc3.GzbbQy.FBgfMOyfiClQG-gh3stuXH3O-VpbPDfnwHwvOo")