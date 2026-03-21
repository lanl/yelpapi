# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Install dependencies:
```
pip install -e ".[dev]"
```

Run tests (coverage included by default via `pyproject.toml`):
```
pytest
```

Run a single test:
```
pytest tests/test_yelpapi.py::TestYelpAPI::test_calls_api
```

## Architecture

This is a thin Python wrapper around the [Yelp Fusion API](https://docs.developer.yelp.com/docs/fusion-intro). The entire implementation lives in `yelpapi/yelpapi.py` as a single `YelpAPI` class.

**Design philosophy:** The wrapper is intentionally minimal and extensible — all API parameters are passed through `**kwargs` directly to the HTTP request, so it doesn't break when Yelp adds new parameters. The only thing that would break it is a URL scheme change.

**Request flow:** Each public method (e.g., `search_query`, `business_query`) validates required parameters, then delegates to `_query()`, which strips `None`-valued kwargs before issuing the GET request via a shared `requests.Session`. Errors from Yelp's API (returned as JSON with an `error` key) are raised as `YelpAPI.YelpAPIError`. Methods that require a location share a `_require_location_or_lat_lng()` helper.

**Session management:** A single `requests.Session` is reused for all calls (performance benefit). Users should close it via context manager (`with YelpAPI(...) as api`) or explicitly via `api.close()`.

**Tests** use `requests-mock` (via the `mock_request` autouse fixture in `conftest.py`) to intercept HTTP calls, and `Faker` for generating random test data. No real API calls are made in tests.

## Releasing

Bump the version in `pyproject.toml`, update `CHANGES.md`, then push an annotated tag. The `publish.yml` GitHub Actions workflow will build, publish to PyPI, and create a GitHub release automatically. The annotated tag message is used as the release notes:

```
git tag -a vX.Y.Z -m "vX.Y.Z" && git push origin vX.Y.Z
```
