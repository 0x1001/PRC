import code
import prcexception
################################################################################
############################## Classes #########################################
################################################################################
class PRCException(prcexception.PRCException): pass

class PRCServer(object):
    """
        This is main PRCServer class

        Variables:
        _input_queue        - Input queue for interpreter commands
        _output_queue       - Output queue for commands output
        _console_thread     - Console Thread
        _comm_server        - Socket server
        _comm_server_thread - Communication Thread

    """
    def __init__(self):
        import Queue
        from comm import CommServer

        self._input_queue = Queue.Queue()
        self._output_queue = Queue.Queue()

        console = Console()
        console.set_inout_queues(self._input_queue,self._output_queue)
        self._console_thread = threading.Thread(target=console.interact)
        self._console_thread.daemon = True

        self._comm_server = _setup_commserver()
        self._comm_server_thread = threading.Thread(target=self._comm_server.serve_forever)
        self._comm_server_thread.daemon = True

    def _setup_commserver(self):
        """
            Prepares CommServer

            Input:
            Nothing

            Returns:
            Nothing
        """
        from comm import CommServer
        import socket
        import SocketServer

        class Handler(CommServer): pass

        SocketServer.ThreadingTCPServer.request_queue_size=3
        try:
            server_handle = SocketServer.ThreadingTCPServer((ip,port),Handler)
        except socket.error as error:
            raise CommServerException(str(error))

        return server_handle

    def start(self):
        """
            Starts server

            Input:
            Nothing

            Returns:
            Nothing
        """
        self._console_thread.start()
        self._comm_server_thread.start()

class Console(code.InteractiveConsole):
    """
        Console class

        Variables:
        _input_queue            - Input command queue
        _output_queue           - Output data queue

    """
    def raw_input(self,prompt=None):
        """
            Raw input for interpreter

            Input:
            data        - Input python code string

            Returns:
            data
        """
        return self._input_queue.get()

    def set_inout_queues(self,input_queue,output_queue):
        """
            Sets input and output queue

            Input:
            input_queue         - Input command queue
            output_queue        - Output data queue

            Returns:
            Nothing
        """
        self._input_queue = input_queue
        self._output_queue = output_queue

    def write(self,data):
        """
            Write output function

            Input:
            data        - Data to write

            Returns:
            Nothing
        """
        self._output_queue.put(data)

################################################################################
############################## Functions #######################################
################################################################################
