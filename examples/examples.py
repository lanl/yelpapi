#!/usr/bin/env python

"""
    Copyright (c) 2013, Triad National Security, LLC
    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
    following conditions are met:

    * Redistributions of source code must retain the above copyright notice, this list of conditions and the following
      disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
      following disclaimer in the documentation and/or other materials provided with the distribution.
    * Neither the name of Triad National Security, LLC nor the names of its contributors may be used to endorse or
      promote products derived from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
    WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

"""
    Example call:
        ./examples.py "[API Key]"
"""

from yelpapi import YelpAPI
import argparse
from pprint import pprint

argparser = argparse.ArgumentParser(description='Example Yelp queries using yelpapi. '
                                                'Visit https://www.yelp.com/developers/v3/manage_app to get the '
                                                'necessary API keys.')
argparser.add_argument('api_key', type=str, help='Yelp Fusion API Key')
args = argparser.parse_args()

yelp_api = YelpAPI(args.api_key)

"""
    Example search by location text and term. 
    
    Search API: https://www.yelp.com/developers/documentation/v3/business_search
"""
print('***** 5 best rated ice cream places in Austin, TX *****\n{}\n'.format("yelp_api.search_query(term='ice cream', "
                                                                             "location='austin, tx', sort_by='rating', "
                                                                             "limit=5)"))
response = yelp_api.search_query(term='ice cream', location='austin, tx', sort_by='rating', limit=5)
pprint(response)
print('\n-------------------------------------------------------------------------\n')


"""
    Example search by centroid and category.
    
    all Yelp categories: https://www.yelp.com/developers/documentation/v3/all_category_list
    centroid: https://www.flickr.com/places/info/2487956
"""
print('***** 5 bike rentals in San Francisco *****\n{}\n'.format("yelp_api.search_query(categories='bikerentals', "
                                                                 "longitude=-122.4392, latitude=37.7474, limit=5)"))
response = yelp_api.search_query(categories='bikerentals', longitude=-122.4392, latitude=37.7474, limit=5)
pprint(response)
print('\n-------------------------------------------------------------------------\n')


"""
    Example phone search query.
    
    Phone Search API: https://www.yelp.com/developers/documentation/v3/business_search_phone
"""
print('***** search for business by phone number *****\n{}\n'.format("yelp_api.phone_search_query("
                                                                     "phone='+13193375512')"))
response = yelp_api.phone_search_query(phone='+13193375512')
pprint(response)
print('\n-------------------------------------------------------------------------\n')


"""
    Example business match query with the 'best' type.
    
    Business Match API: https://www.yelp.com/developers/documentation/v3/business_match
"""
print('***** search for business best match *****\n{}\n'.format("yelp_api.business_match_query(name='Splash Cafe', "
                                                                "address1='197 Pomeroy Ave', ",
                                                                "city='Pismo Beach', state='CA', country='US')"))
response = yelp_api.business_match_query(name='Splash Cafe',
                                         address1='197 Pomeroy Ave',
                                         city='Pismo Beach',
                                         state='CA',
                                         country='US')
pprint(response)
print('\n-------------------------------------------------------------------------\n')


"""
    Example business match query with the 'lookup' type.
    
    Business Match API: https://www.yelp.com/developers/documentation/v3/business_match
"""
print('***** search for business best match *****\n{}\n'.format("yelp_api.business_match_query(name='Splash Cafe', "
                                                                "address1='197 Pomeroy Ave', ",
                                                                "city='Pismo Beach', state='CA', country='US', match_type='lookup')"))
response = yelp_api.business_match_query(name='Splash Cafe',
                                         address1='197 Pomeroy Ave',
                                         city='Pismo Beach',
                                         state='CA',
                                         country='US',
                                         match_type='lookup')
pprint(response)
print('\n-------------------------------------------------------------------------\n')


"""
    Example transaction search query.
    
    Transaction Search API: https://www.yelp.com/developers/documentation/v3/transactions_search
