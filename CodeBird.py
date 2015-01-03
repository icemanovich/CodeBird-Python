# coding=utf-8
import pycurl
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


    # /**
    #  * The OAuth consumer key of your registered app
    #  */
    # protected static $_oauth_consumer_key = null
    # /**
    #  * The corresponding consumer secret
    #  */
    # protected static $_oauth_consumer_secret = null
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
        except ImportError as e:
            self._use_curl = False

    def grt_version(self):
        return self._version

    def set_timeout(self, timeout):
        self._timeout = int(timeout)

    def set_connection_timeout(self, timeout):
        self._connectionTimeout = int(timeout)


    def _call_api_curl(self, httpmethod="Get", method='', params=None, multipart=False, app_only_auth=False, internal=False):
        """
        Calls the API using cURL
        :param string          httpmethod    The HTTP method to use for making the request (Get or Post)
        :param string          method        The API method to call
        :param array  optional params        The parameters to send along
        :param bool   optional multipart     Whether to use multipart/form-data
        :param bool   optional app_only_auth Whether to use app-only bearer authentication
        :param bool   optional internal      Whether to use internal call
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

            request_headers = ''
            url = 'http://ya.ru'


            buffer = BytesIO()
            c = pycurl.Curl()

            if httpmethod.lower() is not "get":
                c.setopt(pycurl.POST, 1)
                c.setopt(pycurl.POSTFIELDS, params)

            c.setopt(pycurl.URL, url)

        # request_headers[] = 'Authorization: ' . $authorization;
        # request_headers[] = 'Expect:';

            if self._timeout is not None:
                c.setopt(self._CURLOPT_TIMEOUT_MS, self._timeout)

            if self._connectionTimeout is not None:
                c.setopt(self._CURLOPT_CONNECTTIMEOUT_MS, self._connectionTimeout)

            c.setopt(pycurl.FOLLOWLOCATION, 0)
            c.setopt(pycurl.HEADER, 1)
            c.setopt(pycurl.HTTPHEADER, request_headers)
            c.setopt(pycurl.SSL_VERIFYPEER, 1)
            c.setopt(pycurl.SSL_VERIFYHOST, 2)
            # c.setopt(pycurl.CAINFO, __DIR__ . '/cacert.pem')
            c.setopt(pycurl.WRITEDATA, buffer)
            c.perform()
            code = c.getinfo(c.RESPONSE_CODE)
            print("CODE [%s] :: Time [%s]" % (code, c.getinfo(c.TOTAL_TIME)))
            c.close()
            return buffer.getvalue().decode()
        except Exception as e:
            print("ERROR :: ", e)



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




if __name__ == '__main__':
    print("Start")

    curl = CodeBird().make_curl()
    print("\nOUT :: ", curl)
