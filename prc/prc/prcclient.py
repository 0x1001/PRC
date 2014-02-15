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
        _output_thread          - Output thread reference
    """
    def __init__(self,ip="127.0.0.1",port=prc.DEFAULT_PORT):
        from comm import getHostName
        import time
        import threading

        self._ip = ip
        self._port = port

        self._session_id = getHostName() + "_" + str(time.time()).replace(".","")

        self._output_thread = threading.Thread(target=self._receiveConsoleOutput)
        self._output_thread.daemon = True

        self._input_thread = threading.Thread(target=self._input)
        self._input_thread.daemon = True

        self._exit = threading.Event()
        self._synch = threading.Semaphore(0)

    def start(self):
        """
            This function starts RPCClient

            Input:
            Nothing

            Returns:
            Nothing
        """
        self._start_session()
        self._output_thread.start()
        self._input_thread.start()

        while True:
            if self._exit.wait(0.2): break

    def _start_session(self):
        """
            This function starts PRC session

            Input:
            Nothing

            Returns:
            Nothing
        """
        from comm import protocol, sendAndReceive, CommClientException

        try:
            sendAndReceive(self._ip,self._port,protocol.frame(prc.PRC_NEW_SESSION,self._session_id))
        except CommClientException as error:
            self._exit.set()
            raise PRCClientException("Connection problem: " + str(error))

    def _input(self):
        """
            This function handles user input (client input)

            Input:
            Nothing

            Returns:
            Nothing
        """
        while not self._exit.is_set(): self._sendConsoleInput(raw_input(self._prompt()))

    def _prompt(self):
        """
            This function gets prompt from server

            Input:
            Nothing

            Returns:
            prompt
        """
        from comm import protocol, sendAndReceive, CommClientException

        try:
            frame = sendAndReceive(self._ip,self._port,protocol.frame(prc.PRC_PROMPT,self._session_id))
        except CommClientException as error:
            self._exit.set()
            raise PRCClientException("Connection problem: " + str(error))

        cmd,prompt = protocol.analyze(frame)

        self._synch.acquire()

        return prompt

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

        try:
            frame = sendAndReceive(self._ip,self._port,protocol.frame(prc.PRC_CODE,(self._session_id,data)))
        except CommClientException as error:
            self._exit.set()
            raise PRCClientException("Connection problem: " + str(error))

        self._synch.acquire()

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
        import sys
        from comm import protocol, sendAndReceive, CommClientException

        while True:
            if self._exit.is_set(): break

            try:
                frame = sendAndReceive(self._ip,self._port,protocol.frame(prc.PRC_OUTPUT,self._session_id))
            except CommClientException as error:
                self._exit.set()
                raise PRCClientException("Connection problem: " + str(error))

            cmd,data = protocol.analyze(frame)
            if cmd == prc.PRC_OUTPUT:
                sys.stdout.write(data)
            elif cmd == prc.PRC_CONFIRM:
                self._synch.release()
            elif cmd == prc.PRC_EXIT:
                self._synch.release()
                self._exit.set()
