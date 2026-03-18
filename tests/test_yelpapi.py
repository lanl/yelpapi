import pytest
import requests
from unittest.mock import patch

from yelpapi import YelpAPI
from yelpapi.yelpapi import (
    AUTOCOMPLETE_API_URL,
    BUSINESS_API_URL,
    BUSINESS_MATCH_API_URL,
    EVENT_LOOKUP_API_URL,
    EVENT_SEARCH_API_URL,
    FEATURED_EVENT_API_URL,
    PHONE_SEARCH_API_URL,
    REVIEWS_API_URL,
    SEARCH_API_URL,
    TRANSACTION_SEARCH_API_URL,
)


@pytest.fixture
def api_key(faker):
    return faker.pystr()


@pytest.fixture
def yelp(api_key):
    return YelpAPI(api_key)


@pytest.fixture
def random_dict(faker):
    """A random dictionary that's JSON serializable."""
    return faker.pydict(10, True, value_types=['str', 'int', 'float', 'list', 'dict'])


class TestYelpAPI:
    def test_calls_api(self, yelp, api_key, faker, mock_request, random_dict):
        url = faker.uri()
        mock_call = mock_request.get(url, json=random_dict)

        resp = yelp._query(url)

        assert resp == random_dict
        assert mock_call.last_request.headers['Authorization'] == 'Bearer {}'.format(api_key)

    def test_filters_none_params(self, yelp, faker, mock_request, random_dict):
        url = faker.uri()
        mock_call = mock_request.get(url, json={})
        none_subset = list(random_dict.keys())[:faker.random_int(1, len(random_dict))]
        for k in none_subset:
            random_dict[k] = None
        expect_params = {
            k: [str(v) if isinstance(v, (int, float)) else v]
            for k, v in random_dict.items()
            if v is not None
        }

        yelp._query(url, **random_dict)

        assert mock_call.last_request.qs == expect_params

    @pytest.mark.parametrize('has_timeout', [True, False])
    def test_uses_timeout(self, has_timeout, faker, mock_request, random_dict):
        url = faker.uri()
        mock_call = mock_request.get(url, json=random_dict)
        timeout_s = faker.random_int(1, 60) if has_timeout else None
        yelp = YelpAPI(faker.pystr(), timeout_s=timeout_s)

        resp = yelp._query(url)

        assert resp == random_dict
        assert mock_call.last_request.timeout == timeout_s

    def test_expects_json(self, yelp, faker, mock_request):
        url = faker.uri()
        mock_request.get(url, content=bytes(faker.binary(length=256)))

        with pytest.raises(ValueError):
            yelp._query(url)

    def test_raises_yelp_api_error(self, yelp, faker, mock_request, random_dict):
        url = faker.uri()
        error_code = faker.random_int(1, 999)
        error_description = faker.paragraph()
        random_dict['error'] = {'code': error_code, 'description': error_description}
        mock_request.get(url, json=random_dict)

        with pytest.raises(YelpAPI.YelpAPIError) as exc_info:
            yelp._query(url)

        assert exc_info.value.args[0] == '{}: {}'.format(error_code, error_description)

    @pytest.mark.parametrize('status_code', [400, 401, 403, 404, 500])
    def test_raises_http_error(self, yelp, faker, mock_request, status_code):
        url = faker.uri()
        mock_request.get(url, status_code=status_code)

        with pytest.raises(requests.exceptions.HTTPError):
            yelp._query(url)

    def test_context_manager(self, api_key):
        with patch.object(YelpAPI, 'close') as mock_close:
            with YelpAPI(api_key) as api:
                assert isinstance(api, YelpAPI)
        mock_close.assert_called_once()


class TestAutocompleteQuery:
    def test_requires_text(self, yelp):
        with pytest.raises(ValueError):
            yelp.autocomplete_query()

    def test_success(self, yelp, faker, mock_request, random_dict):
        mock_request.get(AUTOCOMPLETE_API_URL, json=random_dict)

        assert yelp.autocomplete_query(text=faker.word()) == random_dict


class TestBusinessQuery:
    @pytest.mark.parametrize('invalid_id', [None, ''])
    def test_requires_id(self, yelp, invalid_id):
        with pytest.raises(ValueError):
            yelp.business_query(invalid_id)

    def test_success(self, yelp, faker, mock_request, random_dict):
        business_id = faker.pystr()
        mock_request.get(BUSINESS_API_URL.format(business_id), json=random_dict)

        assert yelp.business_query(business_id) == random_dict


