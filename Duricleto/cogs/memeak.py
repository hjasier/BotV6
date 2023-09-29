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
import requests
from bs4 import BeautifulSoup
import os
import schedule
import time
import threading
import aioschedule
import tweepy
import praw
import asyncpraw
import youtube_dl


reddit = praw.Reddit(
    client_id='-kAZ7DdW2t5SVnKr97Duag',
    client_secret='KKs68KzfJEOU7nB18oMLZh2IQYqNdQ',
    user_agent='txuklamemes'
)
ruta = "/home/bot/BotV6/Duricleto/cogs/archivos/memeak/"

def download_media(url):
    # Configura opciones para descargar el contenido multimedia
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': ruta+'media.mp4',
        'writethumbnail': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def get_reddit_meme(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    random_post = random.choice(list(subreddit.new(limit=100)))
    if random_post.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        # Si es una imagen estática, descárgala directamente
        response = requests.get(random_post.url)
        file_extension = random_post.url.split('.')[-1]
        with open(ruta+f'meme.{file_extension}', 'wb') as file:
            file.write(response.content)     
        return random_post.title, f'meme.{file_extension}'
    elif random_post.url.endswith('.mp4') and not random_post.is_video:
        response = requests.get(random_post.url)
        file_extension = random_post.url.split('.')[-1]
        with open(ruta+f'meme.{file_extension}', 'wb') as file:
            file.write(response.content)     
        return random_post.title, f'meme.{file_extension}'
    elif random_post.is_video:
        download_media(random_post.url)
        return random_post.title, 'media.mp4'
    
    else:
        print(f"No se puede descargar el contenido multimedia: {random_post.url}")
        return get_reddit_meme(subreddit_name)


def get_memea():
    horrialde_random = random.randint(1,132)
    search = f'https://memeka.eus/meme-galeria?page={horrialde_random}'
    raw_page = requests.get(search)
    formatted_page = BeautifulSoup(raw_page.content, "html.parser")

    galeriaDiv = (formatted_page.find_all("div", class_="galeria"))[0]
    memesRow = (galeriaDiv.find_all("div", class_="row"))[0]
    randomMemeNum = random.randint(0,((len(memesRow)-1)/2)-1)

    randomMemeDiv = (memesRow.find_all("div", class_="meme"))[randomMemeNum]
    randomMemeA = (randomMemeDiv.find_all("a"))[0]
    randomMemeLinka = (randomMemeA.find_all("img"))[0]
    return randomMemeLinka['src']

def get_meme():
    pag_random = random.randint(1,2500)
    search = f'https://es.memedroid.com/memes/top/ever?page={pag_random}'
    raw_page = requests.get(search)
    formatted_page = BeautifulSoup(raw_page.content, "html.parser")

    galeriaDiv = (formatted_page.find_all("div", class_="gallery-memes-container"))[0]
    totalMemes = (formatted_page.find_all("article", class_="gallery-item"))
    randomMemeNum = random.randint(0,len(totalMemes)-1)

    randomMemeDiv = totalMemes[randomMemeNum]
    memeDiv = (randomMemeDiv.find_all("div", class_="item-aux-container"))[0]

    header = (memeDiv.find_all("header"))
    video = (memeDiv.find_all("div", class_="video-container"))
    if video:
        return get_meme()
    pic = 0
    titulo = ''
    if not header == []:
        titulo = (str((memeDiv.find_all("a", class_="dyn-link"))[0].encode_contents())[2:-1])
        titulo = bytes(titulo, 'raw_unicode_escape').decode('utf-8')
        pic = 2
    memeA = (memeDiv.find_all("a", class_="dyn-link"))[pic]
    memepic = (memeA.find_all("picture"))[0]
    memeSource = (memepic.find_all("img"))[0]    
    return {'t':titulo,'s':memeSource['src']}
     





class ConfirmarDelete(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) 

    @discord.ui.button(label="❌", custom_id="cancelar_elim", style=discord.ButtonStyle.blurple)
    async def cancelar_elim_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.message.edit(view=eliminar_mensaje_btn())
        await button.response.defer()  

    @discord.ui.button(label="Fijar 📌", custom_id="fijar", style=discord.ButtonStyle.green)
    async def fijar_meme(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.message.edit(view=None)
        await button.response.defer()  

    @discord.ui.button(label="Eliminar 🗑️", custom_id="confirmar_elim", style=discord.ButtonStyle.red)
    async def confirmar_elim_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.message.delete()
        await button.response.defer()  




class eliminar_mensaje_btn(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) 


    @discord.ui.button(label="🗑️",custom_id="eliminar_mensaje", style=discord.ButtonStyle.gray)
    async def button_callback(self, button, interaction):
        await button.message.edit(view=ConfirmarDelete())
        await button.response.defer()  




class memeak(commands.Cog, name="memeak"):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler_task = None
        bot.add_view(eliminar_mensaje_btn()) 
        


    async def sendMemeaKanalara(self):
        guild = self.bot.get_guild(1006149775038627860)
        channel = guild.get_channel(1110679397964460072)
        memeLink = get_memea()
        imagen_data = requests.get(memeLink).content
        ruta = '/home/bot/BotV6/Duricleto/cogs/archivos/memeak/memea.jpg'
        with open(ruta, 'wb') as f:
            f.write(imagen_data)
        await channel.send(file=discord.File(ruta))
        os.remove(ruta)

    async def sendMemeKanalara(self):
        guild = self.bot.get_guild(1006149775038627860)
        channel = guild.get_channel(1110679397964460072)
        meme = get_meme()
        memeLink = meme['s']
        memeTitulo = meme['t']
        imagen_data = requests.get(memeLink).content
        ruta = '/home/bot/BotV6/Duricleto/cogs/archivos/memeak/memea.jpg'
        with open(ruta, 'wb') as f:
            f.write(imagen_data)
        embed = discord.Embed(title=memeTitulo)
        embed.set_image(url=f'attachment://memea.jpg')
        await channel.send(file=discord.File(ruta), embed=embed, view=eliminar_mensaje_btn()) 
        os.remove(ruta)

    async def sendRedditMemeKanalara(self):
        guild = self.bot.get_guild(1006149775038627860)
        channel = guild.get_channel(1110679397964460072)  
        randomSubreddit = random.choice(["MemesESP","orslokx","ILLOJUANOFICIAL"])
        titulo,file = get_reddit_meme(randomSubreddit)
        media = discord.File(ruta+file, filename=file)
        if not 'mp4' in file:
            embed = discord.Embed(title=titulo)
            embed.set_image(url=f'attachment://{file}')
            await channel.send(file=media, embed=embed, view=eliminar_mensaje_btn())  
        else:
            print("Enviando video")
            await channel.send(file=media)    


        os.remove(ruta+file)


    def start_scheduler(self):
        if self.scheduler_task is None:
            self.scheduler_task = asyncio.create_task(self.scheduler_loop())

    async def scheduler_loop(self):
        # Ejecutar la función cada x tiempo
        while True:
            opciones = ["memedroid","reddit"]
            pesos = [0.05, 0.95]
            choice = random.choices(opciones, weights=pesos)[0]
            if choice == "memedroid":
                await self.sendMemeKanalara()
            else:
                await self.sendRedditMemeKanalara()
            await asyncio.sleep(3600)

    @commands.Cog.listener()
    async def on_ready(self):
        self.start_scheduler()

    @commands.hybrid_command(name="memea",description="Meme bat bidaltzen dut")           
    async def memea(self, ctx: discord.Interaction):
        memeLink = get_memea()
        imagen_data = requests.get(memeLink).content
        ruta = '/home/bot/BotV6/Duricleto/cogs/archivos/memeak/memea.jpg'
        with open(ruta, 'wb') as f:
            f.write(imagen_data)
        await ctx.send(file=discord.File(ruta))
        os.remove(ruta)
        
    @commands.hybrid_command(name="meme",description="Envio un momo")           
    async def meme(self, ctx: discord.Interaction):
        meme = get_meme()
        memeLink = meme['s']
        memeTitulo = meme['t']
        imagen_data = requests.get(memeLink).content
        ruta = '/home/bot/BotV6/Duricleto/cogs/archivos/memeak/meme.jpg'        
        with open(ruta, 'wb') as f:
            f.write(imagen_data)
        if not memeTitulo== '':
            await ctx.send(f"**{memeTitulo}**")
        await ctx.send(file=discord.File(ruta))
        os.remove(ruta)
        




async def setup(bot):
    await bot.add_cog(memeak(bot))


