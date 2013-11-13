import unittest
import prc

class PRCBasicTest(unittest.TestCase):
    def setUp(self):
        try: self.server = prc.PRCServer()
        except prc.PRCServer as error: self.fail("Init Error" + str(error))

        try: self.server.start()
        except prc.PRCServer as error: self.fail("Start Error" + str(error))

    def tearDown(self):
        try: self.server.stop()
        except prc.PRCServer as error: self.fail("Stop Error" + str(error))

        del(self.server)

    def test_PRCClient(self):
        client = prc.PRCClient()
        client._start_session()
        with self.assertRaises(SystemExit):
            client._sendConsoleInput("exit()")

if __name__ == '__main__':
    unittest.main()