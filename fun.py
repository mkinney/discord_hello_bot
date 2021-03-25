#!/usr/bin/env python

# Work with Python 3.6
import random
import asyncio
import aiohttp
import json
import os
from discord import Game
from discord.ext.commands import Bot

BOT_PREFIX = ("!")

discord_fun_token = os.environ['DISCORD_FUN_TOKEN']
cmc_key = os.environ['X_CMC_PRO_API_KEY']

client = Bot(command_prefix=BOT_PREFIX)


@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Answers from the beyond.",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
    ]
    await context.channel.send(random.choice(possible_responses) + ", " + context.message.author.mention)


@client.command()
async def square(context, number: str):
    squared_value = int(number) * int(number)
    await context.channel.send(str(number) + " squared is " + str(squared_value))


@client.event
async def on_ready():
    game=Game(name="with humans")
    await client.change_presence(activity=game)
    print("Logged in as " + client.user.name)


# Note: This requires an argument, but will default to some coins.
@client.command(name='prices')
async def prices(context, symbols="btc,eth"):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = { 'X-CMC_PRO_API_KEY': cmc_key }
    params = {'start': 1, 'limit': 1000, 'convert': 'USD'}
    _symbols = symbols.upper().split(',')

    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url, params=params, headers=headers)
        response = await raw_response.text()
        #print(response)
        response = json.loads(response)
        msg = ""
        for d in response["data"]:
            name = d["name"]
            symbol = d["symbol"]
            quote = d["quote"]["USD"]["price"]
            if symbol in _symbols:
                msg = msg + "`{:30s}({:5s}) {:>12,.4f}`".format(name, symbol, quote) + '\n'
        await context.channel.send(msg)


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(discord_fun_token)
