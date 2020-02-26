################################################################################
################################### Classes ####################################
################################################################################
from future import standard_library
import base64
import pickle
    
standard_library.install_aliases()


class ProtocolException(Exception): 
    pass

    
################################################################################
############### Functions Encode / Decode ######################################
################################################################################
def frame(cmd, data=None):
    """
        This function creates protocol frame

        Input:
        cmd     - Command
        data    - Data associated with command

        Returns:
        protocol_data       - Protocol frame
    """
    return _encode((cmd, data))

def analyze(frame):
    """
        This function analyzes protocol frame

        Input:
        frame

        Retruns:
        command, data
    """
    return _decode(frame)

################################################################################
############################## Functions #######################################
################################################################################

def _encode(data):
    """
        This function encodes data

        Input:
        data        - Data to encode

        Returns:
        data        - Encoded data
    """
    return base64.b64encode(pickle.dumps(data))

def _decode(data):
    """
        This function decodes data

        Input:
        data        - Encoded data

        Returns:
        data        - Decoded data
    """
    return pickle.loads(base64.b64decode(data))
