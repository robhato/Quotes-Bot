import asyncio
import discord 
from discord.ext import commands
import datetime
import sys
import os
import sqlite3 as sql

TOKEN = os.environ.get('QBT')
client = commands.Bot(command_prefix='!', case_insensitive=True)
start_run = False

@client.event
async def on_ready():
	db = sql.connect('main.sqlite')
	cur = db.cursor()
	cur.execute('''
		CREATE TABLE IF NOT EXISTS quotes(
			quote text,
			author text
		)
		''')
	cur.execute('''
		CREATE TABLE IF NOT EXISTS authors(
			author text PRIMARY KEY,
			contributions integer
		)
		''')
	print('Bot is ready!')
	return await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='The Boys'))

initial_extensions = ['cogs.extras', 'cogs.quotes_db']

if __name__ == '__main__':
	for extension in initial_extensions:
		try:
			client.load_extension(extension)
		except Exception as e:
			print(f'Failed to load extension {extension}', file=sys.stderr)
			traceback.print_exc()

@client.command(pass_context=True)
async def ping(ctx):
	await ctx.send("Pong!")

client.run(TOKEN)