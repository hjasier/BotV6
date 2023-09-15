import os 
import discord
from dotenv import load_dotenv
import asyncio
import time
from discord.utils import get
from gtts import gTTS
import eyed3
import ffmpeg
import glob
import platform
import random
import aiohttp
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.app_commands import Choice
from typing import List
from mutagen.mp3 import MP3        
import pyrubberband as pyrb
from pydub import AudioSegment  
import mp3
from wave import Wave_read

cola = []
global now_playing
global global_speed
global curLang
curLang = {'lang': 'es', 'tld': 'es'}
now_playing = False

global_speed = 1

idCanalMain = 1006149775038627865
ruta = "/home/bot/BotV6/Duricleto/cogs/archivos/audios/"


idiomas_choices = [
    app_commands.Choice(name='Español (España)', value=0),
    app_commands.Choice(name='Español (México)', value=1),
    app_commands.Choice(name='Portugués (Brasil)', value=3),
    app_commands.Choice(name='Portugués (Portugal)', value=4),
    app_commands.Choice(name='Inglés (Estados Unidos)', value=6),
    app_commands.Choice(name='Inglés (India)', value=7),
    app_commands.Choice(name='Francés (Francia)', value=9),
    app_commands.Choice(name='Mandarín (Taiwán)', value=10),
    app_commands.Choice(name='Árabe', value=12),
    app_commands.Choice(name='Catalán', value=16),
    app_commands.Choice(name='Alemán', value=19),
    app_commands.Choice(name='Indonesio', value=27),
    app_commands.Choice(name='Italiano', value=29),
    app_commands.Choice(name='Japonés', value=31),
    app_commands.Choice(name='Rumano', value=46),
    app_commands.Choice(name='Ruso', value=47),
    app_commands.Choice(name='Turco', value=59),
    app_commands.Choice(name='Chino Mandarín', value=64)
]


idiomas = {
    0: {'lang': 'es', 'tld': 'es'},
    1: {'lang': 'es', 'tld': 'com.mx'},
    3: {'lang': 'pt', 'tld': 'com.br'},
    4: {'lang': 'pt', 'tld': 'pt'},
    6: {'lang': 'en', 'tld': 'us'},
    7: {'lang': 'en', 'tld': 'co.in'},
    9: {'lang': 'fr', 'tld': 'fr'},
    10: {'lang': 'zh-TW', 'tld': 'any'},
    12: {'lang': 'ar', 'tld': 'ar'},
    16: {'lang': 'ca', 'tld': 'ca'},
    19: {'lang': 'de', 'tld': 'de'},
    27: {'lang': 'id', 'tld': 'id'},
    29: {'lang': 'it', 'tld': 'it'},
    31: {'lang': 'ja', 'tld': 'ja'},
    46: {'lang': 'ro', 'tld': 'ro'},
    47: {'lang': 'ru', 'tld': 'ru'},
    59: {'lang': 'tr', 'tld': 'tr'},
    64: {'lang': 'zh-CN', 'tld': 'any'}
}


    






def get_duración(ruta_archivo):
    audio = MP3(ruta_archivo)
    duracion = audio.info.length
    return duracion

def conversor_wav_mp3(file_id):
    with open(ruta+f'{file_id}.wav', 'rb') as read_file, open(ruta+f'{file_id}.mp3', 'wb') as write_file:
        wav_file = Wave_read(read_file)
        sample_size = wav_file.getsampwidth()
        sample_rate = wav_file.getframerate()
        nchannels = wav_file.getnchannels()
        if sample_size != 2:
            raise ValueError("Only PCM 16-bit sample size is supported (input audio: %s)" % sample_size)
        encoder = mp3.Encoder(write_file)
        encoder.set_bit_rate(64)
        encoder.set_channels(nchannels)
        encoder.set_quality(5)   # 2-highest, 7-fastest
        encoder.set_mode(mp3.MODE_STEREO if nchannels == 2 else mp3.MODE_SINGLE_CHANNEL)
        while True:
            pcm_data = wav_file.readframes(8000)
            if pcm_data:
                encoder.write(pcm_data)
            else:
                encoder.flush()
                break