class TestBusinessMatchQuery:
    @pytest.mark.parametrize('missing_param', ['name', 'city', 'state', 'country', 'address1'])
    def test_requires_all_params(self, yelp, faker, missing_param):
        params = {
            'name': faker.company(),
            'city': faker.city(),
            'state': faker.state_abbr(),
            'country': faker.country_code(),
            'address1': faker.street_address(),
        }
        del params[missing_param]

        with pytest.raises(ValueError):
            yelp.business_match_query(**params)

    def test_success(self, yelp, faker, mock_request, random_dict):
        mock_request.get(BUSINESS_MATCH_API_URL, json=random_dict)

        assert yelp.business_match_query(
            name=faker.company(),
            city=faker.city(),
            state=faker.state_abbr(),
            country=faker.country_code(),
            address1=faker.street_address(),
        ) == random_dict


class TestEventLookupQuery:
    @pytest.mark.parametrize('invalid_id', [None, ''])
    def test_requires_id(self, yelp, invalid_id):
        with pytest.raises(ValueError):
            yelp.event_lookup_query(invalid_id)

    def test_success(self, yelp, faker, mock_request, random_dict):
        event_id = faker.pystr()
        mock_request.get(EVENT_LOOKUP_API_URL.format(event_id), json=random_dict)

        assert yelp.event_lookup_query(event_id) == random_dict


class TestEventSearchQuery:
    def test_success(self, yelp, mock_request, random_dict):
        mock_request.get(EVENT_SEARCH_API_URL, json=random_dict)

        assert yelp.event_search_query() == random_dict


class TestFeaturedEventQuery:
    def test_requires_location_or_lat_lng(self, yelp):
        with pytest.raises(ValueError):
            yelp.featured_event_query()

    def test_success(self, yelp, faker, mock_request, random_dict):
        mock_request.get(FEATURED_EVENT_API_URL, json=random_dict)

        assert yelp.featured_event_query(location=faker.city()) == random_dict


class TestPhoneSearchQuery:
    def test_requires_phone(self, yelp):
        with pytest.raises(ValueError):
            yelp.phone_search_query()

    def test_success(self, yelp, faker, mock_request, random_dict):
        mock_request.get(PHONE_SEARCH_API_URL, json=random_dict)

        assert yelp.phone_search_query(phone=faker.phone_number()) == random_dict


class TestReviewsQuery:
    @pytest.mark.parametrize('invalid_id', [None, ''])
    def test_requires_id(self, yelp, invalid_id):
        with pytest.raises(ValueError):
            yelp.reviews_query(invalid_id)

    def test_success(self, yelp, faker, mock_request, random_dict):
        business_id = faker.pystr()
        mock_request.get(REVIEWS_API_URL.format(business_id), json=random_dict)

        assert yelp.reviews_query(business_id) == random_dict


class TestSearchQuery:
    def test_requires_location_or_lat_lng(self, yelp):
        with pytest.raises(ValueError):
            yelp.search_query()

    def test_success(self, yelp, faker, mock_request, random_dict):
        mock_call = mock_request.get(SEARCH_API_URL, json=random_dict)
        term = faker.word()
        location = '{}, {}'.format(faker.city(), faker.state_abbr())
        limit = faker.random_int(1, 10)

        resp = yelp.search_query(term=term, location=location, sort_by='rating', limit=limit)

        assert resp == random_dict
        assert mock_call.last_request.qs == {
            'term': [term],
            'location': [location],
            'sort_by': ['rating'],
            'limit': [str(limit)],
        }


class TestTransactionSearchQuery:
    @pytest.mark.parametrize('invalid_type', [None, ''])
    def test_requires_transaction_type(self, yelp, faker, invalid_type):
        with pytest.raises(ValueError):
            yelp.transaction_search_query(invalid_type, location=faker.city())

    def test_requires_location_or_lat_lng(self, yelp, faker):
        with pytest.raises(ValueError):
            yelp.transaction_search_query(faker.word())

    def test_success(self, yelp, faker, mock_request, random_dict):
        transaction_type = faker.word()
        mock_request.get(TRANSACTION_SEARCH_API_URL.format(transaction_type), json=random_dict)

        assert yelp.transaction_search_query(transaction_type, location=faker.city()) == random_dict
