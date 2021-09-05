import discord
import asyncio

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from discord.ext import commands

class Stock(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stock(self, ctx):
        url = 'https://stocktrack.ca/?s=wm&upc=71171954104'
        driver = webdriver.Chrome(executable_path='C:\\Users\\Administrator\\Desktop\\Bot\\chromedriver.exe')

        driver.get(url)

        iframe = driver.find_elements_by_tag_name('iframe')[0]
        driver.switch_to.frame(iframe)

        try:
            myElem = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, r'/html/body/div[3]/div/div[1]/div[2]/div/div/div[2]/div[2]/div/div/table/tbody/tr/td[2]')))
        except TimeoutException:
            print("Loading took too much time!")
            return

        elem = driver.find_element_by_xpath(r'/html/body/div[3]/div/div[1]/div[2]/div/div/div[2]/div[2]/div/div/table/tbody/tr/td[2]')
        while "?" in elem.text:
            await asyncio.sleep(60)
        print(elem.text)
        embed = discord.Embed(
            title=f'PS5 Stock',
            description=f'{elem.text}',
            colour=discord.Colour.red()
        )

        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Stock(bot))



