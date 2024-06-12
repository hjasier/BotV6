import platform
import random
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.app_commands import Choice
from typing import List
import asyncio
from easy_pil import *
import requests        
from PIL import Image,ImageDraw, ImageFilter
from PIL import features 
import io
from io import BytesIO
from discord import File
from pymongo import MongoClient
from dotenv import load_dotenv
import asyncio
import datetime
import os
import string
load_dotenv()
cluster = MongoClient(os.getenv('MONGO_URL'))
db = cluster["database"]
usersdb = db["usuarios"]
vozconxdatadb = db["vozconxdata"]



#-----------------------------------------------------------------------------------------------------------------
#            SISTEMA DE NIVELES
#-----------------------------------------------------------------------------------------------------------------

async def process_level_system(message):
    for data in usersdb.find({'_id':message.author.id}):
        contador_mensajes = data['cur_msgs'] + 1
        cur_xp = data['xp']
        level = data['level']
    if random.randint(0,5) == 3:
        print('Reward')
        random_xp = round(random.uniform(15.0,25.0),5)
        cur_xp += random_xp
        t_req_xp = 0
        for x in range(0,level+1):
            t_req_xp += (5 * (x ** 2) + (50 * x) + 100) #El total de toda la xp requerida para subir de nivel 
        if cur_xp >= t_req_xp:
            level = level+1
            await levelear_user(message,level)
    usersdb.update_one({'_id':message.author.id},{"$set":{'xp':cur_xp,'level':level,'cur_msgs':contador_mensajes}})
    
    
    
        
async def levelear_user(name,lvl):
    #await client.change_presence(activity=discord.Game("{name} ha subido a lvl {lvl}"))
    return
      
    
        
        
#-----------------------------------------------------------------------------------------------------------------        
 
        

