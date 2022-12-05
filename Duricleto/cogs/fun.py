import random

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands
from translate import Translator
translator= Translator(to_lang="spanish")

class Choice(discord.ui.View):
    @discord.ui.button(label="Cara", style=discord.ButtonStyle.blurple)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = "Cara"
        self.stop()

    @discord.ui.button(label="Cruz", style=discord.ButtonStyle.blurple)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = "Cruz"
        self.stop()


class RockPaperScissors(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Scissors", description="You choose scissors.", emoji="✂"
            ),
            discord.SelectOption(
                label="Rock", description="You choose rock.", emoji="🪨"
            ),
            discord.SelectOption(
                label="paper", description="You choose paper.", emoji="🧻"
            ),
        ]
        super().__init__(
            placeholder="Choose...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        choices = {
            "rock": 0,
            "paper": 1,
            "scissors": 2,
        }
        user_choice = self.values[0].lower()
        user_choice_index = choices[user_choice]

        bot_choice = random.choice(list(choices.keys()))
        bot_choice_index = choices[bot_choice]

        result_embed = discord.Embed(color=0x9C84EF)
        result_embed.set_author(
            name=interaction.user.name,
            icon_url=interaction.user.avatar.url
        )

        if user_choice_index == bot_choice_index:
            result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0xF59E42
        elif user_choice_index == 0 and bot_choice_index == 2:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x9C84EF
        elif user_choice_index == 1 and bot_choice_index == 0:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x9C84EF
        elif user_choice_index == 2 and bot_choice_index == 1:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x9C84EF
        else:
            result_embed.description = f"**I won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0xE02B2B
        await interaction.response.edit_message(embed=result_embed, content=None, view=None)


class RockPaperScissorsView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(RockPaperScissors())


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
    async def rock_paper_scissors(self, context: Context) -> None:
        view = RockPaperScissorsView()
        await context.send("Elije tu respuesta", view=view)












async def setup(bot):
    await bot.add_cog(Fun(bot))
