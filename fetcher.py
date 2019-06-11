#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

.. _Google Python Style Guide
    https://github.com/google/styleguide/blob/gh-pages/pyguide.md
"""

__copyright__ = 'Copyright 2019, University of Messina'
__author__ = 'Lorenzo Carnevale <lorenzocarnevale@gmail.com>'
__credits__ = ''
__description__ = ''


# standard libraries
import os
import sys
import json
import argparse
# thierd parties libraries
from tqdm import tqdm
import tweepy
import pandas as pd


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--credentials",
						dest="credentials",
						help="Credentials filename.",
						type=str)

    parser.add_argument("-H", "--hashtag",
						dest="hashtag",
						help="Select the hashtag.",
						type=str)

    parser.add_argument("-l", "--lang",
                        dest="lang",
                        help="Define the tweets' language to be fetched.",
                        type=str, default='en')

    options = parser.parse_args()

    with open(options.credentials, 'r') as f:
        conf = json.load(f)
        CONSUMER_KEY = conf["consumer_key"]
        CONSUMER_SECRET = conf["consumer_secret"]
        ACCESS_KEY = conf["access_key"]
        ACCESS_SECRET = conf["access_secret"]
    OUT_DIRECTORY = 'data/'

    # access to Tweet APIs
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)

	# fetching tweets
    columns = [
		'timestamp',
		'text',
		'language',
		'username',
		'coordinates'
	]
    df = pd.DataFrame(columns=columns)
    try:
        print('Start fetching...')
        for status in tqdm(tweepy.Cursor(api.search, q=options.hashtag, lang=options.lang, rpp=100, tweet_mode='extended', include_rts=False).items(),unit="status"):
            if (not status.retweeted) and ('RT @' not in status.full_text):
                row = [
					status.created_at,
					status.full_text,
					status.lang,
					status.user.screen_name,
                    status.coordinates
                ]
            df.loc[status._json['id']] = row
    except KeyboardInterrupt:
        print("\nforced closing")
    finally:
        filename = '%s%s.csv' % (OUT_DIRECTORY, options.hashtag)
        if not os.path.exists(OUT_DIRECTORY):
            os.makedirs(OUT_DIRECTORY)
        df.to_csv(filename)
        print("saved on ", filename)


if __name__ == '__main__':
	main()
	exit()
