import discord
from discord import app_commands
from discord.ext import commands
from utils.constants import owner_list
from typing import Optional, Literal


class OwnerCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    #Command which Loads a Module. Remember to use dot path. e.g: cogs.owner
    @commands.command(name='load')
    @commands.is_owner()
    async def load_cog(self, ctx: commands.Context, *, cog: str):
        try:
            await self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    #Command which Unloads a Module. Remember to use dot path. e.g: cogs.owner
    @commands.command(name='unload')
    @commands.is_owner()
    async def unload_cog(self, ctx: commands.Context, *, cog: str):
        try:
            await self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    #Command which Reloads a Module. Remember to use dot path. e.g: cogs.owner
    @commands.command(name='reload')
    @commands.is_owner()
    async def reload_cog(self, ctx: commands.Context, *, cog: str):
        try:
            await self.bot.unload_extension(cog)
            await self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')


# sync the owner_commands only in the BotTest Server
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        OwnerCommands(bot),
        guild = discord.Object(id=695553825494532127))
