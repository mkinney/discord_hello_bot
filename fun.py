#!/usr/bin/env python

import random
import asyncio
import aiohttp
import json
import os
import requests
from discord import Embed, File, Game
from discord.ext.commands import Bot
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd

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


@client.command(brief='Sample parsing of arguments')
async def square(context, number: str):
    squared_value = int(number) * int(number)
    await context.channel.send(str(number) + " squared is " + str(squared_value))


# show how to embed an image in Discord
@client.command(brief='Show how to embed an image')
async def showimage(context):
    file = File("bitcoin.png")
    e = Embed()
    e.set_image(url="attachment://bitcoin.png")
    await context.channel.send(file = file, embed=e)


# show how to generate and embed an image in Discord
@client.command(brief='Show how to generate a graph then embed the image')
async def samplegraph(context):
    # generate a sample graph
    data = [25., 5., 150., 100.]
    x_values = range(len(data))
    fig = plt.bar(x_values, data)
    #plt.show()
    plt.savefig('samplegraph.png')
    plt.close()

    # now send the file to Discord
    file = File("samplegraph.png")
    e = Embed()
    e.set_image(url="attachment://samplegraph.png")
    # TODO: how to remove the temp image after shared?
    await context.channel.send(file = file, embed=e)


# Show how to plot a simple finance chart (candlesticks)
# Note: See https://github.com/matplotlib/mplfinance/blob/master/examples/savefig.ipynb
@client.command(brief='Show how to generate a financial chart (candlesticks)')
async def samplefinance(context):
    # Extracting Data for plotting
    df = pd.read_csv('SP500_NOV2019_Hist.csv', index_col=0, parse_dates=True)
    mpf.plot(df, type='candle', volume=True, savefig='samplefinance.png')

    # now send the file to Discord
    file = File("samplefinance.png")
    e = Embed()
    e.set_image(url="attachment://samplefinance.png")
    # TODO: how to remove the temp image after shared?
    await context.channel.send(file = file, embed=e)


# Plot data from coingecko
# See https://stackoverflow.com/questions/66035927/how-to-make-a-pandas-timestamp-object-subscriptable
@client.command(brief='Show graph from CoinGecko')
async def samplecg(context):
    API_URL = 'https://api.coingecko.com/api/v3'
    r = requests.get(API_URL + '/coins/bitcoin/market_chart?vs_currency=usd&days=3&interval=hourly')
    d = r.json()

    df = pd.DataFrame(d['prices'], columns = ['dateTime', 'price'])
    df['date'] = pd.to_datetime(df['dateTime'], unit='ms')

    ohlcdf = df.set_index('date')['price'].resample('4h').ohlc()
    mpf.plot(ohlcdf, type='candle', style='yahoo', savefig='samplecg.png')

    # now send the file to Discord
    file = File("samplecg.png")
    e = Embed()
    e.set_image(url="attachment://samplecg.png")
    # TODO: how to remove the temp image after shared?
    await context.channel.send(file = file, embed=e)


@client.event
async def on_ready():
    game=Game(name="with humans")
    await client.change_presence(activity=game)
    print("Logged in as " + client.user.name)


# Note: This requires an argument, but will default to some coins.
@client.command(name='prices', brief='Show Coinmarketcap prices from list (ex: "btc,eth")')
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
