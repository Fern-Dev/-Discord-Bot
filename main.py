import discord
import random
import time
import os
import math
import asyncio
import json

from dotenv import load_dotenv
from discord.ext import commands
from collections import OrderedDict 
from operator import getitem

def loadDB(dict):
  with open(f'{dict}.json') as json_file:
    return json.load(json_file)

def saveDB(name, dict):
  with open(f"{name}.json", 'w') as outfile:
    json.dump(dict, outfile)


load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_BOT_SECRET")

bot = commands.Bot(command_prefix="$")

users = loadDB('users')
games = loadDB('games')


@bot.event
async def on_ready():
  await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('with Python🐍'))
  print(f'Logged on as {bot.user}!')


bot.remove_command('help')
@bot.command()
async def help(ctx):
  embed=discord.Embed(color=0xf0f40b)
  embed.add_field(name="🎲 Game commands", value="`coinflip`, `jackpot`, `highlow`", inline=False)
  embed.add_field(name="⚙️ Other commands", value="`balance`, `top`, `daily`, `search` \n\nBot prefix is: $", inline=True)
  await ctx.channel.send(embed=embed)



##########################################################################################################
#███╗░░░███╗██╗░██████╗░█████╗░███████╗██╗░░░░░██╗░░░░░░█████╗░███╗░░██╗███████╗░█████╗░██╗░░░██╗░██████╗#
#████╗░████║██║██╔════╝██╔══██╗██╔════╝██║░░░░░██║░░░░░██╔══██╗████╗░██║██╔════╝██╔══██╗██║░░░██║██╔════╝#
#██╔████╔██║██║╚█████╗░██║░░╚═╝█████╗░░██║░░░░░██║░░░░░███████║██╔██╗██║█████╗░░██║░░██║██║░░░██║╚█████╗░#
#██║╚██╔╝██║██║░╚═══██╗██║░░██╗██╔══╝░░██║░░░░░██║░░░░░██╔══██║██║╚████║██╔══╝░░██║░░██║██║░░░██║░╚═══██╗#
#██║░╚═╝░██║██║██████╔╝╚█████╔╝███████╗███████╗███████╗██║░░██║██║░╚███║███████╗╚█████╔╝╚██████╔╝██████╔╝#
#╚═╝░░░░░╚═╝╚═╝╚═════╝░░╚════╝░╚══════╝╚══════╝╚══════╝╚═╝░░╚═╝╚═╝░░╚══╝╚══════╝░╚════╝░░╚═════╝░╚═════╝░#
##########################################################################################################  
@bot.command()
async def top(ctx):
  string ='```md\nTOP 10\n======\n```'
  
  res = OrderedDict(sorted(users.items(), key = lambda x: getitem(x[1], 'balance'), reverse=True)) 

  i = 1
  for k,v in res.items():
    if v['balance'] != 0 and i <= 10:
      name = await bot.fetch_user(int(k))
      string = f'{string[0:len(string)-3]}{i}.  < {str(name)} > - ${int(res[str(k)]["balance"])} \n```'
      i += 1

  await ctx.channel.send(string)

@bot.command()
async def balance(ctx):
  value = 0

  try:
    value = int(users[str(ctx.author.id)]['balance'])
  except KeyError: 
    users[str(ctx.author.id)] = {
        'balance' : 1000,
        'daily_time_left' : 0.0
    }
    saveDB('users', users)
    value = int(users[str(ctx.author.id)]['balance'])

  embed = discord.Embed(
  title = f'BALANCE: ${value}',
  colour = discord.Colour.green()
  )

  embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

	# SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
  await ctx.channel.send(embed = embed)

