import json
import os
import discord


#from dotenv import load_dotenv
from discord.ext import commands

def loadDB(dict):
  with open(f'{dict}.json') as json_file:
    return json.load(json_file)

def saveDB(name, dict):
  with open(f"{name}.json", 'w') as outfile:
    json.dump(dict, outfile)

users = loadDB('users')
games = loadDB('games')

bot = commands.Bot(command_prefix="$")

@bot.event
async def on_ready():
  await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('with Python🐍'))
  print(f'Logged on as {bot.user}!')

#Load all cogs/modules from cogs folder
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            print(filename)
            bot.load_extension(f'cogs.{filename[:-3]}')
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(f'cogs.{filename[:-3]}', exc))
            
            
#Start Bot   
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_SECRET")
bot.run(DISCORD_TOKEN, bot=True, reconnect=True)

