# yelpapi

[![Build Status](https://travis-ci.org/gfairchild/yelpapi.svg?branch=master)](https://travis-ci.org/gfairchild/yelpapi)

## AUTHOR
Geoffrey Fairchild
* [https://www.gfairchild.com/](https://www.gfairchild.com/)
* [https://github.com/gfairchild](https://github.com/gfairchild)
* [https://www.linkedin.com/in/gfairchild/](https://www.linkedin.com/in/gfairchild/)

## LICENSE
This software is licensed under the [BSD 3-Clause License](http://opensource.org/licenses/BSD-3-Clause). Please refer to the separate [LICENSE.txt](LICENSE.txt) file for the exact text of the license. You are obligated to give attribution if you use this code.

## ABOUT
yelpapi is a pure Python implementation of the [Yelp Fusion API](https://www.yelp.com/developers/documentation/v3/get_started) (aka Yelp v3 API). It is simple, fast, and robust to any changes Yelp may make to the API in the future.

## REQUIREMENTS
This code requires Python 2.7 or higher and [requests](https://github.com/requests/requests).

## INSTALL
yelpapi is available on PyPI at https://pypi.python.org/pypi/yelpapi.

Install using [pip](http://www.pip-installer.org/):

    pip install yelpapi

Install from source:

    python setup.py install

## USING THIS CODE
This API is demonstrated more thoroughly in [examples.py](examples/examples.py), but the following chunk of code demonstrates basic use of yelpapi. 

```python
from yelpapi import YelpAPI
yelp_api = YelpAPI(api_key)
search_results = yelp_api.search_query(args)
```

You can also set timeouts so API calls do not block indefinitely in degraded network
conditions.

```python
from yelpapi import YelpAPI
yelp_api = YelpAPI(api_key, timeout_s=3.0)
search_results = yelp_api.search_query(args)
```

## METHODS
* [Autocomplete API](https://www.yelp.com/developers/documentation/v3/autocomplete) - `autocomplete_query(...)`
* [Business API](https://www.yelp.com/developers/documentation/v3/business) - `business_query(...)`
* [Business Match API](https://www.yelp.com/developers/documentation/v3/business_match) - `business_match_query(...)`
* [Event Lookup API](https://www.yelp.com/developers/documentation/v3/event) - `event_lookup_query(...)`
* [Event Search API](https://www.yelp.com/developers/documentation/v3/event_search) - `event_search_query(...)`
* [Featured Event API](https://www.yelp.com/developers/documentation/v3/featured_event) - `featured_event_query(...)`
* [Phone Search API](https://www.yelp.com/developers/documentation/v3/business_search_phone) - `phone_search_query(...)`
* [Reviews API](https://www.yelp.com/developers/documentation/v3/business_reviews) - `reviews_query(...)`
* [Search API](https://www.yelp.com/developers/documentation/v3/business_search) - `search_query(...)`
* [Transaction Search API](https://www.yelp.com/developers/documentation/v3/transactions_search) - `transaction_search_query(...)`
