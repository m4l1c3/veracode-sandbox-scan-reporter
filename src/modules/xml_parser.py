from defusedxml import ElementTree as ET

class XmlParser(object):
    def __init__(self):
        return

    def parse_xml(self, xml_output):
        """
        Open and parse an xml file.
        @return xml_tree An xml tree instance. None if error.
        """
        try:
            tree = ET.fromstring(xml_output)
        except SyntaxError as se:
            raise se

        return tree