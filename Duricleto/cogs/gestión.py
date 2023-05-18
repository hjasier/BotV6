import platform
import random
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.app_commands import Choice
import asyncio



        
        






class gestión(commands.Cog, name="Gestión"):
    def __init__(self, client):
        self.client = client


        @client.command(aliases=['garbi'])
        async def clear(ctx,num_mensajes):
            return await ctx.channel.purge(limit=int(num_mensajes)+1)

        
        #Comando Say
        @client.command(aliases=['esan'])
        async def say(ctx, *args):
            msg = ' '.join(args)
            await ctx.message.delete()
            botmsg = await ctx.send(msg)





async def setup(client):
    await client.add_cog(gestión(client))























































