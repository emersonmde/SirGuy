from discord.ext import commands


class Text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        """Says hello"""
        await ctx.send('Hello {}'.format(ctx.author.display_name))
