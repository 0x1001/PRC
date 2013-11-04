import code
import prcexception
################################################################################
############################## Classes #########################################
################################################################################
class PRCClientException(prcexception.PRCException): pass

class PRCClient(object):
    """
        This class is main Client class.
        It is responsible for communication with PRCServer

        Variables:
        _session_id             - Client session id
        _ip                     - Server ip address
        _port                   - Server port
        _console_output_thread  - Console output thread
    """
    def __init__(self,ip=None,port=None):
        from comm import getHostName
        import time
        import threading
        import prcserver

        self._session_id = getHostName() + "_" + str(time.time()).replace(".","")

        self._ip = ip if ip else getHostName()
        self._port = port if port else prcserver.DEFAULT_PORT

        self._console_output_thread = threading.Thread(target=self._receiveConsoleOutput)

    def start(self):
        """
            This function starts RPCClient

            Input:
            Nothing

            Returns:
            Nothing
        """
        self._start_session()
        self._console_output_thread.start()

        self._input()

    def _start_session(self):
        """
            This function starts PRC session

            Input:
            Nothing

            Returns:
            Nothing
        """
        import protocol
        from comm import sendAndReceive

        sendAndReceive(self._ip,self._port,protocol.client_new_session(self._session_id))

    def _input(self):
        """
            This function handles user input

            Input:
            Nothing

            Returns:
            Nothing
        """
        while True: self._sendConsoleInput(raw_input())

    def _sendConsoleInput(self,data):
        """
            This function sends command.
            Blocking funnction.

            Input:
            data        - Input python command

            Returns:
            Nothing
        """
        from comm import sendAndReceive

        sendAndReceive(self._ip,self._port,data)

    def _receiveConsoleOutput(self):
        """
            This function polls for console output

            Input:
            ip          - Server address
            port        - Server port

            Returns:
            Nothing
        """
        #while True: print ""