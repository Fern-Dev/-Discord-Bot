import discord
import random
import asyncio
import math
import time
import main

from discord.ext import commands


###########################################################
#░░░░░██╗░█████╗░░█████╗░██╗░░██╗██████╗░░█████╗░████████╗#
#░░░░░██║██╔══██╗██╔══██╗██║░██╔╝██╔══██╗██╔══██╗╚══██╔══╝#
#░░░░░██║███████║██║░░╚═╝█████═╝░██████╔╝██║░░██║░░░██║░░░#
#██╗░░██║██╔══██║██║░░██╗██╔═██╗░██╔═══╝░██║░░██║░░░██║░░░#
#╚█████╔╝██║░░██║╚█████╔╝██║░╚██╗██║░░░░░╚█████╔╝░░░██║░░░#
#░╚════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░░░░░╚════╝░░░░╚═╝░░░#
###########################################################

class Jackpot(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def jackpot(self, ctx, arg, arg2):

      bet = float(arg2)
      bet = math.floor(bet)
      bet = int(bet)

      balance = 0

      try:
        balance = int(main.users[str(ctx.author.id)]['balance'])
      except KeyError: 
        main.users[str(ctx.author.id)] = {
          'balance' : 1000,
          'daily_time_left' : 0.0
        }
        main.saveDB('users', main.users)
        balance = int(main.users[str(ctx.author.id)]['balance'])

      if balance >= bet and bet > 0:
        if str(arg) == 'create':
          for id,v in main.games.items():
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

          main.games[str(message.id)] = {
              'type' : 'jackpot',
              'channel' : str(ctx.channel.id),
              'creator' : str(ctx.author.id),
              'bet' : int(bet),
              'time' : time.time(),
              'players' : {
                str(ctx.author.id) : int(bet)
              }
          }
          main.saveDB('games', main.games)

          main.users[str(ctx.author.id)]['balance'] = int(main.users[str(ctx.author.id)]['balance']) - bet
          main.saveDB('users', main.users)

          await asyncio.sleep(60)

          randomTicket = random.randint(1, 100)
          total = 0
          print(randomTicket)
          for k,v in main.games[str(message.id)]['players'].items():

            print('')
            print(total)
            print((((int(v)) / int(main.games[str(message.id)]['bet'])) * 100))
            
            if randomTicket > total and (randomTicket <= total + (((int(v)) / int(main.games[str(message.id)]['bet'])) * 100)):
              winner_user = await self.bot.fetch_user(int(k))
              main.users[str(k)]['balance'] = int(main.users[str(k)]['balance']) + int(main.games[str(message.id)]['bet'])
              main.saveDB('users', main.users)

              embed = discord.Embed(
              title = f'JACKPOT: ${main.games[str(message.id)]["bet"]}',
              description = f'**{winner_user.name}** won ${main.games[str(message.id)]["bet"]} with {((((int(v)) / int(main.games[str(message.id)]["bet"])) * 100)):.2f}%',
              colour = discord.Colour.green()
              )

              embed.add_field(name='Credits:', value =f'You have ${main.users[str(k)]["balance"]}', inline=False)

              embed.set_author(name=winner_user.name, icon_url=winner_user.avatar_url)

              await message.edit(embed = embed)

              del main.games[str(message.id)]
              main.saveDB('games', main.games)

              return
            else:
              total += (((int(v)) / int(main.games[str(message.id)]['bet'])) * 100)


        elif str(arg) == 'join':
          for id,v in main.games.items():
            if v['type'] =='jackpot':
              channel = self.bot.get_channel(int(v['channel']))
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
                main.users[str(ctx.author.id)]['balance'] = int(main.users[str(ctx.author.id)]['balance']) - bet
                main.saveDB('users', main.users)

                v['players'][str(ctx.author.id)] = int(bet)
                v['bet'] = int(v['bet']) + int(bet)
                main.saveDB('games', main.games)

                odds_str = ''
                for k2,v2 in v['players'].items():
                  user_creator = await self.bot.fetch_user(int(v["creator"]))
                  user = await self.bot.fetch_user(int(k2))
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
          for id,v in main.games.items():
            if v['type'] =='jackpot':
              channel = self.bot.get_channel(int(v['channel']))
              message = await channel.fetch_message(int(id))

              if str(ctx.author.id) in v['players']:
                main.users[str(ctx.author.id)]['balance'] = int(main.users[str(ctx.author.id)]['balance']) - bet
                main.saveDB('users', main.users)

                v['players'][str(ctx.author.id)] = int(v['players'][str(ctx.author.id)]) + int(bet)
                v['bet'] = int(v['bet']) + int(bet)
                main.saveDB('games', main.games)

                odds_str = ''
                for k2,v2 in v['players'].items():
                  user_creator = await self.bot.fetch_user(int(v["creator"]))
                  user = await self.bot.fetch_user(int(k2))
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
    
            
def setup(bot):
    bot.add_cog(Jackpot(bot))

