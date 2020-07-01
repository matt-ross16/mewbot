#Author smilegodly
import requests
import subprocess
import discord
from discord.ext import commands
from discord import Game
import asyncio
from datetime import datetime
from datetime import time
import youtube_dl
from utils.funcs import Funcs
from utils.ytplayer import Music
from utils.secretgrabber import getSecret
from utils.apod import Apod
from itertools import cycle
import io
import aiohttp


PREFIX = ("!", "?", "./", "~")

bot = commands.Bot(command_prefix=PREFIX)

bot.remove_command('help')

secret = getSecret()

@bot.event
async def on_ready():
	game = discord.Game("RuneLite")
	await bot.change_presence(status=discord.Status.idle, activity=game)
	print("Logged in as ")
	print(bot.user.name)
	print(bot.user.id)
	print("-------------")


async def my_background_task():
	await bot.wait_until_ready()
	morningTime = time.fromisoformat('10:00')
	channel = bot.get_channel(409198534949077024) # channel ID
	while not bot.is_closed():
		now = datetime.now()
		if(now.hour == morningTime.hour):
			
			apodData = Apod.getApodData()

			if(apodData['media_type'] == 'image'):

				data = getImageFromUrl(apodData['url'])

				await channel.send(":rocket:"+ "\t" + "__**" + apodData['title'] + "**__" +"\t" + ":rocket:" + 
					"\t" + "__**" + apodData['date'] + "**__" + "\t" + ":rocket:" + "\n")
				await channel.send(file=discord.File(data, 'apod.png'))
				await channel.send("```" + "\n" + apodData['explanation'] + "\n" + "```")

			elif(apodData['media_type'] == 'video'):
				await channel.send(":rocket:"+ "\t" + "__**" + apodData['title'] + "**__" +"\t" + ":rocket:" + 
					"\t" + "__**" + apodData['date'] + "**__" + "\t" + ":rocket:" + "\n")
				await channel.send(apodData['url'].replace("?rel=0", "").replace("embed/", "watch?v=") + "\n")
				await channel.send("```" + "\n" + apodData['explanation'] + "\n" + "```")

		await asyncio.sleep(5*60) # task to runs every 30 mins

bot.add_cog(Music(bot))
bot.add_cog(Funcs(bot))
task = bot.loop.create_task(my_background_task())
bot.run(secret)
