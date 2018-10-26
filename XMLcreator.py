import xml.etree.ElementTree as ET

tree = ET.ElementTree()
root = ET.Element("root")  
items = ET.SubElement(root, 'items') 


id=1

def create_item(**kwargs):
    global id
    
    item = ET.SubElement(items, 'item')
    ET.SubElement(item, 'itemID').text = str(id)
    for key, value in kwargs.items():
        ET.SubElement(item, key).text = str(value)
    
    id +=1

    
    
    

create_item(name='Sword', value =100 )
create_item(name='Shield',value =90)
create_item(name='Potion', value = 10)


tree = ET.ElementTree(root)
tree.write('output.xml')
