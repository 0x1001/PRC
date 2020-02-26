from builtins import str
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import prc

class PRCBasicTest(unittest.TestCase):
    def setUp(self):
        try: 
            self.server = prc.PRCServer()
        except prc.PRCServer as error: 
            self.fail("Init Error" + str(error))

        try: 
            self.server.start()
        except prc.PRCServer as error: 
            self.fail("Start Error" + str(error))

    def tearDown(self):
        try: 
            self.server.stop()
        except prc.PRCServer as error: 
            self.fail("Stop Error" + str(error))

    def test_PRCClient(self):
        client = prc.PRCClient()
        client._exit.set()
        client.start()

if __name__ == '__main__':
    unittest.main()
