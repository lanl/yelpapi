import warnings
from typing import Any

import pytest
import requests
import requests_mock
from unittest.mock import patch

from yelpapi import YelpAPI

URL = 'https://api.yelp.com/v3/test'

# A path parameter containing characters that must be percent-encoded so it can't change the path, add a query string,
# or add a fragment; non-ASCII (e.g., "café-de-flore-paris") is valid in Yelp aliases.
PATH_PARAM = 'a/b?c=1#é%'
ENCODED = 'a%2Fb%3Fc%3D1%23%C3%A9%25'

# Every public query method, called with minimal valid arguments: (method name, positional args, required kwargs,
# expected URL). URLs are spelled out rather than built from the *_API_URL constants so that a typo in a constant is
# caught.
Endpoint = tuple[str, list[str], dict[str, Any], str]
GET_ENDPOINTS: list[Endpoint] = [
    ('autocomplete_query', [], {'text': 'pizz'}, 'https://api.yelp.com/v3/autocomplete'),
    ('business_query', [PATH_PARAM], {}, f'https://api.yelp.com/v3/businesses/{ENCODED}'),
    ('business_engagement_query', [], {'business_ids': 'a,b'}, 'https://api.yelp.com/v3/businesses/engagement'),
    ('business_food_and_drinks_insights_query', [PATH_PARAM], {},
     f'https://api.yelp.com/v3/businesses/{ENCODED}/insights/food_and_drinks'),
    ('business_insights_query', [], {'business_ids': 'a,b', 'date_range_start': '202601', 'date_range_end': '202603'},
     'https://api.yelp.com/v3/businesses/insights'),
    ('business_match_query', [],
     {'name': 'Gary Danko', 'city': 'San Francisco', 'state': 'CA', 'country': 'US', 'address1': '800 N Point St'},
     'https://api.yelp.com/v3/businesses/matches'),
    ('business_risk_signals_insights_query', [PATH_PARAM], {},
     f'https://api.yelp.com/v3/businesses/{ENCODED}/insights/risk_signals'),
    ('business_service_offerings_query', [PATH_PARAM], {},
     f'https://api.yelp.com/v3/businesses/{ENCODED}/service_offerings'),
    ('categories_query', [], {}, 'https://api.yelp.com/v3/categories'),
    ('category_query', [PATH_PARAM], {}, f'https://api.yelp.com/v3/categories/{ENCODED}'),
    ('event_lookup_query', [PATH_PARAM], {}, f'https://api.yelp.com/v3/events/{ENCODED}'),
    ('event_search_query', [], {}, 'https://api.yelp.com/v3/events'),
    ('featured_event_query', [], {'location': 'Boston, MA'}, 'https://api.yelp.com/v3/events/featured'),
    ('job_survey_query', [PATH_PARAM], {}, f'https://api.yelp.com/v3/jobs/{ENCODED}/survey'),
    ('phone_search_query', [], {'phone': '+14159083801'}, 'https://api.yelp.com/v3/businesses/search/phone'),
    ('reviews_query', [PATH_PARAM], {}, f'https://api.yelp.com/v3/businesses/{ENCODED}/reviews'),
    ('review_highlights_query', [PATH_PARAM], {}, f'https://api.yelp.com/v3/businesses/{ENCODED}/review_highlights'),
    ('search_query', [], {'location': 'Boston, MA'}, 'https://api.yelp.com/v3/businesses/search'),
    ('transaction_search_query', [PATH_PARAM], {'location': 'Boston, MA'},
     f'https://api.yelp.com/v3/transactions/{ENCODED}/search'),
]
POST_ENDPOINTS: list[Endpoint] = [
    ('ai_chat_query', [], {'query': 'best tacos'}, 'https://api.yelp.com/ai/chat/v2'),
    ('business_rapc_enabledness_query', [PATH_PARAM], {'is_enabled': True},
     f'https://api.yelp.com/v3/businesses/{ENCODED}/rapc_enabledness'),
    ('jobs_query', [], {'query': 'leaky faucet'}, 'https://api.yelp.com/v3/jobs'),
    ('request_a_quote_query', [],
     {'job_alias': 'job_faucet_repair', 'survey_responses': [], 'submit_to_nearby_businesses': True,
      'customer_info': {'first_name': 'Ada'}},
     'https://api.yelp.com/v3/projects'),
]
ENDPOINTS = GET_ENDPOINTS + POST_ENDPOINTS
ENDPOINT_PARAMS = 'method_name, args, kwargs, url'


