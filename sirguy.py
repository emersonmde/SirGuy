import yaml
from discord.ext import commands
from cogs.Text import Text
from cogs.Music import Music


# TODO: Use env vars instead of yml
with open('options.yml', 'r') as options_stream:
    try:
        options = yaml.safe_load(options_stream)
    except yaml.YAMLError as err:
        print('Error reading options.yml')
        exit(1)

if 'token' not in options:
    print('Error: No bot token found in options.yml')
    exit(1)

# discord.opus.load_opus('SirGuy')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Sir Guy of Gisbourne has arrived')

bot.add_cog(Text(bot))
bot.add_cog(Music(bot))
bot.run(options['token'])
