import platform
import random
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.app_commands import Choice
from typing import List
import googletrans
from googletrans import Translator
import asyncio
from enum import Enum



euskaraldia_status = True


async def check_mahi_language(message):
    if not euskaraldia_status:return
    if not len(message.content.split()) > 2:return
    translator = Translator()
    hizk = translator.detect(message.content)
    if not hizk.lang == 'eu':
        await message.delete()
        esaldiberri = translator.translate(message.content, dest='eu')
        abisu = await message.channel.send('mahi honetan euskaraz eitten dugu 😡')
        webhook = await message.channel.create_webhook(name=message.author.name)
        await webhook.send(str(esaldiberri.text), username=message.author.name, avatar_url=message.author.avatar)
        await asyncio.sleep(3)
        await abisu.delete()
        await webhook.delete()
        
        




class gestión_slash(commands.Cog, name="general2"):
    def __init__(self, bot):
        self.bot = bot
        
    
    euskaraldia_status = True
    
    def get_status():
        print(euskaraldia_status)
        return euskaraldia_status


    

        
    @commands.hybrid_command(name="euskaraldia",description="Euskaraz ekiteko garaia ezarpena")           
    @app_commands.choices(egoera=[app_commands.Choice(name='Itzali', value=0),app_commands.Choice(name='Piztu', value=1),]) 
    async def euskaraldia(self, i: discord.Interaction, egoera:app_commands.Choice[int]):
        global euskaraldia_status
        
        if egoera.value == 0:
            await i.channel.send('Euskaraldia itzali da')
            euskaraldia_status = False
        else:
            await i.channel.send('Euskaraldia piztu da')
            euskaraldia_status = True
        print(euskaraldia_status)





async def setup(bot):
    await bot.add_cog(gestión_slash(bot))