@pytest.fixture
def api_key(faker):
    return faker.pystr()


@pytest.fixture
def yelp(api_key):
    with YelpAPI(api_key) as api:
        yield api


@pytest.fixture
def random_dict(faker):
    """A random dictionary that's JSON serializable."""
    return faker.pydict(10, True, value_types=['str', 'int', 'float', 'list', 'dict'])


class TestYelpAPI:
    def test_get_sends_auth_header_and_returns_json(self, yelp, api_key, mock_request, random_dict):
        mock_call = mock_request.get(URL, json=random_dict)

        assert yelp._get(URL) == random_dict
        assert mock_call.last_request.headers['Authorization'] == f'Bearer {api_key}'

    def test_post_sends_auth_header_and_json_body(self, yelp, api_key, mock_request, random_dict):
        mock_call = mock_request.post(URL, json=random_dict)

        assert yelp._post(URL, query='tacos', nested={'a': [1, 2]}) == random_dict
        assert mock_call.last_request.headers['Authorization'] == f'Bearer {api_key}'
        assert mock_call.last_request.json() == {'query': 'tacos', 'nested': {'a': [1, 2]}}
        assert mock_call.last_request.qs == {}

    def test_get_drops_only_none_params(self, yelp, mock_request):
        mock_call = mock_request.get(URL, json={})

        yelp._get(URL, term='pizza', limit=None, offset=0, open_now=False, location='')

        assert mock_call.last_request.qs == {
            'term': ['pizza'], 'offset': ['0'], 'open_now': ['False'], 'location': [''],
        }

    def test_post_drops_only_none_params(self, yelp, mock_request):
        mock_call = mock_request.post(URL, json={})

        yelp._post(URL, query='tacos', chat_id=None, offset=0, open_now=False, location='', items=[])

        assert mock_call.last_request.json() == {
            'query': 'tacos', 'offset': 0, 'open_now': False, 'location': '', 'items': [],
        }

    @pytest.mark.parametrize('method', ['_get', '_post'])
    @pytest.mark.parametrize('timeout_s', [None, 2.5])
    def test_uses_timeout(self, mock_request, method, timeout_s):
        mock_call = mock_request.register_uri(requests_mock.ANY, URL, json={})

        with YelpAPI('key', timeout_s=timeout_s) as yelp:
            getattr(yelp, method)(URL)

        assert mock_call.last_request.timeout == timeout_s

    def test_rejects_non_json_body(self, yelp, mock_request):
        mock_request.get(URL, text='<html>not json</html>')

        with pytest.raises(requests.exceptions.JSONDecodeError):
            yelp._get(URL)

    @pytest.mark.parametrize('status_code', [400, 401, 403, 404, 429, 500])
    def test_raises_http_error(self, yelp, mock_request, status_code):
        mock_request.get(URL, status_code=status_code, json={'error': {'code': 'ERROR', 'description': 'error'}})

        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            yelp._get(URL)

        assert exc_info.value.response.status_code == status_code

    @pytest.mark.parametrize('error, message', [
        ({'code': 'BAD', 'description': 'bad request'}, 'BAD: bad request'),
        ('something went wrong', 'something went wrong'),
        ({'code': 'BAD'}, 'BAD: None'),
        ({'description': 'bad request'}, 'None: bad request'),
        (['a', 'b'], "['a', 'b']"),
    ])
    def test_raises_yelp_api_error(self, yelp, mock_request, error, message):
        mock_request.get(URL, json={'businesses': [], 'error': error})

        with pytest.raises(YelpAPI.YelpAPIError) as exc_info:
            yelp._get(URL)

        assert exc_info.value.args[0] == message

    @pytest.mark.parametrize('body, type_name', [
        ('"an error occurred"', 'str'),
        ('["error"]', 'list'),
        ('42', 'int'),
        ('null', 'NoneType'),
    ])
    def test_rejects_non_dict_json(self, yelp, mock_request, body, type_name):
        mock_request.get(URL, text=body)

        with pytest.raises(YelpAPI.YelpAPIError) as exc_info:
            yelp._get(URL)

        assert exc_info.value.args[0] == f'Unexpected response type: {type_name}'

    @pytest.mark.parametrize('status_code', [202, 204])
    def test_empty_success_response(self, yelp, mock_request, status_code):
        mock_request.post(URL, status_code=status_code)

        assert yelp._post(URL) == {}

    def test_202_with_body_is_parsed(self, yelp, mock_request, random_dict):
        mock_request.post(URL, status_code=202, json=random_dict)

        assert yelp._post(URL) == random_dict

    def test_200_with_empty_body_raises(self, yelp, mock_request):
        mock_request.post(URL, status_code=200)

        with pytest.raises(requests.exceptions.JSONDecodeError):
            yelp._post(URL)

    def test_query_alias_is_deprecated(self, yelp, mock_request, random_dict):
        mock_call = mock_request.get(URL, json=random_dict)

        with pytest.warns(FutureWarning, match='_get') as record:
            assert yelp._query(URL, term='pizza') == random_dict
        assert mock_call.last_request.qs == {'term': ['pizza']}
        # stacklevel=2 attributes the warning to the caller, not to yelpapi itself.
        assert record[0].filename == __file__

    def test_subclass_overriding_query_warns(self):
        with pytest.warns(FutureWarning, match='override _get') as record:
            class LegacySubclass(YelpAPI):
                def _query(self, url, **kwargs):
                    return {}
        assert record[0].filename == __file__

    def test_subclass_without_query_override_does_not_warn(self):
        with warnings.catch_warnings():
            warnings.simplefilter('error')

            class ModernSubclass(YelpAPI):
                def _get(self, url, **kwargs):
                    return {}

    def test_close_closes_session(self, api_key):
        yelp = YelpAPI(api_key)
        with patch.object(yelp._yelp_session, 'close') as mock_close:
            yelp.close()
        mock_close.assert_called_once_with()

    def test_context_manager(self, api_key):
        with patch.object(YelpAPI, 'close') as mock_close:
            yelp = YelpAPI(api_key)
            with yelp as api:
                assert api is yelp
                mock_close.assert_not_called()
        mock_close.assert_called_once_with()

    def test_context_manager_closes_on_error(self, api_key):
        with patch.object(YelpAPI, 'close') as mock_close:
            with pytest.raises(RuntimeError), YelpAPI(api_key):
                raise RuntimeError
        mock_close.assert_called_once_with()

    def test_reuses_one_session(self, yelp, mock_request):
        mock_request.register_uri(requests_mock.ANY, URL, json={})

        with patch.object(yelp._yelp_session, 'request', wraps=yelp._yelp_session.request) as mock_session_request:
            yelp._get(URL)
            yelp._post(URL)

        assert mock_session_request.call_count == 2


