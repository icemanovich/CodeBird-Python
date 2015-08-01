# coding=utf-8
import pycurl
import urllib.parse
import os
import time
import hashlib
import hmac
import base64
from io import BytesIO
import requests

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

    _endpoint = 'https://api.twitter.com/1.1/'
    """ The API endpoint to use """

    _endpoint_media = 'https://upload.twitter.com/1.1/'
    """ The media API endpoint to use """

    _endpoint_oauth = 'https://api.twitter.com/'
    """ The API endpoint base to use """

    _endpoint_old = 'https://api.twitter.com/1/'
    """ The API endpoint to use for old requests """

    _oauth_token = None
    """ The Request or access token. Used to sign requests """

    _oauth_token_secret = None
    """ The corresponding request or access token secret """

    """ The format of data to return from API calls """
    # _return_format = CODEBIRD_RETURNFORMAT_OBJECT

    """ The file formats that Twitter accepts as image uploads """
    # _supported_media_files = array(IMAGETYPE_GIF, IMAGETYPE_JPEG, IMAGETYPE_PNG)

    _version = '2.6.1'
    """ The current Codebird version """

    _use_curl = True
    """ Auto-detect cURL absence """

    _timeout = 10000
    """ Request timeout """

    _connectionTimeout = 3000
    """ Connection timeout """

    # =================================================== #

    def __init__(self):
        try:
            import pycurl
        except ImportError:
            self._use_curl = False
            print('Unable to find pycurl extension.')

    def get_version(self):
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
        :param str|None token:  OAuth request or access token
        :param str|None secret: OAuth request or access token secret
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

    def _detect_internal(self, method_name) -> bool:
        """ Detects if API call is internal
        :param str method: The API method to call
        :return: Whether the method is defined in internal API
        """

        return method_name in ['users/recommendations']

    def _detect_media(self, method) -> bool:
        """ Detects if API call should use media endpoint
        :param str method: The API method to call
        :return: Whether the method is defined in media API
        """

        return method in ['media/upload']

    def _detect_old(self, method) -> bool:
        """ Detects if API call should use old endpoint

        :param str method: The API method to call
        :return: Whether the method is defined in old API
        """

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

        api_methods = self.get_api_methods()

        for httpmethod in api_methods:
            if method in api_methods[httpmethod]:
                return httpmethod

        raise Exception("Can't find HTTP method to use for \"%s\"." % method)

    def _detect_multipart(self, method) -> bool:
        """Detects if API call should use multipart/form-data

        :param str method: The API method to call
        :return: Whether the method should be sent as multipart
        """
        multi_parts = [
            # Tweets
            'statuses/update_with_media',
            'media/upload',

            # Users
            'account/update_profile_background_image',
            'account/update_profile_image',
            'account/update_profile_banner'
        ]
        return method in multi_parts

    # ----------
    def __getattr__(self, fn):
        def call(*args, **kwargs):
            """ Main API handler working on any requests you issue
            :param args:
            :param kwargs:
            :param str optional fn:      The member function you called
            :param dict optional params: The parameters you sent along
            :return: The API reply encoded in the set return_format
            """
            print("MAGIC_CALL :: ", fn, args, kwargs)

            params = args[0] if len(args) > 0 else {}
            print("CALL :: ", fn, params)

            # parse parameters
            apiparams = self._parse_api_params(params)

            # stringify null and boolean parameters
            apiparams = self._stringify_null_bool_params(apiparams)

            app_only_auth = False
            if len(params) > 1:
                # convert app_only_auth param to bool
                app_only_auth = bool(params[1])

            # reset token when requesting a new token
            # (causes 401 for signature error on subsequent requests)
            if fn == 'oauth_requestToken':
                self.set_token(None, None)

            # map function name to API method
            method, method_template = self._mapFnToApiMethod(fn, apiparams)

            httpmethod = self._detect_method(method_template, apiparams)
            multipart  = self._detect_multipart(method_template)
            internal   = self._detect_internal(method_template)

            return self._call_api(httpmethod, method, apiparams, multipart, app_only_auth, internal)

        return call

    def _call_api(self, httpmethod, method, params=list, multipart=False, app_only_auth=False, internal=False):
        """ Calls the API
        :param str httpmethod:              The HTTP method to use for making the request
        :param str method:                  The API method to call
        :param list optional params:        The parameters to send along
        :param bool optional multipart:     Whether to use multipart/form-data
        :param bool optional app_only_auth: Whether to use app-only bearer authentication
        :return:
        """

        if not app_only_auth and self._oauth_token is None and method[:5] != "oauth":
            raise Exception('To call this API, the OAuth access token must be set.')

        if self._use_curl:
            return self._call_api_curl(httpmethod, method, params, multipart, app_only_auth, internal)

        return self._call_api_no_curl(httpmethod, method, params, multipart, app_only_auth, internal)

    def _call_api_curl(self, httpmethod="GET", method='', params=None, multipart=False, app_only_auth=False, internal=False):
        """ Calls the API using cURL
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
            authorization, url, params, request_headers = self._call_api_preparations(
                httpmethod, method, params, multipart, app_only_auth)

            buffer = BytesIO()
            c = pycurl.Curl()

            if httpmethod.upper() != "GET":
                c.setopt(pycurl.POST, 1)
                c.setopt(pycurl.POSTFIELDS, params)

            print("URL :: " + url)
            c.setopt(pycurl.URL, url)

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
            # c.setopt(pycurl.CAPATH, os.path.dirname(os.path.abspath(__file__)) + '/src/cacert.pem')
            c.setopt(pycurl.WRITEDATA, buffer)
            c.perform()
            code = c.getinfo(c.RESPONSE_CODE)

            print("CODE [%s] :: Time [%s]" % (code, c.getinfo(c.TOTAL_TIME)))
            c.close()
            return buffer.getvalue().decode()

        except Exception as e:
            print("ERROR :: ", e)

    # #####################################################

    def _call_api_no_curl(self, httpmethod="GET", method='', params=None, multipart=False, app_only_auth=False, internal=False):

        """Calls the API without cURL

        :param str httpmethod:  The HTTP method to use for making the request
        :param str method: The API method to call
        :param list optional params: The parameters to send along
        :param bool optional multipart:  Whether to use multipart/form-data
        :param bool optional app_only_auth: Whether to use app-only bearer authentication
        :param bool optional internal: Whether to use internal call
        :return: The API reply, encoded in the set return_format
        """
        #
        # TODO :: Write code for API call without CURL request !!!
        #
        authorization, url, params, request_headers = self._call_api_preparations(
                httpmethod, method, params, multipart, app_only_auth)

        # hostname          = parse_url($url, PHP_URL_HOST)
        request_headers = [
            'Authorization: ' + authorization,
            'Accept: */*',
            'Connection: Close'
        ]

        if httpmethod != 'GET' and multipart is False:
            request_headers.append('Content-Type: application/x-www-form-urlencoded')

        #
        # TODO :: @see https://docs.python.org/2/library/ssl.html#client-side-operation
        #

        # $context = stream_context_create(array(
        #     'http' => array(
        #         'method'           => $httpmethod,
        #         'protocol_version' => '1.1',
        #         'header'           => implode("\r\n", $request_headers),
        #         'timeout'          => $this->_timeout / 1000,
        #         'content'          => $httpmethod === 'POST' ? $params : null,
        #         'ignore_errors'    => true
        #     ),
        #     'ssl' => array(
        #         'verify_peer'  => false,
        #         'cafile'       => __DIR__ . '/cacert.pem',
        #         'verify_depth' => 5,
        #         'peer_name'    => $hostname
        #     )
        # ));
        #
        # $reply   = @file_get_contents($url, false, $context);
        # $headers = $http_response_header;
        # $result  = '';
        # foreach ($headers as $header) {
        #     $result .= $header . "\r\n";
        # }
        # $result .= "\r\n" . $reply;
        #
        # // find HTTP status
        # $httpstatus = '500';
        # $match      = array();
        # if (preg_match('/HTTP\/\d\.\d (\d{3})/', $headers[0], $match)) {
        #     $httpstatus = $match[1];
        # }
        #
        # list($headers, $reply) = $this->_parseApiHeaders($result);
        # $reply                 = $this->_parseApiReply($reply);
        # $rate                  = $this->_getRateLimitInfo($headers);
        # switch ($this->_return_format) {
        #     case CODEBIRD_RETURNFORMAT_ARRAY:
        #         $reply['httpstatus'] = $httpstatus;
        #         $reply['rate']       = $rate;
        #         break;
        #     case CODEBIRD_RETURNFORMAT_OBJECT:
        #         $reply->httpstatus = $httpstatus;
        #         $reply->rate       = $rate;
        #         break;
        # }
        # return $reply;
    # #####################################################



    def _parse_api_params(self, params) -> dict:
        """Parse given params, detect query-style params
        :param str|list params: Parameters to parse
        :return: dict
        """

        api_params = {}
        if len(params) == 0:
            return api_params

        # if (is_array($params[0])) {
        #     // given parameters are array
        #     $apiparams = $params[0];
        #     if (! is_array($apiparams)) {
        #         $apiparams = array();
        #     }
        #     return apiparams;
        # }

        # // user gave us query-style params
        # parse_str($params[0], $apiparams);
        # if (! is_array($apiparams)) {
        #     $apiparams = array();
        # }

        # if (! get_magic_quotes_gpc()) {
        #     return $apiparams;
        # }

        # // remove auto-added slashes recursively if on magic quotes steroids
        # foreach($apiparams as $key => $value) {
        #     if (is_array($value)) {
        #         $apiparams[$key] = array_map('stripslashes', $value);
        #     } else {
        #         $apiparams[$key] = stripslashes($value);
        #     }
        # }

        return api_params

    def is_scalar(self, value):
        return isinstance(value, (type(None), str, int, float, bool))

    def _stringify_null_bool_params(self, api_params) -> dict:
        """ Replace null and boolean parameters with their string representations
        :param dict api_params: Parameter array to replace in
        :return:
        """
        for value in api_params.items():
            if not self.is_scalar(value):
                # no need to try replacing arrays
                continue
            if value[1] is None:
                api_params[value[0]] = 'null'
            elif isinstance(value[1], bool):
                api_params[value[0]] = 'true' if value[1] is True else 'false'
        return api_params

    def _mapFnToApiMethod(self, fn, apiparams) -> (str, str):
        """ Maps called PHP magic method name to Twitter API method

        :param str fn:    Function called
        :param list|dict apiparams: by ref API parameters
        :return (str, str): string method, string method_template
        """

        # replace _ by /
        method = self._map_fn_insert_slashes(fn)

        # undo replacement for URL parameters
        method = self._map_fn_restore_param_underscores(method)

        # copy string
        method_template = (method + '.')[:-1]
        #
        # // replace AA by URL parameters
        # method_template = method
        # $match           = array();
        # if (preg_match('/[A-Z_]{2,}/', $method, $match)) {
        #     foreach ($match as $param) {
        #         $param_l = strtolower($param);
        #         $method_template = str_replace($param, ':' . $param_l, $method_template);
        #         if (! isset($apiparams[$param_l])) {
        #             for ($i = 0; $i < 26; $i++) {
        #                 $method_template = str_replace(chr(65 + $i), '_' . chr(97 + $i), $method_template);
        #             }
        #             throw new \Exception(
        #                 'To call the templated method "' . $method_template
        #                 . '", specify the parameter value for "' . $param_l . '".'
        #             );
        #         }
        #         $method  = str_replace($param, $apiparams[$param_l], $method);
        #         unset($apiparams[$param_l]);
        #     }
        # }
        #
        # // replace A-Z by _a-z
        for i in range(26):
            method = method.replace(chr(65 + i), '_' + chr(97 + i), 1)
            method_template = method_template.replace(chr(65 + i), '_' + chr(97 + i), 1)

        return method, method_template

    def _map_fn_insert_slashes(self, fn) -> str:
        """ API method mapping: Replaces _ with / character
        :param str fn: Function called
        :return str:   API method to call
        """
        return '/'.join(fn.split('_'))

    def _map_fn_restore_param_underscores(self, method) -> str:
        """ API method mapping: Restore _ character in named parameters

        :param str method: API method to call
        :return: API method with restored underscores
        """
        url_parameters_with_underscore = ['screen_name', 'place_id']
        for param in url_parameters_with_underscore:
            param = param.upper()
            replacement_was = param.replace('_', '/')
            method = method.replace(replacement_was, param)

        return method

    def _call_api_preparations(self, httpmethod, method, params, multipart, app_only_auth):
        """ Do preparations to make the API call

        :param str httpmethod:          The HTTP method to use for making the request
        :param str method:              The API method to call
        :param dict params:             The parameters to send along
        :param boolean multipart:       Whether to use multipart/form-data
        :param boolean app_only_auth:   Whether to use app-only bearer authentication
        :return: (str authorization, st url, dict params, dict request_headers)
        """

        url             = self._get_endpoint(method)
        authorization   = None
        request_headers = list

        if httpmethod == 'GET':
            if not app_only_auth:
                authorization = self._sign(httpmethod, url, params)

            # if (json_encode($params) !== '{}'
            #     && json_encode($params) !== '[]'
            # ) {
            #     $url .= '?' . http_build_query($params);
            # }
        else:
            if multipart:
                if not app_only_auth:
                    authorization = self._sign(httpmethod, url, {})

                # params = self._buildMultipart(method, params)
            else:
                if not app_only_auth:
                    authorization = self._sign(httpmethod, url, params)

                # params        = http_build_query(params)

            # if multipart:
            #     first_newline      = strpos($params, "\r\n");
            #     multipart_boundary = substr($params, 2, $first_newline - 2);
            #     request_headers[]  = 'Content-Type: multipart/form-data; boundary='  + multipart_boundary

        if app_only_auth:
            if self._oauth_consumer_key is None and self._oauth_bearer_token is None:
                raise Exception('To make an app-only auth API request, consumer key or bearer token must be set.')

            # automatically fetch bearer token, if necessary
            # if self._oauth_bearer_token is None:
            #     self.oauth2_token()

            authorization = 'Bearer ' + self._oauth_bearer_token

        return authorization, url, params, request_headers

    #
    # /**
    #  * Parses the API reply to separate headers from the body
    #  *
    #  * @param string $reply The actual raw HTTP request reply
    #  *
    #  * @return array (headers, reply)
    #  */
    def _parseApiHeaders(self, reply):

        # split headers and body
        headers = []
        pass
        # $reply = explode("\r\n\r\n", $reply, 4);
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

    # /**
    #  * Check if there were any SSL certificate errors
    #  *
    #  * @param int $validation_result The curl error number
    #  *
    #  * @return void
    #  */
    # protected function _validateSslCertificate($validation_result)
    # {
    #     if (in_array(
    #             $validation_result,
    #             array(
    #                 CURLE_SSL_CERTPROBLEM,
    #                 CURLE_SSL_CACERT,
    #                 CURLE_SSL_CACERT_BADFILE,
    #                 CURLE_SSL_CRL_BADFILE,
    #                 CURLE_SSL_ISSUER_ERROR
    #             )
    #         )
    #     ) {
    #         throw new \Exception(
    #             'Error ' . $validation_result
    #             . ' while validating the Twitter API certificate.'
    #         );
    #     }
    # }

    """
        Signing helpers
    """
    def _url(self, data) -> str:
        """ URL-encodes the given data
        :param str|list data:
        :return: The encoded data
        """
        if isinstance(data, list) or isinstance(data, dict):
            return data
    #         return array_map(array(
    #             $this,
    #             '_url'
    #         ), $data);
        elif self.is_scalar(data):
            #
            # TODO :: Incorrect Quoting URL address
            #
            return urllib.parse.quote(data)
    #         return str_replace(array(
    #             '+',
    #             '!',
    #             '*',
    #             "'",
    #             '(',
    #             ')'
    #         ), array(
    #             ' ',
    #             '%21',
    #             '%2A',
    #             '%27',
    #             '%28',
    #             '%29'
    #         ), rawurlencode($data));
            # source = http://yandex.ru/news.php?type=123&query=qwerty+1
            # http%3A//yandex.ru/news.php%3Ftype%3D123%26query%3Dqwerty%2B1       ## python way
            # http%3A%2F%2Fyandex.ru%2Fnews.php%3Ftype%3D123%26query%3Dqwerty%2B1 ### php urlencode
            # http%3A%2F%2Fyandex.ru%2Fnews.php%3Ftype%3D123%26query%3Dqwerty%2B1 ### php rawurlencode

        else:
            return ''

    def _sha1(self, data) -> str:
        """ Gets the base64-encoded SHA1 hash for the given data

        :param str data: The data to calculate the hash from
        :return str:     The hash
        """
        if self._oauth_consumer_secret is None:
            raise Exception('To generate a hash, the consumer secret must be set.')

        # key = "CONSUMER_SECRET&TOKEN_SECRET"
        key = self._oauth_consumer_secret + '&'
        if self._oauth_token_secret is not None:
            key += self._oauth_token_secret

        # The Base String as specified here:
        # raw = "BASE_STRING" # as specified by oauth
        hashed = hmac.new(bytes(key, 'utf-8'), bytes(data, 'utf-8'), 'sha1')

        # The signature
        s = base64.b64encode(hashed.digest()).decode('utf-8')
        print("SING :: ", s)
        return s

    def _nonce(self, length=8) -> str:
        """ Generates a (hopefully) unique random string
        :param int optional length: The length of the string to generate
        :return str: The random string
        """
        if length < 1:
            raise Exception('Invalid nonce length.')

        return hashlib.md5(str(int(time.time())).encode('utf-8')).hexdigest()[:length]

    def _sign(self, httpmethod, method, params={}, append_to_get=False) -> str:
        """ Generates an OAuth signature
        :param str           httpmethod:    Usually either 'GET' or 'POST' or 'DELETE'
        :param str           method:        The API method to call
        :param dict optional params:        The API call parameters, associative
        :param bool optional append_to_get: Whether to append the OAuth params to GET
        :return str: Authorization HTTP header
        """

        if self._oauth_consumer_key is None:
            raise Exception('To generate a signature, the consumer key must be set.')

        sign_params = {
            'consumer_key'    : self._oauth_consumer_key,
            'version'         : '1.0',
            'timestamp'       : str(int(time.time())),
            'nonce'           : self._nonce(),
            'signature_method': 'HMAC-SHA1'
        }

        sign_base_params = {}
        for value in sign_params.items():
            sign_base_params['oauth_' + value[0]] = self._url(value[-1])

        if self._oauth_token is not None:
            sign_base_params['oauth_token'] = self._url(self._oauth_token)

        # signature = ''
        # if append_to_get is True:   # is True
        #     for value in params.items():
        #         sign_base_params[value[0]] = self._url(value[-1])
        #
        #     sign_base_string = []
        #     for value in sign_base_params.items():
        #         sign_base_string.append(value[0] + '=' + value[-1])
        #
        #     sign_base_string = '&'.join(sign_base_string)
        #     signature = self._sha1(httpmethod + '&' + self._url(method) + '&' + self._url(sign_base_string))

        oauth_params = sign_base_params.copy()
        for value in params.items():
            sign_base_params[value[0]] = self._url(value[1])

        sign_base_string = []
        for value in sign_base_params.items():
            sign_base_string.append(value[0] + '=' + value[-1])

        sign_base_string = '&'.join(sign_base_string)
        signature = self._sha1(httpmethod + '&' + self._url(method) + '&' + self._url(sign_base_string))

        # ksort($sign_base_params);
        # $sign_base_string = '';
        # foreach ($sign_base_params as $key => $value) {
        #     $sign_base_string .= $key . '=' . $value . '&';
        # }
        # $sign_base_string = substr($sign_base_string, 0, -1);
        # $signature        = $this->_sha1($httpmethod . '&' . $this->_url($method) . '&' . $this->_url($sign_base_string));

        params = sign_base_params if append_to_get is True else oauth_params

        params['oauth_signature'] = signature
        # sign_base_params['oauth_signature'] = signature
        # params = sign_base_params

        authorization = []
        if append_to_get is True:
            for value in sorted(params.items()):
                authorization.append(value[0] + '="' + self._url(value[-1]) + '"')
            return ', '.join(authorization)

        for value in sorted(params.items()):
            authorization.append(value[0] + '="' + self._url(value[-1]) + '"')

        authorization = 'OAuth ' + ', '.join(authorization)

        return authorization

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
        @see https://gist.github.com/kennethreitz/973705
        urllib.request()...
        """
        try:
            user = 'user'
            paswd = 'pass'

            r = requests.get('https://api.github.com', auth=(user, paswd))

            data = r.content.decode()
            # data = r.text
            print(r.status_code)
            print(r.headers['content-type'])
            print(data)

        except Exception as e:
            print("ERROR :: ", e)
