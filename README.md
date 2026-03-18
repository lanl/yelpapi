# yelpapi

[![Tests](https://github.com/lanl/yelpapi/actions/workflows/tests.yml/badge.svg)](https://github.com/lanl/yelpapi/actions/workflows/tests.yml)

## LICENSE
This software is licensed under the [BSD 3-Clause License](http://opensource.org/licenses/BSD-3-Clause). Please refer to the separate [LICENSE](LICENSE) file for the exact text of the license. You are obligated to give attribution if you use this code.

## ABOUT
yelpapi is a pure Python implementation of the [Yelp Fusion API](https://docs.developer.yelp.com/docs/fusion-intro). It is simple, fast, and robust to any changes Yelp may make to the API in the future.

## REQUIREMENTS
This code requires Python 3.9 or higher and [requests](https://github.com/requests/requests).

## INSTALL
yelpapi is available on PyPI at https://pypi.org/project/yelpapi/.

Install using [pip](http://www.pip-installer.org/):

    pip install yelpapi

## USING THIS CODE
This API is demonstrated more thoroughly in [examples.py](examples/examples.py), but the following chunk of code demonstrates basic use of yelpapi:

```python
from yelpapi import YelpAPI
with YelpAPI(api_key) as yelp_api:
    search_results = yelp_api.search_query(args)
```

You can also set timeouts so API calls do not block indefinitely in degraded network conditions:

```python
from yelpapi import YelpAPI
with YelpAPI(api_key, timeout_s=3.0) as yelp_api:
    search_results = yelp_api.search_query(args)
```

Under the covers, this module uses a [`requests.Session`](https://requests.readthedocs.io/en/latest/user/advanced/#session-objects) object for issuing all API calls, which offers potentially significant performance benefits over issuing separate API calls outside of a session. You should be sure to close the underlying session when all API interactions are complete. The above examples demonstrate using the class as a context manager, which will automatically close the connection when you're done and is the preferred way of using the class, but you can also manually close it like this if a context manager won't work for your use case:

```python
from yelpapi import YelpAPI
try:
    yelp_api = YelpAPI(api_key)
    search_results = yelp_api.search_query(args)
finally:
    yelp_api.close()
```

## METHODS
* [Autocomplete API](https://docs.developer.yelp.com/reference/v3_autocomplete) - `autocomplete_query(...)`
* [Business API](https://docs.developer.yelp.com/reference/v3_business_info) - `business_query(...)`
* [Business Engagement Metrics API](https://docs.developer.yelp.com/reference/v3_get_businesses_engagement) - `business_engagement_query(...)`
* [Business Match API](https://docs.developer.yelp.com/reference/v3_business_match) - `business_match_query(...)`
* [Business Service Offerings API](https://docs.developer.yelp.com/reference/v3_business_service_offerings) - `business_service_offerings_query(...)`
* [Categories API](https://docs.developer.yelp.com/reference/v3_all_categories) - `categories_query(...)`
* [Category API](https://docs.developer.yelp.com/reference/v3_categories) - `category_query(...)`
* [Event Lookup API](https://docs.developer.yelp.com/reference/v3_event) - `event_lookup_query(...)`
* [Event Search API](https://docs.developer.yelp.com/reference/v3_events_search) - `event_search_query(...)`
* [Featured Event API](https://docs.developer.yelp.com/reference/v3_featured_event) - `featured_event_query(...)`
* [Phone Search API](https://docs.developer.yelp.com/reference/v3_business_phone_search) - `phone_search_query(...)`
* [Review Highlights API](https://docs.developer.yelp.com/reference/v3_business_review_highlights) - `review_highlights_query(...)`
* [Reviews API](https://docs.developer.yelp.com/reference/v3_business_reviews) - `reviews_query(...)`
* [Search API](https://docs.developer.yelp.com/reference/v3_business_search) - `search_query(...)`
* [Transaction Search API](https://docs.developer.yelp.com/reference/v3_transaction_search) - `transaction_search_query(...)`
