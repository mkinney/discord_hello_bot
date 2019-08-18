# Create smallest droplet Ubuntu 18 on [Digital Ocean](https://www.digitalocean.com/).

# Run these commands: (note that *dbots* can be changed to most any other username)

    apt-get update 
    apt-get -y upgrade
    apt-get -y install python3-pip virtualenv
    useradd -m -s /bin/bash dbots
    passwd dbots
    su - dbots
    vi .bashrc (and add the environment variable)
    git clone <thisrepo>
    cd discord_hello_bot
    source venv/bin/activate
    pip install -r requirements.txt
    ./hello.py
   
# Test that the bot responds in discord

# Kill the hello.py script by pressing ^C twice

# Create discord_hello service

    cp discord_hello /etc/systemd/system/discord_hello
    systemctl daemon-reload
    systemctl enable discord_hello
