import discord
from discord.ext import commands
import json
import os
import random
from __main__ import send_cmd_help
import asyncio
from .utils.dataIO import dataIO


class Store():

    """
    This houses all the dicts for Kitten's reactions.
    """
    items = {
        "food": {
            "biscuit": {
                "price": 10,
                "refills": 5,
                "image": None
            },
            "catnip": {
                "price": 10,
                "refills": 5,
                "image": None
            },
            "kibble": {
                "price": 10,
                "refills": 5,
                "image": None
            },
            "tuna": {
                "price": 10,
                "refills": 5,
                "image": None
            },
            "chicken": {
                "price": 10,
                "refills": 5,
                "image": None
            },
            "die": {
                "price": 0,
                "refills": -500,
                "image": None
            },
            "live": {
                "price": 0,
                "refills": 500,
                "image": None
            }
        },
        "toys": {
            "post": {
                "price": 5,
                "fun": 5,
                "desc": "**The Scratching Post:**\nThe scratching post is a classic item for kitten to play with.",
                "image": None
            },
            "wool": {
                "price": 5,
                "fun": 5,
                "desc": "**The Bundle of Wool:**\nKittens love to play with a big ol' bundle of wool",
                "image": None
            },
            "mouse": {
                "price": 5,
                "fun": 5,
                "desc": "**The Small Toy Mouse:**\nHe chase it, he smack it, he love it!",
                "image": None
            },
            "ball1": {
                "price": 5,
                "fun": 5,
                "desc": "**The Bell Ball:**\n*tingle tingle* You may think this is the sounds of your keys, but alas it's just kitten",
                "image": None
            },
            "box": {
                "price": 5,
                "fun": 5,
                "desc": "**The Cardboard Box:**\nA favourite among kittens, what's not to love about a box?",
                "image": None
            },
            "die": {
                "price": 0,
                "fun": -500,
                "image": None
            },
            "live": {
                "price": 0,
                "fun": 500,
                "image": None
            }
        }
    }

    reactions_string = {

        "feeding": {
            "dead": [
                "You left {name} to die, and *now* you want to feed them!?"
            ],
            "item_fail": [
                "I tried to find some but it seems I don't have any {item}"
            ],
            "max": [
                "Woah, let's not get crazy now.",
                "I don't think {name} could cram that much in!"
            ],
            "full": [
                "{name} is too full right now, check back later!"
            ],
            "success": [
                "{name} is so grateful for {amount} {item}"
            ]
        },
        "playing": {
            "notbored": [
                "{name} is not bored, check back later!"
            ],
            "success": [
                "{name} loves playing with the {item}"
            ]
        }
    }

    reaction_images = {

        "eating": ["https://s-media-cache-ak0.pinimg.com/originals/ff/a5/01/ffa501668e70ffd5ff8296210497c295.gif",
                   "https://data.whicdn.com/images/104258646/original.gif",
                   "https://m.popkey.co/bd1b0e/E8pyv.gif",
                   "https://media.tenor.com/images/f9b4e97f53a1a702976b9f89ddca6815/tenor.gif",
                   "https://s-media-cache-ak0.pinimg.com/originals/28/c8/8a/28c88a2a62d598a9eab8f7d19f6b5946.gif",
                   "https://media.giphy.com/media/R52934IAVt4jK/giphy.gif",
                   "https://s-media-cache-ak0.pinimg.com/originals/11/5e/77/115e779d8cb93a09ba0cee619c95e7ab.gif",
                   "https://s-media-cache-ak0.pinimg.com/originals/cb/82/05/cb8205c6998eb9377d70820a49e24f69.gif",
                   "https://media.giphy.com/media/yDheBbdYrObTy/giphy.gif"],

        "playing": ["https://media.giphy.com/media/nKdTwjNLfUNpu/giphy.gif",
                    "https://s-media-cache-ak0.pinimg.com/originals/8b/f6/7a/8bf67aafb78c20a6364226d5c79eac87.gif",
                    "http://img46.laughinggif.com/pic/HTTP2ltYWdlczUuZmFucG9wLmNvbS9pbWFnZS9waG90b3MvMjQ4MDAwMDAvUHVzaGVlbi1wdXNoZWVuLXRoZS1jYXQtMjQ4OTczNjUtMzYwLTI4MC5naWYlog.gif",
                    "https://media.giphy.com/media/lXwEriEvWswj6/giphy.gif",
                    "https://media.giphy.com/media/jEyKIvmt0BgLC/giphy.gif",
                    "http://pa1.narvii.com/6410/61c23e3246e95c9f42c97b6579e007344678418e_hq.gif",
                    "https://media.giphy.com/media/G1h8PvAJjZr5S/giphy.gif"],

        "dead": "https://thekenyonthrill.files.wordpress.com/2014/01/meow.png"
    }

    def dead_image():
        return Store.reaction_images['dead']

    def random_reaction_image(state):
        """
        Return a random image for the [state]
        states include: playing, eating
        """

        return random.choice(Store.reaction_images[state])

    def food_image(item):
        """
        Get the image for the food [item], if there is no image
        a random eating image is returned
        """

        return Store.items['food'].get('image', random.choice(Store.reaction_images['eating']))

    def toy_image(item):
        """
        Get the image for the toy [item], if there is no image
        a random playing image is returned
        """

        return Store.items['toys'].get('image', random.choice(Store.reaction_images['playing']))

    def random_reply(state, action):
        """
        Get a reply for the <state> and <action>
        e.g. Store.random_reply('feeding', 'full')
        """
        return random.choice(Store.reactions_string[state][action])

    def get_item(type, item):
        """
        Get the information for an <item> in the items dict
        """
        return Store.items[type][item]


