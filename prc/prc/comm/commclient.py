import comm

######################################################################################
################################### Classes ##########################################
######################################################################################

class CommClientException(comm.CommException): pass

class CommClient(comm.Comm):
    """
        This class is responsible for Client communication

        Constants:
        MAX_RETRY           - Max client retry if cannot connect to server
        CONNECTION_TIMEOUT  - Time between next connection attempt in case of connection interrupt

        Variables:
        socket_reference    - socket handle
        connection_attempt  - Number of connection retry
    """
    MAX_RETRY = 2
    CONNECTION_TIMEOUT = 2

    def __init__(self):
        self.open()
        self.connection_attempt = 1

    def connect(self,ip,port):
        """
            This function connects to ip on port.
            It retrys MAX_RETRY times.

            Variables:
            ip          - Ip address
            port        - port

            Returns:
            Nothing
        """
        import time
        import socket

        if self.connection_attempt > self.MAX_RETRY:
            raise CommClientException("Cannot connect to " + ip + ":" + str(port))

        try:
            self.socket_reference.connect((ip, port))
        except socket.error:
            self.connection_attempt += 1
            self.close()
            time.sleep(self.CONNECTION_TIMEOUT)
            reload(socket)
            self.open()
            self.connect(ip,port)

    def _lowLevelRecv(self,buffer):
        """
            Low level receive function.

            Input:
            buffer  - Buffer size

            Returns:
            Received data
        """
        return self.socket_reference.recv(buffer)

    def _lowLevelSend(self,data):
        """
            Low level send function.

            Input:
            data    - data to send

            Returns:
            Send data size
        """
        return self.socket_reference.send(data)

    def _lowLevelClose(self):
        """
            Low level close function.

            Input:
            Nothing

            Returns:
            Nothing
        """
        self.socket_reference.close()

    def _lowLevelOpen(self):
        """
            Low level open function.

            Input:
            Nothing

            Returns:
            Nothing
        """
        import socket
        self.socket_reference = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

######################################################################################
################################### Functions ########################################
######################################################################################

def sendAndReceive(ip,port,data_to_send,retry=None):
    """
        This function sends and receives frames from server

        Input:
        data_to_send    - frame to send

        Returns:
        Received data
    """
    connection = CommClient()
    if retry != None: connection.MAX_RETRY = retry
    connection.connect(ip,port)
    connection.send(data_to_send)
    data_received = connection.receive()
    connection.close()

    return data_received
