import discord
import random
import asyncio
import math
import main

from discord.ext import commands
from discord.ext.commands import BucketType

###########################################
#░██████╗██╗░░░░░░█████╗░████████╗░██████╗#
#██╔════╝██║░░░░░██╔══██╗╚══██╔══╝██╔════╝#
#╚█████╗░██║░░░░░██║░░██║░░░██║░░░╚█████╗░#
#░╚═══██╗██║░░░░░██║░░██║░░░██║░░░░╚═══██╗#
#██████╔╝███████╗╚█████╔╝░░░██║░░░██████╔╝#
#╚═════╝░╚══════╝░╚════╝░░░░╚═╝░░░╚═════╝░#
###########################################

class Slots(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def slots(self, ctx, arg):

        slotItems = ['💯', '💰', '💵', '🏅', '💎']
        animEmoji = '<a:slot:774891932840099860>'

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

        if balance >= bet and bet > 0:
            stop1 = random.randint(0,4)
            stop2 = random.randint(0,4)
            stop3 = random.randint(0,4)

            #Deduct bet
            main.users[str(ctx.author.id)]['balance'] = int(main.users[str(ctx.author.id)]['balance']) - bet
            main.saveDB('users', main.users)


            embed = discord.Embed(
            colour = discord.Colour.gold()
            )

            embed.add_field(name =f'**Slot | User: {ctx.author.name}**', value=f'**---------------------\n-| {animEmoji} | {animEmoji} | {animEmoji} |-\n---------------------\n--- SPINNING ---**', inline=False)

            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

            message = await ctx.channel.send(embed = embed)

            for i in range(3):
                await asyncio.sleep(3)

                embed = discord.Embed(
                colour = discord.Colour.gold()
                )
                if i == 0:
                    embed.add_field(name =f'**Slot | User: {ctx.author.name}**', value=f'**---------------------\n-| {slotItems[stop1]} | {animEmoji} | {animEmoji} |-\n---------------------\n--- SPINNING ---**', inline=False)
                elif i == 1:
                    embed.add_field(name =f'**Slot | User: {ctx.author.name}**', value=f'**---------------------\n-| {slotItems[stop1]} | {slotItems[stop2]} | {animEmoji} |-\n---------------------\n--- SPINNING ---**', inline=False)
                else:
                    embed.add_field(name =f'**Slot | User: {ctx.author.name}**', value=f'**---------------------\n-| {slotItems[stop1]} | {slotItems[stop2]} | {slotItems[stop3]} |-\n---------------------\n--- SPINNING ---**', inline=False)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                
                await message.edit(embed=embed)

            #Two Medals
            if ((stop1 == 3) and (stop2 == 3)) or ((stop2 == 3) and (stop3 == 3)) or ((stop1 == 3) and (stop3 == 3)):
                main.users[str(ctx.author.id)]['balance'] = int(main.users[str(ctx.author.id)]['balance']) + math.floor(bet * 0.5)
                main.saveDB('users', main.users)

                embed = discord.Embed(
                colour = discord.Colour.gold()
                )
                embed.add_field(name =f'**Slot | User: {ctx.author.name}**', value=f'**---------------------\n-| {slotItems[stop1]} | {slotItems[stop2]} | {slotItems[stop3]} |-\n---------------------\n--- YOU WON ---**', inline=False)
                embed.add_field(name ='**Profit**', value = f'**${math.floor(bet * 0.5) - bet}**', inline=True)
                embed.add_field(name ='**New Balance**', value = f'**${int(main.users[str(ctx.author.id)]["balance"])}**', inline=True)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                await message.edit(embed=embed)
            #Two Diamonds
            elif ((stop1 == 4) and (stop2 == 4)) or ((stop2 == 4) and (stop3 == 4)) or ((stop1 == 4) and (stop3 == 4)):
                main.users[str(ctx.author.id)]['balance'] = int(main.users[str(ctx.author.id)]['balance']) + math.floor(bet * 2)
                main.saveDB('users', main.users)

                embed = discord.Embed(
                colour = discord.Colour.green()
                )
                embed.add_field(name =f'**Slot | User: {ctx.author.name}**', value=f'**---------------------\n-| {slotItems[stop1]} | {slotItems[stop2]} | {slotItems[stop3]} |-\n---------------------\n--- YOU WON ---**', inline=False)
                embed.add_field(name ='**Profit**', value = f'**${math.floor(bet * 2)}**', inline=True)
                embed.add_field(name ='**New Balance**', value = f'**${int(main.users[str(ctx.author.id)]["balance"])}**', inline=True)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                await message.edit(embed=embed)
            #Two 100
            elif ((stop1 == 0) and (stop2 == 0)) or ((stop2 == 0) and (stop3 == 0)) or ((stop1 == 0) and (stop3 == 0)):
                main.users[str(ctx.author.id)]['balance'] = int(main.users[str(ctx.author.id)]['balance']) + math.floor(bet * 2)
                main.saveDB('users', main.users)

                embed = discord.Embed(
                colour = discord.Colour.green()
                )
                embed.add_field(name =f'**Slot | User: {ctx.author.name}**', value=f'**---------------------\n-| {slotItems[stop1]} | {slotItems[stop2]} | {slotItems[stop3]} |-\n---------------------\n--- YOU WON ---**', inline=False)
                embed.add_field(name ='**Profit**', value = f'**${math.floor(bet * 2)}**', inline=True)
                embed.add_field(name ='**New Balance**', value = f'**${int(main.users[str(ctx.author.id)]["balance"])}**', inline=True)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                await message.edit(embed=embed)
            #Three Medals
            elif ((stop1 == 3) and (stop2 == 3) and (stop3 == 3)):
                main.users[str(ctx.author.id)]['balance'] = int(main.users[str(ctx.author.id)]['balance']) + math.floor(bet * 2.5)
                main.saveDB('users', main.users)

                embed = discord.Embed(
                colour = discord.Colour.green()
                )
                embed.add_field(name =f'**Slot | User: {ctx.author.name}**', value=f'**---------------------\n-| {slotItems[stop1]} | {slotItems[stop2]} | {slotItems[stop3]} |-\n---------------------\n--- YOU WON ---**', inline=False)
                embed.add_field(name ='**Profit**', value = f'**${math.floor(bet * 2.5)}**', inline=True)
                embed.add_field(name ='**New Balance**', value = f'**${int(main.users[str(ctx.author.id)]["balance"])}**', inline=True)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                await message.edit(embed=embed)
            #Three Diamonds
            elif ((stop1 == 4) and (stop2 == 4) and (stop3 == 4)):
                main.users[str(ctx.author.id)]['balance'] = int(main.users[str(ctx.author.id)]['balance']) + math.floor(bet * 3)
                main.saveDB('users', main.users)

                embed = discord.Embed(
                colour = discord.Colour.green()
                )
                embed.add_field(name =f'**Slot | User: {ctx.author.name}**', value=f'**---------------------\n-| {slotItems[stop1]} | {slotItems[stop2]} | {slotItems[stop3]} |-\n---------------------\n--- YOU WON ---**', inline=False)
                embed.add_field(name ='**Profit**', value = f'**${math.floor(bet * 3)}**', inline=True)
                embed.add_field(name ='**New Balance**', value = f'**${int(main.users[str(ctx.author.id)]["balance"])}**', inline=True)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                await message.edit(embed=embed)
            #Two Cash
            elif ((stop1 == 2) and (stop2 == 2)) or ((stop2 == 2) and (stop3 == 2)) or ((stop1 == 2) and (stop3 == 2)):
                main.users[str(ctx.author.id)]['balance'] = int(main.users[str(ctx.author.id)]['balance']) + math.floor(bet * 3.5)
                main.saveDB('users', main.users)

                embed = discord.Embed(
                colour = discord.Colour.green()
                )
                embed.add_field(name =f'**Slot | User: {ctx.author.name}**', value=f'**---------------------\n-| {slotItems[stop1]} | {slotItems[stop2]} | {slotItems[stop3]} |-\n---------------------\n--- YOU WON ---**', inline=False)
                embed.add_field(name ='**Profit**', value = f'**${math.floor(bet * 3.5)}**', inline=True)
                embed.add_field(name ='**New Balance**', value = f'**${int(main.users[str(ctx.author.id)]["balance"])}**', inline=True)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                await message.edit(embed=embed)
            #Three 100
            elif ((stop1 == 0) and (stop2 == 0) and (stop3 == 0)):
                main.users[str(ctx.author.id)]['balance'] = int(main.users[str(ctx.author.id)]['balance']) + math.floor(bet * 4)
                main.saveDB('users', main.users)

                embed = discord.Embed(
                colour = discord.Colour.green()
                )
                embed.add_field(name =f'**Slot | User: {ctx.author.name}**', value=f'**---------------------\n-| {slotItems[stop1]} | {slotItems[stop2]} | {slotItems[stop3]} |-\n---------------------\n--- YOU WON ---**', inline=False)
                embed.add_field(name ='**Profit**', value = f'**${math.floor(bet * 4)}**', inline=True)
                embed.add_field(name ='**New Balance**', value = f'**${int(main.users[str(ctx.author.id)]["balance"])}**', inline=True)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                await message.edit(embed=embed)
            #Two Money Bag
            elif ((stop1 == 1) and (stop2 == 1)) or ((stop2 == 1) and (stop3 == 1)) or ((stop1 == 1) and (stop3 == 1)):
                main.users[str(ctx.author.id)]['balance'] = int(main.users[str(ctx.author.id)]['balance']) + math.floor(bet * 7)
                main.saveDB('users', main.users)

                embed = discord.Embed(
                colour = discord.Colour.green()
                )
                embed.add_field(name =f'**Slot | User: {ctx.author.name}**', value=f'**---------------------\n-| {slotItems[stop1]} | {slotItems[stop2]} | {slotItems[stop3]} |-\n---------------------\n--- YOU WON ---**', inline=False)
                embed.add_field(name ='**Profit**', value = f'**${math.floor(bet * 7)}**', inline=True)
                embed.add_field(name ='**New Balance**', value = f'**${int(main.users[str(ctx.author.id)]["balance"])}**', inline=True)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                await message.edit(embed=embed)
            #Three Cash
            elif ((stop1 == 2) and (stop2 == 2) and (stop3 == 2)):
                main.users[str(ctx.author.id)]['balance'] = int(main.users[str(ctx.author.id)]['balance']) + math.floor(bet * 7)
                main.saveDB('users', main.users)

                embed = discord.Embed(
                colour = discord.Colour.green()
                )
                embed.add_field(name =f'**Slot | User: {ctx.author.name}**', value=f'**---------------------\n-| {slotItems[stop1]} | {slotItems[stop2]} | {slotItems[stop3]} |-\n---------------------\n--- YOU WON ---**', inline=False)
                embed.add_field(name ='**Profit**', value = f'**${math.floor(bet * 7)}**', inline=True)
                embed.add_field(name ='**New Balance**', value = f'**${int(main.users[str(ctx.author.id)]["balance"])}**', inline=True)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                await message.edit(embed=embed)
            #Three Money Bag
            elif ((stop1 == 1) and (stop2 == 1) and (stop3 == 1)):
                main.users[str(ctx.author.id)]['balance'] = int(main.users[str(ctx.author.id)]['balance']) + math.floor(bet * 15)
                main.saveDB('users', main.users)

                embed = discord.Embed(
                colour = discord.Colour.green()
                )
                embed.add_field(name =f'**Slot | User: {ctx.author.name}**', value=f'**---------------------\n-| {slotItems[stop1]} | {slotItems[stop2]} | {slotItems[stop3]} |-\n---------------------\n--- YOU WON ---**', inline=False)
                embed.add_field(name ='**Profit**', value = f'**${math.floor(bet * 15)}**', inline=True)
                embed.add_field(name ='**New Balance**', value = f'**${int(main.users[str(ctx.author.id)]["balance"])}**', inline=True)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                await message.edit(embed=embed)
            else:
                embed = discord.Embed(
                colour = discord.Colour.red()
                )
                embed.add_field(name =f'**Slot | User: {ctx.author.name}**', value=f'**---------------------\n-| {slotItems[stop1]} | {slotItems[stop2]} | {slotItems[stop3]} |-\n---------------------\n--- YOU LOST ---**', inline=False)
                embed.add_field(name ='**Profit**', value = f'**$-{bet}**', inline=True)
                embed.add_field(name ='**New Balance**', value = f'**${int(main.users[str(ctx.author.id)]["balance"])}**', inline=True)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                
                await message.edit(embed=embed)

        else:
            embed = discord.Embed(
            title = f'ERROR: Insufficent Funds',
            description = f'Remaining: {balance}',
            colour = discord.Colour.red()
            )

            embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/coin-flip.gif')
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

            await ctx.channel.send(embed = embed)


    @slots.error
    async def slots_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(color=discord.Colour.gold())
            embed.add_field(name="Help", value="Slot Machine", inline=False)
            embed.add_field(name="Winnings", value="🏅🏅❔ - **0.5x**\n💎💎❔ - **2x**\n💯💯❔ - **2x**\n🏅🏅🏅 - **2.5x**\n💎💎💎 - **3x**\n💵💵❔ - **3.5x**\n💯💯💯 - **4x**\n💰💰❔ - **7x**\n💵💵💵 - **7x**\n💰💰💰 - **15x**\n", inline=False)
            embed.add_field(name="Usage", value="**$slots <bet>**", inline=True)

            await ctx.channel.send(embed = embed)
    
def setup(bot):
    bot.add_cog(Slots(bot))