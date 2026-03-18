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

# Example call:
#     ./examples.py "[API Key]"

import argparse
from pprint import pprint

from yelpapi import YelpAPI

SEP = '\n-------------------------------------------------------------------------\n'

argparser = argparse.ArgumentParser(
    description='Example Yelp queries using yelpapi. '
                'Visit https://docs.developer.yelp.com/docs/fusion-intro to get the necessary API keys.',
)
argparser.add_argument('api_key', type=str, help='Yelp Fusion API Key')
args = argparser.parse_args()

with YelpAPI(args.api_key) as yelp_api:
    # Search API: https://docs.developer.yelp.com/reference/v3_business_search
    print("***** 5 best rated ice cream places in Austin, TX *****\nyelp_api.search_query(term='ice cream', location='austin, tx', sort_by='rating', limit=5)\n")
    response = yelp_api.search_query(term='ice cream', location='austin, tx', sort_by='rating', limit=5)
    pprint(response)
    print(SEP)

    # Search API (by coordinates): https://docs.developer.yelp.com/reference/v3_business_search
    # all Yelp categories: https://docs.developer.yelp.com/docs/resources-categories
    # centroid: https://www.flickr.com/places/info/2487956
    print("***** 5 bike rentals in San Francisco *****\nyelp_api.search_query(categories='bikerentals', longitude=-122.4392, latitude=37.7474, limit=5)\n")
    response = yelp_api.search_query(categories='bikerentals', longitude=-122.4392, latitude=37.7474, limit=5)
    pprint(response)
    print(SEP)

    # Phone Search API: https://docs.developer.yelp.com/reference/v3_business_phone_search
    print("***** search for business by phone number *****\nyelp_api.phone_search_query(phone='+13193375512')\n")
    response = yelp_api.phone_search_query(phone='+13193375512')
    pprint(response)
    print(SEP)

    # Business Match API: https://docs.developer.yelp.com/reference/v3_business_match
    print("***** search for business match *****\nyelp_api.business_match_query(name='Splash Cafe', address1='197 Pomeroy Ave', city='Pismo Beach', state='CA', country='US')\n")
    response = yelp_api.business_match_query(
        name='Splash Cafe',
        address1='197 Pomeroy Ave',
        city='Pismo Beach',
        state='CA',
        country='US',
    )
    pprint(response)
    print(SEP)

    # Transaction Search API: https://docs.developer.yelp.com/reference/v3_transaction_search
    print("***** businesses in Dallas supporting delivery transactions *****\nyelp_api.transaction_search_query(transaction_type='delivery', location='dallas, tx')\n")
    response = yelp_api.transaction_search_query(transaction_type='delivery', location='dallas, tx')
    pprint(response)
    print(SEP)

    # Business API: https://docs.developer.yelp.com/reference/v3_business_info
    print("***** business information for Amy's on 6th St. *****\nyelp_api.business_query(id='amys-ice-creams-austin-3')\n")
    response = yelp_api.business_query(id='amys-ice-creams-austin-3')
    pprint(response)
    print(SEP)

    # Reviews API: https://docs.developer.yelp.com/reference/v3_business_reviews
    print("***** selected reviews for Amy's on 6th St. *****\nyelp_api.reviews_query(id='amys-ice-creams-austin-3')\n")
    response = yelp_api.reviews_query(id='amys-ice-creams-austin-3')
    pprint(response)
    print(SEP)

    # Review Highlights API: https://docs.developer.yelp.com/reference/v3_business_review_highlights
    # NOTE: requires a Premium Plan
    print("***** review highlights for Amy's on 6th St. *****\nyelp_api.review_highlights_query(id='amys-ice-creams-austin-3')\n")
    response = yelp_api.review_highlights_query(id='amys-ice-creams-austin-3')
    pprint(response)
    print(SEP)

    # Autocomplete API: https://docs.developer.yelp.com/reference/v3_autocomplete
    # centroid: https://www.flickr.com/places/info/2427422
    print("***** autocomplete results for 'Hambur' in Iowa City *****\nyelp_api.autocomplete_query(text='Hambur', longitude=-91.5327, latitude=41.6560)\n")
    response = yelp_api.autocomplete_query(text='Hambur', longitude=-91.5327, latitude=41.6560)
    pprint(response)
    print(SEP)

    # Categories API: https://docs.developer.yelp.com/reference/v3_all_categories
    print("***** all Yelp categories *****\nyelp_api.categories_query()\n")
    response = yelp_api.categories_query()
    pprint(response)
    print(SEP)

    # Category API: https://docs.developer.yelp.com/reference/v3_categories
    print("***** details for the 'icecream' category *****\nyelp_api.category_query(alias='icecream')\n")
    response = yelp_api.category_query(alias='icecream')
    pprint(response)
    print(SEP)

    # Event Search API: https://docs.developer.yelp.com/reference/v3_events_search
    print("***** event search result *****\nyelp_api.event_search_query()\n")
    response = yelp_api.event_search_query()
    pprint(response)
    print(SEP)

    # Event Lookup API: https://docs.developer.yelp.com/reference/v3_event
    print("***** event lookup result using previous search's first event *****\nyelp_api.event_lookup_query(id=response['events'][0]['id'])\n")
    response = yelp_api.event_lookup_query(id=response['events'][0]['id'])
    pprint(response)
    print(SEP)

    # Featured Event API: https://docs.developer.yelp.com/reference/v3_featured_event
    print("***** featured event lookup result for New York City, NY *****\nyelp_api.featured_event_query(location='New York City, NY')\n")
    response = yelp_api.featured_event_query(location='New York City, NY')
    pprint(response)
    print(SEP)

    # Business Engagement Metrics API: https://docs.developer.yelp.com/reference/v3_get_businesses_engagement
    # NOTE: requires special permissions on the Yelp Places API key
    print("***** engagement metrics for Amy's on 6th St. *****\nyelp_api.business_engagement_query(business_ids='amys-ice-creams-austin-3')\n")
    response = yelp_api.business_engagement_query(business_ids='amys-ice-creams-austin-3')
    pprint(response)
    print(SEP)

    # Business Service Offerings API: https://docs.developer.yelp.com/reference/v3_business_service_offerings
    # NOTE: requires special permissions on the Yelp Places API key
    print("***** service offerings for Amy's on 6th St. *****\nyelp_api.business_service_offerings_query(id='amys-ice-creams-austin-3')\n")
    response = yelp_api.business_service_offerings_query(id='amys-ice-creams-austin-3')
    pprint(response)
    print(SEP)

    # Example erroneous search query
    print("***** sample erroneous search query *****\nyelp_api.search_query(term='ice cream', location='austin, tx', sort_by='BAD_SORT')\n")
    try:
        # sort can only take on values "best_match", "rating", "review_count", or "distance"
        yelp_api.search_query(term='ice cream', location='austin, tx', sort_by='BAD_SORT')
    except YelpAPI.YelpAPIError as e:
        print(e)
    print(SEP)

    # Example erroneous business query
    print("***** sample erroneous business query *****\nyelp_api.business_query(id='fake-business')\n")
    try:
        yelp_api.business_query(id='fake-business')
    except YelpAPI.YelpAPIError as e:
        print(e)
