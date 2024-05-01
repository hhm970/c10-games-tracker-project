#!/usr/bin/bash

echo "Downloading Firefox version 113.0"
mkdir -p "/opt/firefox/113.0/firefox/firefox"
curl -Lo "/opt/firefox/113.0/firefox-113.0.tar.bz2" "http://ftp.mozilla.org/pub/firefox/releases/113.0/linux-x86_64/en-US/firefox-113.0.tar.bz2"
tar -jxf "/opt/firefox/113.0/firefox-113.0.tar.bz2" -C "/opt/firefox/113.0/"
rm -rf "/opt/firefox/113.0/firefox-113.0.tar.bz2"

# Download Geckodriver

echo "Downloading Geckodriver version 0.33.0"
mkdir -p "/opt/geckodriver/0.33.0/geckodriver"
curl -Lo "/opt/geckodriver/0.33.0/geckodriver-v0.33.0-linux64.tar.gz" "https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz"
tar -zxf "/opt/geckodriver/0.33.0/geckodriver-v0.33.0-linux64.tar.gz" -C "/opt/geckodriver/0.33.0/"
chmod +x "/opt/geckodriver/0.33.0/geckodriver"
rm -rf "/opt/geckodriver/0.33.0/geckodriver-v0.33.0-linux64.tar.gz"