#!/usr/bin/env python

# Work with Python 3.6
import discord
import os

discord_hello_token = os.environ['DISCORD_HELLO_TOKEN']

client = discord.Client()

@client.event
async def on_message(message):

    # Do not want the bot to reply to itself
    if message.author == client.user:
        return

    # Not sure if this opens up some exploits. Feels unsafe.
    if message.content.startswith('!echo'):
        await message.channel.send(message.content)

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    if message.content.startswith('!help'):
        msg = '''
!echo - repeat what was typed
!hello - replies with 'hello <username>'
!help - this page
'''
        await message.channel.send(msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(discord_hello_token)
