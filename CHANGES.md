# Changes

## 2.2.0 (2018-01-28)
* Revised to remove token/secret access and instead use API keys. Yelp will move to API keys only in March 2018.
* An API key (string) is now needed to instantiate a YelpAPI object. 

## 2.1.0 (2017-10-19)
* Implement new [Business Match API](https://www.yelp.com/developers/documentation/v3/business_match).   
**NOTE**: This API is currently in beta. Yelp requires your app join the [Yelp Developer Beta Program](https://www.yelp.com/developers/v3/manage_app) to gain access to it.

## 2.0.1 (2017-02-27)
* Remove reliance on `ez_setup.py`.
* Add `setup.cfg` to instruct the build process to build universal wheels.

## 2.0 (2017-02-27)
* Implement the new Yelp Fusion API (aka Yelp v3 API). Note that yelpapi v1.4 is the last version to support the Yelp v2 API. [The Yelp v2 API is being deprecated, so all new developers should move to the new Fusion API ASAP.](https://engineeringblog.yelp.com/2017/02/recent-improvements-to-the-fusion-api.html)
  * Use OAuth 2.0 for authentication.
  * Implement new [Transaction Search API](https://www.yelp.com/developers/documentation/v3/transactions_search), [Reviews API](https://www.yelp.com/developers/documentation/v3/business_reviews), and [Autocomplete API](https://www.yelp.com/developers/documentation/v3/autocomplete).

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