def test_endpoints_cover_all_public_query_methods():
    """Keeps the endpoint tables (and therefore TestEndpoints) in sync with the public API."""
    public = {name for name in vars(YelpAPI) if name.endswith('_query') and not name.startswith('_')}
    assert public == {endpoint[0] for endpoint in ENDPOINTS}


# The filters fail these tests on any unexpected warning; the order matters, since the topmost mark wins.
@pytest.mark.filterwarnings('ignore:business_service_offerings_query is deprecated:DeprecationWarning')
@pytest.mark.filterwarnings('error')
class TestEndpoints:
    """
        Behavior shared by every public query method. The mocks match exactly one HTTP method and URL, so requests-mock
        raises NoMockAddress if a method uses the wrong URL, swaps GET/POST, or doesn't percent-encode a path parameter.
    """

    @pytest.mark.parametrize(ENDPOINT_PARAMS, GET_ENDPOINTS, ids=[endpoint[0] for endpoint in GET_ENDPOINTS])
    def test_get_request(self, yelp, mock_request, random_dict, method_name, args, kwargs, url):
        mock_call = mock_request.get(url, json=random_dict)

        assert getattr(yelp, method_name)(*args, **kwargs, extra_param='extra') == random_dict

        assert mock_call.last_request.qs == {k: [v] for k, v in {**kwargs, 'extra_param': 'extra'}.items()}

    @pytest.mark.parametrize(ENDPOINT_PARAMS, POST_ENDPOINTS, ids=[endpoint[0] for endpoint in POST_ENDPOINTS])
    def test_post_request(self, yelp, mock_request, random_dict, method_name, args, kwargs, url):
        mock_call = mock_request.post(url, json=random_dict)

        assert getattr(yelp, method_name)(*args, **kwargs, extra_param='extra') == random_dict

        assert mock_call.last_request.qs == {}
        assert mock_call.last_request.json() == {**kwargs, 'extra_param': 'extra'}

    @pytest.mark.parametrize(ENDPOINT_PARAMS, ENDPOINTS, ids=[endpoint[0] for endpoint in ENDPOINTS])
    def test_raises_yelp_api_error(self, yelp, mock_request, method_name, args, kwargs, url):
        """Each method returns the parsed response rather than the raw JSON."""
        mock_request.register_uri(requests_mock.ANY, url, json={'error': {'code': 'BAD', 'description': 'bad'}})

        with pytest.raises(YelpAPI.YelpAPIError, match='^BAD: bad$'):
            getattr(yelp, method_name)(*args, **kwargs)


