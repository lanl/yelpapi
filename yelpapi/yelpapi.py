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

from __future__ import annotations

from types import TracebackType
from typing import Any

import requests

AUTOCOMPLETE_API_URL = 'https://api.yelp.com/v3/autocomplete'
BUSINESS_API_URL = 'https://api.yelp.com/v3/businesses/{}'
BUSINESS_ENGAGEMENT_API_URL = 'https://api.yelp.com/v3/businesses/engagement'
BUSINESS_MATCH_API_URL = 'https://api.yelp.com/v3/businesses/matches'
BUSINESS_SERVICE_OFFERINGS_API_URL = 'https://api.yelp.com/v3/businesses/{}/service_offerings'
CATEGORIES_API_URL = 'https://api.yelp.com/v3/categories'
CATEGORY_API_URL = 'https://api.yelp.com/v3/categories/{}'
EVENT_LOOKUP_API_URL = 'https://api.yelp.com/v3/events/{}'
EVENT_SEARCH_API_URL = 'https://api.yelp.com/v3/events'
FEATURED_EVENT_API_URL = 'https://api.yelp.com/v3/events/featured'
PHONE_SEARCH_API_URL = 'https://api.yelp.com/v3/businesses/search/phone'
REVIEW_HIGHLIGHTS_API_URL = 'https://api.yelp.com/v3/businesses/{}/review_highlights'
REVIEWS_API_URL = 'https://api.yelp.com/v3/businesses/{}/reviews'
SEARCH_API_URL = 'https://api.yelp.com/v3/businesses/search'
TRANSACTION_SEARCH_API_URL = 'https://api.yelp.com/v3/transactions/{}/search'


