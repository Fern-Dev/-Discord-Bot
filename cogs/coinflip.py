import discord
import random
import asyncio
import math
import main

from discord.ext import commands


###########################################################
#  ░█████╗░░█████╗░██╗███╗░░██╗███████╗██╗░░░░░██╗██████╗░#
#  ██╔══██╗██╔══██╗██║████╗░██║██╔════╝██║░░░░░██║██╔══██╗#
#  ██║░░╚═╝██║░░██║██║██╔██╗██║█████╗░░██║░░░░░██║██████╔╝#
#  ██║░░██╗██║░░██║██║██║╚████║██╔══╝░░██║░░░░░██║██╔═══╝░#
#  ╚█████╔╝╚█████╔╝██║██║░╚███║██║░░░░░███████╗██║██║░░░░░#
#  ░╚════╝░░╚════╝░╚═╝╚═╝░░╚══╝╚═╝░░░░░╚══════╝╚═╝╚═╝░░░░░#
###########################################################

class Coinflip(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coinflip(self, ctx, arg):

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
            embed = discord.Embed(
                title=f'COINFLIP: ${bet}',
                description='Press ✅ to join.',
                colour=discord.Colour.blue()
            )

            embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/coin-flip.gif')
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

            message = await ctx.channel.send(embed=embed)
            main.games[str(message.id)] = {
                'type': 'coinflip',
                'channel': str(ctx.channel.id),
                'creator': str(ctx.author.id),
                'started': False,
                'bet': int(bet)
            }
            main.saveDB('games', main.games)
            await message.add_reaction('✅')
        else:
            embed = discord.Embed(
                title=f'ERROR: Insufficent Funds',
                description=f'Remaining: {balance}',
                colour=discord.Colour.red()
            )

            embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/coin-flip.gif')
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

            await ctx.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.emoji.name == "✅" and payload.user_id != self.bot.user.id:
            messageID = payload.message_id
            for id, v in main.games.items():
                if id == str(messageID) and v['type'] == 'coinflip':
                    channel = self.bot.get_channel(int(v['channel']))
                    message = await channel.fetch_message(int(id))

                    if str(v['creator']) != str(payload.user_id):
                        user_original = await self.bot.fetch_user(int(v['creator']))
                        user_opponent = await self.bot.fetch_user(payload.user_id)

                        opponent_balance = 0

                        try:
                            opponent_balance = int(main.users[str(user_opponent.id)]['balance'])
                        except KeyError:
                            main.users[str(user_opponent.id)] = {
                                'balance': 1000,
                                'daily_time_left': 0.0
                            }
                            main.saveDB('users', main.users)
                            opponent_balance = int(main.users[str(user_opponent.id)]['balance'])

                        if opponent_balance < int(v['bet']):
                            embed = discord.Embed(
                                title=f'ERROR: Insufficent Funds',
                                description=f'Remaining: {opponent_balance:.2f}',
                                colour=discord.Colour.red()
                            )

                            embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/coin-flip.gif')
                            embed.set_author(name=user_opponent.name, icon_url=user_opponent.avatar_url)

                            await channel.send(embed=embed)
                            return

                        if int(main.users[str(user_original.id)]['balance']) < int(v['bet']):
                            new_bal = int(main.users[str(user_original.id)]['balance'])
                            embed = discord.Embed(
                                title=f'GAME CANCELED: Creator has Insufficent Funds',
                                description=f'Remaining Creator Balance: {new_bal}',
                                colour=discord.Colour.red()
                            )

                            embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/coin-flip.gif')
                            embed.set_author(name=user_opponent.name, icon_url=user_opponent.avatar_url)

                            await message.edit(embed=embed)

                            del main.games[str(id)]
                            main.saveDB('games', main.games)
                            return

                        if (v['started'] == True):
                            return
                        v['started'] = True

                        user_original_avatar = user_original.avatar_url
                        user_opponent_avatar = user_opponent.avatar_url

                        # Generates Winning Ticket
                        ticket_number = random.random()

                        if ticket_number <= 0.5:
                            # Player 1

                            main.users[str(user_original.id)]['balance'] = int(
                                main.users[str(user_original.id)]['balance']) + int(v['bet'])
                            main.users[str(user_opponent.id)]['balance'] = int(
                                main.users[str(user_opponent.id)]['balance']) - int(v['bet'])
                            main.saveDB('users', main.users)

                            embed = discord.Embed(
                                title=f"COINFLIP: ${v['bet']}",
                                description='In Progress',
                                colour=discord.Colour.blue()
                            )

                            embed.add_field(name='Player 1:', value=f'{user_original.mention}')
                            embed.add_field(name='Player 2:', value=f'{user_opponent.mention}')

                            embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/coin-flip.gif')
                            embed.set_image(url='https://media1.giphy.com/media/51Upkuhc9bYruR9fn6/giphy.gif')
                            embed.set_author(name=user_original.name, icon_url=user_original_avatar)

                            await message.edit(embed=embed)

                            await asyncio.sleep(3)

                            embed = discord.Embed(
                                title=f"COINFLIP: ${v['bet']}",
                                description=f'{user_original.mention} **WINS**',
                                colour=discord.Colour.green()
                            )

                            embed.add_field(name='Player 1:', value=f'{user_original.mention}')
                            embed.add_field(name='Player 2:', value=f'{user_opponent.mention}')

                            embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/coin-flip.gif')
                            embed.set_image(url=user_original_avatar)
                            embed.set_author(name=user_original.name, icon_url=user_original_avatar)

                            await message.edit(embed=embed)

                            del main.games[str(id)]
                            main.saveDB('games', main.games)

                            return

                        else:
                            # Player 2
                            main.users[str(user_original.id)]['balance'] = int(
                                main.users[str(user_original.id)]['balance']) - int(v['bet'])
                            main.users[str(user_opponent.id)]['balance'] = int(
                                main.users[str(user_opponent.id)]['balance']) + int(v['bet'])
                            main.saveDB('users', main.users)

                            embed = discord.Embed(
                                title=f"COINFLIP: ${v['bet']}",
                                description='In Progress',
                                colour=discord.Colour.blue()
                            )

                            embed.add_field(name='Player 1:', value=f'{user_original.mention}')
                            embed.add_field(name='Player 2:', value=f'{user_opponent.mention}')

                            embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/coin-flip.gif')
                            embed.set_image(url='https://media1.giphy.com/media/51Upkuhc9bYruR9fn6/giphy.gif')
                            embed.set_author(name=user_original.name, icon_url=user_original_avatar)

                            await message.edit(embed=embed)

                            await asyncio.sleep(3)

                            embed = discord.Embed(
                                title=f"COINFLIP: ${v['bet']}",
                                description=f'{user_opponent.mention} **WINS**',
                                colour=discord.Colour.green()
                            )

                            embed.add_field(name='Player 1:', value=f'{user_original.mention}')
                            embed.add_field(name='Player 2:', value=f'{user_opponent.mention}')

                            embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/coin-flip.gif')
                            embed.set_image(url=user_opponent_avatar)
                            embed.set_author(name=user_original.name, icon_url=user_original_avatar)

                            await message.edit(embed=embed)

                            del main.games[str(id)]
                            main.saveDB('games', main.games)

                            return


def setup(bot):
    bot.add_cog(Coinflip(bot))
