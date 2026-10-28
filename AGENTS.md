# AGENTS.md

This file provides guidance to AI coding agents working with code in this repository.

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

Type-check (strict; configured in `[tool.mypy]` in `pyproject.toml`, which sets the files to check and targets the minimum supported Python):
```
mypy
```

CI (`.github/workflows/tests.yml`) runs `pytest` on every supported Python version and `mypy` once in a separate `typecheck` job. Both must pass.

## Architecture

This is a thin Python wrapper around Yelp's public REST APIs: the [Yelp Places API](https://docs.developer.yelp.com/docs/places-intro), the [Yelp AI API](https://docs.developer.yelp.com/docs/yelp-ai-api), [Yelp Insights](https://docs.developer.yelp.com/docs/yelp-insights), and the [Home Services API](https://docs.developer.yelp.com/docs/home-services-api). The entire implementation lives in `yelpapi/yelpapi.py` as a single `YelpAPI` class, re-exported from `yelpapi/__init__.py` via `__all__`.

**Design philosophy:** The wrapper is intentionally minimal and extensible — all API parameters are passed through `**kwargs` directly to the HTTP request, so it doesn't break when Yelp adds new parameters. The only thing that would break it is a URL scheme change. Public methods return `dict[str, Any]`; don't introduce `TypedDict`s or response models, since they would break this pass-through design.

**Request flow:** Each public method (e.g., `search_query`, `business_query`) validates required parameters, then delegates to `_get()` (GET; kwargs become query string parameters) or `_post()` (POST; kwargs become the JSON body). Both strip `None`-valued kwargs before issuing the request via a shared `requests.Session`, then hand the response to `_parse_response()`, which raises `requests.HTTPError` for HTTP error statuses, returns `{}` for empty `202`/`204` responses, and raises `YelpAPI.YelpAPIError` if the JSON body isn't an object or contains an `error` key. Methods that require a location share a `_require_location_or_lat_lng()` helper.

**Session management:** A single `requests.Session` is reused for all calls (performance benefit). Users should close it via context manager (`with YelpAPI(...) as api`) or explicitly via `api.close()`.

**Tests** use `requests-mock` (via the `mock_request` autouse fixture in `conftest.py`) to intercept HTTP calls, and a fixed-seed `Faker` for generating test data, so every run is deterministic. No real API calls are made in tests.

## Conventions

- **Typing:** The package ships `py.typed` and must pass strict `mypy`. All library code must be fully annotated. Tests and examples are type-checked but may omit annotations; see the `[[tool.mypy.overrides]]` section of `pyproject.toml`.
- **Coverage:** Line coverage of `yelpapi/` is 100%. Keep it there; new code paths need tests.
- **Style:** Use single quotes for strings, and 120-character lines.
- **Adding an endpoint** requires all of the following:
  - a `*_API_URL` constant
  - a method that validates required parameters and calls `_get()` (GET) or `_post()` (POST); path parameters are positional arguments inserted with `quote(value, safe='')`
  - an entry in the `GET_ENDPOINTS` or `POST_ENDPOINTS` table in `tests/test_yelpapi.py` (use `PATH_PARAM` for path parameters)
  - an entry in the `YelpAPI` class docstring's API list
  - an entry in the README "METHODS" list
  - tests covering both validation failures and success

## Supported Python versions

Support only Python versions that are currently maintained (not end-of-life); see https://devguide.python.org/versions/. The minimum is currently 3.11. When adding or dropping a version, update all of these together:

- `requires-python` and the `Programming Language :: Python :: 3.x` classifiers in `pyproject.toml`
- `python_version` in `[tool.mypy]` in `pyproject.toml` (keep it equal to the minimum)
- the `test` job's matrix in `.github/workflows/tests.yml`
- the Python version used by the `typecheck` job in `tests.yml` (keep it equal to the minimum, matching `python_version`)
- the Python version used by `publish.yml` (use the newest supported version)
- the "REQUIREMENTS" section of `README.md`
- `CHANGES.md`

Once the minimum is raised, newly available language and typing features (e.g., `typing.Self` with 3.11) may be used.

## Releasing

1. Bump `version` in `pyproject.toml`.
2. Add a `## X.Y.Z (YYYY-MM-DD)` entry at the top of `CHANGES.md`.
3. Commit, push, and make sure CI is green. The publish workflow does not run tests.
4. Push an annotated tag:

   ```
   git tag -a vX.Y.Z -m "vX.Y.Z" && git push origin vX.Y.Z
   ```

Pushing a `v*` tag triggers `.github/workflows/publish.yml`. Before publishing, it fails if the tag doesn't match the `pyproject.toml` version, or if `CHANGES.md` has no entry for that version. It then builds, publishes to PyPI, and creates a GitHub release whose notes are that version's `CHANGES.md` entry.
