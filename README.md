Used [Make a discord bot in python](https://www.devdungeon.com/content/make-discord-bot-python) to get started with a discord *hello* bot.

# Create a server
If you don't already have a server, create one free one at https://discordapp.com. Simply log in, and then click the plus sign on the left side of the main window to create a new server.

# Create an app
Go to https://discordapp.com/developers/applications/me and create a new app. On your app detail page, save the Client ID. You will need it later to authorize your bot for your server.

# Create a bot account for your app
After creating app, on the app details page, scroll down to the section named bot, and create a bot user. Save the token, you will need it later to run the bot.

# Authorize the bot for your server
Visit the URL

    https://discordapp.com/oauth2/authorize?client_id=XXXXXXXXXXXX&scope=bot
    
but replace XXXX with your app client ID. Choose the server you want to add it to and select authorize.

# Create python environment to run bot (first time)

    virtualenv -p python3 venv
    source venv/bin/activate
    pip install discord.py
    pip freeze > requirements.txt

then later:

    source venv/bin/activate
    pip install -r requirements.txt


# Code the bot
See hello.py

Note: Had to change this line:

    await client.send_message(message.channel, msg)

to

    await message.channel.send(msg)

Another Note: I also pulled the token into an environment variable so I can share the source in git.

    chmod +x hello.py

# Setup somewhere to run the bot
[Spin up a digital ocean droplet](DO.md)

# Also see:
[Discord Docs](https://discordpy.readthedocs.io)
