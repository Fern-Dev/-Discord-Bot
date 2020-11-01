import discord
import random
import asyncio
import math
import main

from discord.ext import commands


##################################################################
#██╗░░██╗██╗░██████╗░██╗░░██╗░░░░░░██╗░░░░░░█████╗░░██╗░░░░░░░██╗#
#██║░░██║██║██╔════╝░██║░░██║░░░░░░██║░░░░░██╔══██╗░██║░░██╗░░██║#
#███████║██║██║░░██╗░███████║█████╗██║░░░░░██║░░██║░╚██╗████╗██╔╝#
#██╔══██║██║██║░░╚██╗██╔══██║╚════╝██║░░░░░██║░░██║░░████╔═████║░#
#██║░░██║██║╚██████╔╝██║░░██║░░░░░░███████╗╚█████╔╝░░╚██╔╝░╚██╔╝░#
#╚═╝░░╚═╝╚═╝░╚═════╝░╚═╝░░╚═╝░░░░░░╚══════╝░╚════╝░░░░╚═╝░░░╚═╝░░#
##################################################################

class Highlow(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def highlow(self, ctx, arg):

      bet = float(arg)
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

      for id,v in main.games.items():
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

        main.games[str(message.id)] = {
            'type' : 'high-low',
            'channel' : str(ctx.channel.id),
            'creator' : str(ctx.author.id),
            'started' : False,
            'bet' : int(bet),
            'multiplier' : 1,
            'win' : 0
        }
        main.saveDB('games', main.games)
        
        await message.add_reaction('⬇️')
        await message.add_reaction('⬆️')

        main.users[str(ctx.author.id)]['balance'] = int(main.users[str(ctx.author.id)]['balance']) - bet
        main.saveDB('users', main.users)

      else:
        embed = discord.Embed(
        title = f'ERROR: Insufficent Funds',
        description = f'Remaining: {balance}',
        colour = discord.Colour.gold()
        )

        embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/coin-flip.gif')
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        await ctx.channel.send(embed = embed)


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.emoji.name == "⬇️" or payload.emoji.name == "⬆️" or payload.emoji.name == "❌" and payload.user_id != self.bot.user.id:
          messageID = payload.message_id
          for id,v in main.games.items():
            if id == str(messageID) and v['type'] == 'high-low':
              channel = self.bot.get_channel(int(v['channel']))
              message = await channel.fetch_message(int(id))

              if str(v['creator']) == str(payload.user_id):
                user_original = await self.bot.fetch_user(int(v['creator']))

                #Generates Winning Ticket 
                ticket_number = random.randint(1,10)

                if payload.emoji.name == "⬇️" and ticket_number <=5:
                  v['multiplier'] = int(v['multiplier']) * 2
                  v['win'] = (int(v['bet']) * int(v['multiplier']))
                  main.saveDB('games', main.games)

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
                  main.saveDB('games', main.games)

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
                  embed.add_field(name='Balance:', value =f'You have ${main.users[str(user_original.id)]["balance"] + int(v["win"])}', inline=False)

                  embed.set_author(name=user_original.name, icon_url=user_original.avatar_url)

                  await message.edit(embed = embed)

                  main.users[str(user_original.id)]['balance'] = int(main.users[str(user_original.id)]['balance']) + int(v['win'])
                  main.saveDB('users', main.users)

                  del main.games[str(id)]
                  main.saveDB('games', main.games)

                  return
                else:
                  embed = discord.Embed(
                  title = f'HIGH-LOW: ${v["bet"]}',
                  colour = discord.Colour.red()
                  )

                  embed.add_field(name='Incorrect!', value = f'Number was **{ticket_number}**', inline=True)
                  embed.add_field(name='Profit:', value =f'$-{v["bet"]}', inline=True)
                  embed.add_field(name='Balance:', value =f'You have ${main.users[str(user_original.id)]["balance"]}', inline=False)

                  embed.set_author(name=user_original.name, icon_url=user_original.avatar_url)

                  await message.edit(embed = embed)

                  del main.games[str(id)]
                  main.saveDB('games', main.games)

                  return
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
      if payload.emoji.name == "⬇️" or payload.emoji.name == "⬆️" or payload.emoji.name == "❌" and payload.user_id != self.bot.user.id:
        messageID = payload.message_id
        for id,v in main.games.items():
          if id == str(messageID) and v['type'] == 'high-low':
            channel = self.bot.get_channel(int(v['channel']))
            message = await channel.fetch_message(int(id))

            if str(v['creator']) == str(payload.user_id):
              user_original = await self.bot.fetch_user(int(v['creator']))

              #Generates Winning Ticket 
              ticket_number = random.randint(1,10)

              if payload.emoji.name == "⬇️" and ticket_number <=5:
                v['multiplier'] = int(v['multiplier']) * 2
                v['win'] = (int(v['bet']) * int(v['multiplier']))
                main.saveDB('games', main.games)

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
                main.saveDB('games', main.games)

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
                embed.add_field(name='Balance:', value =f'You have ${main.users[str(user_original.id)]["balance"]}', inline=False)

                embed.set_author(name=user_original.name, icon_url=user_original.avatar_url)

                await message.edit(embed = embed)

                del main.games[str(id)]
                main.saveDB('games', main.games)

                return
            
def setup(bot):
    bot.add_cog(Highlow(bot))

