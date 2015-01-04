# coding=utf-8
import pycurl
import os
from io import BytesIO


__author__ = 'ignat'
__date__ = '01.12.14 0:04'


class CodeBird:

    """ The current singleton instance """
    instance = None

    """ CONSTANTS """
    CURLE_SSL_CERTPROBLEM = 58
    CURLE_SSL_CACERT = 60
    CURLE_SSL_CACERT_BADFILE = 77
    CURLE_SSL_CRL_BADFILE = 82
    CURLE_SSL_ISSUER_ERROR = 83
    _CURLOPT_TIMEOUT_MS = 155
    _CURLOPT_CONNECTTIMEOUT_MS = 156

    """
    The OAuth consumer key of your registered app
    """
    _oauth_consumer_key = None

    """
    The corresponding consumer secret
    """
    _oauth_consumer_secret = None

    # /**
    #  * The app-only bearer token. Used to authorize app-only requests
    #  */
    # protected static $_oauth_bearer_token = null

    """ The API endpoint to use """
    _endpoint = 'https://api.twitter.com/1.1/'

    """
     * The media API endpoint to use
    """
    _endpoint_media = 'https://upload.twitter.com/1.1/'

    """ The API endpoint base to use """
    _endpoint_oauth = 'https://api.twitter.com/'

    """ The API endpoint to use for old requests """
    _endpoint_old = 'https://api.twitter.com/1/'

    """ The Request or access token. Used to sign requests """
    _oauth_token = None

    """ The corresponding request or access token secret """
    _oauth_token_secret = None

    """ The format of data to return from API calls """
    # _return_format = CODEBIRD_RETURNFORMAT_OBJECT

    """ The file formats that Twitter accepts as image uploads """
    # _supported_media_files = array(IMAGETYPE_GIF, IMAGETYPE_JPEG, IMAGETYPE_PNG)

    """ The current Codebird version """
    _version = '2.6.1'

    """ Auto-detect cURL absence """
    _use_curl = True

    """ Request timeout """
    _timeout = 10000

    """ Connection timeout """
    _connectionTimeout = 3000

    # =================================================== #

    def __init__(self):
        print('INIT')
        try:
            import pycurl
        except ImportError:
            self._use_curl = False

    def grt_version(self):
        return self._version

    def set_timeout(self, timeout):
        self._timeout = int(timeout)

    def set_connection_timeout(self, timeout):
        self._connectionTimeout = int(timeout)

    def set_consumer_key(self, key, secret):
        """ Sets the OAuth consumer key and secret (App key)
        :param str key:    OAuth consumer key
        :param str secret: OAuth consumer secret
        :return: void
        """
        self._oauth_consumer_key    = key
        self._oauth_consumer_secret = secret

    def set_token(self, token, secret):
        """ Sets the OAuth request or access token and secret (User key)
        :param str token:  OAuth request or access token
        :param str secret: OAuth request or access token secret
        :return:
        """
        self._oauth_token        = token
        self._oauth_token_secret = secret

    def get_api_methods(self) -> dict:
        """ Get allowed API methods, sorted by GET or POST
        :return:
        """
        return {
            'GET': [
                'account/settings',
                'account/verify_credentials',
                'application/rate_limit_status',
                'blocks/ids',
                'blocks/list',
                'direct_messages',
                'direct_messages/sent',
                'direct_messages/show',
                'favorites/list',
                'followers/ids',
                'followers/list',
                'friends/ids',
                'friends/list',
                'friendships/incoming',
                'friendships/lookup',
                'friendships/lookup',
                'friendships/no_retweets/ids',
                'friendships/outgoing',
                'friendships/show',
                'geo/id/:place_id',
                'geo/reverse_geocode',
                'geo/search',
                'geo/similar_places',
                'help/configuration',
                'help/languages',
                'help/privacy',
                'help/tos',
                'lists/list',
                'lists/members',
                'lists/members/show',
                'lists/memberships',
                'lists/ownerships',
                'lists/show',
                'lists/statuses',
                'lists/subscribers',
                'lists/subscribers/show',
                'lists/subscriptions',
                'mutes/users/ids',
                'mutes/users/list',
                'oauth/authenticate',
                'oauth/authorize',
                'saved_searches/list',
                'saved_searches/show/:id',
                'search/tweets',
                'statuses/home_timeline',
                'statuses/mentions_timeline',
                'statuses/oembed',
                'statuses/retweeters/ids',
                'statuses/retweets/:id',
                'statuses/retweets_of_me',
                'statuses/show/:id',
                'statuses/user_timeline',
                'trends/available',
                'trends/closest',
                'trends/place',
                'users/contributees',
                'users/contributors',
                'users/profile_banner',
                'users/search',
                'users/show',
                'users/suggestions',
                'users/suggestions/:slug',
                'users/suggestions/:slug/members',

                # // Internal
                'users/recommendations',
                'account/push_destinations/device',
                'activity/about_me',
                'activity/by_friends',
                'statuses/media_timeline',
                'timeline/home',
                'help/experiments',
                'search/typeahead',
                'search/universal',
                'discover/universal',
                'conversation/show',
                'statuses/:id/activity/summary',
                'account/login_verification_enrollment',
                'account/login_verification_request',
                'prompts/suggest',

                'beta/timelines/custom/list',
                'beta/timelines/timeline',
                'beta/timelines/custom/show'
            ],
            'POST': [
                'account/remove_profile_banner',
                'account/settings__post',
                'account/update_delivery_device',
                'account/update_profile',
                'account/update_profile_background_image',
                'account/update_profile_banner',
                'account/update_profile_colors',
                'account/update_profile_image',
                'blocks/create',
                'blocks/destroy',
                'direct_messages/destroy',
                'direct_messages/new',
                'favorites/create',
                'favorites/destroy',
                'friendships/create',
                'friendships/destroy',
                'friendships/update',
                'lists/create',
                'lists/destroy',
                'lists/members/create',
                'lists/members/create_all',
                'lists/members/destroy',
                'lists/members/destroy_all',
                'lists/subscribers/create',
                'lists/subscribers/destroy',
                'lists/update',
                'media/upload',
                'mutes/users/create',
                'mutes/users/destroy',
                'oauth/access_token',
                'oauth/request_token',
                'oauth2/invalidate_token',
                'oauth2/token',
                'saved_searches/create',
                'saved_searches/destroy/:id',
                'statuses/destroy/:id',
                'statuses/lookup',
                'statuses/retweet/:id',
                'statuses/update',
                'statuses/update_with_media', # deprecated, use media/upload
                'users/lookup',
                'users/report_spam',

                # // Internal
                'direct_messages/read',
                'account/login_verification_enrollment__post',
                'push_destinations/enable_login_verification',
                'account/login_verification_request__post',

                'beta/timelines/custom/create',
                'beta/timelines/custom/update',
                'beta/timelines/custom/destroy',
                'beta/timelines/custom/add',
                'beta/timelines/custom/remove'
            ]
        }

    def _get_endpoint(self, method):
        """ Builds the complete API endpoint url
        :param basestring method: The API method to call
        :return: string The URL to send the request to
        """
        if method[:5] == 'oauth':
            url = self._endpoint_oauth + method
        elif self._detect_media(method):
            url = self._endpoint_media + method + '.json'
        elif self._detect_old(method):
            url = self._endpoint_old + method + '.json'
        else:
            url = self._endpoint + method + ".json"
        return url

    def _detect_internal(self, method) -> bool:
        """ Detects if API call is internal
        :param str method: The API method to call
        :return: Whether the method is defined in internal API
        """
        # internals = ['users/recommendations']
        # return in_array($method, $internals);
        return method in ['users/recommendations']

    def _detect_media(self, method) -> bool:
        """ Detects if API call should use media endpoint
        :param str method: The API method to call
        :return: Whether the method is defined in media API
        """
        # $medias = array('media/upload');
        # return in_array($method, $medias);
        return method in ['media/upload']

    def _detect_old(self, method) -> bool:
        """ Detects if API call should use old endpoint

        :param str method: The API method to call
        :return: Whether the method is defined in old API
        """
        # $olds = array('account/push_destinations/device');
        # in_array($method, $olds);
        return method in ['account/push_destinations/device']

    def _detect_method(self, method, params) -> str:
        """ Detects HTTP method to use for API call
        :param str  method: The API method to call
        :param list params: The parameters to send along
        :return str: The HTTP method that should be used
        """
        # multi-HTTP method endpoints

        if method in []:
            method = method + '__post' if len(params) > 0 else method

        apimethods = self.get_api_methods()

        for httpmethod in apimethods:
            if method in apimethods[httpmethod]:
                return httpmethod

        raise Exception("Can't find HTTP method to use for \"%s\"." % method)

    def test_api(self):
        return 'qwerty'

    # ----------
    def __getattr__(self, fn):
        # print(fn, params)
        def handler_function(*args, **kwargs):
            print("INSIDE :: ", fn, args, kwargs)

            params = args[1]
            print(fn, params)
            # /**
        # * Main API handler working on any requests you issue
        # *
        # * @param string $fn    The member function you called
        # * @param array $params The parameters you sent along
        # *
        # * @return mixed The API reply encoded in the set return_format
        # */
        #
        # public function __call($fn, $params)
        # // parse parameters
        #    apiparams = self._parseApiParams(params)

        #    // stringify null and boolean parameters
        #    $apiparams = $this->_stringifyNullBoolParams($apiparams);
        #
        #    $app_only_auth = false;
        #    if (count($params) > 1) {
        #        // convert app_only_auth param to bool
        #        $app_only_auth = !! $params[1];
        #    }
        #
        #    // reset token when requesting a new token
        #    // (causes 401 for signature error on subsequent requests)
        #    if ($fn === 'oauth_requestToken') {
        #        $this->setToken(null, null);
        #    }
        #
        #    // map function name to API method
        #    list($method, $method_template) = $this->_mapFnToApiMethod($fn, $apiparams);
        #
        #    $httpmethod = $this->_detectMethod($method_template, $apiparams);
        #    $multipart  = $this->_detectMultipart($method_template);
        #    $internal   = $this->_detectInternal($method_template);
        #
        #    return $this->_callApi(
        #        $httpmethod,
        #        $method,
        #        $apiparams,
        #        $multipart,
        #        $app_only_auth,
        #        $internal
        #
            return self.test_api()
        return handler_function



    def _call_api_curl(self, httpmethod="GET", method='', params=None, multipart=False, app_only_auth=False, internal=False):
        """
        Calls the API using cURL
        :param str  httpmethod:    The HTTP method to use for making the request (Get or Post)
        :param str  method:        The API method to call
        :param list optional params:        The parameters to send along
        :param bool optional multipart:     Whether to use multipart/form-data
        :param bool optional app_only_auth: Whether to use app-only bearer authentication
        :param bool optional internal:      Whether to use internal call
        :return mixed The API reply, encoded in the set return_format
        """
        try:
            """
            Get Url form params and multipart
            """
            # list ($authorization, $url, $params, $request_headers)
            # = $this->_callApiPreparations(
            #     $httpmethod, $method, $params, $multipart, $app_only_auth
            # );

            # url = 'http://ya.ru'
            url = self._get_endpoint(method)

            buffer = BytesIO()
            c = pycurl.Curl()

            if httpmethod.upper() != "GET":
                c.setopt(pycurl.POST, 1)
                c.setopt(pycurl.POSTFIELDS, params)

            print("URL :: " + url)
            c.setopt(pycurl.URL, url)

            """ TEST STRING """
            authorization = 'OAuth oauth_consumer_key="oLVqNUOVNERDtKfh9n3vW1LXd", oauth_nonce="d99dfd58", oauth_signature="Pe9VdWV5UYppS5LktFccKTqi%2BDI%3D", oauth_signature_method="HMAC-SHA1", oauth_timestamp="1420382028", oauth_token="2578434163-0CPPrAKfg3OtrccnEBjiojvFzZUeWl8fYyJf2bF", oauth_version="1.0"'
            """ END TEST STRING """

            request_headers = ['Authorization: ' + authorization, 'Expect:']

            if self._timeout is not None:
                c.setopt(self._CURLOPT_TIMEOUT_MS, self._timeout)
            if self._connectionTimeout is not None:
                c.setopt(self._CURLOPT_CONNECTTIMEOUT_MS, self._connectionTimeout)

            c.setopt(pycurl.FOLLOWLOCATION, 0)
            c.setopt(pycurl.HEADER, 1)
            c.setopt(pycurl.HTTPHEADER, request_headers)
            c.setopt(pycurl.SSL_VERIFYPEER, 1)
            c.setopt(pycurl.SSL_VERIFYHOST, 2)
            c.setopt(pycurl.CAINFO, os.path.dirname(os.path.abspath(__file__)) + '/src/cacert.pem')
            c.setopt(pycurl.WRITEDATA, buffer)
            c.perform()
            code = c.getinfo(c.RESPONSE_CODE)

            print("CODE [%s] :: Time [%s]" % (code, c.getinfo(c.TOTAL_TIME)))
            c.close()
            return buffer.getvalue().decode()

        except Exception as e:
            print("ERROR :: ", e)


    # /**
    #  * Do preparations to make the API call
    #  *
    #  * @param string  $httpmethod      The HTTP method to use for making the request
    #  * @param string  $method          The API method to call
    #  * @param array   $params          The parameters to send along
    #  * @param bool    $multipart       Whether to use multipart/form-data
    #  * @param bool    $app_only_auth   Whether to use app-only bearer authentication
    #  *
    #  * @return array (string authorization, string url, array params, array request_headers)
    #  */
    # protected function _callApiPreparations(
    #     $httpmethod, $method, $params, $multipart, $app_only_auth
    # )
    # {
    #     $authorization = null;
    #     $url           = $this->_getEndpoint($method);
    #     $request_headers = array();
    #     if ($httpmethod === 'GET') {
    #         if (! $app_only_auth) {
    #             $authorization = $this->_sign($httpmethod, $url, $params);
    #         }
    #         if (json_encode($params) !== '{}'
    #             && json_encode($params) !== '[]'
    #         ) {
    #             $url .= '?' . http_build_query($params);
    #         }
    #     } else {
    #         if ($multipart) {
    #             if (! $app_only_auth) {
    #                 $authorization = $this->_sign($httpmethod, $url, array());
    #             }
    #             $params = $this->_buildMultipart($method, $params);
    #         } else {
    #             if (! $app_only_auth) {
    #                 $authorization = $this->_sign($httpmethod, $url, $params);
    #             }
    #             $params        = http_build_query($params);
    #         }
    #         if ($multipart) {
    #             $first_newline      = strpos($params, "\r\n");
    #             $multipart_boundary = substr($params, 2, $first_newline - 2);
    #             $request_headers[]  = 'Content-Type: multipart/form-data; boundary='
    #                 . $multipart_boundary;
    #         }
    #     }
    #     if ($app_only_auth) {
    #         if (self::$_oauth_consumer_key === null
    #             && self::$_oauth_bearer_token === null
    #         ) {
    #             throw new \Exception('To make an app-only auth API request, consumer key or bearer token must be set.');
    #         }
    #         // automatically fetch bearer token, if necessary
    #         if (self::$_oauth_bearer_token === null) {
    #             $this->oauth2_token();
    #         }
    #         $authorization = 'Bearer ' . self::$_oauth_bearer_token;
    #     }
    #
    #     return array(
    #         $authorization, $url, $params, $request_headers
    #     );
    # }
    #
    # /**
    #  * Parses the API reply to separate headers from the body
    #  *
    #  * @param string $reply The actual raw HTTP request reply
    #  *
    #  * @return array (headers, reply)
    #  */
    # protected function _parseApiHeaders($reply) {
    #     // split headers and body
    #     $headers = array();
    #     $reply = explode("\r\n\r\n", $reply, 4);
    #
    #     // check if using proxy
    #     $proxy_strings = array();
    #     $proxy_strings[strtolower('HTTP/1.0 200 Connection Established')] = true;
    #     $proxy_strings[strtolower('HTTP/1.1 200 Connection Established')] = true;
    #     if (array_key_exists(strtolower(substr($reply[0], 0, 35)), $proxy_strings)) {
    #         array_shift($reply);
    #     } elseif (count($reply) > 2) {
    #         $headers = array_shift($reply);
    #         $reply = array(
    #             $headers,
    #             implode("\r\n", $reply)
    #         );
    #     }
    #
    #     $headers_array = explode("\r\n", $reply[0]);
    #     foreach ($headers_array as $header) {
    #         $header_array = explode(': ', $header, 2);
    #         $key = $header_array[0];
    #         $value = '';
    #         if (count($header_array) > 1) {
    #             $value = $header_array[1];
    #         }
    #         $headers[$key] = $value;
    #     }
    #
    #     if (count($reply) > 1) {
    #         $reply = $reply[1];
    #     } else {
    #         $reply = '';
    #     }
    #
    #     return array($headers, $reply);
    # }
    #
    # /**
    #  * Parses the API reply to encode it in the set return_format
    #  *
    #  * @param string $reply The actual HTTP body, JSON-encoded or URL-encoded
    #  *
    #  * @return array|object The parsed reply
    #  */
    # protected function _parseApiReply($reply)
    # {
    #     $need_array = $this->_return_format === CODEBIRD_RETURNFORMAT_ARRAY;
    #     if ($reply === '[]') {
    #         switch ($this->_return_format) {
    #             case CODEBIRD_RETURNFORMAT_ARRAY:
    #                 return array();
    #             case CODEBIRD_RETURNFORMAT_JSON:
    #                 return '{}';
    #             case CODEBIRD_RETURNFORMAT_OBJECT:
    #                 return new \stdClass;
    #         }
    #     }
    #     if (! $parsed = json_decode($reply, $need_array)) {
    #         if ($reply) {
    #             if (stripos($reply, '<' . '?xml version="1.0" encoding="UTF-8"?' . '>') === 0) {
    #                 // we received XML...
    #                 // since this only happens for errors,
    #                 // don't perform a full decoding
    #                 preg_match('/<request>(.*)<\/request>/', $reply, $request);
    #                 preg_match('/<error>(.*)<\/error>/', $reply, $error);
    #                 $parsed['request'] = htmlspecialchars_decode($request[1]);
    #                 $parsed['error'] = htmlspecialchars_decode($error[1]);
    #             } else {
    #                 // assume query format
    #                 $reply = explode('&', $reply);
    #                 foreach ($reply as $element) {
    #                     if (stristr($element, '=')) {
    #                         list($key, $value) = explode('=', $element, 2);
    #                         $parsed[$key] = $value;
    #                     } else {
    #                         $parsed['message'] = $element;
    #                     }
    #                 }
    #             }
    #         }
    #         $reply = json_encode($parsed);
    #     }
    #     switch ($this->_return_format) {
    #         case CODEBIRD_RETURNFORMAT_ARRAY:
    #             return $parsed;
    #         case CODEBIRD_RETURNFORMAT_JSON:
    #             return $reply;
    #         case CODEBIRD_RETURNFORMAT_OBJECT:
    #             return (object) $parsed;
    #     }
    #     return $parsed;
    # }




    """ =========== TEST =========== """

    def make_curl(self):
        try:
            buffer = BytesIO()
            c = pycurl.Curl()
            c.setopt(pycurl.URL, 'http://ya.ru')
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            c.setopt(pycurl.WRITEDATA, buffer)
            c.setopt(pycurl.SSL_VERIFYHOST, 1)
            c.perform()
            code = c.getinfo(c.RESPONSE_CODE)
            print("CODE [%s] :: Time [%s]" % (code, c.getinfo(c.TOTAL_TIME)))
            c.close()
            return buffer.getvalue().decode()
        except Exception as e:
            print("ERROR :: ", e)

    def make_no_curl(self):
        """
        urllib.request()...
        """
        try:
            pass
        except Exception as e:
            print("ERROR :: ", e)