class Condition():
    """
    This will hold all helpers and condition
    of the kitten.
    """

    default_condition = {  # class variable shared by all instances
        "name": "Kitten",
        "hunger": 0,
        "boredom": 0,
        "hours": 0,
        # "last_fed": str(datetime.datetime.now()),  # later for datettimes
        # "last_play": str(datetime.datetime.now()),
        "notdead": True
    }

    def __init__(self, name, hunger, boredom, hours, notdead):
        self.name = name
        self.hunger = hunger
        self.boredom = boredom
        self.hours = hours
        self.notdead = notdead

    @staticmethod
    def lost_cat(ctx, data):
        server = ctx.message.server
        if server.id not in data:
            data[server.id] = Condition.default_condition
            dataIO.save_json(Kitten.filepath, data)

    @staticmethod
    def found_cat(data, server_id):
        cat = Condition(data.get(server_id).get('name'),
                        data.get(server_id).get('hunger'),
                        data.get(server_id).get('boredom'),
                        data.get(server_id).get('hours'),
                        data.get(server_id).get('notdead'))
        return cat

    def kitten_condition(self):
        easy_string = (
            'Name: {}\n'
            'Hunger: {}\n'
            'Boredom: {}\n'
            'Hours Alive: {}\n'
            'Alive: {}').format(self.name,
                                self.hunger,
                                self.boredom,
                                self.hours,
                                self.notdead)

        return easy_string


