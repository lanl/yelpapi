# yelpapi

## AUTHOR
Geoffrey Fairchild
* [http://www.gfairchild.com/](http://www.gfairchild.com/)
* [https://github.com/gfairchild](https://github.com/gfairchild)
* [http://www.linkedin.com/in/gfairchild/](http://www.linkedin.com/in/gfairchild/)

## LICENSE
This software is licensed under the [BSD 3-Clause License](http://opensource.org/licenses/BSD-3-Clause). Please refer to the separate [LICENSE.txt](LICENSE.txt) file for the exact text of the license. You are obligated to give attribution if you use this code.

## ABOUT
yelpapi is a pure Python implementation of the [Yelp Fusion API](https://www.yelp.com/developers/documentation/v3/get_started) (aka Yelp v3 API). It is simple, fast, and robust to any changes Yelp may make to the API in the future.

**Note:** yelpapi v1.4 was the last version to support the Yelp v2 API, which is [slowly being deprecated](https://engineeringblog.yelp.com/2017/02/recent-improvements-to-the-fusion-api.html). All developers should migrate to the new Yelp Fusion API as soon as possible.

## REQUIREMENTS
This code requires Python 2.7 or higher and [requests_oauthlib](https://github.com/requests/requests-oauthlib).

## INSTALL
yelpapi is available on PyPI at https://pypi.python.org/pypi/yelpapi.

Install using [pip](http://www.pip-installer.org/):

    pip install yelpapi

Install from source:

    python setup.py install

## USING THIS CODE
This API is demonstrated more thoroughly in [examples.py](examples/examples.py), but the following chunk of code demonstrates use of yelpapi. 

```python
from yelpapi import YelpAPI
yelp_api = YelpAPI(client_id, client_secret)
search_results = yelp_api.search_query(args)
business_results = yelp_api.business_query(id=business_id, other_args)
phone_search_results = yelp_api.phone_search_query(phone=phone_number, other_args)
```

### METHODS
* [Search API](https://www.yelp.com/developers/documentation/v3/business_search): `search_query(args)`
* [Phone Search API](https://www.yelp.com/developers/documentation/v3/business_search_phone): `phone_search_query(phone=[PHONE], other_args)`
* [Transaction Search API](https://www.yelp.com/developers/documentation/v3/transactions_search): `transaction_search_query(transaction_type=[TRANSACTION_TYPE], other_args)`
* [Business API](https://www.yelp.com/developers/documentation/v3/business): `business_query(id=[BUSINESS_ID], other_args)`
* [Reviews API](https://www.yelp.com/developers/documentation/v3/business_reviews): `reviews_query(id=[BUSINESS_ID], other_args)`
* [Autocomplete API](https://www.yelp.com/developers/documentation/v3/autocomplete): `autocomplete_query(text=[SEARCH_TEXT], other_args)`
