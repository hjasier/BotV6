import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from pymongo import MongoClient
import os
import asyncio
#--------------------------------------------------------
TOKEN = os.getenv('DISCORD_TOKEN')
cluster = MongoClient(os.getenv('MONGO_URL'))
usersdb = cluster["database"]["usuarios"]
miningdb = cluster["database"]["mining_server"]

#--------------------------------------------------------
#Esto habría que importarlo desde el main con una clase y no definirlo en cada archrivo, pero con los cogs es raro







class btn_server_mining(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


    @discord.ui.button(label="Apuntarme 🎫",custom_id="enroll_user_server_mining", style=discord.ButtonStyle.blurple)
    async def button_callback(self, button, interaction):
        usuarios = [user['_id'] for user in miningdb.find({'type':'user'})]
        if not button.user.id in usuarios:
            miningdb.insert_one({'_id':button.user.id,'type':'user','game_nick':'NotSet'})
            await button.response.send_message("¡Listo!, Mira DM para continuar", ephemeral=True)
            embed = discord.Embed(title="Establecer nombre ingame",description="Desde aquí podras añadirte a la whitelist del server con el nombre que uses en minecratf",color=0x7440FF)
            await button.user.send(embed=embed, view=btn_establecer_nombre_whitelist())
            embed = discord.Embed(title="⬇️ WHITELIST SERVER VII ABIERTA ⬇️",description=f"Jugadores inscritos: {len(usuarios)+1}",color=0x5555FF)
            await button.message.edit(embed=embed)
        else:
            await button.response.send_message("¡Ya estás inscrit@ al server!", ephemeral=True)
            return



class server_mining(commands.Cog):
    def __init__(self, client):
        self.client = client
        client.add_view(btn_server_mining()) 
         
        global btn_establecer_nombre_whitelist
        class btn_establecer_nombre_whitelist(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)
            @discord.ui.button(label="Establecer Nombre 👤",custom_id="request_server_name_change", style=discord.ButtonStyle.blurple)
            async def button_callback(self, button, interaction):
                contador = await button.user.send('Escribe a continuación tu nuevo nombre, tienes ``15`` segundos:')
                def check(m: discord.Message):  # m = discord.Message.
                    return m.author.id == button.user.id and m.channel.id == button.channel.id 
                try:
                    msg = await client.wait_for('message', check = check, timeout = 20.0)
                except asyncio.TimeoutError: 
                    await button.user.send(f"Tiempo agotado :( , vuelve a pulsar el botón para establecer tu nombre de minecraft")
                    return
                else:
                    await button.user.send(f"Tu nuevo nombre ingame es ``{msg.content}`` !")
                    miningdb.update_one({'_id':button.user.id,'game_nick':msg.content})
                    #update_whitelist()
        client.add_view(btn_establecer_nombre_whitelist())






        @client.command()
        async def inscripción_server(ctx):
            return
            embed = discord.Embed(title="⬇️ WHITELIST SERVER VII ABIERTA ⬇️",description="Jugadores inscritos: 0",color=0x5555FF)
            message = await ctx.send(embed=embed, view=btn_server_mining())




async def setup(client):
    await client.add_cog(server_mining(client))
