#-*- encoding=utf-8 -*-  


def FileLine2List(FileName, startLine=0, endLine=sys.maxint):
    RetList = [];
    InFile = open(FileName, 'r');
    CurLineNo = 0;

    line = InFile.readline(); 
    while line and CurLineNo<endLine:       
        if(startLine<=CurLineNo):
            #line = line.strip();
            RetList.append(line);
            
        CurLineNo += 1;
        line = InFile.readline(); 

    InFile.close();
    return RetList;

def List2FileLine(listContent, FileName, LineBeginFlag="", LineEndFlag=""):
    OutFile = open(FileName, 'w');
    for itemX in listContent:
        OutFile.write(LineBeginFlag+ itemX + LineEndFlag);
    OutFile.close();


def Dict2File(dictContent, FileName, ReverseFlag=True, LineBeginFlag="", LineEndFlag=""):
    OutFile = open(FileName, 'w');
    #对字典按照值进行排序！
    ltContent = sorted(dictContent.iteritems(), key=lambda d:d[1], reverse = ReverseFlag)
    for itemX in ltContent:
        OutFile.write(LineBeginFlag+ str(itemX[0]) +":"+str(itemX[1]) + LineEndFlag+"\n");
    OutFile.close();


if "__main__"==__name__:
    pass