def editar_velocidad(file_id):
    audio = AudioSegment.from_file(ruta+f"{file_id}.mp3", format="mp3")
    final = audio.speedup(playback_speed=global_speed)
    final.export(ruta+f"{file_id}.wav", format="wav")
    conversor_wav_mp3(file_id)




def get_source(file_id):
    archivo = ruta+f"{file_id}.mp3"
    audio_source = discord.FFmpegPCMAudio(archivo)
    return audio_source






async def play_audio(voice,source,file_id):
    global now_playing
    now_playing = True
    voice.play(source)
    t = get_duración(ruta+f"{file_id}.mp3")
    await asyncio.sleep(t)
    voice.pause()
    cola.remove(file_id)
    os.remove(os.path.join(ruta, f"{file_id}.mp3"))
    if not cola == []:
        source = get_source(cola[0])
        await play_audio(voice,source,cola[0])
    else:
        now_playing = False
        await voice.disconnect()


def save_file(texto,ctx):
    slowmode = True if global_speed < 1 else False
    tts = gTTS(texto, lang=curLang['lang'],tld=curLang['tld'], slow=slowmode)
    archivo = ruta+f"{ctx.message.id}.mp3"
    tts.save(archivo)
    return ctx.message.id

def formatear_archivo(file_id):
    if global_speed > 1:
        editar_velocidad(file_id)
    return discord.FFmpegPCMAudio(ruta+f"{file_id}.mp3")





class tts_cog(commands.Cog, name="tts_cog"):
    def __init__(self, client):
        self.client = client



    @commands.hybrid_command(name="tts",description="Convierte el texto a voz")
    @app_commands.describe(mensaje="Escribe el mensaje a leer")
    async def tts(self, ctx: Context, *, mensaje: str) -> None:
        archivo = save_file(mensaje,ctx)
        cola.append(ctx.message.id)

        archivo = formatear_archivo(archivo)
        if not ctx.author.voice:
            channel = self.client.get_channel(idCanalMain)
            try:
                voice = await channel.connect()
            except:
                voice = discord.utils.get(ctx.guild.voice_channels, id=channel.id)
        else:
            try:
                voice = await ctx.message.author.voice.channel.connect()
            except:
                voice = discord.utils.get(ctx.guild.voice_channels, id=ctx.message.author.voice.channel.id)
        if not now_playing:
            try: 
                await play_audio(voice,archivo,ctx.message.id)
                embed=discord.Embed(title="", description=f"Reproduciendo mensaje ✅")
                await ctx.send(embed=embed)
            except:
                embed=discord.Embed(title="", description=f"Error leyendo mensaje, prueba a cambiar de idioma ❌")
                await ctx.send(embed=embed)
            
        

    @commands.hybrid_command(name="tts_velocidad",description="Elige la velocidad del tts")
    @app_commands.describe(velocidad="Número del 0.5 - 2 siendo 1 lo default")
    async def tts_velocidad(self, ctx: Context, *, velocidad: str) -> None:
        global global_speed
        speed = float(velocidad)
        if speed < 1:
            speed = 0.5
        elif speed > 2:
            speed = 2
        global_speed = speed
        embed=discord.Embed(title="", description=f"Velocidad ajsutada en {speed} ✅")
        await ctx.send(embed=embed)



    @commands.hybrid_command(name="tts_velocidad",description="Elige la velocidad del tts")
    @app_commands.describe(velocidad="Número del 0.5 - 2 siendo 1 lo default")
    async def tts_velocidad(self, ctx: Context, *, velocidad: str) -> None:
        global global_speed
        speed = float(velocidad)
        if speed < 1:
            speed = 0.5
        elif speed > 2:
            speed = 2
        global_speed = speed
        embed=discord.Embed(title="", description=f"Velocidad ajsutada en {speed} ✅")
        await ctx.send(embed=embed)
        
        
    @commands.hybrid_command(name="tts_idioma",description="Elige el idioma del tts")           
    @app_commands.choices(idioma=idiomas_choices) 
    async def tts_idioma(self, i: discord.Interaction, idioma:app_commands.Choice[int]):
        global curLang 
        curLang = idiomas[idioma.value]
        embed=discord.Embed(title="", description=f"{idioma.name} seteado ✅")
        await i.send(embed=embed)








async def setup(client):
    await client.add_cog(tts_cog(client))