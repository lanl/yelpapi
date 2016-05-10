"""
    Copyright (c) 2013, Los Alamos National Security, LLC
    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
    following conditions are met:

    * Redistributions of source code must retain the above copyright notice, this list of conditions and the following
      disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
      following disclaimer in the documentation and/or other materials provided with the distribution.
    * Neither the name of Los Alamos National Security, LLC nor the names of its contributors may be used to endorse or
      promote products derived from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
    WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
    THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from requests_oauthlib import OAuth1Session

SEARCH_API_URL = 'https://api.yelp.com/v2/search'
BUSINESS_API_URL = 'https://api.yelp.com/v2/business/{}'
PHONE_SEARCH_API_URL = 'https://api.yelp.com/v2/phone_search'


class YelpAPI(object):

    """
        This class implements the complete Yelp 2.0 API. It offers access to the Search API, Business API, and Phone Search API.
        It is simple and completely extensible since it dynamically takes arguments. This will allow it to continue working even
        if Yelp changes the spec. The only thing that should cause this to break is if Yelp changes the URL scheme.
    """

    class YelpAPIError(Exception):

        """
            This class is used for all API errors. For a list of all possible Yelp API errors, see
            https://www.yelp.com/developers/documentation/v2/errors.
        """
        pass

    def __init__(self, consumer_key, consumer_secret, token, token_secret):
        self._yelp_session = OAuth1Session(consumer_key, consumer_secret, token, token_secret)

    @staticmethod
    def _get_clean_parameters(kwargs):
        """
            Clean the parameters by filtering out any parameters that have a None value.
        """
        return dict((k, v) for k, v in kwargs.items() if v is not None)

    def search_query(self, **kwargs):
        """
            This function implements the Yelp Search API (https://www.yelp.com/developers/documentation/v2/search_api).

            Arbitrary keywords can be passed in, and a dynamically-generated dict of businesses will be returned.
        """
        return self._query(SEARCH_API_URL, **kwargs)

    def business_query(self, id, **kwargs):
        """
            This function implements the Yelp Business API (https://www.yelp.com/developers/documentation/v2/business).

            A mandatory business ID (parameter 'id') must be provided, as well as any arbitrary keywords allowed by Yelp. A single dict will be
            returned for the business.
        """
        if not id:
            raise ValueError('A valid business ID parameter ("id") must be provided.')

        return self._query(BUSINESS_API_URL.format(id), **kwargs)

    def phone_search_query(self, **kwargs):
        """
            This function implements the Yelp Phone Search API (https://www.yelp.com/developers/documentation/v2/phone_search).

            A mandatory phone number (parameter 'phone') must be provided, as well as any arbitrary keywords allowed by Yelp. If found, a
            dynamically-generated dict containing information on the matching business will be returned.
        """
        if 'phone' not in kwargs:
            raise ValueError('A phone number parameter ("phone") must be provided.')

        return self._query(PHONE_SEARCH_API_URL, **kwargs)

    def _query(self, url, **kwargs):
        """
            All query methods have the same logic, so don't repeat it! Query the URL, parse the response as JSON, and check for errors. If all
            goes well, return the parsed JSON.
        """
        parameters = YelpAPI._get_clean_parameters(kwargs)
        response = self._yelp_session.get(url, params=parameters)
        response_json = response.json() # it shouldn't happen, but this will raise a ValueError if the response isn't JSON

        # Yelp can return one of many different API errors, so check for one of them
        # possible errors: https://www.yelp.com/developers/documentation/v2/errors
        if 'error' in response_json:
            if 'field' in response_json['error']:
                raise YelpAPI.YelpAPIError(response_json['error']['id'], '{} [field={}]'.format(response_json['error']['text'], response_json['error']['field']))
            else:
                raise YelpAPI.YelpAPIError(response_json['error']['id'], response_json['error']['text'])

        # we got a good response, so return
        return response_json
