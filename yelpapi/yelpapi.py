"""
	Copyright (c) 2013, Los Alamos National Security, LLC
	All rights reserved.

	Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
	following conditions are met:

	* Redistributions of source code must retain the above copyright notice, this list of conditions and the following
	  disclaimer.
	* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
	  following disclaimer in the documentation and/or other materials provided with the distribution.
	* Neither the name of Los Alamos National Security, LLC nor the names of its contributors may be used to endorse or
	  promote products derived from this software without specific prior written permission.

	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
	INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
	DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
	SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
	SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
	WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
	THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from requests_oauthlib import OAuth1Session

SEARCH_API_URL = 'http://api.yelp.com/v2/search'
BUSINESS_API_URL = 'http://api.yelp.com/v2/business/%s'

class YelpAPI(object):
	"""
		This class implements the complete Yelp 2.0 API. It offers access to both the Search API and
		Business API. It is simple and completely extensible since it dynamically takes arguments. This will
		allow it to continue working even if Yelp changes the spec. The only thing that should cause this to break
		is if Yelp changes the URL scheme.
	"""

	class YelpError(Exception):
		"""
			This class is used for all non-API errors. For example, this exception will be raised if a non-JSON-parseable
			response from Yelp is received.
		"""
		pass
	
	class YelpAPIError(Exception):
		"""
			This class is used for all API errors. For a list of all possible Yelp API errors, see
			http://www.yelp.com/developers/documentation/v2/errors.
		"""
		pass

	def __init__(self, consumer_key, consumer_secret, token, token_secret):
		self._yelp_session = OAuth1Session(consumer_key, consumer_secret, token, token_secret)
	
	@staticmethod
	def _get_clean_parameters(kwargs):
		"""
			Clean the parameters by filtering out any parameters that have a None value.
		"""
		return dict((k, v) for k, v in kwargs.items() if v is not None)

	def search_query(self, **kwargs):
		"""
			This function implements the Yelp Search API (http://www.yelp.com/developers/documentation/v2/search_api).
			Arbitrary keywords can be passed in, and a list of businesses (each represented as a dict) will be returned.
		"""
		parameters = YelpAPI._get_clean_parameters(kwargs)
		response = self._yelp_session.get(SEARCH_API_URL, params=parameters)

		#raise YelpError if Yelp returns invalid JSON or something other than JSON
		try:
			response_json = response.json()
		except ValueError as e:
			raise self.YelpError(e)

		#Yelp can return one of many different API errors, so check for one of them
		#possible errors: http://www.yelp.com/developers/documentation/v2/errors
		if 'error' in response_json:
			if 'field' in response_json['error']:
				raise self.YelpAPIError(response_json['error']['id'], '%s [field=%s]' % (response_json['error']['text'], response_json['error']['field']))
			else:
				raise self.YelpAPIError(response_json['error']['id'], response_json['error']['text'])

		#we got a good response, so return
		return response_json
	
	def business_query(self, id, **kwargs):
		"""
			Similar to search_query, this function implements the Yelp Business API (http://www.yelp.com/developers/documentation/v2/business).
			A mandatory business ID must be passed in, as well as any arbitrary keywords allowed by Yelp. A single dict will be returned for the
			business.
		"""
		if not id:
			raise ValueError('A valid business ID must be given.')

		parameters = YelpAPI._get_clean_parameters(kwargs)
		response = self._yelp_session.get(BUSINESS_API_URL % id, params=parameters)

		#Yelp currently returns a 404 HTML page if an invalid business ID is provided, so check for that
		try:
			response_json = response.json()
		except ValueError:
			raise self.YelpError('Unable to parse JSON from Yelp response. This is likely caused by an invalid business ID [id=%s].' % id)

		#we got a good response, so return
		return response_json
