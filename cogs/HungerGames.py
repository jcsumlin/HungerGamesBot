import os, sys, discord, platform, random, aiohttp, json
from discord.ext import commands

if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config


class HungerGames(commands.Cog, name="HungerGames"):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="tribute")
    async def tribute(self, context):
        pass

    @tribute.command(name="add")
    async def __add(self, context, name, image):
        pass


def setup(bot):
    bot.add_cog(HungerGames(bot))