class levels(commands.Cog, name="levels"):
    def __init__(self, client):
        self.client = client


        @client.event
        async def on_voice_state_update(member, before, after):
          #print('Evento Voz')
          if member.bot:
            return
          if not member.voice is None and member.voice.channel.id == 1006149775038627865: 
            #Si el user esta dentro del canal [Se mete]
            usersdb.update_one({'_id':member.id},{"$set":{'last_vc':datetime.datetime.now()}})
          else: #Si el user no esta en el canal [Se sale]
            for data in usersdb.find({'_id':member.id}):
              join = data['last_vc']
              cur_t = data['tiempo_en_llamada']
              cur_xp = data['xp']
              level = data['level']
            if not join == 0:
              now = datetime.datetime.now()
              diferencia = (now - join).total_seconds()
              cur_xp += (random.uniform(0.25,0.75)*diferencia)
              
              while True:
                t_req_xp = 0
                for x in range(0,level+1):
                    t_req_xp += (5 * (x ** 2) + (50 * x) + 100) #El total de toda la xp requerida para subir de nivel 
                if cur_xp >= t_req_xp:          
                  level += 1
                else:
                  break
                
              year = str(now.year)
              
              # Si 'year' no existe, lo inicializa en 0
              cur_t.setdefault(year, 0)
              
              cur_t[year] =  cur_t[year]+diferencia
              usersdb.update_one({'_id':member.id},{"$set":{'tiempo_en_llamada':cur_t,'last_vc':0,'xp':cur_xp,'level':level}})
              vozconxdatadb.insert_one({'user_id':member.id,'join':join,'leave':now})








    @commands.hybrid_command(name="rank",description="Tu rank",)
    async def rank(self, ctx: Context, *,member: discord.Member = None):
      if not member:  
        member = ctx.message.author  
      esperamsg = await ctx.send('<a:emoji_name:1058417728664387624>')
      for data in usersdb.find({'_id':member.id}):
        cur_xp = data['xp']
        cur_lvl = data['level']
        user_personalización = data['personalización_rank']
        
      user_rank = list(reversed(sorted([users_data['xp'] for users_data in usersdb.find()]))).index(cur_xp)
      t_req_xp = 0
      
      for x in range(0,cur_lvl):
        t_req_xp += (5 * (x ** 2) + (50 * x) + 100) 
      lvl_xp = (5 * ((cur_lvl)** 2) + (50 * (cur_lvl+1)) + 100)
      cur_lvl_xp = cur_xp - t_req_xp

      cur_lvl_xp_compl = round(lvl_xp-(lvl_xp-cur_lvl_xp),2)
      cur_lvl_xp_formateada =  cur_lvl_xp_compl
      user_xp = round(cur_xp,2) 

      if cur_lvl_xp_compl > 1000:
        cur_lvl_xp_formateada = str(round(cur_lvl_xp_compl/1000,2))+"k"
      if lvl_xp > 1000:
        lvl_xp_formateada = str(round(lvl_xp/1000,2))+"k"


      if user_xp > 100000:
         user_xp = str(round(user_xp/1000,1)) +"k"
      elif user_xp > 1000:
         user_xp = str(round(user_xp/1000,2)) +"k"

      #--------------Personalización--------------
      color_borde = user_personalización[0]
      color_porcentaje = user_personalización[1]
      color_datos= user_personalización[2]
      user_fondo = user_personalización[4]
      label_oscuro = user_personalización[3]
      fondo_extra = user_personalización[5]
      #-------------------------------------------
                
      percentage = ((cur_lvl_xp*100)/lvl_xp)
      if percentage < 5:
        percentage+=5
      
      response = requests.get(user_fondo)
      backimg = Image.open(BytesIO(response.content))
      background = Editor(backimg)
      
      #--------------HUD--------------
      espacio_datos = Editor('/home/bot/BotV6/Duricleto/cogs/archivos/media/test2.png')
      if label_oscuro == 1:
        sello = Editor("/home/bot/BotV6/Duricleto/cogs/archivos/media/+tgiconoIN.png")
        rank_datos = Editor("/home/bot/BotV6/Duricleto/cogs/archivos/media/label_datosIN.png")   
      else:
        sello = Editor("/home/bot/BotV6/Duricleto/cogs/archivos/media/+tgicono.png")
        rank_datos = Editor("/home/bot/BotV6/Duricleto/cogs/archivos/media/rank_datos.png")
      
        
      profile = await load_image_async(str(member.avatar))
      background = Editor(background).resize((942, 333))
      sello  = Editor(sello).resize((55, 25))
      rank_datos  = Editor(rank_datos).resize((333, 26))
      espacio_datos  = Editor(espacio_datos).resize((383, 83))
      profile = Editor(profile).resize((150, 150)).circle_image()
      
      

      unisansbold_pequeño = Font("/home/bot/BotV6/Duricleto/cogs/archivos/media/UniSansBold.otf", size=36)
      unisansbold = Font("/home/bot/BotV6/Duricleto/cogs/archivos/media/UniSansBold.otf", size=48)
      unisansbold2 = Font("/home/bot/BotV6/Duricleto/cogs/archivos/media/UniSansBold.otf", size=36)
      unisans = Font("/home/bot/BotV6/Duricleto/cogs/archivos/media/UniSansRegular.otf", size=22)
      #-------------------------------------------
      
      if fondo_extra == 1:
        background_extra = Editor("/home/bot/BotV6/Duricleto/cogs/archivos/media/fondoextra.png")
        background_extra  = Editor(background_extra).resize((919, 313))
        background.paste(background_extra.image, (14, 14))#BACKGROUND EXTRA
        
      background.paste(profile.image, (59, 77))#PERFIL
      background.paste(sello.image, (24, 25))#+TG
      background.paste(rank_datos.image, (543, 45))#RANK NIVEL XP
      background.paste(espacio_datos.image, (526, 105)).blend(background)#Rectangulo Datos como Imagen


      background.rectangle((0, 0), width=942, height=10, fill=color_borde)
      background.rectangle((0, 323), width=942, height=10, fill=color_borde)
      background.rectangle((932, 0), width=10, height=333, fill=color_borde)
      background.rectangle((0, 0), width=10, height=333, fill=color_borde)

      background.rectangle((252, 220), width=647, height=51, fill="white", radius=24)#Fondo del %
      background.bar((249, 220), max_width=650, height=51, percentage=percentage ,fill=color_porcentaje, radius=31)#%
      if len(member.name) > 8:
        background.text((244, 100), str(f'{member.name[0:13]}'), font=unisansbold_pequeño, color=color_datos)#Nombre pequeño
      else:
        background.text((244, 100), str(member.name), font=unisansbold, color=color_datos)#Nombre Grande

      #background.rectangle((526, 104), width=383, height=83, fill="white",radius=34)#Rectangulo Datos

      background.text((560, 129), f"#{user_rank+1}", font=unisansbold2, color=color_datos) #Posición en el ranking
      background.text((686, 129), f"{cur_lvl}", font=unisansbold2, color=color_datos) #Nivel user
      background.text((779, 129), f"{user_xp}", font=unisansbold2, color=color_datos) #XP del user

      background.text((746, 285), f"{cur_lvl_xp_formateada} / {lvl_xp_formateada} XP", font=unisans, color="#EEEEEE")#Restante
      file = File(fp=background.image_bytes, filename="rank.png")
      await esperamsg.delete()
      await ctx.send(file=file)



    años_choices = [
        app_commands.Choice(name='2023', value=0),
        app_commands.Choice(name='2024', value=1),
    ]














    @commands.hybrid_command(name="vozrank",description="Te envia tus estadístiacas en el canal barra",)
    @app_commands.choices(año=años_choices) 
    async def vozrank(self, ctx: Context, *,member: discord.Member = None, año:app_commands.Choice[int]=None):
      if not member:  
        member = ctx.message.author  
      if not año:
         año = str(datetime.datetime.now().year)
      else:
        año = año.name
      esperamsg = await ctx.send('<a:emoji_name:1058417728664387624>')
      
      
      for data in usersdb.find({'_id':member.id}):
        tiempo_en_llamada = data['tiempo_en_llamada'][año]
        color_borde = '#FFFFFF'
        try:
          tiempo_en_llamada = data['tiempo_en_llamada'][año]
        except KeyError:
          tiempo_en_llamada = 0  # O cualquier valor predeterminado que desees
      
      días = int(tiempo_en_llamada/60/60/24)
      horas = int(tiempo_en_llamada/3600-(días*24))
      minutos = int(tiempo_en_llamada/60 - horas*60 - días*24*60)
      segundos = int(tiempo_en_llamada - horas*3600 - días*24*3600 - minutos*60)
       
      
      user_rank = list(reversed(sorted([users_data['tiempo_en_llamada'].get(año,0) for users_data in usersdb.find()]))).index(tiempo_en_llamada) +1
      

      t_req_xp = 0

      dias_label = 'DÍAS'
      if días == 1:
        dias_label = 'DÍA'
        
      backimg = Image.open("/home/bot/BotV6/Duricleto/cogs/archivos/media/fondoVozrank.jpg")
      background = Editor(backimg)
      sello = Editor("/home/bot/BotV6/Duricleto/cogs/archivos/media/+tgicono.png")
      profile = await load_image_async(str(member.avatar))
      background = Editor(background).resize((942, 550))
      sello  = Editor(sello).resize((61, 27))
      profile = Editor(profile).resize((175, 175)).circle_image()
      unisansbold_grande = Font("/home/bot/BotV6/Duricleto/cogs/archivos/media/UniSansBold.otf", size=110)
      unisansbold_grande2 = Font("/home/bot/BotV6/Duricleto/cogs/archivos/media/UniSansBold.otf", size=140)
      unisansbold = Font("/home/bot/BotV6/Duricleto/cogs/archivos/media/UniSansBold.otf", size=50)
      unisansbold2 = Font("/home/bot/BotV6/Duricleto/cogs/archivos/media/UniSansBold.otf", size=36)
      unisans = Font("/home/bot/BotV6/Duricleto/cogs/archivos/media/UniSansRegular.otf", size=32)
      unisansmall = Font("/home/bot/BotV6/Duricleto/cogs/archivos/media/UniSansRegular.otf", size=22)

      background_extra = Editor("/home/bot/BotV6/Duricleto/cogs/archivos/media/fondoextra.png")
      background_extra  = Editor(background_extra).resize((1300, 550))
      background.paste(background_extra.image, (14, 14))#BACKGROUND EXTRA
      background.paste(profile.image, (383, 100))#PERFIL
      background.paste(sello.image, (26, 26))#+D
      background.rectangle((0, 0), width=942, height=10, fill='#fff')
      background.rectangle((0, 540), width=942, height=10, fill='#fff')
      background.rectangle((932, 0), width=10, height=550, fill='#fff')
      background.rectangle((0, 0), width=10, height=550, fill='#fff')

      background.text((305, 25), str(f'Tiempo total en #taberna-barra'), font=unisans, color='#fff')
      background.text((400, 310), str(f'{member.name[0:13]}'), font=unisansbold, color='#fff')#Nombre
      background.text((400, 380), f"{horas} horas", font=unisansbold2, color='#fff')
      background.text((400, 425), f"{minutos} minutos", font=unisansbold2, color='#fff')
      background.text((400, 475), f"{segundos} segundos ", font=unisansbold2, color='#fff')
      background.text((750, 505), str(f'Desde 01/01/{año}'), font=unisansmall, color='#fff')

      background.text((137, 195), str(f'{días}'), font=unisansbold_grande, color='#F5FF52')
      background.text((97, 315), str(f'{dias_label}'), font=unisansbold_grande, color='#F5FF52')

      background.text((693, 208), str(f'#{user_rank}'), font=unisansbold_grande2, color='#F5FF52')

      file = File(fp=background.image_bytes, filename="voz_rank.png")
      await esperamsg.delete()
      await ctx.send(file=file)




    @commands.hybrid_command(name="editar_rank",description="Te envia el link para editar tu rank",)
    async def editar_rank(self, ctx: Context):
        random_id = ''.join(random.choice(string.ascii_lowercase) for i in range(6))
        usersdb.update_one({'_id':ctx.author.id},{"$set":{'rank_passw':random_id,'name':ctx.author.name,'avatar':str(ctx.author.avatar)}})
        await ctx.author.send(f'https://embed.tabernagogorra.cat/personalizar_rank/{random_id}/{ctx.author.id}')
        await ctx.send("¡link enviado!, Mira DM para continuar <a:emoji_name:1058417728664387624>", ephemeral=True)



    @commands.hybrid_command(name="ranklist",description="test",)
    async def ranklist(self, ctx: Context):
      año = str(datetime.datetime.now().year)
      top_users = usersdb.find().sort(f"tiempo_en_llamada.{año}", -1).limit(10)
      embed=discord.Embed(title="Vozrank rank del server")
      n = 0
      for user in top_users:
        n += 1
        embed.add_field(name=f'{n}', value=f"{user['name']}", inline=False)
      await ctx.send(embed=embed)
      
      
         



    @commands.hybrid_command(name="vozstats",description="",)
    async def vozstats(self, ctx: Context, *,member: discord.Member = None):
      if not member:  
        member = ctx.message.author  
      esperamsg = await ctx.send('<a:emoji_name:1058417728664387624>')
      
      datos = list(vozconxdatadb.find({'user_id':member.id}))
      
      print(datos)
      numeroConx = len(datos)
      
      media = round(sum((conx['leave'] - conx['join']).total_seconds() for conx in datos)/numeroConx,2)

      
 
     
      #Fondo
      response = requests.get("/home/bot/BotV6/Duricleto/cogs/archivos/media/fondoVozrank.jpg")
      backimg = Image.open(BytesIO(response.content))
      background = Editor(backimg)
      
      
      #Branding
      sello = Editor("/home/bot/BotV6/Duricleto/cogs/archivos/media/+tgicono.png")
      profile = await load_image_async(str(member.avatar))
      background = Editor(background).resize((942, 550))
      sello  = Editor(sello).resize((61, 27))
      unisansbold_grande = Font("/home/bot/BotV6/Duricleto/cogs/archivos/media/UniSansBold.otf", size=110)
      unisansbold_grande2 = Font("/home/bot/BotV6/Duricleto/cogs/archivos/media/UniSansBold.otf", size=140)
      unisansbold = Font("/home/bot/BotV6/Duricleto/cogs/archivos/media/UniSansBold.otf", size=50)
      unisansbold2 = Font("/home/bot/BotV6/Duricleto/cogs/archivos/media/UniSansBold.otf", size=36)
      unisans = Font("/home/bot/BotV6/Duricleto/cogs/archivos/media/UniSansRegular.otf", size=32)
      unisansmall = Font("/home/bot/BotV6/Duricleto/cogs/archivos/media/UniSansRegular.otf", size=22)

      #userImg
      profile = Editor(profile).resize((175, 175)).circle_image()
      
      background_extra = Editor("/home/bot/BotV6/Duricleto/cogs/archivos/media/fondoextra.png")
      background_extra  = Editor(background_extra).resize((1300, 550))
      background.paste(background_extra.image, (14, 14))#BACKGROUND EXTRA
      background.paste(profile.image, (383, 100))#PERFIL
      background.paste(sello.image, (26, 26))#+TG


      background.text((305, 25), str(f'conx totales debug {numeroConx}'), font=unisans, color='#fff')
      background.text((305, 25), str(f'[debug] media {media} segundos'), font=unisans, color='#fff')




      file = File(fp=background.image_bytes, filename="vozstats.png")
      await esperamsg.delete()
      await ctx.send(file=file)




async def setup(client):
    await client.add_cog(levels(client))























































