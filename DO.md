# Create smallest droplet Ubuntu 18 on [Digital Ocean](https://www.digitalocean.com/).

# Run these commands:

    apt-get update 
    apt-get -y upgrade
    apt-get -y install python3-pip virtualenv
    useradd -m -s /bin/bash <someuser>
    passwd <someuser>
    su - <someuser>
    vi .bashrc (and add the environment variable)
    git clone <thisrepo>
    cd discord_hello_bot
    source venv/bin/activate
    pip install -r requirements.txt
    ./hello.py
   
# Test that the bot responds in discord
