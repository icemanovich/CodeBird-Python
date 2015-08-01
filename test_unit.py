__author__ = 'ignat'
__project__ = 'PyBird'


import unittest
from tests import TestMainModule


if __name__ == "__main__":

    suite = unittest.TestLoader().loadTestsFromModule(TestMainModule)
    unittest.TextTestRunner().run(suite)
