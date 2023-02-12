import discord
from discord import app_commands
from discord.ext import commands

class UserCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # say_hi command
    @app_commands.command(name='say_hi', description="Says Hi to you")
    async def say_hi(self, interaction: discord.Interaction, name: str):

        reply = f"Hi {name}!"

        await interaction.response.send_message(reply)

    # add_numbers command
    @app_commands.command(name='add_numbers', description="Adds 2 numbers")
    async def add_numbers(self, interaction: discord.Interaction, num1: int, num2: int):

        reply = num1+num2

        await interaction.response.send_message(reply)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UserCommands(bot))
