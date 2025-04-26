#!/bin/bash

# Installer Google Chrome
apt update && apt install -y wget unzip
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb

# Lancer le bot
python bot.py
