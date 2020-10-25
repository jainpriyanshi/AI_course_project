from xml.etree import ElementTree
import os
import csv

postfiles = ['AI','AImeta','ComputerGraphic','ComputerGraphicmeta','CS','CSmeta','DataScience','DataSciencemeta']
count = 0
for each_file in postfiles:
    tree = ElementTree.parse('xml/'+ each_file +'.xml')
    xml_data = open('csv/'+ each_file +'.csv','w',newline='',encoding='utf-8')
    print('xml/'+ each_file +'.xml')
    print('csv/'+ each_file +'.csv')
    csvwriter = csv.writer(xml_data)
    col_names = ['Id','Text','Topic']
    csvwriter.writerow(col_names)
    root=tree.getroot()
    for eventData in root.findall('row'):
        data = []
        #print(eventData.findatrrib("Tags"))
        #print(eventData.attrib["Tags"])
        data.append(count)
        if eventData.attrib["Body"]:
            data.append(eventData.attrib["Body"])
        else:
            continue
        data.append(each_file)
        csvwriter.writerow(data)
    count+=1
    xml_data.close()