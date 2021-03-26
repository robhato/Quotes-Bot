import discord
from discord.ext import commands
import asyncio
import datetime

class ExtCog(commands.Cog, name='Extras'):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def purge(self, ctx, *, number:int=None):
		if ctx.message.author.guild_permissions.manage_messages:
			try:
				if number is None:
					await ctx.send("You must enter a number!")
				else:
					deleted = await ctx.message.channel.purge(limit=number)
					await ctx.send(f'Messages deleted by {ctx.message.author.mention}: `{len(deleted)}`')
			except:
				await ctx.send('Unable to purge messages!')
		else:
			await ctx.send('You do not have the proper permissions to use this command!')

def setup(client):
	client.add_cog(ExtCog(client))
	print('Extras loaded!')