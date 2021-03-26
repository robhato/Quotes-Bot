import discord
from discord.ext import commands
import asyncio
import datetime
import sqlite3 as sql

class DbCog(commands.Cog, name='Quotes'):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def add_quote(self, ctx, *, quote:str=None):
		db = sql.connect('main.sqlite')
		cur = db.cursor()
		try:
			if quote is None:
				await ctx.send("Please enter a quote!")
			else:
				x = quote.split(" - ")
				q = x[0].lower()
				a = x[1].lower()
				cur.execute('INSERT INTO quotes VALUES (?,?)', (q,a))
				cur.execute('SELECT author FROM authors WHERE author=?', (a,))
				author_exists = cur.fetchone()
				print(author_exists)
				if author_exists:
					cur.execute('UPDATE authors SET contributions = contributions + 1 WHERE author = ?', (a,))
				else:
					cur.execute('INSERT INTO authors VALUES (?, ?)', (a,1))
				db.commit()
				db.close()
				await ctx.send(f'Quote added by {ctx.message.author.mention}!')
		except:
			await ctx.send('Unable to add quote!')

	@commands.command()
	async def get_quotes_by_author(self, ctx, *, author:str=None):
		db = sql.connect('main.sqlite')
		cur = db.cursor()
		try:
			if author is None:
				await ctx.send("Please enter an author's name!")
			else:
				a = author.lower()
				cur.execute('SELECT author FROM quotes WHERE quote = ?', (a,))
				quotes = cur.fetchall()
				clean_quotes = [''.join(i) for i in quotes]
				res = str(clean_quotes)[1:-1]
				db.close()
				await ctx.send(res)
		except:
			await ctx.send('Unable to get quotes!')

	@commands.command()
	async def get_quotes_by_phrase(self, ctx, *, phrase:str=None):
		db = sql.connect('main.sqlite')
		cur = db.cursor()
		try:
			if phrase is None:
				await ctx.send("Please enter a phrase!")
			else:
				p = phrase.lower()
				cur.execute('SELECT author FROM quotes WHERE author LIKE ?', (f'%{p}%',))
				quotes = cur.fetchall()
				clean_quotes = [''.join(i) for i in quotes]
				res = str(clean_quotes)[1:-1]
				db.close()
				await ctx.send(res)
		except:
			await ctx.send('Unable to get quotes!')

	@commands.command()
	async def get_all_quotes(self, ctx):
		db = sql.connect('main.sqlite')
		cur = db.cursor()
		try:
			cur.execute('SELECT author FROM quotes ORDER BY author')
			quotes = cur.fetchall()
			clean_quotes = [''.join(i) for i in quotes]
			res = str(clean_quotes)[1:-1]
			db.close()
			await ctx.send(res)
		except:
			await ctx.send('Unable to get quotes!')

	@commands.command()
	async def contributions(self, ctx, *, author:str=None):
		db = sql.connect('main.sqlite')
		cur = db.cursor()
		try:
			if author is None:
				await ctx.send("Please enter an author's name!")
			else:
				a = author.lower()
				cur.execute('SELECT contributions FROM authors WHERE author = ?', (a,))
				contributions = cur.fetchone()
				res = int(''.join(map(str, contributions)))
				db.close()
				await ctx.send(res)
		except:
			await ctx.send('Unable to get contributions!')

def setup(client):
	client.add_cog(DbCog(client))
	print('Quotes Db Cog loaded!')