#!/usr/bin/env python

"""
    Example call:
        ./examples.py --consumer_key="[CONSUMER KEY]" --consumer_secret="[CONSUMER SECRET]" --token="[TOKEN]" --token_secret="[TOKEN SECRET]"
"""

from yelpapi import YelpAPI
import argparse
from pprint import pprint

argparser = argparse.ArgumentParser(description='Example Yelp queries using yelpapi. Visit https://www.yelp.com/developers/manage_api_keys to get the necessary API keys.')
argparser.add_argument('--consumer_key', type=str, help='Yelp v2.0 API consumer key')
argparser.add_argument('--consumer_secret', type=str, help='Yelp v2.0 API consumer secret')
argparser.add_argument('--token', type=str, help='Yelp v2.0 API token')
argparser.add_argument('--token_secret', type=str, help='Yelp v2.0 API token secret')
args = argparser.parse_args()

yelp_api = YelpAPI(args.consumer_key, args.consumer_secret, args.token, args.token_secret)

"""
    Example search by location text and term. Take a look at https://www.yelp.com/developers/documentation/v2/search_api for
    the various options available.
"""
print('***** 5 best rated ice cream places in Austin, TX *****\n%s\n' % "yelp_api.search_query(term='ice cream', location='austin, tx', sort=2, limit=5)")
response = yelp_api.search_query(term='ice cream', location='austin, tx', sort=2, limit=5)
pprint(response)

print('\n-------------------------------------------------------------------------\n')

"""
    Example search by bounding box and category. See https://www.yelp.com/developers/documentation/v2/all_category_list for an official
    list of Yelp categories. The bounding box definition comes from http://isithackday.com/geoplanet-explorer/index.php?woeid=12587707.
"""
print('***** 5 bike rentals in San Francisco county *****\n%s\n' % "yelp_api.search_query(category_filter='bikerentals', bounds='37.678799,-123.125740|37.832371,-122.356979', limit=5)")
response = yelp_api.search_query(category_filter='bikerentals', bounds='37.678799,-123.125740|37.832371,-122.356979', limit=5)
pprint(response)

print('\n-------------------------------------------------------------------------\n')

"""
    Example business query. Look at https://www.yelp.com/developers/documentation/v2/business for more information.
"""
print("***** selected reviews for Amy's on 6th St. *****\n%s\n" % "yelp_api.business_query(id='amys-ice-creams-austin-3')")
response = yelp_api.business_query(id='amys-ice-creams-austin-3')
pprint(response)

print('\n-------------------------------------------------------------------------\n')

"""
    Example phone search query. Look at https://www.yelp.com/developers/documentation/v2/phone_search for
    more information.
"""
print("***** search for business by phone number *****\n%s\n" % "yelp_api.phone_search_query(phone='+13193375512')")
response = yelp_api.phone_search_query(phone='+13193375512')
pprint(response)

print('\n-------------------------------------------------------------------------\n')

"""
    Example erronious search query.
"""
print('***** sample erronious search query *****\n%s\n' % "yelp_api.search_query(term='ice cream', location='austin, tx', sort=3)")
try:
    # sort can only take on values 0, 1, or 2
    yelp_api.search_query(term='ice cream', location='austin, tx', sort=3)
except YelpAPI.YelpAPIError as e:
    print(e)

print('\n-------------------------------------------------------------------------\n')

"""
    Example erronious business query.
"""
print('***** sample erronious business query *****\n%s\n' % "yelp_api.business_query(id='fake-business')")
try:
    yelp_api.business_query(id='fake-business')
except YelpAPI.YelpError as e:
    print(e)
