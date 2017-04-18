import zipfile as zif
import xml.etree.ElementTree as ET
import csv, os, time


def parser(dir_zip):
    tf0=time.time()
    full_IdLevelList_InZip=[]
    full_IDObjectVel_InZip=[]
    #print('длинна dir_zip для [%s]= %s' % (os.getpid(), len(dir_zip)))
    for zipFile in dir_zip:
        path='./1/'+str(zipFile)
        z=zif.ZipFile(path)
        
        for fileName in z.namelist():
            a=z.read(fileName)
            root = ET.fromstring(a)
            IdLevelList=[]
            for child in root[:2]:
                IdLevelList.append(child.attrib['value'])        
            full_IdLevelList_InZip.append(IdLevelList)
            
            ID=root[0].attrib['value']
            for obgect in root[2]:
                objectVel=obgect.attrib['name']
                obgectLine=[ID, objectVel]
                full_IDObjectVel_InZip.append(obgectLine)
       
    IdLevelList_file = open('IdLevelList.csv', 'a') #Recording to IdLevelList.csv 
    writer = csv.writer(IdLevelList_file)
    for row in full_IdLevelList_InZip:
        writer.writerow(row)
    IdLevelList_file.close()

    IDObjectVel_file = open('IDObjectVel.csv', 'a') #Recording to IDObjectVel.csv 
    writer = csv.writer(IDObjectVel_file)
    for row in full_IDObjectVel_InZip:
        writer.writerow(row)
    IDObjectVel_file.close()

    print('[%s] %s строк -> IdLevelList.csv ' %(os.getpid(), len(full_IdLevelList_InZip)))
    print('[%s] %s строк -> IDObjectVel.csv ' %(os.getpid(), len(full_IDObjectVel_InZip)))
    print('t процесса [%s] = %s сек \n' %(os.getpid(), time.time()-tf0))



#выполнение тела программы 
t0=time.time()

dir_zip = os.listdir('./1') #file num in dir
print('длительность обработки до распараллеливания=', time.time()-t0)

for process in range(4):
    pid=os.fork()
    if pid !=0:
        print('Process %d spawned' % pid)
    else:
        if process == 0:
            type(dir_zip)
            new_dir_zip=dir_zip[:12]         
        elif process == 1:
            new_dir_zip=dir_zip[12:24]
        elif process == 2:
            new_dir_zip=dir_zip[24:36]
        elif process == 3:
            new_dir_zip=dir_zip[36:50]    
        parser(new_dir_zip)
        os._exit(0) 

            

