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

import warnings
from types import TracebackType
from typing import Any, Self
from urllib.parse import quote

import requests

AI_CHAT_API_URL = 'https://api.yelp.com/ai/chat/v2'
AUTOCOMPLETE_API_URL = 'https://api.yelp.com/v3/autocomplete'
BUSINESS_API_URL = 'https://api.yelp.com/v3/businesses/{}'
BUSINESS_ENGAGEMENT_API_URL = 'https://api.yelp.com/v3/businesses/engagement'
BUSINESS_FOOD_AND_DRINKS_INSIGHTS_API_URL = 'https://api.yelp.com/v3/businesses/{}/insights/food_and_drinks'
BUSINESS_INSIGHTS_API_URL = 'https://api.yelp.com/v3/businesses/insights'
BUSINESS_MATCH_API_URL = 'https://api.yelp.com/v3/businesses/matches'
BUSINESS_RAPC_ENABLEDNESS_API_URL = 'https://api.yelp.com/v3/businesses/{}/rapc_enabledness'
BUSINESS_RISK_SIGNALS_INSIGHTS_API_URL = 'https://api.yelp.com/v3/businesses/{}/insights/risk_signals'
BUSINESS_SERVICE_OFFERINGS_API_URL = 'https://api.yelp.com/v3/businesses/{}/service_offerings'
CATEGORIES_API_URL = 'https://api.yelp.com/v3/categories'
CATEGORY_API_URL = 'https://api.yelp.com/v3/categories/{}'
EVENT_LOOKUP_API_URL = 'https://api.yelp.com/v3/events/{}'
EVENT_SEARCH_API_URL = 'https://api.yelp.com/v3/events'
FEATURED_EVENT_API_URL = 'https://api.yelp.com/v3/events/featured'
JOB_SURVEY_API_URL = 'https://api.yelp.com/v3/jobs/{}/survey'
JOBS_API_URL = 'https://api.yelp.com/v3/jobs'
PHONE_SEARCH_API_URL = 'https://api.yelp.com/v3/businesses/search/phone'
PROJECTS_API_URL = 'https://api.yelp.com/v3/projects'
REVIEW_HIGHLIGHTS_API_URL = 'https://api.yelp.com/v3/businesses/{}/review_highlights'
REVIEWS_API_URL = 'https://api.yelp.com/v3/businesses/{}/reviews'
SEARCH_API_URL = 'https://api.yelp.com/v3/businesses/search'
TRANSACTION_SEARCH_API_URL = 'https://api.yelp.com/v3/transactions/{}/search'


