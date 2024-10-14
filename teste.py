import xml.etree.ElementTree as ET
tree = ET.parse('tst.svg')
root = tree.getroot()
a = root.getchildren()
b = root.items()
g = ET.SubElement(root, 'g')
r = ET.SubElement(g, 'rect')
x = root.attrib
pass