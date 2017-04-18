def readmyfile(filename = 'ОКЕИ_тест.txt'):
    """Reading file to list"""
    TableWithoutEmptyLines=[]
    myfile=open(filename)
    for line in myfile:
        if line != '\n': #del empty lines
            TableWithoutEmptyLines.append(line)
    myfile.close() 
    return TableWithoutEmptyLines


def dataToList(fileData = readmyfile(), startLine=0, endLine=len(readmyfile())):
    """Convert data from file to datalist"""
    dataList=[]
    lineNum=0
    for line in fileData:
        if lineNum < endLine:    
            if lineNum >= startLine:
                RawText = line
                lineList = []
                line1 = (RawText.split("│"))# split to row
                for row in line1:
                    lineList.append(row.split())    
                for i in range(len(lineList)):
                    if len(lineList[i])>1:
                        text=''
                        for j in range(len(lineList[i])):
                            text = text+' '+lineList[i][j]
                        lineList[i] = [text]
                dataList.append(lineList)        
            lineNum = lineNum + 1        
    return dataList


def makeFileListToDB(filelist):
    """convert dataList to listDataType, listDataSubTipe,
       and listofData"""
    
    def lineCon(listofData, line):
        """line connection (for lines without code"""
        n = len(listofData)-1
        LastDataLine=listofData[n]
        for i in range(len(LastDataLine)):               
            if line[i]!=[]:                
                LastDataLine[i]=[LastDataLine[i][0]+' '+line[i][0]]

    def TName_Subtipe(listDataType,listDataSubTipe, listofData):
        """form first position in the line"""
        LastDataTypeN = len(listDataType)-1
        TName = listDataType[LastDataTypeN][0][0]

        ListDataSubTipeN=len(listDataSubTipe)-1
        Subtipe = listDataSubTipe[ListDataSubTipeN][1][0]
        
        LastDataLineN=len(listofData)-1
        LastDataLine=listofData[LastDataLineN]
        LastDataLine[0]=[TName+'_'+Subtipe]
        return LastDataLine


    listDataType=[]
    listDataSubTipe=[]
    listofData=[]


    flagAI=0      #Flag of additional information
    FlagNI = 1    #Flag for National or International unit
    flagUN=0      #flag of Unit names
    FlagHeader =0 #Flag of Header

    for line in filelist:
        #print(line,'\n')
        
        if len(line)<2:
            if '┌' in line[0][0]:
                startTableFlag=1
                flagUN=0
            elif '└' in line[0][0]:
                startTableFlag=0
            elif ('├'and'┤') in line[0][0]:
                flagAI=0
            elif line==[[' Приложение А']]:
                pass
            elif line==[['(справочное)']]:
                pass    
            elif '─' not in line[0][0] and flagUN==0:
                listDataType.append(line)           #rerecord
                flagUN=1
                if 'НАЦИОНАЛЬНЫЕ' in line[0][0]:
                    FlagNI = 1                      #Flag for National or International unit
                elif 'МЕЖДУНАРОДНЫЕ' in line[0][0]:
                    FlagNI = 0                      #Flag for National or International unit
            elif flagUN==1:                         #header - cont -> to privious line
                LastDataTypeN = len(listDataType)-1
                LastDataTypeLine=listDataType[LastDataTypeN]
                listDataType[LastDataTypeN]=[[LastDataTypeLine[0][0]+line[0][0]]]

                       
        elif len(line)==3:
            if line[1]!=[] and '---' in line[1][0]:
                pass
            elif line[1]!=[] and '<*>' in line[1][0]:
                flagAI=1                        #Flag of additional information
            elif line[1]!=[] and flagAI==1:
                pass
            elif line[2]!=[]:
                pass
            elif 'N' in line[1][0]:                   
                pass
            else:
                line[0]=listDataType[len(listDataType)-1][0]
                listDataSubTipe.append(line)

        
        elif len(line)==6:
            if line[1]!=[]:
                if line[1][0]=='Код':
                    FlagHeader=1                #Flag of Header
                elif line[1][0]!='Код':
                    FlagHeader=0
                    if FlagNI == 1:
                        line.insert(4,[''])
                        line.insert(6,[''])     #add to National units string
                        listofData.append(line) #record
                        TName_Subtipe(listDataType,listDataSubTipe, listofData)
                    elif FlagNI == 0:
                        line.insert(3,[''])
                        line.insert(5,[''])     #add to International units string
                        listofData.append(line) #rerecord
                        TName_Subtipe(listDataType,listDataSubTipe, listofData)
                        
            elif line[1]==[]:
                if FlagHeader==1:               #to header
                    pass
                elif FlagHeader==0:#print('except code -> to previous line')
                    pass
                    if FlagNI == 1:
                        line.insert(4,[])
                        line.insert(6,[])       #add to National units string
                        lineCon(listofData, line)#rerecord
                        TName_Subtipe(listDataType,listDataSubTipe, listofData)
                        
                    elif FlagNI == 0:
                        line.insert(3,[])
                        line.insert(5,[])       #add to International units string
                        lineCon(listofData, line) #rerecord
                        TName_Subtipe(listDataType,listDataSubTipe, listofData)
                        

        elif len(line)==8:
            if line[1]!=[]:
                if line[1][0]=='Код':
                    FlagHeader=1                #Flag of Header
                elif line[1][0]!='Код':
                    FlagHeader=0                #line with code -> to new line
                    listofData.append(line)     #record
                    TName_Subtipe(listDataType,listDataSubTipe, listofData)
            elif line[1]==[]:
                if FlagHeader==1:
                    pass
                elif FlagHeader==0:
                    lineCon(listofData, line)   #linewhithout code -> rerecord to previous line
                    TName_Subtipe(listDataType,listDataSubTipe, listofData)
                    

    return {'Type':listDataType, 'SubType':listDataSubTipe, 'Data':listofData}

