import discord
from discord.ext import commands
import json
import os
import random
from __main__ import send_cmd_help
import asyncio
import datetime

from cogs.utils import checks
from .utils.dataIO import dataIO

DEFAULT = {
"name" : "Archie",
"hunger" : 0,
"boredom" : 0,
"hours" : 0,
"notdead" : True}

FILEPATH = 'data/kitten/condition.json'

class Kitten():


    def __init__(self, bot):
        self.bot = bot
        self.condition = dataIO.load_json(FILEPATH)
        self.task = self.bot.loop.create_task(self.loop())
        self.dead_check = self.bot.loop.create_task(self.dead())

       
        if "kitten" not in self.condition.keys():
            self.condition["kitten"] = {}
            for server in self.bot.servers:
                self.condition["kitten"][server.id] = DEFAULT
            dataIO.save_json("data/kitten/condition.json", self.condition)

        self.kitten = self.condition["kitten"]

    def __unload(self):
        self.task.cancel()
        self.dead_check.cancel()





    @commands.group(pass_context=True, name="kitten")
    async def _kitten(self, ctx):
        """Keep your kitten hungry and happy, or it will die."""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @_kitten.command(pass_context=True, name="name")
    async def _name(self, ctx):
        """Name your kitten."""
        server = ctx.message.server
        if self.kitten[server.id]['name'] == DEFAULT['name']:
            await self.bot.say(
                "**This is irreversible.** You are about to change the name of your kitten.\n"
                "You can cancel by typing cancel, or waiting 30s.\n"
                "What would you like to name your kitten?")

            answer = await self.bot.wait_for_message(timeout=30, author=ctx.message.author)
            answer = answer.content.title().strip()

            if "cancel" in answer:
                return await self.bot.say("You've chosen to keep the Kitten's name as {}".format(DEFAULT['name']))
            else:
                name = answer

            self.condition["kitten"][server.id]['name'] = name
            await self.bot.say("Kitten's name has been changed to {}".format(name))
        else:
            await self.bot.say("You can't rename your kitten..")

        dataIO.save_json(FILEPATH, self.kitten)

    @_kitten.command(pass_context=True, name="feed")
    async def _feed(self, ctx, feed: int):
        """Feed your kitten some treats"""
        server = ctx.message.server
        if self.kitten[server.id]['notdead'] == False:
            return await self.bot.say("You can't feed a dead kitten.")
        if feed >= 100:
            return await self.bot.say("Woah, let's not get crazy now.")

        if self.kitten[server.id]['hunger'] <= 0:
            return await self.bot.say(
                "{} is too full right now, check back later!".format(self.kitten[server.id]['name'])
                )
        else:
            if self.kitten[server.id]['hunger'] - feed <= 0:
                self.kitten[server.id]['hunger'] = 0
            else:
                self.kitten[server.id]['hunger'] -= feed
            await self.bot.say("{} is so grateful for {} treats".format(self.kitten[server.id]['name'], feed))

            
            dataIO.save_json(FILEPATH, self.condition)

    @_kitten.command(pass_context=True, name="play")
    async def _play(self, ctx):
        """Play with your kitten"""
        server = ctx.message.server
        if self.kitten[server.id]['boredom'] <= 50:
            return await self.bot.say(
                "{} is not bored, check back later!".format(self.kitten[server.id]['name'])
                )
        else:
            self.kitten[server.id]['boredom'] -= 10
            await self.bot.say("{} loves playing with you!".format(self.kitten[server.id]['name']))

            
            dataIO.save_json(FILEPATH, self.condition)
    @_kitten.command(pass_context = True, name = "condition")
    async def _cond(self, ctx):
        """Check the condition of your kitten!"""
        server = ctx.message.server
        if self.kitten[server.id]['notdead'] == False:
            return await self.bot.say("{} has died.".format(self.kitten[server.id]['name']))
        kitty = "Name: {name}\nHunger: {hunger}\nBoredom: {boredom}".format(**self.kitten[server.id])
        await self.bot.say(kitty)

    async def loop(self):
        while not self.bot.is_closed:
            for serverid in self.kitten:
                if self.kitten[serverid]["notdead"] == True:
                    self.kitten[serverid]["hours"] += 1
                    self.kitten[serverid]['hunger'] += random.randint(1, 6)
                    self.kitten[serverid]['boredom'] += random.randint(1, 10) 
                dataIO.save_json(FILEPATH, self.condition)
            else:
                pass
            await asyncio.sleep(30)
                    

    async def dead(self):
        while not self.bot.is_closed:
            for serverid in self.kitten:
                if self.kitten[serverid]['notdead'] == True:
                    if self.kitten[serverid]['hunger'] >= 100:
                        self.kitten[serverid]['hunger'] = 0
                        self.kitten[serverid]['notdead'] = False
                        await self.bot.send_message(bot.get_channel("353524868551147521", "Your kitten has died."))
                dataIO.save_json(FILEPATH, self.condition)
            await asyncio.sleep(30)
#this is a comment to let people know I lost a little sanity with this.
#all times are intended to be 3600 seconds, but 30 for testing.

# cats health goes down as hunger and boredom rise.
# not harsh on health with boredom. 

def check_folder():
    if not os.path.exists('data/kitten'):
        print('Creating kitten folder...purrr')
        os.makedirs('data/kitten')

def check_files():
    if not os.path.exists("data/kitten/condition.json"):
        print("Creating empty conditions.json...")
        dataIO.save_json("data/kitten/condition.json", DEFAULT)

def setup(bot):
    check_folder()
    check_files()

    bot.add_cog(Kitten(bot))