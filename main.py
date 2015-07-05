__author__ = 'ignat'

from CodeBird import CodeBird



if __name__ == '__main__':
    print("Start")

    # consumer_key = 'oLVqNUOVNERDtKfh9n3vW1LXd'
    # consumer_secret = 'uLd0zJDK0nwcjZMN7jg9YMIZVOOasrIWzjJ3BtS1ZR9TnCO5Zl'
    # access_token = '2578434163-0CPPrAKfg3OtrccnEBjiojvFzZUeWl8fYyJf2bF'
    # access_token_secret = '7Y5djMLVmVx0RUbCv7ojtIhI01AjZzSe4eEuuf1YKLpAL'
    consumer_key = 'bZx9BJxzEygTmxNSZLCyvzsCF'
    consumer_secret = '3Vl2ttSEN8hVJFsIdDNNvyyjapPc3yT08lZ6MM583iqcM5MKBP'
    access_token = '2541668575-MoLt0NwOLItRk03rUNymX6XbTqIgl1wpbaV6HOF'
    access_token_secret = 'eK3H05LGVIe02qNqJFzgoFuXXRYfDsKSeaKP88YevQeEI'




    # call Api test
    p_fn = 'application_rateLimitStatus'
    p_params = []
    cb = CodeBird()

    cb.make_no_curl()

    # TODO :: REMOVE
    # cb._use_curl = False

    # cb.set_consumer_key(consumer_key, consumer_secret)
    # cb.set_token(access_token, access_token_secret)
    # out = cb.application_rateLimitStatus()
    # print("OUT :: ", out)

    #
    # TODO :: Add setup.py
    #