@bot.command()
async def daily(ctx):
  time_stamp = 0.0

  try:
    time_stamp = float(users[str(ctx.author.id)]['daily_time_left'])
  except KeyError: 
    users[str(ctx.author.id)] = {
        'balance' : 1000,
        'daily_time_left' : 0.0
    }
    saveDB('users', users)
    time_stamp = 0.0
    time_left = float(time.time() - time_stamp)

  if float(time.time() - time_stamp) >= 86400:
    users[str(ctx.author.id)]['balance'] = int(users[str(ctx.author.id)]['balance']) + 500
    users[str(ctx.author.id)]['daily_time_left'] = time.time()
    saveDB('users', users)

    remainging_balance = int(users[str(ctx.author.id)]['balance'])

    embed = discord.Embed(
    title = f'DAILY BONUS: $500 CLAIMED',
    description = f'New Balance: ${remainging_balance}',
    colour = discord.Colour.green()
    )
    
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

    await ctx.channel.send(embed = embed)
  else:
    time_left = 86400 - float(time.time() - time_stamp)
    time_left = time_left % (24 * 3600)
    hour = int(time_left // 3600)
    time_left %= 3600
    minutes = int(time_left // 60)
    time_left %= 60
    seconds = int(time_left) 

    embed = discord.Embed(
    title = f'ERROR: ALREADY CLAIMED',
    description = f'Time Remaining: **{hour:02d}**:**{minutes:02d}**:**{seconds:02d}**',
    colour = discord.Colour.red()
    )

    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

    await ctx.channel.send(embed = embed)

@bot.command()
async def search(ctx):
  balance = 0

  try:
    balance = int(users[str(ctx.author.id)]['balance'])
  except KeyError: 
    users[str(ctx.author.id)] = {
        'balance' : 1000,
        'daily_time_left' : 0.0
    }
    balance = int(users[str(ctx.author.id)]['balance'])
    saveDB('users', users)

  if balance == 0:
    found =  random.randint(50,75)
    users[str(ctx.author.id)]['balance'] = int(users[str(ctx.author.id)]['balance']) + found
    saveDB('users', users)

    embed = discord.Embed(
    title = f'SEARCH: ${found} CLAIMED',
    description = f'New Balance: ${users[str(ctx.author.id)]["balance"]}',
    colour = discord.Colour.green()
    )
    
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

    await ctx.channel.send(embed = embed)
  else:
    embed = discord.Embed(
    title = f'ERROR: Balance must be $0',
    colour = discord.Colour.red()
    )

    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

    await ctx.channel.send(embed = embed)



@bot.command()
async def set_balance(ctx, arg, arg2):
  if str(ctx.author.id) == '167432518914539521':
    users[str(arg)]['balance'] = int(arg2)
    saveDB('users', users)
    await ctx.channel.send(f'Set {arg}\'s balance: {arg2}')

##########################################################
#  ░█████╗░░█████╗░██╗███╗░░██╗███████╗██╗░░░░░██╗██████╗░#
#  ██╔══██╗██╔══██╗██║████╗░██║██╔════╝██║░░░░░██║██╔══██╗#
#  ██║░░╚═╝██║░░██║██║██╔██╗██║█████╗░░██║░░░░░██║██████╔╝#
#  ██║░░██╗██║░░██║██║██║╚████║██╔══╝░░██║░░░░░██║██╔═══╝░#
#  ╚█████╔╝╚█████╔╝██║██║░╚███║██║░░░░░███████╗██║██║░░░░░#
#  ░╚════╝░░╚════╝░╚═╝╚═╝░░╚══╝╚═╝░░░░░╚══════╝╚═╝╚═╝░░░░░#
###########################################################
@bot.command()
async def coinflip(ctx, arg):

  bet = float(arg)
  bet = math.floor(bet)
  bet = int(bet)

  balance = 0

  try:
    balance = int(users[str(ctx.author.id)]['balance'])
  except KeyError: 
    users[str(ctx.author.id)] = {
      'balance' : 1000,
      'daily_time_left' : 0.0
    }
    saveDB('users', users)
    balance = int(users[str(ctx.author.id)]['balance'])

  if balance >= bet and bet > 0:
    embed = discord.Embed(
    title = f'COINFLIP: ${bet}',
    description = 'Press ✅ to join.',
    colour = discord.Colour.blue()
    )

    embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/coin-flip.gif')
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

    message = await ctx.channel.send(embed = embed)
    games[str(message.id)] = {
        'type' : 'coinflip',
        'channel' : str(ctx.channel.id),
        'creator' : str(ctx.author.id),
        'started' : False,
        'bet' : int(bet)
    }
    saveDB('games', games)
    await message.add_reaction('✅')
  else:
    embed = discord.Embed(
    title = f'ERROR: Insufficent Funds',
    description = f'Remaining: {balance}',
    colour = discord.Colour.red()
    )

    embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/coin-flip.gif')
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

    await ctx.channel.send(embed = embed)


@bot.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name == "✅" and payload.user_id != bot.user.id:
      messageID = payload.message_id
      for id,v in games.items():
        if id == str(messageID) and v['type'] == 'coinflip':
          channel = bot.get_channel(int(v['channel']))
          message = await channel.fetch_message(int(id))

          if str(v['creator']) != str(payload.user_id):
            user_original = await bot.fetch_user(int(v['creator']))
            user_opponent = await bot.fetch_user(payload.user_id)

            opponent_balance = 0

            try:
              opponent_balance = int(users[str(user_opponent.id)]['balance'])
            except KeyError: 
              users[str(user_opponent.id)] = {
                  'balance' : 1000,
                  'daily_time_left' : 0.0
              }
              saveDB('users', users)
              opponent_balance = int(users[str(user_opponent.id)]['balance'])

            if opponent_balance < int(v['bet']):
              embed = discord.Embed(
              title = f'ERROR: Insufficent Funds',
              description = f'Remaining: {opponent_balance:.2f}',
              colour = discord.Colour.red()
              )

              embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/coin-flip.gif')
              embed.set_author(name=user_opponent.name, icon_url=user_opponent.avatar_url)

              await channel.send(embed = embed) 
              return

            if int(users[str(user_original.id)]['balance']) < int(v['bet']):
              new_bal = int(users[str(user_original.id)]['balance'])
              embed = discord.Embed(
              title = f'GAME CANCELED: Creator has Insufficent Funds',
              description = f'Remaining Creator Balance: {new_bal}',
              colour = discord.Colour.red()
              )

              embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/coin-flip.gif')
              embed.set_author(name=user_opponent.name, icon_url=user_opponent.avatar_url)

              await message.edit(embed = embed)

              del games[str(id)]
              saveDB('games', games)
              return

            if (v['started'] == True):
              return
            v['started'] = True
          
            user_original_avatar = user_original.avatar_url
            user_opponent_avatar = user_opponent.avatar_url

            #Generates Winning Ticket 
            ticket_number = random.random()

            if ticket_number <= 0.5:
              #Player 1

              users[str(user_original.id)]['balance'] = int(users[str(user_original.id)]['balance']) + int(v['bet'])
              users[str(user_opponent.id)]['balance'] = int(users[str(user_opponent.id)]['balance']) - int(v['bet'])
              saveDB('users', users)

              embed = discord.Embed(
              title = f"COINFLIP: ${v['bet']}",
              description = 'In Progress',
              colour = discord.Colour.blue()
              )

              embed.add_field(name='Player 1:', value =f'{user_original.mention}')
              embed.add_field(name='Player 2:', value =f'{user_opponent.mention}')

              embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/coin-flip.gif')
              embed.set_image(url='https://media1.giphy.com/media/51Upkuhc9bYruR9fn6/giphy.gif')
              embed.set_author(name=user_original.name, icon_url=user_original_avatar)

              await message.edit(embed = embed)

              time.sleep(3)

              embed = discord.Embed(
              title = f"COINFLIP: ${v['bet']}",
              description = f'{user_original.mention} **WINS**',
              colour = discord.Colour.green()
              )

              embed.add_field(name='Player 1:', value =f'{user_original.mention}')
              embed.add_field(name='Player 2:', value =f'{user_opponent.mention}')

              embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/coin-flip.gif')
              embed.set_image(url=user_original_avatar)
              embed.set_author(name=user_original.name, icon_url=user_original_avatar)

              await message.edit(embed = embed)

              del games[str(id)]
              saveDB('games', games)

              return

            else:
              #Player 2
              users[str(user_original.id)]['balance'] = int(users[str(user_original.id)]['balance']) - int(v['bet'])
              users[str(user_opponent.id)]['balance'] = int(users[str(user_opponent.id)]['balance']) + int(v['bet'])
              saveDB('users', users)

              embed = discord.Embed(
              title = f"COINFLIP: ${v['bet']}",
              description = 'In Progress',
              colour = discord.Colour.blue()
              )

              embed.add_field(name='Player 1:', value =f'{user_original.mention}')
              embed.add_field(name='Player 2:', value =f'{user_opponent.mention}')

              embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/coin-flip.gif')
              embed.set_image(url='https://media1.giphy.com/media/51Upkuhc9bYruR9fn6/giphy.gif')
              embed.set_author(name=user_original.name, icon_url=user_original_avatar)

              await message.edit(embed = embed)

              time.sleep(3)

              embed = discord.Embed(
              title = f"COINFLIP: ${v['bet']}",
              description = f'{user_opponent.mention} **WINS**',
              colour = discord.Colour.green()
              )

              embed.add_field(name='Player 1:', value =f'{user_original.mention}')
              embed.add_field(name='Player 2:', value =f'{user_opponent.mention}')

              embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/coin-flip.gif')
              embed.set_image(url=user_opponent_avatar)
              embed.set_author(name=user_original.name, icon_url=user_original_avatar)

              await message.edit(embed = embed)

              del games[str(id)]
              saveDB('games', games)

              return
    #HIGH LOW
    elif payload.emoji.name == "⬇️" or payload.emoji.name == "⬆️" or payload.emoji.name == "❌" and payload.user_id != bot.user.id:
      messageID = payload.message_id
      for id,v in games.items():
        if id == str(messageID) and v['type'] == 'high-low':
          channel = bot.get_channel(int(v['channel']))
          message = await channel.fetch_message(int(id))

          if str(v['creator']) == str(payload.user_id):
            user_original = await bot.fetch_user(int(v['creator']))

            #Generates Winning Ticket 
            ticket_number = random.randint(1,10)

            if payload.emoji.name == "⬇️" and ticket_number <=5:
              v['multiplier'] = int(v['multiplier']) * 2
              v['win'] = (int(v['bet']) * int(v['multiplier']))
              saveDB('games', games)

              embed = discord.Embed(
              title = f'HIGH-LOW: ${v["bet"]}',
              colour = discord.Colour.green()
              )

              embed.add_field(name='Correct!', value = f'Number was **{ticket_number}**', inline=True)
              embed.add_field(name='Multiplier:', value =f'{v["multiplier"]}x', inline=True)
              embed.add_field(name='Continue:', value ='Use ⬇️ or ⬆️', inline=False)
              embed.add_field(name='Stop:', value ='Use ❌ to cashout.', inline=False)

              embed.set_author(name=user_original.name, icon_url=user_original.avatar_url)

              await message.edit(embed = embed)

              await message.add_reaction('❌')
              return
            elif payload.emoji.name == "⬆️" and ticket_number >=6:
              v['multiplier'] = int(v['multiplier']) * 2
              v['win'] = (int(v['bet']) * int(v['multiplier']))
              saveDB('games', games)

              embed = discord.Embed(
              title = f'HIGH-LOW: ${v["bet"]}',
              colour = discord.Colour.green()
              )

              embed.add_field(name='Correct!', value = f'Number was **{ticket_number}**', inline=True)
              embed.add_field(name='Multiplier:', value =f'{v["multiplier"]}x', inline=True)
              embed.add_field(name='Continue:', value ='Use ⬇️ or ⬆️', inline=False)
              embed.add_field(name='Stop:', value ='Use ❌ to cashout.', inline=False)

              embed.set_author(name=user_original.name, icon_url=user_original.avatar_url)

              await message.edit(embed = embed)

              await message.add_reaction('❌')
              return
            elif payload.emoji.name == "❌" and int(v['win']) > 0:
              embed = discord.Embed(
              title = f'HIGH-LOW: ${v["bet"]}',
              colour = discord.Colour.green()
              )

              embed.add_field(name='Stopped at:', value = f'{v["multiplier"]}x', inline=True)
              embed.add_field(name='Profit:', value =f'${v["win"]}', inline=True)
              embed.add_field(name='Balance:', value =f'You have ${users[str(user_original.id)]["balance"] + int(v["win"])}', inline=False)

              embed.set_author(name=user_original.name, icon_url=user_original.avatar_url)

              await message.edit(embed = embed)

              users[str(user_original.id)]['balance'] = int(users[str(user_original.id)]['balance']) + int(v['win'])
              saveDB('users', users)

              del games[str(id)]
              saveDB('games', games)

              return
            else:
              embed = discord.Embed(
              title = f'HIGH-LOW: ${v["bet"]}',
              colour = discord.Colour.red()
              )

              embed.add_field(name='Incorrect!', value = f'Number was **{ticket_number}**', inline=True)
              embed.add_field(name='Profit:', value =f'$-{v["bet"]}', inline=True)
              embed.add_field(name='Balance:', value =f'You have ${users[str(user_original.id)]["balance"]}', inline=False)

              embed.set_author(name=user_original.name, icon_url=user_original.avatar_url)

              await message.edit(embed = embed)

              del games[str(id)]
              saveDB('games', games)

              return
##################################################################
#██╗░░██╗██╗░██████╗░██╗░░██╗░░░░░░██╗░░░░░░█████╗░░██╗░░░░░░░██╗#
#██║░░██║██║██╔════╝░██║░░██║░░░░░░██║░░░░░██╔══██╗░██║░░██╗░░██║#
#███████║██║██║░░██╗░███████║█████╗██║░░░░░██║░░██║░╚██╗████╗██╔╝#
#██╔══██║██║██║░░╚██╗██╔══██║╚════╝██║░░░░░██║░░██║░░████╔═████║░#
#██║░░██║██║╚██████╔╝██║░░██║░░░░░░███████╗╚█████╔╝░░╚██╔╝░╚██╔╝░#
#╚═╝░░╚═╝╚═╝░╚═════╝░╚═╝░░╚═╝░░░░░░╚══════╝░╚════╝░░░░╚═╝░░░╚═╝░░#
##################################################################

@bot.command()
async def highlow(ctx, arg):

  bet = float(arg)
  bet = math.floor(bet)
  bet = int(bet)

  balance = 0

  try:
    balance = int(users[str(ctx.author.id)]['balance'])
  except KeyError: 
    users[str(ctx.author.id)] = {
      'balance' : 1000,
      'daily_time_left' : 0.0
    }
    saveDB('users', users)
    balance = int(users[str(ctx.author.id)]['balance'])

  for id,v in games.items():
    if v['type'] =='high-low':
      if v['creator'] == str(ctx.author.id):
        embed = discord.Embed(
        title = f'ERROR: Game In Progress',
        description = 'Finish your other game first.',
        colour = discord.Colour.red()
        )

        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        await ctx.channel.send(embed = embed)
        return

  if balance >= bet and bet > 0:
    embed = discord.Embed(
    title = f'HIGH-LOW: ${bet}',
    description = 'Guess if number is high or low (low = 1-5, high = 6-10)',
    colour = discord.Colour.gold()
    )

    embed.add_field(name='Low:', value ='⬇️')
    embed.add_field(name='High:', value ='⬆️')

    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

    message = await ctx.channel.send(embed = embed)

    games[str(message.id)] = {
        'type' : 'high-low',
        'channel' : str(ctx.channel.id),
        'creator' : str(ctx.author.id),
        'started' : False,
        'bet' : int(bet),
        'multiplier' : 1,
        'win' : 0
    }
    saveDB('games', games)
    
    await message.add_reaction('⬇️')
    await message.add_reaction('⬆️')

    users[str(ctx.author.id)]['balance'] = int(users[str(ctx.author.id)]['balance']) - bet
    saveDB('users', users)

  else:
    embed = discord.Embed(
    title = f'ERROR: Insufficent Funds',
    description = f'Remaining: {balance}',
    colour = discord.Colour.gold()
    )

    embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/coin-flip.gif')
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

    await ctx.channel.send(embed = embed)

@bot.event
async def on_raw_reaction_remove(payload):
  if payload.emoji.name == "⬇️" or payload.emoji.name == "⬆️" or payload.emoji.name == "❌" and payload.user_id != bot.user.id:
    messageID = payload.message_id
    for id,v in games.items():
      if id == str(messageID) and v['type'] == 'high-low':
        channel = bot.get_channel(int(v['channel']))
        message = await channel.fetch_message(int(id))

        if str(v['creator']) == str(payload.user_id):
          user_original = await bot.fetch_user(int(v['creator']))

          #Generates Winning Ticket 
          ticket_number = random.randint(1,10)

          if payload.emoji.name == "⬇️" and ticket_number <=5:
            v['multiplier'] = int(v['multiplier']) * 2
            v['win'] = (int(v['bet']) * int(v['multiplier']))
            saveDB('games', games)

            embed = discord.Embed(
            title = f'HIGH-LOW: ${v["bet"]}',
            colour = discord.Colour.green()
            )

            embed.add_field(name='Correct!', value = f'Number was **{ticket_number}**', inline=True)
            embed.add_field(name='Multiplier:', value =f'{v["multiplier"]}x', inline=True)
            embed.add_field(name='Continue:', value ='Use ⬇️ or ⬆️', inline=False)
            embed.add_field(name='Stop:', value ='Use ❌ to cashout.', inline=False)

            embed.set_author(name=user_original.name, icon_url=user_original.avatar_url)

            await message.edit(embed = embed)

            await message.add_reaction('❌')
            return
          elif payload.emoji.name == "⬆️" and ticket_number >=6:
            v['multiplier'] = int(v['multiplier']) * 2
            v['win'] = (int(v['bet']) * int(v['multiplier']))
            saveDB('games', games)

            embed = discord.Embed(
            title = f'HIGH-LOW: ${v["bet"]}',
            colour = discord.Colour.green()
            )

            embed.add_field(name='Correct!', value = f'Number was **{ticket_number}**', inline=True)
            embed.add_field(name='Multiplier:', value =f'{v["multiplier"]}x', inline=True)
            embed.add_field(name='Continue:', value ='Use ⬇️ or ⬆️', inline=False)
            embed.add_field(name='Stop:', value ='Use ❌ to cashout.', inline=False)

            embed.set_author(name=user_original.name, icon_url=user_original.avatar_url)

            await message.edit(embed = embed)

            await message.add_reaction('❌')
            return
          else:
            embed = discord.Embed(
            title = f'HIGH-LOW: ${v["bet"]}',
            colour = discord.Colour.red()
            )

            embed.add_field(name='Incorrect!', value = f'Number was **{ticket_number}**', inline=True)
            embed.add_field(name='Profit:', value =f'$-{v["bet"]}', inline=True)
            embed.add_field(name='Balance:', value =f'You have ${users[str(user_original.id)]["balance"]}', inline=False)

            embed.set_author(name=user_original.name, icon_url=user_original.avatar_url)

            await message.edit(embed = embed)

            del games[str(id)]
            saveDB('games', games)

            return


@bot.command()
async def jackpot(ctx, arg, arg2):

  bet = float(arg2)
  bet = math.floor(bet)
  bet = int(bet)

  balance = 0

  try:
    balance = int(users[str(ctx.author.id)]['balance'])
  except KeyError: 
    users[str(ctx.author.id)] = {
      'balance' : 1000,
      'daily_time_left' : 0.0
    }
    saveDB('users', users)
    balance = int(users[str(ctx.author.id)]['balance'])

  if balance >= bet and bet > 0:
    if str(arg) == 'create':
      for id,v in games.items():
        if v['type'] =='jackpot':
          embed = discord.Embed(
          title = f'ERROR: Game In Progress',
          description = 'Finish your other game first.',
          colour = discord.Colour.red()
          )

          embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

          await ctx.channel.send(embed = embed)
          return

      embed = discord.Embed(
      title = f'JACKPOT: ${bet}',
      description = f'**{ctx.author.name}** started a jackpot!',
      colour = discord.Colour.gold()
      )

      embed.add_field(name='Join:', value ='**$jackpot join <bet>**', inline=False)
      embed.add_field(name='Pot:', value =f'**${bet}**', inline=False)
      embed.add_field(name='Odds:', value =f'{ctx.author.name}: **100.00%**', inline=False)

      embed.set_footer(text="Timeleft: 60s")
      embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

      message = await ctx.channel.send(embed = embed)

      games[str(message.id)] = {
          'type' : 'jackpot',
          'channel' : str(ctx.channel.id),
          'creator' : str(ctx.author.id),
          'bet' : int(bet),
          'time' : time.time(),
          'players' : {
            str(ctx.author.id) : int(bet)
          }
      }
      saveDB('games', games)

      users[str(ctx.author.id)]['balance'] = int(users[str(ctx.author.id)]['balance']) - bet
      saveDB('users', users)

      await asyncio.sleep(60)

      randomTicket = random.randint(1, 100)
      total = 0
      print(randomTicket)
      for k,v in games[str(message.id)]['players'].items():

        print('')
        print(total)
        print((((int(v)) / int(games[str(message.id)]['bet'])) * 100))
        
        if randomTicket > total and (randomTicket <= total + (((int(v)) / int(games[str(message.id)]['bet'])) * 100)):
          winner_user = await bot.fetch_user(int(k))
          users[str(k)]['balance'] = int(users[str(k)]['balance']) + int(games[str(message.id)]['bet'])
          saveDB('users', users)

          embed = discord.Embed(
          title = f'JACKPOT: ${games[str(message.id)]["bet"]}',
          description = f'**{winner_user.name}** won ${games[str(message.id)]["bet"]} with {((((int(v)) / int(games[str(message.id)]["bet"])) * 100)):.2f}%',
          colour = discord.Colour.green()
          )

          embed.add_field(name='Credits:', value =f'You have ${users[str(k)]["balance"]}', inline=False)

          embed.set_author(name=winner_user.name, icon_url=winner_user.avatar_url)

          await message.edit(embed = embed)

          del games[str(message.id)]
          saveDB('games', games)

          return
        else:
          total += (((int(v)) / int(games[str(message.id)]['bet'])) * 100)


    elif str(arg) == 'join':
      for id,v in games.items():
        if v['type'] =='jackpot':
          channel = bot.get_channel(int(v['channel']))
          message = await channel.fetch_message(int(id))

          if str(ctx.author.id) in v['players']:
            embed = discord.Embed(
            title = f'ERROR: Already joined jackpot.',
            description = f'**$jackpot raise <bet>**',
            colour = discord.Colour.gold()
            )

            embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/coin-flip.gif')
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

            await ctx.channel.send(embed = embed)
          else:
            users[str(ctx.author.id)]['balance'] = int(users[str(ctx.author.id)]['balance']) - bet
            saveDB('users', users)

            v['players'][str(ctx.author.id)] = int(bet)
            v['bet'] = int(v['bet']) + int(bet)
            saveDB('games', games)

            odds_str = ''
            for k2,v2 in v['players'].items():
              user_creator = await bot.fetch_user(int(v["creator"]))
              user = await bot.fetch_user(int(k2))
              odds_str = f'{odds_str}\n{str(user.name)}: **{(((int(v2)) / int(v["bet"])) * 100):.2f}%**'

            embed = discord.Embed(
            title = f'JACKPOT: ${v["bet"]}',
            description = f'**{user_creator.name}** started a jackpot!',
            colour = discord.Colour.gold()
            )

            embed.add_field(name='Join:', value ='**$jackpot join <bet>**', inline=False)
            embed.add_field(name='Pot:', value =f'**${v["bet"]}**', inline=False)
            embed.add_field(name='Odds:', value =f'{odds_str}', inline=False)

            embed.set_footer(text="Timeleft: " + str(int(60 - (time.time() - int(v['time'])))) +'s')
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

            await message.edit(embed = embed)

    elif str(arg) == 'raise':
      for id,v in games.items():
        if v['type'] =='jackpot':
          channel = bot.get_channel(int(v['channel']))
          message = await channel.fetch_message(int(id))

          if str(ctx.author.id) in v['players']:
            users[str(ctx.author.id)]['balance'] = int(users[str(ctx.author.id)]['balance']) - bet
            saveDB('users', users)

            v['players'][str(ctx.author.id)] = int(v['players'][str(ctx.author.id)]) + int(bet)
            v['bet'] = int(v['bet']) + int(bet)
            saveDB('games', games)

            odds_str = ''
            for k2,v2 in v['players'].items():
              user_creator = await bot.fetch_user(int(v["creator"]))
              user = await bot.fetch_user(int(k2))
              odds_str = f'{odds_str}\n{str(user.name)}: **{(((int(v2)) / int(v["bet"])) * 100):.2f}%**'

            embed = discord.Embed(
            title = f'JACKPOT: ${v["bet"]}',
            description = f'**{user_creator.name}** started a jackpot!',
            colour = discord.Colour.gold()
            )

            embed.add_field(name='Join:', value ='**$jackpot join <bet>**', inline=False)
            embed.add_field(name='Pot:', value =f'**${v["bet"]}**', inline=False)
            embed.add_field(name='Odds:', value =f'{odds_str}', inline=False)

            embed.set_footer(text="Timeleft: " + str(int(60 - (time.time() - int(v['time'])))) +'s')
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

            await message.edit(embed = embed)
          
  else:
    embed = discord.Embed(
    title = f'ERROR: Insufficent Funds or Invalid Bet',
    description = f'Remaining: {balance}',
    colour = discord.Colour.gold()
    )

    embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/coin-flip.gif')
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

    await ctx.channel.send(embed = embed)










# EXECUTES THE BOT WITH THE SPECIFIED TOKEN.
bot.run(DISCORD_TOKEN)

