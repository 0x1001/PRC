################################################################################
################################### Constants ##################################
################################################################################
PRC_ROOT = "PRC_ROOT"
PRC_NEW_SESSION = "PRC_NEW_SESSION"
PRC_DATA = "PRC_DATA"
PRC_CONFIRM = "PRC_CONFIRM"
################################################################################
################################### Classes ####################################
################################################################################
import prcexception
import xml.etree.ElementTree as ET

class ProtocolException(prcexception.PRCException): pass

################################################################################
############### Functions Encode / Decode ######################################
################################################################################

def client_new_session(new_session):
    """
        Encodes new session

        Input:
        new_session     - New session id

        Returns:
        encoded data
    """
    root = _root()
    ET.SubElement(root,PRC_NEW_SESSION).set(PRC_DATA,_encode(new_session))

    return ET.tostring(root,encoding="us-ascii",method="xml")

def server_new_session(data):
    """
        Decodes new session

        Input:
        Data        - Encoded data

        Returns:
        Session id
    """
    return _decode(ET.fromstring(data)[0].get(PRC_DATA))

def confirm():
    """
        Confirmation

        Input:
        Nothing

        Returns:
        Confirmation data
    """
    root = _root()
    ET.SubElement(root,PRC_CONFIRM)
    return ET.tostring(root,encoding="us-ascii",method="xml")

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
    import base64
    return base64.b64encode(data)

def _decode(data):
    """
        This function decodes data

        Input:
        data        - Encoded data

        Returns:
        data        - Decoded data
    """
    import base64
    return base64.b64decode(data)

def _root():
    """
        Returns root node

        Input:
        Nothing

        Returns:
        root node
    """
    return ET.Element(PRC_ROOT)

def analyze(data):
    """
        This function analyzes data

        Input:
        data

        Retruns:
        data signature
    """
    try:
        root = ET.fromstring(data)
    except ET.ParseError as error:
        raise ProtocolException(str(error))
    if root.tag != PRC_ROOT: raise ProtocolException("Root tag does not match! " + root.tag)

    return root[0].tag
