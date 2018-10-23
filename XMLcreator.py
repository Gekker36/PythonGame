import xml.etree.ElementTree as ET

tree = ET.ElementTree()
root = ET.Element("root")  
items = ET.SubElement(root, 'items') 

# item = ET.SubElement(items, 'item')


# itemID = ET.SubElement(item, 'itemID').text = '01'  
# itemName = ET.SubElement(item, 'itemName').text = 'Sword'
# itemValue = ET.SubElement(item, 'itemValue').text = '100'  
id=1
 


def create_item(name, value = 0, stackSize = 1):
    global id
    item = ET.SubElement(items, 'item')
    itemID = ET.SubElement(item, 'itemID').text = str(id)
    itemName = ET.SubElement(item, 'name').text = str(name)
    value = ET.SubElement(item, 'value').text = str(value) 
    stackSize = ET.SubElement(item, 'stackSize').text = str(stackSize) 
    id +=1

    

create_item('Sword',100)
create_item('Shield',90)




# mydata = ET.tostring(data, encoding='utf8').decode('utf8')
tree = ET.ElementTree(root)
tree.write('output.xml')
