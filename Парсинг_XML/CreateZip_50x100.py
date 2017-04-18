import xml.etree.ElementTree as ET
import random
import zipfile as zif


def zipFileMake(zipNumber, fileNumber): #create n ZIPs
    zipNameStr = './1/test'
    for zipNum in range(zipNumber):
        zipName = zipNameStr+str(zipNum)+'.zip'
        z=zif.ZipFile(zipName, mode='w')

    #create new xml file
        for fileNum in range(fileNumber):
            root = ET.Element('root')

            List=list('qwertyuiopasdfghjklzxcvbnm')
            random.shuffle(List)
            strValue=str(fileNum)+''.join(List)
            var1 = ET.SubElement(root, 'var', name='id', value=strValue)

            randNum = str(random.uniform(1, 100))
            var2 = ET.SubElement(root, 'var', name='level', value=randNum)

            objects = ET.SubElement(root, 'objects')
            for i in range(random.randint(1,10)):
                random.shuffle(List)
                strName=''.join(List)
                ET.SubElement(objects, 'object', name=strName)#'random string'

            tree = ET.ElementTree(root)
            filename=('file_' + str(fileNum)+'.xml')
            #tree.write(filename)
            z.writestr(filename, ET.tostring(root))
        z.close()
        


zipFileMake(50,100)

