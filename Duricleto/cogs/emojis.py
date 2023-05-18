import platform
import random
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.app_commands import Choice
from typing import Literal, Union, NamedTuple,List
import asyncio
import re


regex = r":(\w+):"


def getEmoji(string):
    coincidencia = re.search(regex, string)
    if coincidencia:
        palabra = coincidencia.group(1)
        return palabra
    

async def procesarEmoji(client,message):
    emoji = getEmoji(message.content)
    e = discord.utils.get(client.emojis, name=emoji)
    if e.animated:
        await message.delete()
        webhook = await message.channel.create_webhook(name=message.author.name)
        frase = re.sub(regex, f"<a:{e.name}:{e.id}>", message.content)
        await webhook.send(str(frase), username=message.author.name, avatar_url=message.author.avatar)
        await asyncio.sleep(3)
        await webhook.delete()

def get_embed(page, pages):
    emojis = pages[page]
    embed = discord.Embed()
    embed.set_author(name="Emojis Disponibles")
    for emoji in emojis:
        embed.add_field(name=f"<a:{emoji.name}:{emoji.id}>", value=emoji.name, inline=True)
    embed.set_footer(text=f"Página {page + 1}/{len(pages)}")
    return embed


emojiArray = Literal['apl', 'permaban', 'mining', 'italibaguet', 'blowjob', 'lul', 'paesoestan', 'paja1', 'italibaget', 'Italibaget', 'pichula_xd', 'sad', 'simp_animado', 'regalo', 'load1', 'lloros', 'examendemorgado', 'gayv2', 'examendeirene', 'loro', 'stonksa', 'thonk', 'dowarrownemoji']


class EmojiCog(commands.Cog, name="emojiCog"):
    def __init__(self, bot):
        self.bot = bot
        
        @bot.tree.command()
        @app_commands.describe(emoji='Emoji animado a enviar')
        async def emoji(ctx: Context, emoji: emojiArray):
            #await ctx.response.defer()
            await ctx.response.send_message(f"Enviando emoji", ephemeral=True)
            e = discord.utils.get(ctx.client.emojis, name=emoji)
            webhook = await ctx.channel.create_webhook(name=ctx.user.name)
            await webhook.send(str(f"<a:{e.name}:{e.id}>"), username=ctx.user.name, avatar_url=ctx.user.avatar)
            await asyncio.sleep(3)
            await webhook.delete()
            


    @commands.hybrid_command(name="emojis", description="Lista de Emojis Disponibles")
    async def emojis(self, ctx: Context):
        emojis = []
        for guild in self.bot.guilds:
            for e in guild.emojis:
                emojiNames = [emoji.name for emoji in emojis]
                if e.animated and e.name not in ['waiting', 'carga', 'load2', 'failed', 'succed', 'check', 'waiting2', 'si_animado', 'no_animado', 'tik_animado']+emojiNames:
                    emojis.append(e)

        if not emojis:
            await ctx.send("No hay emojis disponibles.")
            return

        items_per_page = 25
        pages = [emojis[i:i + items_per_page] for i in range(0, len(emojis), items_per_page)]

        current_page = 0
        embed = get_embed(current_page, pages)

        message = await ctx.send(embed=embed)
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

        
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️"]

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                if str(reaction.emoji) == "➡️" and current_page < len(pages) - 1:
                    current_page += 1
                    embed = get_embed(current_page, pages)
                    await message.edit(embed=embed)
                elif str(reaction.emoji) == "⬅️" and current_page > 0:
                    current_page -= 1
                    embed = get_embed(current_page, pages)
                    await message.edit(embed=embed)
                await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                break


        





async def setup(bot):
    await bot.add_cog(EmojiCog(bot))
