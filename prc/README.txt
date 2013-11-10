===
PRC
===

**Python Remote Console - PRC**

Python Remote Console client and server communicate via sockets. PRCClient connects to PRCServer and gains access to its Python console.
Everything what PRCClient types is sent and executed on PRCServer.

This can have several applications including:

- Access to remote machine resources like files on hard drives, computation power.
- Runtime debugging of complex Python scripts. PRCServer can be configured to access script internal variables, objects, states.
- Remote Procedure Call (RPC). PRCClient can remotely start processes, applications, other executables on PRCServer.

PRCServer usage example
-----------------------
PRCServer runs socket server that spawns Python console for each PRCClient.

example_server.py::
    
    from prc import PRCServer
    import time

    # Creates PRCServer object
    server = PRCServer()

    # Example of a mutable variable
    counter = [0]

    # This will allow access to counter variable in PRC
    server.add_variable("counter",counter)

    # Starts PRCServer. Non blocking!
    server.start()

    # Example of worker thread that increments counter
    while True:
        counter[0] += 1
        time.sleep(1)

PRCClient usage example
-----------------------
PRCClient connects to PRCServer console and acts as a proxy.

example_client.py::
    
    from prc import PRCClient

    # Starts PRCClient
    #
    # Only stderr is redirected to RPCClient output
    # To redirect stdout type following code in PRCClient console:
    #   import sys
    #   sys.stdout = __prcconsole__
    #
    # Type exit() for exit.
    PRCClient().start()
    
PRCClient client console looks like this::
    
    Python 2.7.3 (default, Apr 10 2012, 23:31:26) [MSC v.1500 32 bit (Intel)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    (PRCConsole)

    >>> import sys
    >>> sys.stdout = __prcconsole__
    >>> counter
    [62]

    >>> counter
    [64]
    
    >>> import subprocess
    >>> subprocess.call("start notepad",shell=True)
    >>> exit()
    
PRCClient constructor accepts two input paramiters: server address and port.

Contribution
------------
Anyone is welcome to contribute to this project. Source code is available on GitHub.
https://github.com/0x1001/PRC

