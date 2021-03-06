#!/usr/bin/env python

import random
import asyncio
import aiohttp
import subprocess
import json
import os
import re
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


# show how to run a command and send output to discord (ex: "fortune")
# Might need to run "sudo apt install fortune" (or "brew install fortune")
@client.command(brief='Run the "fortune" command')
async def fortune(context):
    output = subprocess.getoutput("fortune")
    await context.channel.send(output)
    # for fun, sleep for 2 seconds then remove user's bot request
    # Note: This assumes the bot has appropriate permssions
    message = context.message
    await asyncio.sleep(2)
    await message.delete()


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
    await context.channel.send(file = file, embed=e)
    await asyncio.sleep(5)
    os.remove('samplegraph.png')


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
    await context.channel.send(file = file, embed=e)
    await asyncio.sleep(5)
    os.remove('samplefinance.png')


# Plot data from coingecko
# See https://stackoverflow.com/questions/66035927/how-to-make-a-pandas-timestamp-object-subscriptable
@client.command(brief='Show graph from CoinGecko (defaults to "bitcoin")',
                description='Can specify any coin at CoinGecko. (ex: "ethereum")')
async def cg(context, symbol="bitcoin"):
    API_URL = 'https://api.coingecko.com/api/v3'

    # lower case all symbols
    symbol = symbol.lower()

    # allow for some short names
    if symbol in ("eth"):
        symbol = "ethereum"
    if symbol in ("btc"):
        symbol = "bitcoin"
    if symbol in ("whirl"):
        symbol = "whirl-finance"

    filename = 'cg.png'
    r = requests.get(API_URL + f"/coins/{symbol}/market_chart?vs_currency=usd&days=90")
    d = r.json()

    found = False
    try:
        df = pd.DataFrame(d['prices'], columns = ['dateTime', 'price'])
        df['date'] = pd.to_datetime(df['dateTime'], unit='ms')

        ohlcdf = df.set_index('date')['price'].resample('1d').ohlc()
        mpf.plot(ohlcdf, type='candle', mav=(21, 50),
                 tight_layout=True,
                 title=f'Coingecko:{symbol} 1H MAV(Blue=21,Orange=50)',
                 style='yahoo', figscale=2.0,
                 datetime_format='%m-%d', xrotation=90,
                 savefig=filename)

        # now send the file to Discord
        file = File(filename)
        e = Embed()
        e.set_image(url=f"attachment://{filename}")
        await context.channel.send(file = file, embed=e)
        await asyncio.sleep(5)
        os.remove(filename)
        found = True
    except KeyError:
        await context.channel.send(f'Warning: Symbol({symbol}) must not be valid. Try another.')
    if not found:
        r = requests.get(API_URL + "/coins/list?include_platform=true")
        d = r.json()
        for data in d:
            if symbol in (data["symbol"], data["name"]):
                await context.channel.send(f'Might try using ({data["id"]})')


# persist the list to local file
@client.command(brief='Update contracts for DevGuru',
                description='Update the list of BEP20 contracts from CoinGecko')
async def cgu(context):
    API_URL = 'https://api.coingecko.com/api/v3'
    r = requests.get(API_URL + "/coins/list?include_platform=true")
    d = r.json()
    with open('cgu.txt', 'w') as outfile:
        json.dump(d, outfile)
    await context.channel.send(f'Updated list')


# use local file instead of doing a web call everytime
@client.command(brief='Show info about contracts from local file',
                description='Show info from CoinGecko. To update the local file run "cgu"')
async def cgi(context, symbol):
    with open('cgu.txt') as json_file:
        data = json.load(json_file)
    found = False
    for d in data:
        if symbol in [ d['id'], d['symbol'], d['name'] ]:
            found = True
            await context.channel.send(f'Found: {d}')
    if not found:
        await context.channel.send(f'Could not find symbol({symbol})')


# use local file instead of doing a web call everytime
@client.command(brief='Show DevGuru link',
                description='Show info from DevGuru using local list from CoinGecko. To update the local file run "cgu"')
async def dg(context, symbol):
    with open('cgu.txt') as json_file:
        data = json.load(json_file)
    found = False
    for d in data:
        if symbol in [ d['id'], d['symbol'], d['name'] ]:
            found = True
            foundBC = False
            try:
                bc = d["platforms"]["binance-smart-chain"]
                foundBC = True
                if bc:
                    await context.channel.send(f'https://dex.guru/token/{bc}-bsc')
            except:
                pass
            # not binance, try ETH
            if not foundBC:
                try:
                    bc = d["platforms"]["ethereum"]
                    foundBC = True
                    if bc:
                        await context.channel.send(f'https://dex.guru/token/{bc}-eth')
                except:
                    pass
    if not found:
        await context.channel.send(f'Could not find symbol({symbol})')


# default to Fox 0xFAd8E46123D7b4e77496491769C167FF894d2ACB
@client.command(brief='Show number of holders for a contract',
                description='There are some short names. (etna, fox, hac, kirby, paw, rcvr, safemoon, uprize, whirl)')
async def holders(context, contract):

    # make the interface a little easier
    if contract in ("etna"):
        contract = "0x51f35073ff7cf54c9e86b7042e59a8cc9709fc46"
    if contract in ("fox"):
        contract = "0xFAd8E46123D7b4e77496491769C167FF894d2ACB"
    if contract in ("hac"):
        contract = "0xff56f98b5ec157b0cb208a152fbdba215129db15"
    if contract in ("kirby"):
        contract = "0x23b360e387d9e4d2646609861e68adc621a3af82"
    if contract in ("paw"):
        contract = "0x1CAA1e68802594EF24111ff0D10Eca592A2B5c58"
    if contract in ("rcvr"):
        contract = "0x26d4552879cdcc32599e2ff1c1e2a438d5c5323e"
    if contract in ("safemoon"):
        contract = "0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3"
    if contract in ("uprize"):
        contract = "0xbbab7de13326baa537fc9d329cbc70879c1578ee"
    if contract in ("whirl"):
        contract = "0x7f479d78380ad00341fdd7322fe8aef766e29e5a"

    if contract != '':
        url = f'https://bscscan.com/token/{contract}'
        page = requests.get(url)
        # Use regular expressions to find string in the html.
        # "I have a problem. I know! I'll use regular expressions.
        # Now I have two problems."
        p = re.compile(r'.* number of holders ([0-9,]+) ', re.DOTALL)
        m = p.match(page.text)
        holders = m.group(1)
        await context.channel.send(f'number of holders:{holders}')
    else:
        await context.channel.send(f'Warning: Could not determine number of holders.')


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
