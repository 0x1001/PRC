from .. import pdcexception

######################################################################################
################################### Classes ##########################################
######################################################################################

class XMLCoderException(pdcexception.PDCException): pass

class XMLCoder(object):
    """
        This class is resposible for common xml coder
        functions and constants for communication

        Constants:
        ENCODE_DATA     - If set to True all data will be encoded
    """

    ENCODE_DATA = True
    COMPRESS_DATA = True

    def _b64Code(self,data):
        """
            This function codes string to base64 string.

            Input:
            data    - input string

            Returns:
            Encoded string
        """
        if self.ENCODE_DATA == True:
            return data.encode('base64')
        else:
            return data

    def _b64Decode(self,data):
        """
            This function decodes base64 string to normal string

            Input:
            data    - base64 string

            Returns:
            Decoded string
        """
        if self.ENCODE_DATA == True:
            return data.decode('base64')
        else:
            return data

    def _compress(self,data):
        """
            This function compresses data

            Input:
            data    - Data to be compressed

            Return:
            Compressed data
        """
        if self.COMPRESS_DATA == True:
            return data.encode('zip')
        else:
            return data

    def _decompress(self,data):
        """
            This function decompresses data

            Input:
            data    - Data to be decompressed

            Return:
            decompressed data
        """
        import zlib

        if self.COMPRESS_DATA == True:
            try:
                return data.decode('zip')
            except zlib.error as error:
                raise XMLCoderException(str(error))
        else:
            return data