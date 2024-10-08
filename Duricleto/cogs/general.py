import asyncio
import platform
import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.app_commands import Choice
from typing import List
import os

class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot



    @commands.hybrid_command(name="help",description="Lista de todos los comandos cargados.")
    async def help(self, context: Context) -> None:
        embed = discord.Embed(
            title="🧰 Ayuda 🧰", description="Lista de todos los comandos disponibles:", color=0x9C84EF)
        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            data = []
            for command in commands:
                description = command.description.partition('\n')[0]
                data.append(f"{'.'}{command.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(name=i.capitalize(),value=f'```{help_text}```', inline=False)
        await context.send(embed=embed)





    @commands.hybrid_command(name="ping",description="Comprobar estado del bot",)
    async def ping(self, context: Context) -> None:
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"El bot está online con una latencia de {round(self.bot.latency * 1000)}ms respecto al servidor",
            color=0x9C84EF
        )
        await context.send(embed=embed)





    @commands.hybrid_command(name="8ball",description="Ask any question to the bot.",)
    @app_commands.describe(question="The question you want to ask.")
    async def eight_ball(self, context: Context, *, question: str) -> None:
        answers = ["It is certain.", "It is decidedly so.", "You may rely on it.", "Without a doubt.",
                   "Yes - definitely.", "As I see, yes.", "Most likely.", "Outlook good.", "Yes.",
                   "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
                   "Cannot predict now.", "Concentrate and ask again later.", "Don't count on it.", "My reply is no.",
                   "My sources say no.", "Outlook not so good.", "Very doubtful."]
        embed = discord.Embed(
            title="**My Answer:**",
            description=f"{random.choice(answers)}",
            color=0x9C84EF
        )
        embed.set_footer(
            text=f"The question was: {question}"
        )
        await context.send(embed=embed)





        

    @commands.hybrid_command(name="bitcoin",description="Precio actual del bitcoin",)
    async def bitcoin(self, context: Context) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.coindesk.com/v1/bpi/currentprice/BTC.json") as request:
                if request.status == 200:
                    data = await request.json(
                        content_type="application/javascript")
                    embed = discord.Embed(
                        title="Bitcoin 🪙",
                        description=f"El precio actual del bitcoin es {data['bpi']['USD']['rate']} :dollar:",
                        color=0x9C84EF
                    )
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="Ha sucedido un error :/",
                        color=0xE02B2B
                    )
                await context.send(embed=embed)



    @commands.hybrid_command(name="reiniciarmusikleto",description="Reinicia el bot de musicleto",)
    async def reiniciarMusikleto(self, ctx: Context) -> None:
        os.system("pm2 restart LavalinkServer")  
        embed=discord.Embed(title="", color=0xffbb00)
        embed.add_field(name="Bot ", value="Reiniciando 🔄", inline=False)
        embed.add_field(name="Lavalink ", value="Reiniciando 🔄", inline=True)
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(1)
        os.system("pm2 restart playerbot")  
        embed2=discord.Embed(title="", color=0xeeff00)
        embed2.add_field(name="Bot ", value="Reiniciando ✅", inline=False)
        embed2.add_field(name="Lavalink ", value="Reiniciando 🔄", inline=True)
        await msg.edit(embed=embed2)
        await asyncio.sleep(1)
        embed3=discord.Embed(title="Musikleto reiniciado ✅", color=0x66ff00)
        embed3.add_field(name="Bot ", value="Reiniciado ✅", inline=False)
        embed3.add_field(name="Lavalink ", value="Reiniciado ✅", inline=True)
        await msg.edit(embed=embed3)
        
                




    @commands.hybrid_command(name="kaixo",description="Kaixo Egun ON Zelan Zaudete",)
    async def kaixo(self, ctx: Context) -> None:
        if not ctx.author.voice:
            channel = self.client.get_channel(1006149775038627865)
            try:
                voice = await channel.connect()
            except:
                voice = discord.utils.get(ctx.guild.voice_channels, id=channel.id)
        else:
            try:
                voice = await ctx.message.author.voice.channel.connect()
            except:
                voice = discord.utils.get(ctx.guild.voice_channels, id=ctx.message.author.voice.channel.id)         

            
            file = discord.FFmpegPCMAudio("/home/bot/BotV6/Duricleto/cogs/archivos/audios/Kaixo recortado.mp3")
            voice.play(file);
            await asyncio.sleep(3)
            await voice.disconnect()



async def setup(bot):
    await bot.add_cog(General(bot))
