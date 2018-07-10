import logging

import pytest
from yelpapi import YelpAPI
from yelpapi.yelpapi import SEARCH_API_URL

log = logging.getLogger(__name__)


@pytest.fixture
def api_key(faker):
    return faker.pystr()


@pytest.fixture
def yelp(api_key):
    return YelpAPI(api_key)


@pytest.fixture
def random_dict(faker):
    """ A random dictionary that's JSON serializable """
    return faker.pydict(10, True, 'str', 'int', 'float', 'list', 'dict')


class TestYelpAPI:
    def test_calls_api(self, yelp, api_key, faker, mock_request, random_dict):
        url = faker.uri()
        mock_call = mock_request.get(url, json=random_dict)

        assert 0 == mock_call.call_count

        resp = yelp._query(url)

        assert resp == random_dict
        assert 1 == mock_call.call_count
        assert (
            'Bearer {}'.format(api_key)
            == mock_call.last_request.headers['Authorization']
        )

    def test_filters_none_params(self, yelp, faker, mock_request, random_dict):
        url = faker.uri()
        mock_call = mock_request.get(url, json={})
        none_subset = (
            list(random_dict.keys())[:faker.random_int(1, len(random_dict))]
        )
        for k in none_subset:
            random_dict[k] = None
        expect_params = {
            k: [str(v) if isinstance(v, (int, float)) else v]
            for k, v in random_dict.items()
            if v is not None
        }

        assert 0 == mock_call.call_count

        yelp._query(url, **random_dict)

        assert 1 == mock_call.call_count
        assert expect_params == mock_call.last_request.qs

    @pytest.mark.parametrize('has_timeout', [True, False])
    def test_uses_timeout(self, has_timeout, faker, mock_request, random_dict):
        url = faker.uri()
        mock_call = mock_request.get(url, json=random_dict)
        timeout_s = faker.random_int(1, 60) if has_timeout else None
        yelp = YelpAPI(faker.pystr(), timeout_s=timeout_s)

        assert 0 == mock_call.call_count

        resp = yelp._query(url)

        assert resp == random_dict
        assert 1 == mock_call.call_count
        assert timeout_s == mock_call.last_request.timeout

    def test_expects_json(self, yelp, faker, mock_request):
        url = faker.uri()
        mock_call = mock_request.get(url, content=bytes(faker.binary(length=256)))

        assert 0 == mock_call.call_count

        with pytest.raises(ValueError):
            yelp._query(url)

        assert 1 == mock_call.call_count

    def test_raises_error(self, yelp, faker, mock_request, random_dict):
        url = faker.uri()
        error_code = faker.random_int(1, 999)
        error_description = faker.paragraph()
        random_dict['error'] = {
            'code': error_code,
            'description': error_description,
        }
        mock_call = mock_request.get(url, json=random_dict)

        assert 0 == mock_call.call_count

        with pytest.raises(YelpAPI.YelpAPIError) as e:
            yelp._query(url, **random_dict)

        assert 1 == mock_call.call_count
        exc = e.value
        assert '{}: {}'.format(error_code, error_description) == exc.args[0]

    class TestSearchQuery:
        def test_location_and_term(self, mock_request, faker, yelp, random_dict):
            mock_call = mock_request.get(SEARCH_API_URL, json=random_dict)
            term = faker.word()
            location = '{}, {}'.format(faker.city(), faker.state_abbr())
            limit = faker.random_int(1, 10)
            expect_params = {
                'term': [term],
                'location': [location],
                'sort_by': ['rating'],
                'limit': [str(limit)],
            }

            assert 0 == mock_call.call_count

            resp = yelp.search_query(
                term=term,
                location=location,
                sort_by='rating',
                limit=limit,
            )

            assert random_dict == resp
            assert 1 == mock_call.call_count
            assert expect_params == mock_call.last_request.qs

        @pytest.mark.parametrize('has_location', [True, False])
        @pytest.mark.parametrize('has_lat_lng', [True, False])
        def test_requires_location_or_lat_lng(
            self,
            has_location,
            has_lat_lng,
            mock_request,
            faker,
            yelp,
        ):
            mock_call = mock_request.get(SEARCH_API_URL, json={})
            has_enough_params = has_location or has_lat_lng
            params = {}
            if has_location:
                params['location'] = faker.city()
            if has_lat_lng:
                params['latitude'] = faker.latitude()
                params['longitude'] = faker.longitude()

            assert 0 == mock_call.call_count

            if has_enough_params:
                yelp.search_query(**params)
                assert 1 == mock_call.call_count
            else:
                with pytest.raises(ValueError):
                    yelp.search_query(**params)
                assert 0 == mock_call.call_count
