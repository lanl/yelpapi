# Changes

## 2.8.0 (2026-10-28)
* **Heads up for subclassers:** the private request helper `YelpAPI._query()` has been renamed to `YelpAPI._get()`, and the new POST helper is `YelpAPI._post()`.
    * If your subclass *calls* `self._query(...)` to reach endpoints this library doesn't wrap, switch to `self._get(...)`. `_query()` still works for this release but emits a `FutureWarning`.
    * If your subclass *overrides* `_query()` (e.g., for caching, retries, or logging), override `_get()` (and `_post()` for POST endpoints) instead. Public methods no longer call `_query()`, so an override of it is no longer used. Defining such a subclass emits a `FutureWarning`.
    * `_query()` will be removed in 2.9.0.
* Added 8 new API endpoints: AI Chat (`ai_chat_query`), Business Insights (`business_insights_query`), Business Food & Drinks Insights (`business_food_and_drinks_insights_query`), Business Risk Signal Insights (`business_risk_signals_insights_query`), Business Request a Phone Call (`business_rapc_enabledness_query`), Jobs (`jobs_query`), Job Survey (`job_survey_query`), and Request a Quote (`request_a_quote_query`).
* Added support for POST endpoints, which send `**kwargs` as the JSON request body (with `None` values removed). Successful responses with no body (e.g., `202 Accepted`) return an empty dict.
* `business_service_offerings_query` now emits a `DeprecationWarning`, because Yelp has deprecated the endpoint in favor of "Jobs offered" on the Business API.
* Fixed: a latitude or longitude of `0` (the equator or prime meridian) is now accepted by `search_query`, `featured_event_query`, and `transaction_search_query` instead of raising `ValueError`.
* Fixed: `business_match_query` now accepts an empty `address1`, which Yelp allows for service businesses with no street address.
* Fixed: a malformed `error` object in a response (e.g., a plain string, or one missing `code` or `description`) now raises `YelpAPI.YelpAPIError` instead of a `TypeError` or `KeyError`.
* Path parameters (business IDs, aliases, event IDs, job aliases, and transaction types) are now percent-encoded, so characters like `/`, `?`, and `#` can no longer change the URL that is requested.
* Clarified the `YelpAPI.YelpAPIError` docs: HTTP error statuses raise `requests.HTTPError`, while `YelpAPIError` covers error objects and non-object bodies in successful responses.
* Updated docstrings to match Yelp's current docs (plan and access requirements, `match_threshold`, the 20-ID limit for `business_ids`, and required fields for Request a Quote).
* Fixed the examples so they catch `requests.HTTPError` and keep going when an endpoint needs a paid plan or extra access.
* Strengthened the test suite: every endpoint's URL, HTTP method, and parameters are now checked, and test data is deterministic.

## 2.7.0 (2026-10-28)
* Dropped support for end-of-life Python 3.9 and 3.10; added Python 3.15. Minimum supported version is now 3.11.
* `YelpAPI.__enter__` now returns `Self`, so subclasses are typed correctly when used as context managers.
* Declared `__all__` in the `yelpapi` package so `from yelpapi import YelpAPI` passes `mypy --strict` (no implicit re-export) and Pyright's private-import checks.
* Added the `Typing :: Typed` classifier.
* A JSON response body that isn't an object (e.g., a string or list) now raises `YelpAPI.YelpAPIError` instead of an unhelpful `TypeError` or silently returning the wrong type.

## 2.6.0 (2026-03-17)
* Added 5 new API endpoints: Business Engagement Metrics (`business_engagement_query`), Business Service Offerings (`business_service_offerings_query`), Categories (`categories_query`), Category by Alias (`category_query`), and Review Highlights (`review_highlights_query`).
* Updated all documentation URLs to the current `docs.developer.yelp.com` reference format.
* Migrated from `setup.py` to `pyproject.toml` (hatchling build backend).
* Dropped Python 3.8 support; added Python 3.13 and 3.14. Minimum supported version is now 3.9.
* Migrated CI from Travis CI to GitHub Actions.
* Added type hints throughout.
* Reached 100% test coverage.

## 2.5.1 (2023-10-10)
* Raise [`HTTPError`](https://requests.readthedocs.io/en/latest/api/#requests.HTTPError) if one occurs (PR #25).

## 2.5.0 (2022-08-04)
* Implemented new `close()` method to close the `requests.Session` object we use for performant API interactions. This can also be used as a context manager (this is the preferred way).
    * Clarified [`README.md`](README.md) to make it clear that the user should always be sure to close the connection.

## 2.4.1 (2022-08-01)
* Dropping EOL Python versions, adding newly-supported versions.
* Updating dependencies in [`requirements.txt`](requirements.txt).
* Updating project URL (moved from [@gfairchild](https://github.com/gfairchild)'s personal namespace to [@lanl](https://github.com/lanl)'s namespace).

## 2.4.0 (2019-04-19)
* `match_type` parameter for the business match endpoint was deprecated on April 1, 2019 (see [Yelp's changelog](https://www.yelp.com/developers/v3/changelog)). (courtesy @davebulaval)
* Added a check to ensure a required parameter, `address1`, is provided when using the business match endpoint. (courtesy @davebulaval)
* Support for Python versions <3.4 is removed (i.e., this no longer works with Python 2.7). This is due to some dependencies that also have abandoned Python 2 support.

## 2.3.0 (2018-07-11)
* Provided a means to set timeouts to API calls. (courtesy @goodspark)
* Added unit tests, including Travis CI automation. (courtesy @goodspark)

## 2.2.2 (2018-01-28)
* Add better top-level documentation for `YelpAPI`.
* To avoid wasting API calls on obviously invalid requests, consistently check for parameters required for requests to succeed.

## 2.2.1 (2018-01-28)
* Fix a few minor inconsistencies in the code.

## 2.2.0 (2018-01-28)
* Revised to remove token/secret access and instead use API keys. Yelp will move to API keys only in March 2018. (courtesy @tamos)
* An API key is now needed to instantiate a `YelpAPI` object. (courtesy @tamos)
* Added support for 3 new endpoints:
    * [Event Lookup API](https://www.yelp.com/developers/documentation/v3/event)
    * [Event Search API](https://www.yelp.com/developers/documentation/v3/event_search)
    * [Featured Event API](https://www.yelp.com/developers/documentation/v3/featured_event)
* `business_match_query` no longer assumes the country is the U.S. if the country code is missing.

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