"""
print("***** businesses in Dallas supporting delivery transactions *****\n{}\n".format("yelp_api.transaction_search_"
                                                                                       "query(transaction_type="
                                                                                       "'delivery', location='dallas, "
                                                                                       "tx')"))
response = yelp_api.transaction_search_query(transaction_type='delivery', location='dallas, tx')
pprint(response)
print('\n-------------------------------------------------------------------------\n')


"""
    Example business query.
    
    Business API: https://www.yelp.com/developers/documentation/v3/business
"""
print("***** business information for Amy's on 6th St. *****\n{}\n".format("yelp_api.business_query(id='amys-ice-"
                                                                           "creams-austin-3')"))
response = yelp_api.business_query(id='amys-ice-creams-austin-3')
pprint(response)
print('\n-------------------------------------------------------------------------\n')


"""
    Example reviews query.
    
    Reviews API: https://www.yelp.com/developers/documentation/v3/business_reviews
"""
print("***** selected reviews for Amy's on 6th St. *****\n{}\n".format("yelp_api.reviews_query(id='amys-ice-"
                                                                       "creams-austin-3')"))
response = yelp_api.reviews_query(id='amys-ice-creams-austin-3')
pprint(response)
print('\n-------------------------------------------------------------------------\n')


"""
    Example autocomplete query.
    
    Autocomplete API: https://www.yelp.com/developers/documentation/v3/autocomplete
    centroid: https://www.flickr.com/places/info/2427422
"""
print("***** autocomplete results for 'Hambur' in Iowa City *****\n{}\n".format("yelp_api.autocomplete_query("
                                                                                "text='Hambur', longitude=-91.5327, "
                                                                                "latitude=41.6560)"))
response = yelp_api.autocomplete_query(text='Hambur', longitude=-91.5327, latitude=41.6560)
pprint(response)
print('\n-------------------------------------------------------------------------\n')


"""
    Example event search query.
    
    Event Search API: https://www.yelp.com/developers/documentation/v3/event_search
"""
print("***** event search result *****\n{}\n".format("yelp_api.event_search_query()"))
response = yelp_api.event_search_query()
pprint(response)
print('\n-------------------------------------------------------------------------\n')


"""
    Example event lookup query.
    
    Event Lookup API: https://www.yelp.com/developers/documentation/v3/event
"""
print("***** event lookup result using previous search's first event *****\n{}\n".format("yelp_api.event_lookup_"
                                                                                         "query(id=response['events']"
                                                                                         "[0]['id'])"))
response = yelp_api.event_lookup_query(id=response['events'][0]['id'])
pprint(response)
print('\n-------------------------------------------------------------------------\n')


"""
    Example featured event query.
    
    Featured Event API: https://www.yelp.com/developers/documentation/v3/featured_event
"""
print("***** featured event lookup result for New York City, NY *****\n{}\n".format("yelp_api.featured_event_"
                                                                                    "query(location='New York City, "
                                                                                    "NY')"))
response = yelp_api.featured_event_query(location='New York City, NY')
pprint(response)
print('\n-------------------------------------------------------------------------\n')


"""
    Example erroneous search query.
"""
print('***** sample erroneous search query *****\n{}\n'.format("yelp_api.search_query(term='ice cream', "
                                                               "location='austin, tx', sort_by='BAD_SORT')"))
try:
    # sort can only take on values "best_match", "rating", "review_count", or "distance"
    yelp_api.search_query(term='ice cream', location='austin, tx', sort_by='BAD_SORT')
except YelpAPI.YelpAPIError as e:
    print(e)
print('\n-------------------------------------------------------------------------\n')


"""
    Example erroneous business query.
"""
print('***** sample erroneous business query *****\n{}\n'.format("yelp_api.business_query(id='fake-business')"))
try:
    yelp_api.business_query(id='fake-business')
except YelpAPI.YelpAPIError as e:
    print(e)
