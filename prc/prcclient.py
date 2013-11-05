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
        from comm import protocol
        import prc
        from comm import sendAndReceive

        sendAndReceive(self._ip,self._port,protocol.frame(prc.PRC_NEW_SESSION,self._session_id))

    def _prompt(self):
        """
            This function gets prompt from server

            Input:
            Nothing

            Returns:
            prompt
        """
        from comm import protocol
        import prc
        from comm import sendAndReceive

        frame = sendAndReceive(self._ip,self._port,protocol.frame(prc.PRC_PROMPT,self._session_id))
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
        while True: self._sendConsoleInput(raw_input(self._prompt()))

    def _sendConsoleInput(self,data):
        """
            This function sends command.
            Blocking funnction.

            Input:
            data        - Input python command

            Returns:
            Nothing
        """
        from comm import protocol
        import prc
        from comm import sendAndReceive

        sendAndReceive(self._ip,self._port,protocol.frame(prc.PRC_CODE,(self._session_id,data)))

    def _receiveConsoleOutput(self):
        """
            This function polls for console output

            Input:
            ip          - Server address
            port        - Server port

            Returns:
            Nothing
        """
        from comm import protocol
        import prc
        from comm import sendAndReceive
        import time

        while True:
            frame = sendAndReceive(self._ip,self._port,protocol.frame(prc.PRC_OUTPUT,self._session_id))
            cmd,data = protocol.analyze(frame)
            if data != "": print data

            time.sleep(1)