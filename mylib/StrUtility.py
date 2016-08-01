#-*- encoding=utf-8 -*-  


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
        return "", -1;
    return ThisTString[StartPos : StartPos+Len], StartPos;

def GetAllSubStr(ThisTString, StartFlag, EndFlag, ltFilterFlags=[], bAllFlagsNeedExist=True, StartPos=0):
    ltRet = [];
    StringLen = len(ThisTString);
    while(StartPos<StringLen):
        StartPos, Len = GetSubStrInfo(ThisTString, StartFlag, EndFlag, StartPos);
        #print "?????", StartPos, Len
        if (Len <= 0) :
            break;
        subStr = ThisTString[StartPos : StartPos+Len];
        #print "??????", subStr
        bNeedtoRet = True;
        iFoundCnt  = 0;
        for flag in ltFilterFlags:
            if(subStr.find(flag)>=0):
                if(not bAllFlagsNeedExist):
                    break;
                iFoundCnt += 1;
            else:
                if(bAllFlagsNeedExist):
                    bNeedtoRet = False;
                    break;   
                
        if(bNeedtoRet or iFoundCnt==len(ltFilterFlags)):
            ltRet.append((subStr, StartPos));
            #print "append ==================>";
        StartPos += Len;
        pass
 
    return ltRet;

if "__main__"==__name__:
    ThisTString = "{{{ab}c}";
    print "0:", GetSubStr (ThisTString, "{", "}");
    print "1:", GetSubStr (ThisTString, "{", "}", 1);
    print "2:", GetSubStr (ThisTString, "{", "}", 2);
    print "3:", GetSubStr (ThisTString, None, "}");
    print "4:", GetSubStr (ThisTString, "{", None);