class YelpAPI:
    """
        This class implements the complete Yelp Fusion API. It offers access to the following APIs:

            * Autocomplete API - https://docs.developer.yelp.com/reference/v3_autocomplete
            * Business API - https://docs.developer.yelp.com/reference/v3_business_info
            * Business Engagement Metrics API - https://docs.developer.yelp.com/reference/v3_get_businesses_engagement
            * Business Match API - https://docs.developer.yelp.com/reference/v3_business_match
            * Business Service Offerings API - https://docs.developer.yelp.com/reference/v3_business_service_offerings
            * Categories API - https://docs.developer.yelp.com/reference/v3_all_categories
            * Category API - https://docs.developer.yelp.com/reference/v3_categories
            * Event Lookup API - https://docs.developer.yelp.com/reference/v3_event
            * Event Search API - https://docs.developer.yelp.com/reference/v3_events_search
            * Featured Event API - https://docs.developer.yelp.com/reference/v3_featured_event
            * Phone Search API - https://docs.developer.yelp.com/reference/v3_business_phone_search
            * Review Highlights API - https://docs.developer.yelp.com/reference/v3_business_review_highlights
            * Reviews API - https://docs.developer.yelp.com/reference/v3_business_reviews
            * Search API - https://docs.developer.yelp.com/reference/v3_business_search
            * Transaction Search API - https://docs.developer.yelp.com/reference/v3_transaction_search

        It is simple and completely extensible since it dynamically takes arguments. This will allow it to continue
        working even if Yelp changes the spec. The only thing that should cause this to break is if Yelp changes the URL
        scheme.

        The structure of each method is quite simple. Some parameters help form the request URL (e.g., a ID of some
        sort), and other parameters are a part of the JSON request. Parameters that are a part of the URL are
        explicitly asked for as a part of the method definition. Parameters that are a part of the JSON request
        are passed via `**kwargs`. Some parameters are required, and others are optional. To avoid unnecessarily using
        precious API calls, each method explicitly checks for parameters that are required in order for the query to
        succeed before issuing the call.

        This class will create and use a single `requests.Session` object for all API calls, which will provide a nice
        performance boost with many calls. To avoid keeping unnecessary connections open, you should be sure to close
        the Session once all Yelp API interactions are complete. This can be done manully by calling close() or by
        using it as a context manager.
    """

    class YelpAPIError(Exception):
        """
            This class is used for all API errors. Currently, there is no master list of all possible errors, but
            there is an open issue on this: https://github.com/Yelp/yelp-fusion/issues/95.
        """
        pass

    def __init__(self, api_key: str, timeout_s: float | None = None) -> None:
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
        self._timeout_s = timeout_s
        self._yelp_session = requests.Session()
        self._headers = {'Authorization': f'Bearer {api_key}'}

    def close(self) -> None:
        """
            When the user is done interacting with the API, self.close() should be called to close the Session.
        """
        self._yelp_session.close()

    def __enter__(self) -> YelpAPI:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def autocomplete_query(self, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Autocomplete API.

            documentation: https://docs.developer.yelp.com/reference/v3_autocomplete

            required parameters:
                * text - search text
        """
        if not kwargs.get('text'):
            raise ValueError('Valid text (parameter "text") must be provided.')

        return self._query(AUTOCOMPLETE_API_URL, **kwargs)

    def business_query(self, id: str, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Business API.

            documentation: https://docs.developer.yelp.com/reference/v3_business_info

            required parameters:
                * id - business ID
        """
        if not id:
            raise ValueError('A valid business ID (parameter "id") must be provided.')

        return self._query(BUSINESS_API_URL.format(id), **kwargs)

    def business_match_query(self, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Business Match API.

            documentation: https://docs.developer.yelp.com/reference/v3_business_match

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

    def business_engagement_query(self, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Business Engagement Metrics API.

            documentation: https://docs.developer.yelp.com/reference/v3_get_businesses_engagement

            required parameters:
                * business_ids - comma-separated list of business IDs

            NOTE: requires special permissions on the Yelp Places API key.
        """
        if not kwargs.get('business_ids'):
            raise ValueError('Valid business IDs (parameter "business_ids") must be provided.')

        return self._query(BUSINESS_ENGAGEMENT_API_URL, **kwargs)

    def business_service_offerings_query(self, id: str, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Business Service Offerings API.

            documentation: https://docs.developer.yelp.com/reference/v3_business_service_offerings

            required parameters:
                * id - business ID or alias

            NOTE: requires special permissions on the Yelp Places API key.
        """
        if not id:
            raise ValueError('A valid business ID (parameter "id") must be provided.')

        return self._query(BUSINESS_SERVICE_OFFERINGS_API_URL.format(id), **kwargs)

    def categories_query(self, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Categories API.

            documentation: https://docs.developer.yelp.com/reference/v3_all_categories

            optional parameters:
                * locale - filter by locale and localize category names
        """
        return self._query(CATEGORIES_API_URL, **kwargs)

    def category_query(self, alias: str, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Category API.

            documentation: https://docs.developer.yelp.com/reference/v3_categories

            required parameters:
                * alias - category alias
        """
        if not alias:
            raise ValueError('A valid category alias (parameter "alias") must be provided.')

        return self._query(CATEGORY_API_URL.format(alias), **kwargs)

    def event_lookup_query(self, id: str, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Event Lookup API.

            documentation: https://docs.developer.yelp.com/reference/v3_event

            required parameters:
                * id - event ID
        """
        if not id:
            raise ValueError('A valid event ID (parameter "id") must be provided.')

        return self._query(EVENT_LOOKUP_API_URL.format(id), **kwargs)

    def event_search_query(self, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Event Search API.

            documentation: https://docs.developer.yelp.com/reference/v3_events_search
        """
        return self._query(EVENT_SEARCH_API_URL, **kwargs)

    def featured_event_query(self, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Featured Event API.

            documentation: https://docs.developer.yelp.com/reference/v3_featured_event

            required parameters:
                * one of either:
                    * location - text specifying a location to search for
                    * latitude and longitude
        """
        self._require_location_or_lat_lng(kwargs)

        return self._query(FEATURED_EVENT_API_URL, **kwargs)

    def phone_search_query(self, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Phone Search API.

            documentation: https://docs.developer.yelp.com/reference/v3_business_phone_search

            required parameters:
                * phone - phone number
        """
        if not kwargs.get('phone'):
            raise ValueError('A valid phone number (parameter "phone") must be provided.')

        return self._query(PHONE_SEARCH_API_URL, **kwargs)

    def reviews_query(self, id: str, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Reviews API.

            documentation: https://docs.developer.yelp.com/reference/v3_business_reviews

            required parameters:
                * id - business ID
        """
        if not id:
            raise ValueError('A valid business ID (parameter "id") must be provided.')

        return self._query(REVIEWS_API_URL.format(id), **kwargs)

    def review_highlights_query(self, id: str, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Review Highlights API.

            documentation: https://docs.developer.yelp.com/reference/v3_business_review_highlights

            required parameters:
                * id - business ID or alias

            NOTE: requires a Premium Plan.
        """
        if not id:
            raise ValueError('A valid business ID (parameter "id") must be provided.')

        return self._query(REVIEW_HIGHLIGHTS_API_URL.format(id), **kwargs)

    def search_query(self, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Search API.

            documentation: https://docs.developer.yelp.com/reference/v3_business_search

            required parameters:
                * one of either:
                    * location - text specifying a location to search for
                    * latitude and longitude
        """
        self._require_location_or_lat_lng(kwargs)

        return self._query(SEARCH_API_URL, **kwargs)

    def transaction_search_query(self, transaction_type: str, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Transaction Search API.

            documentation: https://docs.developer.yelp.com/reference/v3_transaction_search

            required parameters:
                * transaction_type - transaction type
                * one of either:
                    * location - text specifying a location to search for
                    * latitude and longitude
        """
        if not transaction_type:
            raise ValueError('A valid transaction type (parameter "transaction_type") must be provided.')

        self._require_location_or_lat_lng(kwargs)

        return self._query(TRANSACTION_SEARCH_API_URL.format(transaction_type), **kwargs)

    def _require_location_or_lat_lng(self, kwargs: dict[str, Any]) -> None:
        if not kwargs.get('location') and (not kwargs.get('latitude') or not kwargs.get('longitude')):
            raise ValueError('A valid location (parameter "location") or latitude/longitude combination '
                             '(parameters "latitude" and "longitude") must be provided.')

    def _query(self, url: str, **kwargs: Any) -> dict[str, Any]:
        """
            All query methods have the same logic, so don't repeat it! Query the URL, parse the response as JSON,
            and check for errors. If all goes well, return the parsed JSON.
        """
        parameters = {k: v for k, v in kwargs.items() if v is not None}
        response = self._yelp_session.get(
            url,
            headers=self._headers,
            params=parameters,
            timeout=self._timeout_s,
        )
        response.raise_for_status()

        response_json = response.json()

        # Yelp can return one of many different API errors, so check for one of them.
        # The Yelp Fusion API does not yet have a complete list of errors, but this is on the TODO list; see
        # https://github.com/Yelp/yelp-fusion/issues/95 for more info.
        if 'error' in response_json:
            raise YelpAPI.YelpAPIError(f'{response_json["error"]["code"]}: {response_json["error"]["description"]}')

        return response_json
