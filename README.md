# yelpapi

## AUTHOR
Geoffrey Fairchild
* [http://www.gfairchild.com/](http://www.gfairchild.com/)
* [https://github.com/gfairchild](https://github.com/gfairchild)
* [http://www.linkedin.com/in/gfairchild/](http://www.linkedin.com/in/gfairchild/)

## LICENSE
This software is licensed under the [BSD 3-Clause License](http://opensource.org/licenses/BSD-3-Clause). Please refer to the separate [LICENSE.txt](LICENSE.txt) file for the exact text of the license. You are obligated to give attribution if you use this code.

## ABOUT
yelpapi is a pure Python implementation of the [Yelp v2.0 API](http://www.yelp.com/developers/documentation/v2/overview). It is simple, fast, and robust to any changes Yelp may make to the API in the future.

## REQUIREMENTS
This code requires Python 2.7 or higher and [requests_oauthlib](https://github.com/requests/requests-oauthlib).

## INSTALL
yelpapi is available on PyPI at https://pypi.python.org/pypi/yelpapi.

Install using [pip](http://www.pip-installer.org/):

	pip install yelpapi

Install from source:

	python setup.py install

## USING THIS CODE
This API is demonstrated more thoroughly in [examples.py](examples/examples.py), but the basic idea is very simple:

```python
from yelpapi import YelpAPI
yelp_api = YelpAPI(consumer_key, consumer_secret, token, token_secret)
search_results = yelp_api.search_query(args)
business_results = yelp_api.business_query(id=business_id, other_args)
```

`args` and `other_args` are parameters that come directly from Yelp's [Search API documentation](http://www.yelp.com/developers/documentation/v2/search_api) and [Business API documentation](http://www.yelp.com/developers/documentation/v2/business). You only provide parameters you care about.

## DIFFERENCES
Yelp v2.0 Python implementations:

* [Official Yelp GitHub repo](https://github.com/Yelp/yelp-api/tree/master/v2/python)
* [python-yelp](https://github.com/adamhadani/python-yelp)
* [python-yelp-v2](https://github.com/mathisonian/python-yelp-v2)

yelpapi differs from other implementations in that it is completely dynamic with respect to both the input provided by the programmer and the output provided by Yelp. Most other implementations return the results as instances of pre-defined classes, while yelpapi returns a simply-defined, dynamically-generated `dict`. The benefit here is much smaller and simpler API implementation as well as preparedness for any changes Yelp may make to the API in the future.
