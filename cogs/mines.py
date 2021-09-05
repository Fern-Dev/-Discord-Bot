import discord
import random
import asyncio
import math
import time
import main

from discord.ext import commands


#########################################
#███╗░░░███╗██╗███╗░░██╗███████╗░██████╗#
#████╗░████║██║████╗░██║██╔════╝██╔════╝#
#██╔████╔██║██║██╔██╗██║█████╗░░╚█████╗░#
#██║╚██╔╝██║██║██║╚████║██╔══╝░░░╚═══██╗#
#██║░╚═╝░██║██║██║░╚███║███████╗██████╔╝#
#╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝╚══════╝╚═════╝░#
#########################################

class Mines(commands.Cog):

    def __init__(self, bot):
      self.bot = bot

    def constructMinesMessage(self, item, bomb, id):
      mines = [('A1', 'B1', 'C1', 'D1'), ('A2', 'B2', 'C2', 'D2'), ('A3', 'B3', 'C3', 'D3'), ('A4', 'B4', 'C4', 'D4')]
      msg = '```\n'
      for i in range(0,4):
          msg += '--------------------\n|'
          for i2 in range(0,4):
            if (item == (i, i2)) and (bomb == False):
              msg += f' ✅ |'
            elif (item == (i, i2)) and (bomb == True):
              msg += f' ❌ |'
            else:
              msg += f' {mines[i][i2]} |'
          msg += '\n'
      msg += '--------------------\n```\nNext: **$0**\nTotal: **$0**\nOdds for win: **87.50%**'
      
      for id, v in main.games.items():
          if v['type'] == 'mines' and v['creator'] == str(id):
            pass
      a = coinflip.testdict
      return msg

    @commands.command()
    async def mines(self, ctx, arg):
      
      bet = float(arg)
      bet = math.floor(bet)
      bet = int(bet)

      balance = 0

      try:
        balance = int(main.users[str(ctx.author.id)]['balance'])
      except KeyError:
        main.users[str(ctx.author.id)] = {
            'balance': 1000,
            'daily_time_left': 0.0
        }
        main.saveDB('users', main.users)
        balance = int(main.users[str(ctx.author.id)]['balance'])

      if balance >= bet and bet > 0:
        for id, v in main.games.items():
          if v['type'] == 'mines' and v['creator'] == str(ctx.author.id):
            embed = discord.Embed(
              title=f'ERROR: Game In Progress',
              description='Finish your other game first.',
              colour=discord.Colour.red()
            )

            embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)
            return

        embed=discord.Embed(
          title="**Try to avoid two bombs**", 
          description="Use: **$<field>**\nExample: **$A1**\nUse: **$stop** to stop",
          colour=discord.Colour.gold()
        )
        await ctx.channel.send(embed=embed)

        bombs = [(random.randint(0,3),random.randint(0,3)), (random.randint(0,3),random.randint(0,3))]

        message = await ctx.channel.send(self.constructMinesMessage((99,99), False))

        main.games[str(message.id)] = {
              'type' : 'mines',
              'channel' : str(ctx.channel.id),
              'creator' : str(ctx.author.id),
              'bet' : int(bet),
              'selection' : [],
              'bombs' : bombs
          }
        main.saveDB('games', main.games)

        main.users[str(ctx.author.id)]['balance'] = int(main.users[str(ctx.author.id)]['balance']) - bet
        main.saveDB('users', main.users)
      else:
        embed = discord.Embed(
          title=f'ERROR: Insufficent Funds or Invalid Bet',
          description=f'Remaining: {balance}',
          colour=discord.Colour.gold()
        )

        embed.set_thumbnail(
          url='https://acegif.com/wp-content/uploads/coin-flip.gif')
        embed.set_author(
          name=ctx.author.name,
          icon_url=ctx.author.avatar_url)

        await ctx.channel.send(embed=embed)

    @commands.command()
    async def A1(self, ctx):
      for id, v in main.games.items():
          if v['type'] == 'mines' and v['creator'] == str(ctx.author.id):
            channel = self.bot.get_channel(int(v['channel']))
            message = await channel.fetch_message(int(id))
            if (0,0) in v['bombs']:
              await message.edit(content = self.constructMinesMessage((0, 0), True))
            elif not 'A1' in v['selection']:
              v['selection'].append('A1')
              await message.edit(content = self.constructMinesMessage((0, 0), False))




    @mines.error
    async def mines_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(color=discord.Colour.gold())
            embed.add_field(
                name="Help", value="Try to avoid 2 bombs in field", inline=False)
            embed.add_field(name="Commands",
                            value="$field Example: $a1", inline=False)
            embed.add_field(name="Winnings",
                            value="Up to 7x your bet", inline=False)
            embed.add_field(name="Usage", value="$mines <bet>", inline=False)
            await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Mines(bot))
