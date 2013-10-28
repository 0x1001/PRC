import xmlcoder
######################################################################################
################################### Classes ##########################################
######################################################################################

class XmlEncodeException(xmlcoder.XMLCoderException): pass

class XmlEncode(xmlcoder.XMLCoder):
    """
        This class is resposible for encoding xml
        RR communication

        Example:
            frame = XmlEncode()
            frame.addChildNode("Example")
            frame.addChildNode("Node1")
            frame.addAttribute("attribute1","attr1")
            frame.addAttribute("attribute2","attr2")
            frame.addBrotherNode("Node2")
            frame.addAttribute("attribute3","attr3")
            frame.addBrotherNode("Node3")
            frame.addChildNode("Node4")
            frame.addBrotherNode("Node5")
            frame.addBrotherNode("Node6")
            print frame.toXml()

            This will create:
            <?xml version="1.0" ?>
            <Example>
            <Node1 attribute1="YXR0cjE=" attribute2="YXR0cjI="/>
            <Node2 attribute3="YXR0cjM="/>
            <Node3><Node4/><Node5/><Node6/>
            </Node3>
            </Example>

            Note: All attributes are encoded in Base64 if self.ENCODE_DATA is True
        Variables:
        dom         - DOM object
        root        - Root of current node
        current     - Current node
    """

    def __init__(self):
        from xml.dom.minidom import Document

        self.dom = Document()
        self.current = self.dom
        self.root = self.dom

    def toXml(self):
        """
            This function converts XML DOM object to XML

            Input:
            Nothing

            Returns
            XML string
        """
        return self.dom.toxml()

    def addChildNode(self,tag_name):
        """
            This function creates child node in current node.
            After new node is created, current node is set to it.

            Input:
            tag_name    - Child node name

            Returns:
            Nothing
        """
        new_node = self.dom.createElement(tag_name)
        self.current.appendChild(new_node)
        self.root = self.current
        self.current = new_node

    def addParentNode(self,tag_name):
        """
            This function creates parent node in relation to current node.
            After new node is created, current node is set to it.

            Input:
            tag_name    - Parent node name

            Returns:
            Nothing
        """
        new_node = self.dom.createElement(tag_name)
        self.root.parentNode.appendChild(new_node)
        self.current = new_node

    def addBrotherNode(self,tag_name):
        """
            This function creates brother node to current node.
            After new node is created, current node is set to it.

            Input:
            tag_name    - Brother node name

            Returns:
            Nothing
        """

        new_node = self.dom.createElement(tag_name)
        self.root.appendChild(new_node)
        self.current = new_node

    def addAttribute(self,attribute,value):
        """
            This function adds new attribute to current node

            Input:
            attribute   - attribute name
            value       - attribute value

            Returns:
            Nothing
        """
        if not isinstance(value,str) and not isinstance(value,unicode): raise XmlEncodeException(attribute + " is not string")
        if value == "":
            self.current.setAttribute(attribute,value)
        else:
            self.current.setAttribute(attribute,self._b64Code(self._compress(value)))