class TestAIChatQuery:
    @pytest.mark.parametrize('invalid_query', [None, ''])
    def test_requires_query(self, yelp, invalid_query):
        with pytest.raises(ValueError, match='"query"'):
            yelp.ai_chat_query(query=invalid_query)


class TestAutocompleteQuery:
    @pytest.mark.parametrize('invalid_text', [None, ''])
    def test_requires_text(self, yelp, invalid_text):
        with pytest.raises(ValueError, match='"text"'):
            yelp.autocomplete_query(text=invalid_text)


class TestBusinessQuery:
    @pytest.mark.parametrize('invalid_id', [None, ''])
    def test_requires_id(self, yelp, invalid_id):
        with pytest.raises(ValueError, match='"id"'):
            yelp.business_query(invalid_id)


class TestBusinessMatchQuery:
    @pytest.fixture
    def params(self):
        return {'name': 'Gary Danko', 'city': 'San Francisco', 'state': 'CA', 'country': 'US',
                'address1': '800 N Point St'}

    @pytest.mark.parametrize('missing_param', ['name', 'city', 'state', 'country', 'address1'])
    def test_requires_all_params(self, yelp, params, missing_param):
        del params[missing_param]

        with pytest.raises(ValueError, match=f'"{missing_param}"'):
            yelp.business_match_query(**params)

    @pytest.mark.parametrize('empty_param', ['name', 'city', 'state', 'country'])
    def test_rejects_empty_params(self, yelp, params, empty_param):
        params[empty_param] = ''

        with pytest.raises(ValueError, match=f'"{empty_param}"'):
            yelp.business_match_query(**params)

    def test_allows_empty_address1(self, yelp, mock_request, params):
        mock_call = mock_request.get('https://api.yelp.com/v3/businesses/matches', json={})
        params['address1'] = ''

        yelp.business_match_query(**params)

        assert mock_call.last_request.qs['address1'] == ['']


class TestBusinessEngagementQuery:
    @pytest.mark.parametrize('invalid_ids', [None, ''])
    def test_requires_business_ids(self, yelp, invalid_ids):
        with pytest.raises(ValueError, match='"business_ids"'):
            yelp.business_engagement_query(business_ids=invalid_ids)


class TestBusinessFoodAndDrinksInsightsQuery:
    @pytest.mark.parametrize('invalid_id', [None, ''])
    def test_requires_id(self, yelp, invalid_id):
        with pytest.raises(ValueError, match='"id"'):
            yelp.business_food_and_drinks_insights_query(invalid_id)


