import os
import discord
from discord.ext import commands
import logging

# Gets token from a file
from dotenv import load_dotenv
load_dotenv('tokens/discord_token.env')
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

#handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

class MyBot(commands.Bot):

    def __init__(self):

        intents = discord.Intents().default()

        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=intents,
            status=discord.Status.online, 
            activity=discord.Game("/help")
        )

        self.initial_extensions = [
            "cogs.OwnerCommands",
            "cogs.UserCommands"
        ]   

    async def setup_hook(self):

        for ext in self.initial_extensions:
            await self.load_extension(ext)

    async def close(self):
        await super().close()
        await self.session.close()


    async def on_ready(self):
        print(f'{self.user} has connected to Discord')

bot = MyBot()
bot.run(DISCORD_TOKEN)
#bot.run(DISCORD_TOKEN, log_handler=handler, log_level=logging.DEBUG)
