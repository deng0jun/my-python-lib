#-*- encoding=utf-8 -*-  




class StrEx(str):
    def __init__(self, initVal=""):
        self = initVal;
    pass

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
        StartPos, Len = ThisTString.GetSubStrInfo(StartFlag, EndFlag, StartPos);
        if (Len <= 0) :
            return "";
        return ThisTString[StartPos : StartPos+Len];


    def __getitem__(self, key):
        #print "333 ;;;;;;;;;;;;;;;;;", type(key.start), type(key.stop)  
        if(isinstance(key.start, str) and isinstance(key.stop, str)):
            return self.GetSubStr(key.start, key.stop);
        if(not isinstance(key.start, str) and not isinstance(key.stop, str)):
            return super(StrEx, self).__getitem__(key);
        if(not isinstance(key.start, str)):
            if(self.find(key.stop)<=0):
                key.stop = None;
            return super(StrEx, self).__getitem__(key);
        if(not isinstance(key.stop, str)):
            return self.GetSubStr(key.start, key.stop);
        return "";

if "__main__"==__name__:
    strObj = StrEx("ABCDEFGHIJKLMNOPQRST")
    #print strObj[2:5], strObj.GetSubStr("2", "6");
    print strObj["CD":"R"]
