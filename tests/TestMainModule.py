__author__ = 'ignat'

import unittest
from CodeBird import CodeBird


class TestMainModule(unittest.TestCase):
    """
    :type cb: CodeBird
    """

    cb = None

    @classmethod
    def setUpClass(cls):
        cls.cb = CodeBird()

    @classmethod
    def tearDownClass(cls):
        cls.cb = None

    def test_keys(self):
        """
        Test OAuth keys setter

        :return:
        """

        cb = CodeBird()
        self.assertEqual(CodeBird._version, self.cb.get_version())

        consumer_key = 'bZx9BJxzEygTmxNSZLCyvzsCF'
        consumer_secret = '3Vl2ttSEN8hVJFsIdDNNvyyjapPc3yT08lZ6MM583iqcM5MKBP'
        access_token = '2541668575-MoLt0NwOLItRk03rUNymX6XbTqIgl1wpbaV6HOF'
        access_token_secret = 'eK3H05LGVIe02qNqJFzgoFuXXRYfDsKSeaKP88YevQeEI'

        cb.set_consumer_key(consumer_key, consumer_secret)
        self.assertEqual(cb._oauth_consumer_key, consumer_key)
        self.assertEqual(cb._oauth_consumer_secret, consumer_secret)

        cb.set_token(access_token, access_token_secret)
        self.assertEqual(cb._oauth_token, access_token)
        self.assertEqual(cb._oauth_token_secret, access_token_secret)

    def test_api_methods(self):
        """
        Implement data provider to test api methods
        """
        pass

    def test__nonce(self):
        """
        :exception Exception
        :return:
        """

        # default value
        hash_string = self.cb._nonce()
        self.assertEqual(len(hash_string), 8)

        length = 5
        hash_string = self.cb._nonce(length)
        self.assertEqual(len(hash_string), length)

        # expect Raise an Exception
        length = 0
        self.assertRaises(Exception, self.cb._nonce, length)



if __name__ == '__main__':
    unittest.main()
