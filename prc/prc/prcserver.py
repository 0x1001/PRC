import code
import prc
import SocketServer
################################################################################
############################## Constants #######################################
################################################################################
DEFAULT_PORT = 49988

################################################################################
############################## Classes #########################################
################################################################################
class PRCServerException(prc.PRCException): pass

class PRCServer(object):
    """
        This is main PRCServer class

        Variables:
        _comm_server            - Socket server
        _comm_server_thread     - Communication Thread
    """
    def __init__(self,ip=None,port=None):
        from comm import server_factory
        from comm import CommServerException
        import threading

        ip = ip if ip else ""
        port = port if port else DEFAULT_PORT

        try: self._comm_server = server_factory(ip,port,request_handler,PRCSocketServer)
        except CommServerException as error: raise PRCServerException(error)

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
        self._comm_server_thread.join()

    def add_variable(self,name,value):
        """
            This function adds locals for PRCConsole

            Input:
            name        - Variable name
            value       - Variable value

            Returns:
            Nothing
        """
        self._comm_server.add_local_variable(name,value)

class PRCConsole(code.InteractiveConsole):
    """
        Console class. Runs interact function in thread

        Variables:
        _input_queue            - Input command queue
        _output_queue           - Output data queue
        _prompt                 - Current prompt
        _code_executed          - Code executed by interpreter event
        _prompt_ready           - Prompt ready event
        _exit                   - Exit event
    """
    def __init__(self,locals={}):
        import Queue
        import threading

        locals["__prcconsole__"] = self
        locals["__name__"] = "__prcconsole__"
        locals["__doc__"] = "Python Remote Console"

        code.InteractiveConsole.__init__(self,locals,filename="<PRCConsole>")

        self._input_queue = Queue.Queue()
        self._output_queue = Queue.Queue()

        self._prompt = None
        self._code_executed = threading.Event()
        self._prompt_ready = threading.Event()
        self._exit = threading.Event()

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
        self._prompt = prompt
        self._prompt_ready.set()
        return self._input_queue.get()

    def get_input_queue(self):
        """
            Returns input queue

            Input:
            Nothing

            Returns:
            Queue
        """
        return self._input_queue

    def get_output_queue(self):
        """
            Returns input queue

            Input:
            Nothing

            Returns:
            Queue
        """
        return self._output_queue

    def get_prompt(self):
        """
            This function returns current prompt

            Input:
            Nothing

            Returns:
            prompt
        """
        self._prompt_ready.wait()
        return self._prompt

    def write(self,data):
        """
            Write output function

            Input:
            data        - Data to write

            Returns:
            Nothing
        """
        self._output_queue.put(data)

    def wait_for_code(self):
        """
            This function waits for code to be executed on server

            Input:
            Nothing

            Returns:
            Nothing
        """
        self._code_executed.wait()
        self._code_executed.clear()

    def push(self,*args,**kargs):
        """
            Adding synchronization elements

            Input:
            Nothing

            Returns:
            Nothing
        """
        try: return_value = code.InteractiveConsole.push(self,*args,**kargs)
        except SystemExit:
            self._exit.set()
            raise
        finally: self._code_executed.set()

        return return_value

    def is_system_exit(self):
        """
            Checks if console is exited

            Input:
            Nothing

            Returns:
            True/False
        """
        return self._exit.is_set()

class PRCSocketServer(SocketServer.ThreadingTCPServer):
    """
        PRC socket server with support for consoles.

        Variables:
        _consoles       - Dictionary with consoles
        _consoles_lock  - Lock for consoles dictonary
        _locals         - Custom locals for PRCConsole
    """
    def __init__(self,*args,**kargs):
        import threading

        SocketServer.ThreadingTCPServer.__init__(self,*args,**kargs)
        self._consoles = {}
        self._consoles_lock = threading.RLock()
        self._locals = {}

    def add_local_variable(self,name,value):
        """
            This function adds locals for PRCConsole

            Input:
            name        - Variable name
            value       - Variable value

            Returns:
            Nothing
        """
        self._locals[name] = value

    def add_console(self,session_id):
        """
            Adds new console

            Input:
            session_id       - Client ID

            Returns:
            Nothing
        """
        with self._consoles_lock: self._consoles[session_id] = PRCConsole(self._locals)

    def remove_console(self,session_id):
        """
            Removes client console

            Input:
            session_id       - Client ID

            Returns:
            Nothing
        """
        with self._consoles_lock: self._consoles.pop(session_id)

    def get_console(self,session_id):
        """
            Gets client console

            Input:
            session_id       - Client ID

            Returns:
            Console
        """
        with self._consoles_lock: return self._consoles[session_id]

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
    from comm import protocol
    import Queue

    recv_frame = request.receive()

    cmd,data = protocol.analyze(recv_frame)

    if cmd == prc.PRC_NEW_SESSION:
        request.server.add_console(data)
        send_frame = protocol.frame(prc.PRC_CONFIRM)

    elif cmd == prc.PRC_OUTPUT:
        output_queue = request.server.get_console(data).get_output_queue()
        output = []
        while True:
            try: output.append(output_queue.get(False))
            except Queue.Empty: break

        if output != []: send_frame = protocol.frame(prc.PRC_OUTPUT,"".join(output))
        else: send_frame = protocol.frame(prc.PRC_OUTPUT)

    elif cmd == prc.PRC_PROMPT:
        prompt = request.server.get_console(data).get_prompt()
        send_frame = protocol.frame(prc.PRC_PROMPT,prompt)

    elif cmd == prc.PRC_CODE:
        session_id, code = data
        request.server.get_console(session_id).get_input_queue().put(code)
        request.server.get_console(session_id).wait_for_code()

        if request.server.get_console(session_id).is_system_exit():
            send_frame = protocol.frame(prc.PRC_EXIT)
        else:
            send_frame = protocol.frame(prc.PRC_CONFIRM)

    else:
        raise PRCServerException("Not implemented! " + str(cmd))

    request.send(send_frame)
    request.close()
