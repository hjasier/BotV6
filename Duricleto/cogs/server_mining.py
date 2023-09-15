import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.utils import get
from pymongo import MongoClient
import os
import asyncio
from googleapiclient.discovery import build
import requests
from bs4 import BeautifulSoup
import random
import json
import time


#--------------------------------------------------------
TOKEN = os.getenv('DISCORD_TOKEN')
cluster = MongoClient(os.getenv('MONGO_URL'))
usersdb = cluster["database"]["usuarios"]
miningdb = cluster["database"]["mining_server"]

#--------------------------------------------------------
#Esto habría que importarlo desde el main con una clase y no definirlo en cada archrivo, pero con los cogs es raro

mcserver = '2a11547d'



votos_reiniciar = []


def get_foto_google(search):
    api_key = 'AIzaSyDuYdzy5dKj-inDAlQX7oHFG151CtXgYG0'
    ran = random.randint(0, 9)
    resource = build('customsearch', 'v1', developerKey=api_key).cse()
    result = resource.list(q=f'{search}',cx='013d682ac094eda30',searchType="image").execute()
    url = result['items'][ran]['link']
    return url

def get_mod_description(mod_name):
    final_search = ''
    if ' ' in mod_name:
        splitted_name = mod_name.split(' ')
        for x in range(len(splitted_name)):
            final_search+= '+'+splitted_name[x] if not x==0 else splitted_name[x]
    else:
        final_search = mod_name
    mod_subfix = '+Mod' if not 'mod' in mod_name.lower() else ''
    search = f'https://www.minecrafteo.com/?s={final_search}{mod_subfix}'
    raw_page = requests.get(search)
    formatted_page = BeautifulSoup(raw_page.content, "html.parser")
    results = (formatted_page.find_all("header", class_="entry-header"))[0]
    results = results.find_all("a")
    for link in results:
        link_url = link["href"]
        break
    raw_page = requests.get(link_url)
    formatted_page = BeautifulSoup(raw_page.content, "html.parser")
    results = (formatted_page.find_all("div", class_="entry-content"))[0]
    descripción = str(results.find_all("p")[0])[:-4][3:]
    link_url = search
    descripción = ''
    results = {'url':link_url,'descripción':str(descripción)}
    return results




async def mod_suggestion_formatter(message):
    await message.delete()
    mod_img = get_foto_google(f'Minecraft {message.content} mod logo')
    título = message.content if (not '(' in message.content) else (message.content.split('(')[0])
    mod_data = get_mod_description(título)
    color = random.choice([0xFF5733,0xbbdb39,0x6258fe,0xd19af9,0x16c370,0x4877f6])
    embed=discord.Embed(title=f'MOD: {título.capitalize()}',url=mod_data['url'], description=mod_data['descripción'], color=color)
    if '(' in message.content:
        embed.add_field(name="Extra", value=f"{message.content.split('(')[1][:-1]}", inline=False)
    embed.set_thumbnail(url=mod_img)
    
    formatted_mod = await message.channel.send(embed=embed)
    print(message.author.name)

    
    
    

