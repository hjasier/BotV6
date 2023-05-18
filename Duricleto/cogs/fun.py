import random

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands
from translate import Translator
translator= Translator(to_lang="spanish")

cur_ppt_plays = []

class Choice(discord.ui.View):
    @discord.ui.button(label="Cara", style=discord.ButtonStyle.blurple)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = "Cara"
        self.stop()

    @discord.ui.button(label="Cruz", style=discord.ButtonStyle.blurple)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = "Cruz"
        self.stop()


class ppt_btns(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="tijeras", emoji="✂"),
            discord.SelectOption(label="piedra", emoji="🪨"),
            discord.SelectOption(label="papel", emoji="🧻"),
        ]
        
        super().__init__(
            placeholder="Elige un opción...",
            min_values=1,
            max_values=1,
            options=options,
        )
        
        

    async def callback(self, interaction: discord.Interaction):
        choices = {"piedra": 0,"papel": 1,"tijeras": 2,}
        
        user_choice = self.values[0].lower()
        user_choice_index = choices[user_choice]
        
        
        
        for cur_play in cur_ppt_plays:
            if cur_play['_id'] == interaction.message.id:
                cur_value = cur_play[interaction.user.id]
                cur_play[interaction.user.id] == user_choice_index
                if cur_value == 1:
                    player_2_value = cur_play['player2']
                else:
                    player_2_value = cur_play['player1']
            if player_2_value == 'NotSet':
                return 
                #await interaction.response.edit_message
                
                
                



        result_embed = discord.Embed(color=0x9C84EF)
        result_embed.set_author(
            name=interaction.user.name,
            icon_url=interaction.user.avatar.url
        )

        if user_choice_index == player_2_value:
            result_embed.description = f"**Empate**"
            result_embed.colour = 0xF59E42
        elif user_choice_index == 0 and player_2_value == 2:
            result_embed.description = f"ha ganado el jugador 1"
            result_embed.colour = 0x9C84EF
        elif user_choice_index == 1 and player_2_value == 0:
            result_embed.description = f"ha ganado el jugador 1"
            result_embed.colour = 0x9C84EF
        elif user_choice_index == 2 and player_2_value == 1:
            result_embed.description = f"ha ganado el jugador 1"
            result_embed.colour = 0x9C84EF
        else:
            result_embed.description = f"**ha ganado el jugador 2**"
            result_embed.colour = 0xE02B2B
        await interaction.response.edit_message(embed=result_embed, content=None, view=None)


class RockPaperScissorsView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ppt_btns())


class ppt_unirse_btn(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Unirme 👊",custom_id="enroll_user_ppt", style=discord.ButtonStyle.green)
    async def button_callback(self, button, interaction):
        for cur_play in cur_ppt_plays:
            if cur_play['_id'] == button.message.id:
                cur_play[button.user.name] == 2
                cur_play['player2'] == 'NotSet'
                
        await button.message.edit(content='¡1..2..3 fuera!',view=RockPaperScissorsView())





class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command(name="datorandom",description="Te escupo un dataje random")
    async def randomfact(self, context: Context) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
                if request.status == 200:
                    data = await request.json()
                    traducido = translator.translate(data["text"])
                    embed = discord.Embed(
                        description=traducido,
                        color=0xD75BF4
                    )
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="Ha sucedido un error, prueba más tarde",
                        color=0xE02B2B
                    )
                embed.set_author(name=data["text"], icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/United-kingdom_flag_icon_round.svg/2048px-United-kingdom_flag_icon_round.svg.png')
                await context.send(embed=embed)



    @commands.hybrid_command(name="caraocruz",description="Tira una moneda")
    async def caraocruz(self, context: Context) -> None:
        buttons = Choice()
        embed = discord.Embed(description="Cual es tu apuesta",color=0x9C84EF)
        message = await context.send(embed=embed, view=buttons)
        await buttons.wait()  # Esperamos a que el usuario eliga una opc
        result = random.choice(["Cara", "Cruz"])
        embed = discord.Embed(description=f"La moneda ha caido en {result}",color=0x9C84EF)
        await message.edit(embed=embed, view=None, content=None)



    @commands.hybrid_command(name="ppt",description="Jugar a piedra papel tijera")
    async def rock_paper_scissors(self, ctx: Context) -> None:
        
        embed=discord.Embed(title="Piedra Papel Tijera Online", color=0xff66ed)
        embed.set_thumbnail(url="https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/b680a062246147.5a8a773c6932d.gif")
        embed.add_field(name="Jugador 1", value=f"{ctx.author.name} <a:emoji_name:1050058905079787631>", inline=True)
        embed.add_field(name="Jugador 2", value="Esperando <a:emoji_name:1050056882770952232>", inline=True)
        await ctx.send(embed=embed, view=ppt_unirse_btn())
        cur_ppt_plays.append({'_id':ctx.message.id,ctx.author.name:1,'player1':'NotSet'})













async def setup(bot):
    await bot.add_cog(Fun(bot))
