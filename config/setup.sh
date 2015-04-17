#!/bin/bash
#
# Set up a new production box.
#

# install necessary packages
apt-get update
apt-get install -y git nginx python3 pip3 nodejs-legacy npm supervisor yui-compressor
npm install -g typescript nunjucks
pip3 install -r requirements.txt

# install redis from ppa so we get the latest
apt-get install -y python-software-properties
add-apt-repository -y ppa:rwky/redis
apt-get update
apt-get install -y redis-server

# create logs directory
mkdir -p /var/www/letsreview.io/logs/{nginx,gunicorn,review}
