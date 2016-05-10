# Changes

## 1.4 (2016-05-10)
* Use HTTPS for all API calls.
* Use new string formatter.
* Remove `YelpError` since the business API now returns a JSON error when given a bad business ID.

## 1.3 (2015-05-22)
* Adding support for the [Phone Search API](https://www.yelp.com/developers/documentation/v2/phone_search).

## 1.2 (2013-10-08)
* yelpapi is now fully Python 3+ compliant.

## 1.1 (2013-10-04)
* Transitioning from using [python-oauth2](https://github.com/simplegeo/python-oauth2) and [requests](https://github.com/kennethreitz/requests) to just using [requests-oauthlib](https://github.com/requests/requests-oauthlib).
* Moving to setuptools (using [ez_setup.py](https://bitbucket.org/pypa/setuptools/downloads/ez_setup.py) to manage it).

## 1.0 (2013-10-03)
* Initial release.
