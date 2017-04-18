import DBconnect as db
import pars as mf

fileData = mf.readmyfile()
filelist=mf.dataToList(fileData)
ListToDB = mf.makeFileListToDB(filelist)

db.createDBTables()

for line in ListToDB['Type']:
    a=db.insUnitData(line)
if a == 1:
    print('----\n')
else:
    print('UnitData inserted to DB \n----\n')


for line in ListToDB['SubType']:
    a=db.insSubTypeData(line)
if a == 1:
    print('----\n')
else:
    print('SubUnitData inserted to DB \n----\n')


for line in ListToDB['Data']:
    a=db.insData(line)
if a == 1:
    print('----\n')
else:
    print('Data inserted to DB \n----\n')


#db.readTypeData() #селект из базы
#db.DropDBTables() #удалить таблицы из базы

