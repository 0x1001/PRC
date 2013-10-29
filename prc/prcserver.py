import code
import prcexception
import SocketServer
################################################################################
############################## Constants #######################################
################################################################################
DEFAULT_PORT = 49988

################################################################################
############################## Classes #########################################
################################################################################
class PRCServerException(prcexception.PRCException): pass

class PRCServer(object):
    """
        This is main PRCServer class

        Variables:
        _comm_server            - Socket server
        _comm_server_thread     - Communication Thread
        _ip                     - Server address
        _port                   - Server port
    """
    def __init__(self,ip=None,port=None):
        from comm import getHostName
        from comm import server_factory

        self._ip = ip if ip else getHostName()
        self._port = port if port else DEFAULT_PORT

        try: self._comm_server = server_factory(self._ip,self._port,request_handler,PRCSocketServer)
        except comm.CommServerException as error: raise PRCServerException(error)

        self._comm_server_thread = threading.Thread(target=self._comm_server.serve_forever)
        self._comm_server_thread.daemon = True

    def start(self):
        """
            Starts server

            Input:
            Nothing

            Returns:
            Nothing
        """
        self._comm_server_thread.start()

    def stop(self):
        """
            Stops PRC Server

            Input:
            Nothing

            Returns:
            Nothing
        """
        self._comm_server.shutdown()

class Console(code.InteractiveConsole):
    """
        Console class. Runs interact function in thread

        Variables:
        _input_queue            - Input command queue
        _output_queue           - Output data queue
    """
    def __init__(self,*args,**kargs):
        import Queue

        super(Console,self).__init__(*args,**kargs)

        self._input_queue = Queue.Queue()
        self._output_queue = Queue.Queue()

        console_thread = threading.Thread(target=self.interact)
        console_thread.daemon = True
        console_thread.start()

    def raw_input(self,prompt=None):
        """
            Raw input for interpreter

            Input:
            prompt      - Python prompt string

            Returns:
            data
        """
        return self._input_queue.get()

    def get_input_queue(self,input_queue,output_queue):
        """
            Returns input queue

            Input:
            Nothing

            Returns:
            Queue
        """
        return self._input_queue

    def get_output_queue(self,input_queue,output_queue):
        """
            Returns input queue

            Input:
            Nothing

            Returns:
            Queue
        """
        return self._output_queue

    def write(self,data):
        """
            Write output function

            Input:
            data        - Data to write

            Returns:
            Nothing
        """
        self._output_queue.put(data)

class PRCSocketServer(SocketServer.ThreadingTCPServer):
    """
        PRC socket server with support for consoles.

        Variables:
        _consoles       - Dictionary with consoles
    """
    def __init__(self,*args,**kargs):
        import threading

        super(PRCSocketServer,self).__init__(*args,**kargs)
        self._consoles = {}
        self._consoles_lock = threading.RLock()

    def add_console(self,client_id):
        """
            Adds new console

            Input:
            client_id       - Client ID

            Returns:
            Nothing
        """
        with self._consoles_lock: self._consoles[client_id] = Console()

    def remove_console(self,client_id):
        """
            Removes client console

            Input:
            client_id       - Client ID

            Returns:
            Nothing
        """
        with self._consoles_lock: self._consoles.pop(client_id)

    def get_console(self,client_id):
        """
            Gets client console

            Input:
            client_id       - Client ID

            Returns:
            Console
        """
        with self._consoles_lock: return self._consoles[client_id]

################################################################################
############################## Functions #######################################
################################################################################

def request_handler(request):
    """
        Handles clients requestes

        Input:
        request     - Client request

        Returns:
        Nothing
    """
    #request.server.add_console(client_id)
    #request.server.remove_console(client_id)
    #console = request.server.get_console(client_id)
    #output_queue = console.get_output_queue()
    #input_queue = console.get_input_queue()

    # Requestes:
    #   Create new console for client_id
    #   Execute commands for client_id
    #   Sends output string continuously for client_id