class TestBusinessInsightsQuery:
    @pytest.fixture
    def params(self):
        return {'business_ids': 'a,b', 'date_range_start': '202601', 'date_range_end': '202603'}

    @pytest.mark.parametrize('missing_param', ['business_ids', 'date_range_start', 'date_range_end'])
    def test_requires_all_params(self, yelp, params, missing_param):
        del params[missing_param]

        with pytest.raises(ValueError, match=f'"{missing_param}"'):
            yelp.business_insights_query(**params)

    @pytest.mark.parametrize('empty_param', ['business_ids', 'date_range_start', 'date_range_end'])
    def test_rejects_empty_params(self, yelp, params, empty_param):
        params[empty_param] = ''

        with pytest.raises(ValueError, match=f'"{empty_param}"'):
            yelp.business_insights_query(**params)


class TestBusinessRapcEnablednessQuery:
    @pytest.mark.parametrize('invalid_id', [None, ''])
    def test_requires_id(self, yelp, invalid_id):
        with pytest.raises(ValueError, match='"id"'):
            yelp.business_rapc_enabledness_query(invalid_id, is_enabled=True)

    def test_requires_is_enabled(self, yelp):
        with pytest.raises(ValueError, match='"is_enabled"'):
            yelp.business_rapc_enabledness_query('biz-id')

    def test_disable_returns_empty_dict(self, yelp, mock_request):
        # Yelp acknowledges with an empty 202; False must be sent rather than rejected as missing.
        mock_call = mock_request.post('https://api.yelp.com/v3/businesses/biz-id/rapc_enabledness', status_code=202)

        assert yelp.business_rapc_enabledness_query('biz-id', is_enabled=False) == {}
        assert mock_call.last_request.json() == {'is_enabled': False}


class TestBusinessRiskSignalsInsightsQuery:
    @pytest.mark.parametrize('invalid_id', [None, ''])
    def test_requires_id(self, yelp, invalid_id):
        with pytest.raises(ValueError, match='"id"'):
            yelp.business_risk_signals_insights_query(invalid_id)


class TestBusinessServiceOfferingsQuery:
    @pytest.mark.parametrize('invalid_id', [None, ''])
    def test_requires_id(self, yelp, invalid_id):
        with pytest.warns(DeprecationWarning), pytest.raises(ValueError, match='"id"'):
            yelp.business_service_offerings_query(invalid_id)

    def test_is_deprecated(self, yelp, mock_request):
        mock_request.get('https://api.yelp.com/v3/businesses/biz-id/service_offerings', json={})

        with pytest.warns(DeprecationWarning, match='business_query') as record:
            yelp.business_service_offerings_query('biz-id')
        # stacklevel=2 attributes the warning to the caller, not to yelpapi itself.
        assert record[0].filename == __file__


class TestCategoryQuery:
    @pytest.mark.parametrize('invalid_alias', [None, ''])
    def test_requires_alias(self, yelp, invalid_alias):
        with pytest.raises(ValueError, match='"alias"'):
            yelp.category_query(invalid_alias)


class TestEventLookupQuery:
    @pytest.mark.parametrize('invalid_id', [None, ''])
    def test_requires_id(self, yelp, invalid_id):
        with pytest.raises(ValueError, match='"id"'):
            yelp.event_lookup_query(invalid_id)


class TestFeaturedEventQuery:
    def test_requires_location_or_lat_lng(self, yelp):
        with pytest.raises(ValueError, match='"location"'):
            yelp.featured_event_query()

    def test_accepts_lat_lng(self, yelp, mock_request):
        mock_call = mock_request.get('https://api.yelp.com/v3/events/featured', json={})

        yelp.featured_event_query(latitude=42.36, longitude=-71.06)

        assert mock_call.last_request.qs == {'latitude': ['42.36'], 'longitude': ['-71.06']}


class TestJobSurveyQuery:
    @pytest.mark.parametrize('invalid_alias', [None, ''])
    def test_requires_job_alias(self, yelp, invalid_alias):
        with pytest.raises(ValueError, match='"job_alias"'):
            yelp.job_survey_query(invalid_alias)


class TestJobsQuery:
    @pytest.mark.parametrize('invalid_query', [None, ''])
    def test_requires_query(self, yelp, invalid_query):
        with pytest.raises(ValueError, match='"query"'):
            yelp.jobs_query(query=invalid_query)