class YelpAPI:
    """
        This class implements Yelp's public REST APIs (Places, AI, Insights, and Home Services). It offers access to the
        following APIs:

            * AI Chat API - https://docs.developer.yelp.com/reference/v2_ai_chat
            * Autocomplete API - https://docs.developer.yelp.com/reference/v3_autocomplete
            * Business API - https://docs.developer.yelp.com/reference/v3_business_info
            * Business Engagement Metrics API - https://docs.developer.yelp.com/reference/v3_get_businesses_engagement
            * Business Food & Drinks Insights API -
              https://docs.developer.yelp.com/reference/v3_get_business_food_and_drinks_insights
            * Business Insights API - https://docs.developer.yelp.com/reference/v3_businesses_insights
            * Business Match API - https://docs.developer.yelp.com/reference/v3_business_match
            * Business Request a Phone Call API - https://docs.developer.yelp.com/reference/v3_business_rapc_enabledness
            * Business Risk Signal Insights API -
              https://docs.developer.yelp.com/reference/v3_get_business_risk_signals_insights
            * Business Service Offerings API (deprecated) -
              https://docs.developer.yelp.com/reference/v3_business_service_offerings
            * Categories API - https://docs.developer.yelp.com/reference/v3_all_categories
            * Category API - https://docs.developer.yelp.com/reference/v3_categories
            * Event Lookup API - https://docs.developer.yelp.com/reference/v3_event
            * Event Search API - https://docs.developer.yelp.com/reference/v3_events_search
            * Featured Event API - https://docs.developer.yelp.com/reference/v3_featured_event
            * Job Survey API - https://docs.developer.yelp.com/reference/v3_job_survey
            * Jobs API - https://docs.developer.yelp.com/reference/v3_get_jobs
            * Phone Search API - https://docs.developer.yelp.com/reference/v3_business_phone_search
            * Request a Quote API - https://docs.developer.yelp.com/reference/v3_raq_submit_project
            * Review Highlights API - https://docs.developer.yelp.com/reference/v3_business_review_highlights
            * Reviews API - https://docs.developer.yelp.com/reference/v3_business_reviews
            * Search API - https://docs.developer.yelp.com/reference/v3_business_search
            * Transaction Search API - https://docs.developer.yelp.com/reference/v3_transaction_search

        It is simple and completely extensible since it dynamically takes arguments. This will allow it to continue
        working even if Yelp changes the spec. The only thing that should cause this to break is if Yelp changes the URL
        scheme.

        The structure of each method is quite simple. Some parameters help form the request URL (e.g., a ID of some
        sort), and other parameters are a part of the request itself (query string parameters for GET endpoints, or the
        JSON body for POST endpoints). Parameters that are a part of the URL are explicitly asked for as a part of the
        method definition. All other parameters are passed via `**kwargs`. Some parameters are required, and others are
        optional. To avoid unnecessarily using precious API calls, each method explicitly checks for parameters that are
        required in order for the query to succeed before issuing the call.

        This class will create and use a single `requests.Session` object for all API calls, which will provide a nice
        performance boost with many calls. To avoid keeping unnecessary connections open, you should be sure to close
        the Session once all Yelp API interactions are complete. This can be done manually by calling close() or by
        using it as a context manager.
    """

    class YelpAPIError(Exception):
        """
            Raised when a successful HTTP response contains a Yelp `error` object or a body that isn't a JSON object.
            HTTP error statuses (4xx/5xx) raise `requests.HTTPError` instead. The possible errors for each endpoint are
            listed in its documentation, which is linked from the corresponding method.
        """
        pass

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if '_query' in cls.__dict__:
            warnings.warn(
                f'{cls.__name__} overrides YelpAPI._query, which public methods no longer call; override _get (and '
                '_post for POST endpoints) instead. _query will be removed in 2.9.0.',
                FutureWarning,
                stacklevel=2,
            )

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

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def ai_chat_query(self, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp AI Chat API. This is a POST endpoint; parameters are sent as the JSON request body.

            documentation: https://docs.developer.yelp.com/reference/v2_ai_chat

            required parameters:
                * query - natural language query

            optional parameters:
                * chat_id - ID of a previous conversation to continue it (omit for a new conversation)
                * user_context - dict with the user's `latitude` and `longitude`, to tailor location-based answers
                * request_context - dict of processing settings (e.g., `skip_text_generation`)
        """
        if not kwargs.get('query'):
            raise ValueError('A valid query (parameter "query") must be provided.')

        return self._post(AI_CHAT_API_URL, **kwargs)

    def autocomplete_query(self, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Autocomplete API.

            documentation: https://docs.developer.yelp.com/reference/v3_autocomplete

            required parameters:
                * text - search text
        """
        if not kwargs.get('text'):
            raise ValueError('Valid text (parameter "text") must be provided.')

        return self._get(AUTOCOMPLETE_API_URL, **kwargs)

    def business_query(self, id: str, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Business API.

            documentation: https://docs.developer.yelp.com/reference/v3_business_info

            required parameters:
                * id - business ID or alias
        """
        if not id:
            raise ValueError('A valid business ID (parameter "id") must be provided.')

        return self._get(BUSINESS_API_URL.format(quote(id, safe='')), **kwargs)

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

            NOTE: the `match_type` parameter is no longer documented; use `match_threshold` (`none`, `default`, or
            `strict`) to control matching strictness. An empty `address1` is allowed for service businesses that have
            no street address.
        """
        if not kwargs.get('name'):
            raise ValueError('Valid business name (parameter "name") must be provided.')

        if not kwargs.get('city'):
            raise ValueError('Valid city (parameter "city") must be provided.')

        if not kwargs.get('state'):
            raise ValueError('Valid state (parameter "state") must be provided.')

        if not kwargs.get('country'):
            raise ValueError('Valid country (parameter "country") must be provided.')

        if kwargs.get('address1') is None:
            raise ValueError('Valid address (parameter "address1") must be provided.')

        return self._get(BUSINESS_MATCH_API_URL, **kwargs)

    def business_engagement_query(self, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Business Engagement Metrics API.

            documentation: https://docs.developer.yelp.com/reference/v3_get_businesses_engagement

            required parameters:
                * business_ids - comma-separated list of business IDs (maximum of 20)

            NOTE: part of Yelp Insights; requires Yelp Insights access for your API key.
        """
        if not kwargs.get('business_ids'):
            raise ValueError('Valid business IDs (parameter "business_ids") must be provided.')

        return self._get(BUSINESS_ENGAGEMENT_API_URL, **kwargs)

    def business_food_and_drinks_insights_query(self, id: str, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Business Food & Drinks Insights API.

            documentation: https://docs.developer.yelp.com/reference/v3_get_business_food_and_drinks_insights

            required parameters:
                * id - business ID or alias

            NOTE: part of Yelp Insights; requires Yelp Insights access for your API key.
        """
        if not id:
            raise ValueError('A valid business ID (parameter "id") must be provided.')

        return self._get(BUSINESS_FOOD_AND_DRINKS_INSIGHTS_API_URL.format(quote(id, safe='')), **kwargs)

    def business_insights_query(self, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Business Insights API.

            documentation: https://docs.developer.yelp.com/reference/v3_businesses_insights

            required parameters:
                * business_ids - comma-separated list of business IDs (maximum of 20)
                * date_range_start - start month (YYYYMM, e.g., 202601)
                * date_range_end - end month (YYYYMM, e.g., 202603)

            NOTE: part of Yelp Insights; requires Yelp Insights access for your API key.
        """
        if not kwargs.get('business_ids'):
            raise ValueError('Valid business IDs (parameter "business_ids") must be provided.')

        if not kwargs.get('date_range_start'):
            raise ValueError('A valid start month (parameter "date_range_start") must be provided.')

        if not kwargs.get('date_range_end'):
            raise ValueError('A valid end month (parameter "date_range_end") must be provided.')

        return self._get(BUSINESS_INSIGHTS_API_URL, **kwargs)

    def business_rapc_enabledness_query(self, id: str, **kwargs: Any) -> dict[str, Any]:
        """
            Enable or disable Request a Phone Call for a business. This is a POST endpoint; parameters are sent as the
            JSON request body. On success, Yelp returns no content, so an empty dict is returned.

            documentation: https://docs.developer.yelp.com/reference/v3_business_rapc_enabledness

            required parameters:
                * id - business ID or alias
                * is_enabled - whether Request a Phone Call should be enabled; pass a bool (`True` or `False`), not a
                  string, since the value is sent to Yelp as-is

            NOTE: requires an OAuth access token with the "leads" scope rather than a Yelp API key. Pass the
            access token as `api_key` when constructing `YelpAPI`.
        """
        if not id:
            raise ValueError('A valid business ID (parameter "id") must be provided.')

        if kwargs.get('is_enabled') is None:
            raise ValueError('A valid enabled flag (parameter "is_enabled") must be provided.')

        return self._post(BUSINESS_RAPC_ENABLEDNESS_API_URL.format(quote(id, safe='')), **kwargs)

    def business_risk_signals_insights_query(self, id: str, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Business Risk Signal Insights API.

            documentation: https://docs.developer.yelp.com/reference/v3_get_business_risk_signals_insights

            required parameters:
                * id - business ID or alias

            NOTE: part of Yelp Insights; requires Yelp Insights access for your API key.
        """
        if not id:
            raise ValueError('A valid business ID (parameter "id") must be provided.')

        return self._get(BUSINESS_RISK_SIGNALS_INSIGHTS_API_URL.format(quote(id, safe='')), **kwargs)

    def business_service_offerings_query(self, id: str, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Business Service Offerings API.

            documentation: https://docs.developer.yelp.com/reference/v3_business_service_offerings

            required parameters:
                * id - business ID or alias

            NOTE: requires special permissions on the Yelp API key.

            DEPRECATED: Yelp has deprecated this endpoint in favor of "Jobs offered", which can be enabled on the
            Business API (see `business_query`).
        """
        warnings.warn(
            'business_service_offerings_query is deprecated by Yelp; use "Jobs offered" via business_query instead.',
            DeprecationWarning,
            stacklevel=2,
        )

        if not id:
            raise ValueError('A valid business ID (parameter "id") must be provided.')

        return self._get(BUSINESS_SERVICE_OFFERINGS_API_URL.format(quote(id, safe='')), **kwargs)

    def categories_query(self, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Categories API.

            documentation: https://docs.developer.yelp.com/reference/v3_all_categories

            optional parameters:
                * locale - filter by locale and localize category names
        """
        return self._get(CATEGORIES_API_URL, **kwargs)

    def category_query(self, alias: str, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Category API.

            documentation: https://docs.developer.yelp.com/reference/v3_categories

            required parameters:
                * alias - category alias
        """
        if not alias:
            raise ValueError('A valid category alias (parameter "alias") must be provided.')

        return self._get(CATEGORY_API_URL.format(quote(alias, safe='')), **kwargs)

    def event_lookup_query(self, id: str, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Event Lookup API.

            documentation: https://docs.developer.yelp.com/reference/v3_event

            required parameters:
                * id - event ID
        """
        if not id:
            raise ValueError('A valid event ID (parameter "id") must be provided.')

        return self._get(EVENT_LOOKUP_API_URL.format(quote(id, safe='')), **kwargs)

    def event_search_query(self, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Event Search API.

            documentation: https://docs.developer.yelp.com/reference/v3_events_search
        """
        return self._get(EVENT_SEARCH_API_URL, **kwargs)

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

        return self._get(FEATURED_EVENT_API_URL, **kwargs)

    def job_survey_query(self, job_alias: str, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Job Survey API.

            documentation: https://docs.developer.yelp.com/reference/v3_job_survey

            required parameters:
                * job_alias - job alias (e.g., `job_faucet_repair`, from `jobs_query`)

            NOTE: part of the Home Services API; access is disabled by default and must be requested from Yelp.
        """
        if not job_alias:
            raise ValueError('A valid job alias (parameter "job_alias") must be provided.')

        return self._get(JOB_SURVEY_API_URL.format(quote(job_alias, safe='')), **kwargs)

    def jobs_query(self, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Jobs API. This is a POST endpoint; parameters are sent as the JSON request body.

            documentation: https://docs.developer.yelp.com/reference/v3_get_jobs

            required parameters:
                * query - description of the home service the user needs

            optional parameters:
                * locale - locale of the query and response (e.g., en_US)

            NOTE: part of the Home Services API; access is disabled by default and must be requested from Yelp.
        """
        if not kwargs.get('query'):
            raise ValueError('A valid query (parameter "query") must be provided.')

        return self._post(JOBS_API_URL, **kwargs)

    def phone_search_query(self, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Phone Search API.

            documentation: https://docs.developer.yelp.com/reference/v3_business_phone_search

            required parameters:
                * phone - phone number
        """
        if not kwargs.get('phone'):
            raise ValueError('A valid phone number (parameter "phone") must be provided.')

        return self._get(PHONE_SEARCH_API_URL, **kwargs)

    def request_a_quote_query(self, **kwargs: Any) -> dict[str, Any]:
        """
            Submit a Yelp Request a Quote project. This is a POST endpoint; parameters are sent as the JSON request
            body.

            documentation: https://docs.developer.yelp.com/reference/v3_raq_submit_project

            required parameters:
                * job_alias - job alias (e.g., from `jobs_query`)
                * survey_responses - list of survey responses (see `job_survey_query`); each is a dict with
                  `question_alias` and `user_response` (a list of strings)
                * submit_to_nearby_businesses - whether to submit to nearby businesses (bool)
                * customer_info - customer information (dict); requires `first_name`, `email`, and `zip_code`, while
                  `last_name` and `phone` are optional

            optional parameters:
                * business_id - Yelp business ID to send the quote request to; if omitted, Yelp treats
                  `submit_to_nearby_businesses` as true

            NOTE: part of the Home Services API; access is disabled by default and must be requested from Yelp.
        """
        if not kwargs.get('job_alias'):
            raise ValueError('A valid job alias (parameter "job_alias") must be provided.')

        if kwargs.get('survey_responses') is None:
            raise ValueError('Valid survey responses (parameter "survey_responses") must be provided.')

        if kwargs.get('submit_to_nearby_businesses') is None:
            raise ValueError('A valid flag (parameter "submit_to_nearby_businesses") must be provided.')

        if not kwargs.get('customer_info'):
            raise ValueError('Valid customer info (parameter "customer_info") must be provided.')

        return self._post(PROJECTS_API_URL, **kwargs)

    def reviews_query(self, id: str, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Reviews API.

            documentation: https://docs.developer.yelp.com/reference/v3_business_reviews

            required parameters:
                * id - business ID or alias

            NOTE: requires an Enhanced or Premium Plan.
        """
        if not id:
            raise ValueError('A valid business ID (parameter "id") must be provided.')

        return self._get(REVIEWS_API_URL.format(quote(id, safe='')), **kwargs)

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

        return self._get(REVIEW_HIGHLIGHTS_API_URL.format(quote(id, safe='')), **kwargs)

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

        return self._get(SEARCH_API_URL, **kwargs)

    def transaction_search_query(self, transaction_type: str, **kwargs: Any) -> dict[str, Any]:
        """
            Query the Yelp Transaction Search API.

            documentation: https://docs.developer.yelp.com/reference/v3_transaction_search

            required parameters:
                * transaction_type - transaction type; currently only `'delivery'` is supported (US only)
                * one of either:
                    * location - text specifying a location to search for
                    * latitude and longitude
        """
        if not transaction_type:
            raise ValueError('A valid transaction type (parameter "transaction_type") must be provided.')

        self._require_location_or_lat_lng(kwargs)

        return self._get(TRANSACTION_SEARCH_API_URL.format(quote(transaction_type, safe='')), **kwargs)

    def _require_location_or_lat_lng(self, kwargs: dict[str, Any]) -> None:
        if not kwargs.get('location') and (kwargs.get('latitude') is None or kwargs.get('longitude') is None):
            raise ValueError('A valid location (parameter "location") or latitude/longitude combination '
                             '(parameters "latitude" and "longitude") must be provided.')

    def _get(self, url: str, **kwargs: Any) -> dict[str, Any]:
        """
            All GET query methods have the same logic, so don't repeat it! Query the URL with kwargs as query string
            parameters, parse the response as JSON, and check for errors. If all goes well, return the parsed JSON.
        """
        parameters = {k: v for k, v in kwargs.items() if v is not None}
        response = self._yelp_session.get(
            url,
            headers=self._headers,
            params=parameters,
            timeout=self._timeout_s,
        )
        return self._parse_response(response)

    def _post(self, url: str, **kwargs: Any) -> dict[str, Any]:
        """
            Like `_get`, but issues a POST request with kwargs sent as the JSON request body.
        """
        body = {k: v for k, v in kwargs.items() if v is not None}
        response = self._yelp_session.post(
            url,
            headers=self._headers,
            json=body,
            timeout=self._timeout_s,
        )
        return self._parse_response(response)

    def _query(self, url: str, **kwargs: Any) -> dict[str, Any]:
        """
            DEPRECATED: renamed to `_get`. This alias will be removed in 2.9.0. Note that public methods no longer call
            `_query`, so subclasses that override it should override `_get` (and `_post`) instead.
        """
        warnings.warn('YelpAPI._query is deprecated; use YelpAPI._get instead.', FutureWarning, stacklevel=2)

        return self._get(url, **kwargs)

    def _parse_response(self, response: requests.Response) -> dict[str, Any]:
        response.raise_for_status()

        # Some endpoints (e.g., Request a Phone Call) acknowledge success with no body.
        if response.status_code in (202, 204) and not response.content:
            return {}

        response_json = response.json()

        # Every Yelp endpoint returns a JSON object. Anything else (e.g., a bare string or list) is unexpected
        # and must be rejected before the error check below, which assumes a dict.
        if not isinstance(response_json, dict):
            raise YelpAPI.YelpAPIError(f'Unexpected response type: {type(response_json).__name__}')

        # Yelp reports errors as {"error": {"code": ..., "description": ...}}. Malformed error values are still raised.
        if 'error' in response_json:
            error = response_json['error']
            if isinstance(error, dict):
                raise YelpAPI.YelpAPIError(f'{error.get("code")}: {error.get("description")}')
            raise YelpAPI.YelpAPIError(str(error))

        return response_json
