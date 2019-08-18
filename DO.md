# Create smallest droplet Ubuntu 18 on [Digital Ocean](https://www.digitalocean.com/).

# Run these commands:

    apt-get update 
    apt-get -y upgrade
    apt-get -y install python3-pip virtualenv
    useradd -m -s /bin/bash dbots
    passwd dbots
    su - dbots
    vi .env (and add the export DISCORD_HELLO_TOKEN='xxx' line)
    vi .bashrc (and add 'source ./.env' to the end)
    git clone <thisrepo>
    cd discord_hello_bot
    source venv/bin/activate
    pip install -r requirements.txt
   
# Test that the bot responds in discord using python script

    ./hello.py

# Kill the hello.py script by pressing ^C twice

# Test that the bot responds in discord using bash script

    ./hello.bash

# Kill the hello.bash script by pressing ^C twice

# Create discord_hello.service (as root)

    cp discord_hello.service /etc/systemd/system/discord_hello.service
    systemctl daemon-reload
    systemctl start discord_hello.service
    systemctl status discord_hello.service
    tail -n 20 /var/log/syslog
    systemctl enable discord_hello.service

# Create discord_fun.service (as root)

    vi .env (and add the export DISCORD_FUN_TOKEN='xxx' line and 'export X_CMC_PRO_API_KEY=""' where that is your coin market cap pro api key)
    cp discord_fun.service /etc/systemd/system/discord_fun.service
    systemctl daemon-reload
    systemctl start discord_fun.service
    systemctl enable discord_fun.service

# Updating (get updates)
    su - dbots
    cd discord_hello_bot
    git pull
    exit
    systemctl restart discord_hello.service
