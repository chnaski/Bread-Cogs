import discord
import aiohttp
from discord.ext import commands
from .utils import checks
try:
    from PIL import Image, ImageDraw, ImageFont, ImageColor, WebPImagePlugin
    pil_available = True
except:
    pil_available = False


class RIP:
    """RIP a user onto a gravestone"""

    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(pass_context=True)
    async def rip(self, ctx, user:discord.Member):
        """Make a gravestone from a @mention"""

        avatar_image = Image
        a = user.avatar_url
        fnt = ImageFont.truetype('data/drawing/font.ttf', 37)

        async with aiohttp.get(a) as r:
            image = await r.content.read()
        with open('data/rip/avatar.png','wb') as f:
            f.write(image) # I guess there is an easier way

        avatar_image = Image.open('data/rip/avatar.png').convert('RGBA')

        fig = Image.open('data/rip/gravestone.png')

        process = Image.new('RGBA', (600,600), (0,0,0,0)) #transparent

        draw = ImageDraw.Draw(process)        

        process.paste(fig, (0,0)) # gravestone
        author_width = fnt.getsize(" " + user.name)[0] # username on the gravestone
        # process.paste(avatar_image, 125, 285) //// Doesn't work
        draw.text((600 - author_width - 125, 265), " " + user.name, font=fnt, fill=(0,0,0))
        process.save('data/rip/temp.png','PNG', quality=100)

        await self.bot.send_file(ctx.message.channel, 'data/rip/temp.png')

def setup(bot):
    if pil_available is False:
        raise RuntimeError("You don't have Pillow installed, run\n```pip3 install pillow```And try again")
        return
    bot.add_cog(RIP(bot))