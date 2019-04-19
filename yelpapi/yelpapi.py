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

import requests

AUTOCOMPLETE_API_URL = 'https://api.yelp.com/v3/autocomplete'
BUSINESS_API_URL = 'https://api.yelp.com/v3/businesses/{}'
BUSINESS_MATCH_API_URL = 'https://api.yelp.com/v3/businesses/matches'
EVENT_LOOKUP_API_URL = 'https://api.yelp.com/v3/events/{}'
EVENT_SEARCH_API_URL = 'https://api.yelp.com/v3/events'
FEATURED_EVENT_API_URL = 'https://api.yelp.com/v3/events/featured'
PHONE_SEARCH_API_URL = 'https://api.yelp.com/v3/businesses/search/phone'
REVIEWS_API_URL = 'https://api.yelp.com/v3/businesses/{}/reviews'
SEARCH_API_URL = 'https://api.yelp.com/v3/businesses/search'
TRANSACTION_SEARCH_API_URL = 'https://api.yelp.com/v3/transactions/{}/search'


class YelpAPI:

    """
        This class implements the complete Yelp Fusion API. It offers access to the following APIs:
        
            * Autocomplete API - https://www.yelp.com/developers/documentation/v3/autocomplete
            * Business API - https://www.yelp.com/developers/documentation/v3/business
            * Business Match API - https://www.yelp.com/developers/documentation/v3/business_match
            * Event Lookup API - https://www.yelp.com/developers/documentation/v3/event
            * Event Search API - https://www.yelp.com/developers/documentation/v3/event_search
            * Featured Event API - https://www.yelp.com/developers/documentation/v3/featured_event
            * Phone Search API - https://www.yelp.com/developers/documentation/v3/business_search_phone
            * Reviews API - https://www.yelp.com/developers/documentation/v3/business_reviews
            * Search API - https://www.yelp.com/developers/documentation/v3/business_search
            * Transaction Search API - https://www.yelp.com/developers/documentation/v3/transactions_search

        It is simple and completely extensible since it dynamically takes arguments. This will allow it to continue
        working even if Yelp changes the spec. The only thing that should cause this to break is if Yelp changes the URL
        scheme.

        The structure of each method is quite simple. Some parameters help form the request URL (e.g., a ID of some
        sort), and other parameters are a part of the JSON request. Parameters that are a part of the URL are
        explicitly asked for as a part of the method definition. Parameters that are a part of the JSON request
        are passed via `**kwargs`. Some parameters are required, and others are optional. To avoid unnecessarily using
        precious API calls, each method explicitly checks for parameters that are required in order for the query to
        succeed before issuing the call.
    """

    class YelpAPIError(Exception):

        """
            This class is used for all API errors. Currently, there is no master list of all possible errors, but
            there is an open issue on this: https://github.com/Yelp/yelp-fusion/issues/95.
        """
        pass

    def __init__(self, api_key, timeout_s=None):
        """
            Instantiate a YelpAPI object. An API key from Yelp is required.

            required parameters:
                * api_key - Our Yelp API key

            optional parameters:
                * timeout_s - Timeout, in seconds, to set for all API calls. If the
                  the timeout expires before the request completes, then a Timeout
                  exception will be raised. If this is not given, the default is to
                  block indefinitely.
        """
        self._api_key = api_key
        self._timeout_s = timeout_s
        self._yelp_session = requests.Session()
        self._headers = {'Authorization': 'Bearer {}'.format(self._api_key)}

    def autocomplete_query(self, **kwargs):
        """
            Query the Yelp Autocomplete API.
            
            documentation: https://www.yelp.com/developers/documentation/v3/autocomplete

            required parameters:
                * text - search text
        """
        if not kwargs.get('text'):
            raise ValueError('Valid text (parameter "text") must be provided.')

        return self._query(AUTOCOMPLETE_API_URL, **kwargs)

    def business_query(self, id, **kwargs):
        """
            Query the Yelp Business API.
            
            documentation: https://www.yelp.com/developers/documentation/v3/business

            required parameters:
                * id - business ID
        """
        if not id:
            raise ValueError('A valid business ID (parameter "id") must be provided.')

        return self._query(BUSINESS_API_URL.format(id), **kwargs)

    def business_match_query(self, **kwargs):
        """
            Query the Yelp Business Match API.
            
            documentation: https://www.yelp.com/developers/documentation/v3/business_match

            required parameters:
                * name - business name
                * city
                * state
                * country
                * address1

            NOTE: `match_type` is deprecated since April 1, 2019.
        """
        if not kwargs.get('name'):
            raise ValueError('Valid business name (parameter "name") must be provided.')

        if not kwargs.get('city'):
            raise ValueError('Valid city (parameter "city") must be provided.')

        if not kwargs.get('state'):
            raise ValueError('Valid state (parameter "state") must be provided.')

        if not kwargs.get('country'):
            raise ValueError('Valid country (parameter "country") must be provided.')

        if not kwargs.get('address1'):
            raise ValueError('Valid address (parameter "address1") must be provided.')

        return self._query(BUSINESS_MATCH_API_URL, **kwargs)

    def event_lookup_query(self, id, **kwargs):
        """
            Query the Yelp Event Lookup API.
            
            documentation: https://www.yelp.com/developers/documentation/v3/event

            required parameters:
                * id - event ID
        """
        if not id:
            raise ValueError('A valid event ID (parameter "id") must be provided.')

        return self._query(EVENT_LOOKUP_API_URL.format(id), **kwargs)

    def event_search_query(self, **kwargs):
        """
            Query the Yelp Event Search API.
            
            documentation: https://www.yelp.com/developers/documentation/v3/event_search
        """
        return self._query(EVENT_SEARCH_API_URL, **kwargs)

    def featured_event_query(self, **kwargs):
        """
            Query the Yelp Featured Event API.

            documentation: https://www.yelp.com/developers/documentation/v3/featured_event

            required parameters:
                * one of either:
                    * location - text specifying a location to search for
                    * latitude and longitude
        """
        if not kwargs.get('location') and (not kwargs.get('latitude') or not kwargs.get('longitude')):
            raise ValueError('A valid location (parameter "location") or latitude/longitude combination '
                             '(parameters "latitude" and "longitude") must be provided.')

        return self._query(FEATURED_EVENT_API_URL, **kwargs)

    def phone_search_query(self, **kwargs):
        """
            Query the Yelp Phone Search API.
            
            documentation: https://www.yelp.com/developers/documentation/v3/business_search_phone

            required parameters:
                * phone - phone number
        """
        if not kwargs.get('phone'):
            raise ValueError('A valid phone number (parameter "phone") must be provided.')

        return self._query(PHONE_SEARCH_API_URL, **kwargs)

    def reviews_query(self, id, **kwargs):
        """
            Query the Yelp Reviews API.
            
            documentation: https://www.yelp.com/developers/documentation/v3/business_reviews

            required parameters:
                * id - business ID
        """
        if not id:
            raise ValueError('A valid business ID (parameter "id") must be provided.')

        return self._query(REVIEWS_API_URL.format(id), **kwargs)

    def search_query(self, **kwargs):
        """
            Query the Yelp Search API.
            
            documentation: https://www.yelp.com/developers/documentation/v3/business_search

            required parameters:
                * one of either:
                    * location - text specifying a location to search for
                    * latitude and longitude
        """
        if not kwargs.get('location') and (not kwargs.get('latitude') or not kwargs.get('longitude')):
            raise ValueError('A valid location (parameter "location") or latitude/longitude combination '
                             '(parameters "latitude" and "longitude") must be provided.')

        return self._query(SEARCH_API_URL, **kwargs)

    def transaction_search_query(self, transaction_type, **kwargs):
        """
            Query the Yelp Transaction Search API.
            
            documentation: https://www.yelp.com/developers/documentation/v3/transactions_search
            
            required parameters:
                * transaction_type - transaction type
                * one of either:
                    * location - text specifying a location to search for
                    * latitude and longitude
        """
        if not transaction_type:
            raise ValueError('A valid transaction type (parameter "transaction_type") must be provided.')

        if not kwargs.get('location') and (not kwargs.get('latitude') or not kwargs.get('longitude')):
            raise ValueError('A valid location (parameter "location") or latitude/longitude combination '
                             '(parameters "latitude" and "longitude") must be provided.')

        return self._query(TRANSACTION_SEARCH_API_URL.format(transaction_type), **kwargs)

    @staticmethod
    def _get_clean_parameters(kwargs):
        """
            Clean the parameters by filtering out any parameters that have a None value.
        """
        return dict((k, v) for k, v in kwargs.items() if v is not None)

    def _query(self, url, **kwargs):
        """
            All query methods have the same logic, so don't repeat it! Query the URL, parse the response as JSON,
            and check for errors. If all goes well, return the parsed JSON.
        """
        parameters = YelpAPI._get_clean_parameters(kwargs)
        response = self._yelp_session.get(
            url,
            headers=self._headers,
            params=parameters,
            timeout=self._timeout_s,
        )
        response_json = response.json()  # shouldn't happen, but this will raise a ValueError if the response isn't JSON

        # Yelp can return one of many different API errors, so check for one of them.
        # The Yelp Fusion API does not yet have a complete list of errors, but this is on the TODO list; see
        # https://github.com/Yelp/yelp-fusion/issues/95 for more info.
        if 'error' in response_json:
            raise YelpAPI.YelpAPIError('{}: {}'.format(response_json['error']['code'],
                                                       response_json['error']['description']))

        # we got a good response, so return
        return response_json
