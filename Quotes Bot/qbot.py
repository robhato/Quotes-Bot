import asyncio
import discord 
from discord.ext import commands
import datetime
import sys
import os
import sqlite3 as sql
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ.get('QBT')
client = commands.Bot(command_prefix='!', case_insensitive=True)
start_run = False

def get_quotes(numpages):
    quotes = []
    authors = []
    pages = []
    for i in range(2,numpages+1):
        pages.append("_" + str(i))
    for page in pages:
        base_url = "https://www.brainyquote.com/topics/inspirational-quotes"
        url = base_url + ".html"
        data = requests.get(url).text[:]
        soup = BeautifulSoup(data, 'html.parser')
        # Find quote values and add them to quotes array
        for item in soup.find_all("a", class_="b-qt"):
            quotes.append(item.get_text().rstrip())
        # Find author values and add them to authors array
        for item in soup.find_all("a", class_="bq-aut"):
            authors.append(item.get_text())
    # zip quotes and authors arrays in tuples list
    ans = zip(quotes, authors)
    return ans

inspiration = get_quotes(8)
inspiration = list(inspiration)
# list for quotes from brainy quotes
quo = []
# list for authors of quotes from brainy quotes
aut = []
for i in inspiration:
	quo.append(i[0])
	aut.append(i[1])

@client.event
async def on_ready():
	db = sql.connect('main-a.sqlite')
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
	cur.execute('''
		CREATE TABLE IF NOT EXISTS inspiration(
			quote text,
			author text
		)
		''')
	for i in range(len(quo)):
		cur.execute('INSERT INTO inspiration VALUES (?,?)', (quo[i],aut[i]))
	db.commit()
	db.close()
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