class TestPhoneSearchQuery:
    @pytest.mark.parametrize('invalid_phone', [None, ''])
    def test_requires_phone(self, yelp, invalid_phone):
        with pytest.raises(ValueError, match='"phone"'):
            yelp.phone_search_query(phone=invalid_phone)


class TestRequestAQuoteQuery:
    @pytest.fixture
    def params(self):
        return {
            'job_alias': 'job_faucet_repair',
            'survey_responses': [{'question_alias': 'faucet_type', 'user_response': ['kitchen']}],
            'submit_to_nearby_businesses': True,
            'customer_info': {'first_name': 'Ada', 'email': 'ada@example.com', 'zip_code': '94105'},
        }

    @pytest.mark.parametrize(
        'missing_param', ['job_alias', 'survey_responses', 'submit_to_nearby_businesses', 'customer_info'],
    )
    def test_requires_all_params(self, yelp, params, missing_param):
        del params[missing_param]

        with pytest.raises(ValueError, match=f'"{missing_param}"'):
            yelp.request_a_quote_query(**params)

    @pytest.mark.parametrize('empty_param, empty_value', [('job_alias', ''), ('customer_info', {})])
    def test_rejects_empty_params(self, yelp, params, empty_param, empty_value):
        params[empty_param] = empty_value

        with pytest.raises(ValueError, match=f'"{empty_param}"'):
            yelp.request_a_quote_query(**params)

    def test_allows_false_and_empty_list(self, yelp, mock_request, params):
        mock_call = mock_request.post('https://api.yelp.com/v3/projects', json={})
        params['submit_to_nearby_businesses'] = False
        params['survey_responses'] = []

        yelp.request_a_quote_query(**params)

        assert mock_call.last_request.json() == params


class TestReviewsQuery:
    @pytest.mark.parametrize('invalid_id', [None, ''])
    def test_requires_id(self, yelp, invalid_id):
        with pytest.raises(ValueError, match='"id"'):
            yelp.reviews_query(invalid_id)


class TestReviewHighlightsQuery:
    @pytest.mark.parametrize('invalid_id', [None, ''])
    def test_requires_id(self, yelp, invalid_id):
        with pytest.raises(ValueError, match='"id"'):
            yelp.review_highlights_query(invalid_id)


class TestSearchQuery:
    """
        Also covers _require_location_or_lat_lng, which featured_event_query and transaction_search_query share.
    """

    def test_requires_location_or_lat_lng(self, yelp):
        with pytest.raises(ValueError, match='"location"'):
            yelp.search_query()

    @pytest.mark.parametrize('partial_kwargs', [{'latitude': 37.7749}, {'longitude': -122.4194}])
    def test_rejects_partial_lat_lng(self, yelp, partial_kwargs):
        with pytest.raises(ValueError, match='"location"'):
            yelp.search_query(**partial_kwargs)

    @pytest.mark.parametrize('latitude, longitude', [(37.7749, -122.4194), (0, -78.5), (51.4779, 0), (0.0, 0.0)])
    def test_accepts_lat_lng(self, yelp, mock_request, latitude, longitude):
        mock_call = mock_request.get('https://api.yelp.com/v3/businesses/search', json={})

        yelp.search_query(latitude=latitude, longitude=longitude)

        assert mock_call.last_request.qs == {'latitude': [str(latitude)], 'longitude': [str(longitude)]}


class TestTransactionSearchQuery:
    @pytest.mark.parametrize('invalid_type', [None, ''])
    def test_requires_transaction_type(self, yelp, invalid_type):
        with pytest.raises(ValueError, match='"transaction_type"'):
            yelp.transaction_search_query(invalid_type, location='Boston, MA')

    def test_requires_location_or_lat_lng(self, yelp):
        with pytest.raises(ValueError, match='"location"'):
            yelp.transaction_search_query('delivery')

    def test_accepts_lat_lng(self, yelp, mock_request):
        mock_call = mock_request.get('https://api.yelp.com/v3/transactions/delivery/search', json={})

        yelp.transaction_search_query('delivery', latitude=42.36, longitude=-71.06)

        assert mock_call.last_request.qs == {'latitude': ['42.36'], 'longitude': ['-71.06']}