class btn_server_mining(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        

    @discord.ui.button(label="Apuntarme 🎫",custom_id="enroll_user_server_mining", style=discord.ButtonStyle.blurple)
    async def button_callback(self, button, interaction):
        #return await button.response.send_message("La whitelist ha sido desactivada, se activará el 19 de diciembre <a:emoji_name:1049804966627393567>", ephemeral=True)
        usuarios = [user['_id'] for user in miningdb.find({'type':'user'})]
        if not button.user.id in usuarios:
            miningdb.insert_one({'_id':button.user.id,'type':'user','game_nick':'NotSet'})
            await button.response.send_message("¡Listo!, Mira DM para continuar <a:emoji_name:1049804966627393567>", ephemeral=True)
            embed2=discord.Embed(title="Instrucciones Para el Acceso Al Server", url='https://docs.tabernagogorra.eu/', description="Estas son las instrucciones paso por paso para acceder al server , desde instalar minecraft hasta instalar los mods.", color=0xe1ff00)
            embed2.set_thumbnail(url='https://media.discordapp.net/attachments/829496216807145502/1056600080989294652/1200px-Icon-doc.png?width=599&height=756')
            embed3=discord.Embed(title="Información - Normas y Mods Primera Semana", url='https://docs.tabernagogorra.eu/programacion', description="Durante la primera semana , algunos de los mods estarán deshabilitados pese ha estar incluidos en el ModPack y en el server, para saber que mods están disponibles podeis consultar la guía semana por semana en el siguiente link", color=0x8624ff)
            embed3.set_thumbnail(url='https://media.discordapp.net/attachments/829496216807145502/1056601597578330212/745139.png')
            await button.user.send(embed=embed2)
            await button.user.send('https://docs.tabernagogorra.eu')
            await button.user.send(embed=embed3)
            embed = discord.Embed(title="Establecer nombre ingame",description="Desde aquí podrás añadirte a la whitelist del server con el nombre que uses en minecratf",color=0x7440FF)
            await button.user.send(embed=embed, view=btn_establecer_nombre_whitelist())
            await update_lista()
            role = get(button.guild.roles, id=1047818594693697619)
            await button.user.add_roles(role)
                        
        else:
            await button.response.send_message("¡Ya estás inscrit@ al server! <a:emoji_name:1049804966627393567>", ephemeral=True)
            return


class btn_reiniciar_server(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) 



    @discord.ui.button(label="Votar reinicio server 🔄 ",custom_id="votar_reiniciar_server", style=discord.ButtonStyle.red)
    async def button_callback(self, button, interaction):
        global votos_reiniciar
        votos_reiniciar.append({'_id':button.user.id})
        if len(votos_reiniciar) >= 1:
            await enviar_confirmación_reinicio()
            reiniciar_servidor_MC()
            votos_reiniciar = []
        await updatear_contador_reinicio()
        await button.response.send_message("voto registrado ;) <a:emoji_name:1049804966627393567>", ephemeral=True)
    
        



        
        



class server_mining(commands.Cog):
    def __init__(self, client):
        self.client = client
        client.add_view(btn_server_mining()) 
        client.add_view(btn_reiniciar_server()) 

      
        
         
        global btn_establecer_nombre_whitelist
        class btn_establecer_nombre_whitelist(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)
            @discord.ui.button(label="Establecer Nombre 👤",custom_id="request_server_name_change", style=discord.ButtonStyle.blurple)
            async def button_callback(self, button, interaction):
                if button.channel.type != discord.ChannelType.private:
                    await button.response.send_message("¡Listo!, Mira DM para continuar <a:emoji_name:1049804966627393567>", ephemeral=True)
                else:
                    await button.response.defer()          
                contador = await button.user.send('<a:emoji_name:1049804966627393567> Escribe a continuación tu nuevo nombre, tienes ``15`` segundos:')
                for data in miningdb.find({'_id':button.user.id}):
                    old_name = data['game_nick']

                def check(m: discord.Message):  # m = discord.Message.
                    return m.author.id == button.user.id and m.channel.type == discord.ChannelType.private
                try:
                    msg = await client.wait_for('message', check = check, timeout = 20.0)
                except asyncio.TimeoutError: 
                    await button.user.send(f"Tiempo agotado :( , vuelve a pulsar el botón para establecer tu nombre de minecraft")
                    return
                else:
                    if not miningdb.count_documents({'game_nick':msg.content}) == 0:
                        return await button.user.send('Ya existe un jugador con ese nombre en el servidor, vuelve a pulsar el botón y elige un nuevo nick')
                    embed=discord.Embed(description=f"Estado de tu solicitud [Cambio de nombre] - [{msg.content}]",color=0x2cb6ce)
                    embed.add_field(name="Nombre in-game", value="Esperando 🔄", inline=True)
                    embed.add_field(name="Whitelist", value="Esperando 🔄", inline=True)
                    conf = await button.user.send(embed=embed) 
                    try:
                        miningdb.update_one({'_id':button.user.id},{"$set":{'game_nick':msg.content}})
                        new_valor = 'Actualizado <a:emoji_name:1050058902852620369>'
                    except:
                        new_valor = 'Error <a:emoji_name:1050058900868698232>'
                        
                    embed=discord.Embed(description=f"Estado de tu solicitud [Cambio de nombre] - [{msg.content}]",color=0x2cb6ce)
                    embed.add_field(name="Nombre in-game", value=new_valor, inline=True)
                    embed.add_field(name="Whitelist", value="Esperando <a:emoji_name:1049804966627393567>", inline=True) 
                    embed.set_footer(text="Puede que no puedas entrar al server hasta que se reinicie")
                    await conf.edit(embed=embed) 
                    await update_lista()
                    resp = update_whitelist(msg.content,old_name)
                    if resp == 204:
                        new_valor2 = 'Actualizado <a:emoji_name:1050058902852620369>'
                    else:
                        new_valor2 = f'Error <a:emoji_name:1050058900868698232> Ref.[{resp.status_code}]'
                    embed=discord.Embed(description=f"Estado de tu solicitud [Cambio de nombre] - [{msg.content}]",color=0x2cb6ce)
                    embed.add_field(name="Nombre in-game", value=new_valor, inline=True)
                    embed.add_field(name="Whitelist", value=new_valor2, inline=True) 
                    await conf.edit(embed=embed) 

        client.add_view(btn_establecer_nombre_whitelist())
        
        

        global update_lista
        async def update_lista():
            usuarios = []
            for usuario in miningdb.find({"type":"user"}):
                usuarios.append(usuario)
            embed = discord.Embed(title="<a:emoji_name:1050058902852620369> WHITELIST SERVER VII ABIERTA <a:emoji_name:1050058902852620369>",description=f"Jugadores inscritos: {len(usuarios)}",color=0x5555FF)
            guild = client.get_guild(1006149775038627860)
            for usuario in usuarios:
                if guild.get_member(usuario['_id']) is not None: #esta en el server    
                    game_nick = usuario['game_nick']
                    disc_nick = client.get_user(usuario['_id']).name
                    embed.add_field(name= (disc_nick), value=(game_nick), inline=True)
                else: #no esta en el server
                    miningdb.delete_one({'_id':usuario['_id']})
                    
            channel = client.get_channel(1047988791199137902)
            mensaje = await channel.fetch_message(1048192302012702780)
            await mensaje.edit(embed=embed)
            
            
        @client.command()
        async def updatear_lista(ctx):
            await update_lista()

        @client.command()
        async def jugadores(ctx):
            embed=discord.Embed(title="Lista de jugadores del servidor", description="El nombre de Discord y su nick in-game", color=0x00db7c)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1047831865505099806/1049695071521488916/98.png")

            for usuario in miningdb.find({"type":"user"}):
                game_nick = usuario['game_nick']
                try:
                    disc_nick = client.get_user(usuario['_id']).name
                except:
                    disc_nick = "Perfil Privado"
                embed.add_field(name= (disc_nick), value=(game_nick), inline=True)
            await ctx.send(embed=embed)    
            
        @client.command()
        @commands.has_permissions(administrator=True)
        async def quitar_whitelist(ctx,usuario:discord.Member):
            miningdb.delete_one({'_id':usuario.id})
            mining_rol = get(ctx.guild.roles, id=1047818594693697619)
            await usuario.remove_roles(mining_rol)
            await update_lista()
            await ctx.send(usuario.name + 'ha sido eliminado de la whitelist')
           
            
        @client.command()
        async def reiniciar_btn(ctx):
            return
            embed=discord.Embed(title='Reiniciar el Server', color=0xf12727)
            cur_votos = 0
            embed.add_field(name='\u200b', value=f'{cur_votos}/3', inline=True)
            embed.set_footer(text='Cuando la votación llege a 3/3 el server se reiniciara')
            await ctx.send(embed=embed)
            message = await ctx.send(embed=embed, view=btn_reiniciar_server())        

        global updatear_contador_reinicio
        async def updatear_contador_reinicio():
            embed=discord.Embed(title='Reiniciar el Server', color=0xf12727)
            embed.add_field(name='\u200b', value=f'{len(votos_reiniciar)}/1', inline=True)
            embed.set_footer(text='Cuando la votación llege a 1/1 el server se reiniciará')
            channel = client.get_channel(1049806428380069918)
            mensaje = await channel.fetch_message(1049981811247304744)
            await mensaje.edit(embed=embed)
            
        
                

        global enviar_confirmación_reinicio
        async def enviar_confirmación_reinicio():
            for usuario in votos_reiniciar:
                user = client.get_user(usuario['_id'])
                await user.send('El servidor está siendo reiniciado ;) <a:emoji_name:1049804966627393567>')




       

        @client.command()
        async def anunciar_actualización_mods_a_versión(ctx,*versión):
            versión = ' '.join(versión)
            embed=discord.Embed(title=f"**Versión de Mods Actual** --> ``{versión}``",url="https://docs.tabernagogorra.eu/mods", color=0xdaff24)
            embed.set_footer(text="Si no sabes como actualizar los mods haz click en el título para ir a la guía de instalación de mods",icon_url="https://media.discordapp.net/attachments/1048018114161426493/1050754754248196176/output-onlinegiftools_2.gif")
            channel = client.get_channel(1049806428380069918)
            mensaje = await channel.fetch_message(1051134515873054742)
            await mensaje.edit(embed=embed)
            embed=discord.Embed(title=f"**Nueva Actualización Mods Server ``{versión}``**", url="https://docs.tabernagogorra.eu/mods", description="Para poder acceder al server es necesario que tengas la última versión de los mods instalada",color=0xcdff05)
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1048018114161426493/1050754388748140554/output-onlinegiftools_1.gif?width=1196&height=897")
            embed.set_footer(text="Si no sabes como actualizar los mods haz click en el botón para ir a la guía de actualización",icon_url="https://media.discordapp.net/attachments/1048018114161426493/1050754754248196176/output-onlinegiftools_2.gif")

            [await client.get_user(user['_id']).send(embed=embed) for user in miningdb.find({'type':'user'})]
            #if user['_id']== 404342594940960779 else None
        
        

        @client.command()
        async def anunciar_estreno_server_user(ctx,user:discord.Member):
            embed1=discord.Embed(title="Inauguración Server VII", description="¡¡ El server empieza oficialmente hoy, día 25 a las 17:40 !!", color=0xff00dd)
            embed2=discord.Embed(title="Instrucciones Para el Acceso Al Server", url='https://docs.tabernagogorra.eu/', description="Estas son las instrucciones paso por paso para acceder al server , desde instalar minecraft hasta instalar los mods.", color=0xe1ff00)
            embed2.set_thumbnail(url='https://media.discordapp.net/attachments/829496216807145502/1056600080989294652/1200px-Icon-doc.png?width=599&height=756')
            embed3=discord.Embed(title="Información - Normas y Mods Primera Semana", url='https://docs.tabernagogorra.eu/programacion', description="Durante la primera semana , algunos de los mods estarán deshabilitados pese ha estar incluidos en el ModPack y en el server, para saber que mods están disponibles podeis consultar la guía semana por semana en el siguiente link", color=0x8624ff)
            embed3.set_thumbnail(url='https://media.discordapp.net/attachments/829496216807145502/1056601597578330212/745139.png')
            await user.send(embed=embed1)
            await user.send(embed=embed2)
            await user.send('https://docs.tabernagogorra.eu')
            await user.send(embed=embed3)
            await user.send('https://docs.tabernagogorra.eu/programacion')
            print(f'Enviado a {user.name}')

            
        @client.command()
        async def anunciar_estreno_server(ctx,):
            return
            embed1=discord.Embed(title="Inauguración Server VII", description="¡¡ El server empieza oficialmente hoy, día 25 a las 17:40 !!", color=0xff00dd)
            embed2=discord.Embed(title="Instrucciones Para el Acceso Al Server", url='https://docs.tabernagogorra.eu/', description="Estas son las instrucciones paso por paso para acceder al server , desde instalar minecraft hasta instalar los mods.", color=0xe1ff00)
            embed2.set_thumbnail(url='https://media.discordapp.net/attachments/829496216807145502/1056600080989294652/1200px-Icon-doc.png?width=599&height=756')
            embed3=discord.Embed(title="Información - Normas y Mods Primera Semana", url='https://docs.tabernagogorra.eu/programacion', description="Durante la primera semana , algunos de los mods estarán deshabilitados pese ha estar incluidos en el ModPack y en el server, para saber que mods están disponibles podeis consultar la guía semana por semana en el siguiente link", color=0x8624ff)
            embed3.set_thumbnail(url='https://media.discordapp.net/attachments/829496216807145502/1056601597578330212/745139.png')
            for user in miningdb.find({'type':'user'}):
                    user = client.get_user(user['_id'])
                    await user.send(embed=embed1)
                    await user.send(embed=embed2)
                    await user.send('https://docs.tabernagogorra.eu')
                    await user.send(embed=embed3)
                    await user.send('https://docs.tabernagogorra.eu/programacion')
                    print(f'Enviado a {user.name}')






        @client.command()
        async def reiniciar_contador_reiniciar(ctx):
            await updatear_contador_reinicio()

        @client.command()
        async def contar_mods(ctx):
            messages = [message async for message in ctx.guild.get_channel(1048676891902611496).history(limit=200)]
            await ctx.send(f'**Hay ``{len(messages)}`` mods en el canal <#1048676891902611496>**')





        


            
















async def setup(client):
    await client.add_cog(server_mining(client))
        
    
    
def update_whitelist(name,old):
    data = {"grant_type": "client_credentials","client_id": os.getenv('PUFFER_CLIENT_ID'),"client_secret": os.getenv('PUFFER_TOKEN')}
    r = requests.post(f"https://servers.tabernagogorra.eu/oauth2/token", data=data)    
    new_whitelist = []
    for usuario in miningdb.find({'type':'user'}):
        user_ui = requests.get(f"http://tools.glowingmines.eu/convertor/nick/{usuario['game_nick']}").json()
        new_whitelist.append({'uuid':user_ui['offlinesplitteduuid'],'name':usuario['game_nick']})
    
    #with open(f'/var/lib/pufferpanel/servers/{mcserver}/whitelist.json', 'w') as archivo:
        #json.dump(new_whitelist, archivo)

    headers = {'accept': 'application/json','Content-Type': 'application/json','Authorization':"Bearer " + r.json()["access_token"]}
    if not old == 'NotSet':
        requests.post(f"https://servers.tabernagogorra.eu/proxy/daemon/server/{mcserver}/console", headers=headers,data=f'whitelist remove {old}')
    resp = requests.post(f"https://servers.tabernagogorra.eu/proxy/daemon/server/{mcserver}/console", headers=headers,data=f'whitelist add {name}')

    return 204
        


def reiniciar_servidor_MC():
    data = {"grant_type": "client_credentials","client_id": os.getenv('PUFFER_CLIENT_ID'),"client_secret": os.getenv('PUFFER_TOKEN')}
    r = requests.post(f"https://servers.tabernagogorra.eu/oauth2/token", data=data)
    headers = {'accept': 'application/json','Content-Type': 'application/json','Authorization':"Bearer " + r.json()["access_token"]}
    requests.post(f"https://servers.tabernagogorra.eu/proxy/daemon/server/{mcserver}/stop", headers=headers)
    time.sleep(0.3)
    resp = requests.post(f"https://servers.tabernagogorra.eu/proxy/daemon/server/{mcserver}/start", headers=headers)
    return 204
  
  
  
  
  
  
  
  
  
  
  
        
    
"""        @client.command()
        async def inscripción_server(ctx):
            return
            embed = discord.Embed(title="⬇️ WHITELIST SERVER VII ABIERTA ⬇️",description="Jugadores inscritos: 0",color=0x5555FF)
            message = await ctx.send(embed=embed, view=btn_server_mining())"""