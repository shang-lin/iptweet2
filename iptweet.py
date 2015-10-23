__author__ = 'shanglin'

import tweepy
import requests
import ConfigParser
import sys

default_config = "iptweet.ini"

def load_config(config_file):
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    twitter_config = dict()
    twitter_config['consumer_key'] = config.get('twitter', 'CONSUMER_KEY')
    twitter_config['consumer_secret'] = config.get('twitter', 'CONSUMER_SECRET')
    twitter_config['access_token'] = config.get('twitter', 'ACCESS_TOKEN')
    twitter_config['access_token_secret'] = config.get('twitter', 'ACCESS_TOKEN_SECRET')
    return twitter_config

def tweet(ip, credentials):
    """
    Posts a tweet of the current IP address.
    :param ip:

    """

    auth = tweepy.OAuthHandler(credentials['consumer_key'], credentials['consumer_secret'])
    auth.set_access_token(credentials['access_token'], credentials['access_token_secret'])
    api = tweepy.API(auth)

    status = ip + ' #ip'
    api.update_status(status=status)

def main():

    try:
        twitter_config = load_config(default_config)
    except Exception, e:
        print(e)
        sys.exit(2)

    try:
        with open('ip', 'r') as infile:
            old_ip = infile.read()
    except IOError, e:
        old_ip = ''
    
    response = requests.get('http://shang-lin.com/ip.php')
    ip = response.json()['ip']

    if old_ip == '' or old_ip != ip:
        print "IP address has changed to", ip
        with open('ip', 'w') as outfile:
            outfile.write(ip)
        print "Tweeting new IP."
        tweet(ip, twitter_config)

if __name__ == "__main__":
    main()