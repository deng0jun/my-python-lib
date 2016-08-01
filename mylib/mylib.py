#-*- encoding=utf-8 -*-  
import sys, os, sqlite3; 
#return substr start-pos and length. 
def GetSubStrInfo(ThisTString, StartFlag, EndFlag, StartPos=0):
    ValLen=-1; EndFlagPosTmp=-1; StartFlagPosTmp=-1;
    if(ThisTString==None or StartPos>=len(ThisTString) or StartPos<0):
	    return -1, -1;

    if ((None==StartFlag or len(StartFlag)<=0) and len(EndFlag)>0):
        EndFlagPosTmp = ThisTString.find(EndFlag, StartPos);
        if(EndFlagPosTmp>=StartPos):
            ValLen = EndFlagPosTmp-StartPos;
            return StartPos, ValLen;
        return -1, -1;

    elif(len(StartFlag)>0 and (None==EndFlag or len(EndFlag)<=0)):
        StartFlagPosTmp = ThisTString.find(StartFlag, StartPos);
        if(StartFlagPosTmp>=StartPos):
            ValLen = len(ThisTString)-StartFlagPosTmp + len(StartFlag);
            StartFlagPosTmp = StartFlagPosTmp + len(StartFlag);
            return StartFlagPosTmp, ValLen;
        return -1, -1;

    elif (len(StartFlag)>0 and len(EndFlag)>0):
        while(True):
            StartPos = ThisTString.find(StartFlag, StartPos);

            if (StartPos >= 0):
                EndFlagPosTmp   = StartPos + len(StartFlag);
                StartFlagPosTmp = EndFlagPosTmp;
                while (True):
                    EndFlagPosTmp = ThisTString.find(EndFlag, EndFlagPosTmp);
                    if (EndFlagPosTmp < 0):
                        StartPos += 1;
                        break;
        
                    StartFlagPosTmp = ThisTString.find(StartFlag, StartFlagPosTmp); 

                    if (StartFlagPosTmp >= EndFlagPosTmp or StartFlagPosTmp < 0): 
                        ValLen = EndFlagPosTmp - StartPos - len(StartFlag);
                        return StartPos + len(StartFlag), ValLen

                    StartFlagPosTmp += len(StartFlag);
                    EndFlagPosTmp   += len(EndFlag);
            else:
                break;

    return -1, -1;


def GetSubStr(ThisTString, StartFlag, EndFlag, StartPos=0):
    StartPos, Len = GetSubStrInfo(ThisTString, StartFlag, EndFlag, StartPos);
    if (Len <= 0) :
        return "";
    return ThisTString[StartPos : StartPos+Len];


def get_md5_value(src):
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest
 
def get_sha1_value(src):
    mySha1 = hashlib.sha1()
    mySha1.update(src)
    mySha1_Digest = mySha1.hexdigest()
    return mySha1_Digest

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


############################################
def singleton(cls, *args, **kw):  
    instances = {}  
    def _singleton(*args, **kw):  
        if cls not in instances:  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]  
    return _singleton

@singleton
class DBHelper:
    def __init__(self, DBFileName):
        self.context_ = sqlite3.connect(DBFileName);
        self.cursor_  = self.context_.cursor();

    def __del__(self):
        if(self.context_ is not None):
            self.Commit();
            self.context_.close(); 
    
    def Exec(self, sql, param=None):
        if(self.cursor_ is not None):
            if(param is None):
                self.cursor_.execute(sql);
            else:
                self.cursor_.execute(sql, param);
            
    def Fetch(self, index=-1):
        ltRet = self.cursor_.fetchall();
        if(index<0):
            return ltRet;
        try:
            return list(ltRet[index]);
        except:
            pass;
        return [];

    def Commit(self):
        if(self.context_ is not None):
            self.context_.commit();

    def Rollback(self):
        if(self.context_ is not None):
            self.context_.rollback();

############################################

if "__main__"==__name__:
    ThisTString = "{{{ab}c}";
    print "0:", GetSubStr (ThisTString, "{", "}");
    print "1:", GetSubStr (ThisTString, "{", "}", 1);
    print "2:", GetSubStr (ThisTString, "{", "}", 2);
    print "3:", GetSubStr (ThisTString, None, "}");
    print "4:", GetSubStr (ThisTString, "{", None);