class Entity:
    '''Class to represent an entity. Callable to update the entity's position.'''

    def __init__(self, size, x, y):
        self.x, self.y = x, y
        self.size = size

    def __call__(self, x, y):
        '''Change the position of the entity.'''
        self.x, self.y = x, y

    def boo(self, *args):
        print("BOO :: ", args)

    def __getattr__(self, name):
        def handler_function(*args, **kwargs):
            print(name, args, kwargs)
        return handler_function



if __name__ == '__main__':
    print("Start")

    consumer_key = 'oLVqNUOVNERDtKfh9n3vW1LXd'
    consumer_secret = 'uLd0zJDK0nwcjZMN7jg9YMIZVOOasrIWzjJ3BtS1ZR9TnCO5Zl'
    access_secret = '7Y5djMLVmVx0RUbCv7ojtIhI01AjZzSe4eEuuf1YKLpAL'
    access_token = '2578434163-0CPPrAKfg3OtrccnEBjiojvFzZUeWl8fYyJf2bF'

    # curl = CodeBird()._call_api_curl('GET', 'application_rateLimitStatus')
    curl = CodeBird().boo('fn', 'params', 'pppp')
    # CodeBird()._get_endpoint('application/rate_limit_status')
    print("\nOUT :: ", curl)
    # a = Entity(10, 1, 2)
    # a.boo('test')
    # a.foo('boo/mamazuzu', 1, 2, 3)
    # print("OUT :: ", a)
