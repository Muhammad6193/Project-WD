#!/bin/bash
# Installer Chrome pour undetected_chromedriver
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb

# Démarrer ton bot
python bot.py