class Kitten():

    filepath = 'data/kitten/condition.json'

    def __init__(self, bot):
        self.bot = bot
        self.condition = dataIO.load_json(Kitten.filepath)
        self.task = self.bot.loop.create_task(self.kitten_growth())

    def safe_embed(self, description=None, title=None, image=None, footer=None):
        """
        This will allow me to just change colors, etc. later.
        """
        embed = discord.Embed(
            title=title,
            description=description,
            color=0xffd7d6)
        if image:
            embed.set_thumbnail(url=image)
        if footer:
            embed.set_footer(text=footer)
        return embed

    def save_file(self):
        dataIO.save_json(Kitten.filepath, self.condition)

    @commands.group(pass_context=True, name='kitten')
    async def _kittenBase(self, ctx):
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @_kittenBase.command(pass_context=True, name='condition')
    async def kittens_condition(self, ctx):
        """
        Check your kitten's condition.
        """
        Condition.lost_cat(
            ctx, self.condition)  # check if we have a kitten or not.

        server = ctx.message.server
        kitten = Condition.found_cat(self.condition, server.id)

        if kitten.notdead:
            embed = self.safe_embed(kitten.kitten_condition(), 'Meow!',
                                    image=Store.food_image(None))
        else:
            embed = self.safe_embed(
                'Your kitten has died.',
                image=Store.dead_image())

        await self.bot.say(embed=embed)

    @_kittenBase.command(pass_context=True, name='revive')
    async def revive_kitten(self, ctx):
        """
        Revive your kitten because you're a terrible owner.
        """
        Condition.lost_cat(
            ctx, self.condition)  # check if we have a kitten or not.

        author = ctx.message.author
        server = ctx.message.server
        kitten = Condition.found_cat(self.condition, server.id)

        if kitten.notdead is False:
            await self.bot.say(embed=self.safe_embed(
                ":hospital: **Your kitten is being revived, try not to kill this one.**"
                "\nAre you sure you are prepared to take care of a kitten? (Yes/No)"))

            answer = await self.bot.wait_for_message(timeout=15, author=author)

            if answer is None or answer.content.lower() != "yes":
                return await self.bot.say(embed=self.safe_embed(
                    description="**Okay, {} won't be revived. Disgraceful.**".format(kitten.name),
                    image=Store.dead_image()))
            else:
                await self.bot.say(embed=self.safe_embed(
                    description="**Okay! Your kitten has been revived.**",
                    image=Store.food_image(None)))
                #save new state here
                # should we maybe use the defaults ? Allows name change then.
                self.condition[server.id] = Condition.default_condition
                self.save_file()
                return
        else:
            return await self.bot.say(embed=self.safe_embed(
                description="**{} is not dead.**".format(kitten.name),
                image=Store.food_image(None)))

    @_kittenBase.command(pass_context=True, name='name')
    async def name_kitten(self, ctx, name):
        """
        Set your kitten's name. This can only be done once.
        Choose carefully. Meow. :cat:
        """
        Condition.lost_cat(
            ctx, self.condition)  # check if we have a kitten or not.

        server = ctx.message.server
        kitten = Condition.found_cat(self.condition, server.id)
        AliasCog = self.bot.get_cog('Alias')

        if kitten.name == 'Kitten':
            self.condition[server.id]['name'] = name
            await self.bot.say(embed=self.safe_embed(
                description="**Kitten's name changed to {}**".format(name)))
            self.save_file()
            # self.bot.remove_command('kitten name')
            await ctx.invoke(AliasCog._add_alias, name, to_execute="kitten")
        else:
            await self.bot.say(embed=self.safe_embed(
                "You've already chosen your Kitten's name. It's {}".format(kitten.name)))

    @_kittenBase.command(pass_context=True, name='feed')
    async def feed_kitten(self, ctx, food):
        """Feed your kitten."""

         # TODO: integrate economy

        Condition.lost_cat(
            ctx, self.condition)  # check if we have a kitten or not.

        server = ctx.message.server
        kitten = Condition.found_cat(self.condition, server.id)

        if kitten.hunger <= 15:
            return await self.bot.say(
                embed=self.safe_embed("**{} is too full right now!**".format(kitten.name)))

        if food not in Store.items.get('food'):
            await self.bot.say(embed=self.safe_embed('**Whoops! That\'s not a correct food item.**'))
        else:
            info = Store.get_item('food', food)
            price = info.get('price')
            refills = info.get('refills')
            if kitten.hunger - refills <= 0:
                self.condition[server.id]['hunger'] = 0

             # TODO: maybe complex checking where if kitten is not hungry
             #       it will only eat 3 out of 5 food or something,
             #       if it is still really hungry he keeps meowing
             #       stuff like that

            e_img = Store.food_image(food)
            e_title = "You've gave {} some {}!".format(kitten.name, food)
            author = ctx.message.author
            e_desc = "*nom nom*\nThanks {}, for the {}!".format(author.display_name, food)
            embed = self.safe_embed(
                        title=e_title,
                        description=e_desc,
                        image = e_img)

            await self.bot.say(embed=embed)
        self.save_file()

    @_kittenBase.command(pass_context=True, name='play')
    async def play_with_kitten(self, ctx, toy):
        """
        Play with your Kitten!
        """

         # TODO: integrate economy

        Condition.lost_cat(
            ctx, self.condition)  # check if we have a kitten or not.

        server = ctx.message.server
        kitten = Condition.found_cat(self.condition, server.id)
        condition = self.condition.get(ctx.message.server.id)

        if toy not in Store.items.get('toys'):
            await self.bot.say(embed=self.safe_embed(
                "**Whoops! Couldn't find that toy.**"))
        else:

            info = Store.get_item('toys', toy)
            price = info.get('price')
            refills = info.get('fun')

            if kitten.boredom - refills <= 0:
                condition['boredom'] = 0
            else:
                condition['boredom'] -= refills

            e_img = Store.toy_image(toy)
            e_title = "You've bought {} some {}!".format(condition['name'], toy)
            author = ctx.message.author
            e_desc = "*Meoow*\nThanks {}, for the {}!".format(author.display_name, toy)

            embed = self.safe_embed(
                        title=e_title,
                        description=e_desc)
            embed.set_thumbnail(url=e_img)

            await self.bot.say(embed=embed)
        self.save_file()

    @_kittenBase.command(pass_context=True, name='store')
    async def store_for_kitty(self, ctx):
        """
        List of items to feed / play with you Kitten.
        """
        Condition.lost_cat(
            ctx, self.condition)  # check if we have a kitten or not.

        server = ctx.message.server
        kitten = Condition.found_cat(self.condition, server.id)

        food_list = []
        toy_list = []

        for k, v in Store.items.get('food').items():
            food = "**{}** | Refills: {}".format(k.title(), v.get('price'), v.get('refills'))
            food_list.append(food)

        for k, v in Store.items.get('toys').items():
            toys = "**{}** | Fun: {}".format(k.title(), v.get('fun'))
            toy_list.append(toys)

        embed = self.safe_embed(title='The Store')
        embed.add_field(value="\n".join(food_list), name="Food")
        embed.add_field(value="\n".join(toy_list), name="Toys")
        await self.bot.say(embed=embed)

# loopy mc loopface
    async def kitten_growth(self):
        kitten = self.condition
        while not self.bot.is_closed:
            for server in kitten:
                chance = random.randint(0, 10)
                if kitten[server].get('notdead') and chance < 3:
                    if kitten[server].get('hunger') < 100:
                        kitten[server]['boredom'] += random.randint(
                            0, 6)
                        kitten[server]['hours'] += 1
                        kitten[server]['hunger'] += random.randint(
                            0, 8)
                        self.save_file()
                        if kitten[server].get('hunger') >= 100:
                            kitten[server]['notdead'] = False
                            self.save_file()
                    else:
                        pass
                if kitten[server].get('hunger') >= 100:
                    kitten[server]['notdead'] = False
                    self.save_file()
                else:
                    pass
            await asyncio.sleep(30)

    def __unload(self):
        self.task.cancel()

def scratch_post():
    if not os.path.exists('data/kitten'):
        print('Creating kitten folder...purrr')
        os.makedirs('data/kitten')
    if not os.path.exists("data/kitten/condition.json"):
        print("Scratching in empty conditions.json...")
        dataIO.save_json("data/kitten/condition.json", {})


def setup(bot):
    scratch_post()
    bot.add_cog(Kitten(bot))
