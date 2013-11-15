import code
import prc
################################################################################
############################## Classes #########################################
################################################################################
class PRCClientException(prc.PRCException): pass

class PRCClient(object):
    """
        This class is main Client class.
        It is responsible for communication with PRCServer

        Variables:
        _session_id             - Client session id
        _ip                     - Server ip address
        _port                   - Server port
        _exit                   - Exit Event
    """
    def __init__(self,ip=None,port=None):
        from comm import getHostName
        import time
        import threading
        import prcserver

        self._session_id = getHostName() + "_" + str(time.time()).replace(".","")

        self._ip = ip if ip else getHostName()
        self._port = port if port else prcserver.DEFAULT_PORT

        self._exit = threading.Event()

    def start(self):
        """
            This function starts RPCClient

            Input:
            Nothing

            Returns:
            Nothing
        """
        self._start_session()
        self._input()

    def _start_session(self):
        """
            This function starts PRC session

            Input:
            Nothing

            Returns:
            Nothing
        """
        from comm import protocol, sendAndReceive, CommClientException

        try: sendAndReceive(self._ip,self._port,protocol.frame(prc.PRC_NEW_SESSION,self._session_id))
        except CommClientException as error: raise PRCClientException("Connection problem: " + str(error))
        self._receiveConsoleOutput()

    def _prompt(self):
        """
            This function gets prompt from server

            Input:
            Nothing

            Returns:
            prompt
        """
        from comm import protocol, sendAndReceive, CommClientException

        try: frame = sendAndReceive(self._ip,self._port,protocol.frame(prc.PRC_PROMPT,self._session_id))
        except CommClientException as error: raise PRCClientException("Connection problem: " + str(error))
        cmd,prompt = protocol.analyze(frame)

        return prompt

    def _input(self):
        """
            This function handles user input

            Input:
            Nothing

            Returns:
            Nothing
        """
        while not self._exit.is_set(): self._sendConsoleInput(raw_input(self._prompt()))


    def _sendConsoleInput(self,data):
        """
            This function sends command.
            Blocking funnction.

            Input:
            data        - Input python command

            Returns:
            Nothing
        """
        from comm import protocol, sendAndReceive, CommClientException
        import threading

        console_output_exit = threading.Event()
        console_output_thread = threading.Thread(target=self._receiveConsoleOutputThread,args=(console_output_exit,))
        console_output_thread.start()

        try: frame = sendAndReceive(self._ip,self._port,protocol.frame(prc.PRC_CODE,(self._session_id,data)))
        except CommClientException as error: raise PRCClientException("Connection problem: " + str(error))
        finally: console_output_exit.set()

        console_output_thread.join()
        cmd,data = protocol.analyze(frame)

        if cmd == prc.PRC_EXIT: raise SystemExit

    def _receiveConsoleOutput(self):
        """
            This function receives and prints console output

            Input:
            Nothing

            Returns:
            Nothing
        """
        from comm import protocol, sendAndReceive, CommClientException

        try: frame = sendAndReceive(self._ip,self._port,protocol.frame(prc.PRC_OUTPUT,self._session_id))
        except CommClientException as error: raise PRCClientException("Connection problem: " + str(error))

        cmd,data = protocol.analyze(frame)
        if data: print data

    def _receiveConsoleOutputThread(self,console_output_exit):
        """
            This function polls for console output

            Input:
            console_output_exit     - Console exit event

            Returns:
            Nothing
        """
        while True:
            self._receiveConsoleOutput()

            if console_output_exit.wait(1):
                self._receiveConsoleOutput()
                break