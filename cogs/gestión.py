import platform
import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class gestión(commands.Cog):
    def __init__(self, client):
        self.client = client

        @client.command()
        async def clear(ctx,num_mensajes):
            return await ctx.channel.purge(limit=int(num_mensajes)+1)





async def setup(client):
    await client.add_cog(gestión(client))
