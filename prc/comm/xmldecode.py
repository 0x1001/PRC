import xmlcoder

######################################################################################
################################### Classes ##########################################
######################################################################################

class XmlDecodeException(xmlcoder.XMLCoderException): pass

class XmlDecode(xmlcoder.XMLCoder):
    """
        This class is resposible for decoding xml
        for communication

        Exmaple:
            <?xml version="1.0" ?>
            <Example>
            <Node1 attribute1="YXR0cjE=" attribute2="YXR0cjI="/>
            <Node2 attribute3="YXR0cjM="/>
            <Node3><Node4/><Node5/><Node6/>
            </Node3>
            </Example>

        Can be decoded like this:
        frame = XmlDecode(xml_data)
        frame.getChildNode()                # Returns "Example"
        frame.getChildNode()                # Returns "Node1"
        frame.getAttribute("attribute1")    # Returns "attr1"
        frame.getAttribute("attribute2")    # Returns "attr2"
        frame.getBrotherNode()              # Returns "Node2"
        frame.getBrotherNode()              # Returns "Node3"
        frame.getChildNode()                # Returns "Node4"

        Note: All attributes are encoded if self.ENCODE_DATA is True

        Variables:
        dom             - DOM object
        root            - Root of current node
        current         - current node

        node_index      - Current node index
        root_node_index - Root node index
    """

    def __init__(self,data):
        import xml
        from xml.dom.minidom import parseString

        if not isinstance(data,str): raise XmlDecodeException("Input data is not string")

        try:
            self.dom = parseString(data)
        except xml.parsers.expat.ExpatError as error:
            raise XmlDecodeException(str(error))

        self.node_index = 0
        self.root_node_index = 0
        self.root = self.dom
        self.current = self.dom

    def getChildNode(self):
        """
            This function retrives first child node of current node
            It also changes current node to this retrived child node

            Input:
            Nothing

            Returns:
            Name of retrived child node
        """
        self.root_node_index = self.node_index
        self.node_index = 0
        nodes = self.current._get_childNodes()
        self.root = self.current
        self.current = nodes[self.node_index]
        self.node_index += 1
        return self.current.tagName

    def getParentNode(self):
        """
            This function retrives parent of current node
            It also changes current node to this retrived parent node

            Input:
            Nothing

            Returns:
            Name of retrived parrent node
        """
        self.node_index = self.root_node_index
        self.root = self.root.parentNode
        self.current = self.current.parentNode
        return self.current.tagName

    def getBrotherNode(self):
        """
            This function retrives brother node to current node
            It also changes current node to this retrived brother node

            Input:
            Nothing

            Returns:
            Name of retrived brother node
        """
        nodes = self.root._get_childNodes()
        if len(nodes) == self.node_index: return None
        self.current = nodes[self.node_index]
        self.node_index += 1
        return self.current.tagName

    def getAttribute(self,name):
        """
            This function retrives attribute value from current node

            Input:
            name    - attribute name

            Returns:
            Attribute value
        """
        data = self.current.getAttribute(name)

        if data == "":
            return data
        else:
            return self._decompress(self._b64Decode(data))
