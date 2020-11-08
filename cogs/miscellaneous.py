import discord
import random
import time
import main

from discord.ext import commands
from collections import OrderedDict 
from operator import getitem


##########################################################################################################
#███╗░░░███╗██╗░██████╗░█████╗░███████╗██╗░░░░░██╗░░░░░░█████╗░███╗░░██╗███████╗░█████╗░██╗░░░██╗░██████╗#
#████╗░████║██║██╔════╝██╔══██╗██╔════╝██║░░░░░██║░░░░░██╔══██╗████╗░██║██╔════╝██╔══██╗██║░░░██║██╔════╝#
#██╔████╔██║██║╚█████╗░██║░░╚═╝█████╗░░██║░░░░░██║░░░░░███████║██╔██╗██║█████╗░░██║░░██║██║░░░██║╚█████╗░#
#██║╚██╔╝██║██║░╚═══██╗██║░░██╗██╔══╝░░██║░░░░░██║░░░░░██╔══██║██║╚████║██╔══╝░░██║░░██║██║░░░██║░╚═══██╗#
#██║░╚═╝░██║██║██████╔╝╚█████╔╝███████╗███████╗███████╗██║░░██║██║░╚███║███████╗╚█████╔╝╚██████╔╝██████╔╝#
#╚═╝░░░░░╚═╝╚═╝╚═════╝░░╚════╝░╚══════╝╚══════╝╚══════╝╚═╝░░╚═╝╚═╝░░╚══╝╚══════╝░╚════╝░░╚═════╝░╚═════╝░#
##########################################################################################################

class Miscellaneous(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
        self.bot.remove_command('help')
    @commands.command()
    async def help(self, ctx):
      embed=discord.Embed(color=0xf0f40b)
      embed.add_field(name="🎲 Game commands", value="`coinflip`, `jackpot`, `highlow`, `slots`", inline=False)
      embed.add_field(name="⚙️ Other commands", value="`balance`, `top`, `daily`, `search` \n\nBot prefix is: $", inline=True)
      await ctx.channel.send(embed=embed)
    
    @commands.command()
    async def top(self, ctx):
      string ='```md\nTOP 10\n======\n```'
      
      res = OrderedDict(sorted(main.users.items(), key = lambda x: getitem(x[1], 'balance'), reverse=True)) 

      i = 1
      for k,v in res.items():
        if v['balance'] != 0 and i <= 10:
          name = await self.bot.fetch_user(int(k))
          string = f'{string[0:len(string)-3]}{i}.  < {str(name)} > - ${int(res[str(k)]["balance"])} \n```'
          i += 1

      await ctx.channel.send(string)

    @commands.command()
    async def balance(self, ctx):
      value = 0

      try:
        value = int(main.users[str(ctx.author.id)]['balance'])
      except KeyError: 
        main.users[str(ctx.author.id)] = {
            'balance' : 1000,
            'daily_time_left' : 0.0
        }
        main.saveDB('users', main.users)
        value = int(main.users[str(ctx.author.id)]['balance'])

      embed = discord.Embed(
      title = f'BALANCE: ${value}',
      colour = discord.Colour.green()
      )

      embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
      await ctx.channel.send(embed = embed)

    @commands.command()
    async def daily(self, ctx):
      time_stamp = 0.0

      try:
        time_stamp = float(main.users[str(ctx.author.id)]['daily_time_left'])
      except KeyError: 
        main.users[str(ctx.author.id)] = {
            'balance' : 1000,
            'daily_time_left' : 0.0
        }
        main.saveDB('users', main.users)
        time_stamp = 0.0
        time_left = float(time.time() - time_stamp)

      if float(time.time() - time_stamp) >= 86400:
        main.users[str(ctx.author.id)]['balance'] = int(main.users[str(ctx.author.id)]['balance']) + 500
        main.users[str(ctx.author.id)]['daily_time_left'] = time.time()
        main.saveDB('users', main.users)

        remainging_balance = int(main.users[str(ctx.author.id)]['balance'])

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

    @commands.command()
    async def search(self, ctx):
      balance = 0

      try:
        balance = int(main.users[str(ctx.author.id)]['balance'])
      except KeyError: 
        main.users[str(ctx.author.id)] = {
            'balance' : 1000,
            'daily_time_left' : 0.0
        }
        balance = int(main.users[str(ctx.author.id)]['balance'])
        main.saveDB('users', main.users)

      if balance == 0:
        found =  random.randint(50,75)
        main.users[str(ctx.author.id)]['balance'] = int(main.users[str(ctx.author.id)]['balance']) + found
        main.saveDB('users', main.users)

        embed = discord.Embed(
        title = f'SEARCH: ${found} CLAIMED',
        description = f'New Balance: ${main.users[str(ctx.author.id)]["balance"]}',
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



    @commands.command()
    async def set_balance(self, ctx, arg, arg2):
      if str(ctx.author.id) == '167432518914539521':
        main.users[str(arg)]['balance'] = int(arg2)
        main.saveDB('users', main.users)
        await ctx.channel.send(f'Set {arg}\'s balance: {arg2}')
    
            
def setup(bot):
    bot.add_cog(Miscellaneous(bot))

