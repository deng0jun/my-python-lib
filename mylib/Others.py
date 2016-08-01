#-*- encoding=utf-8 -*-  

import sys, time, os, hashlib 

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
 
 
def LoadPlugins(rootDir, ltExportFuncNames): 
    #print "rootDir", rootDir
    moduleList = [];
    for lists in os.listdir(rootDir):       
        module_file = os.path.join(rootDir, lists)
        if(module_file.endswith(".py") and module_file.find("__init__.py")<0):
            try:
                #print "module_file", module_file;
                fname, ext=os.path.splitext(module_file);
                __names=fname.split(os.sep);
                module_name = ".".join(__names)
                #__import__函数中 ["XXX"] 起到占位符的作用！不能缺！
                #print "....", __names, module_name
                module = __import__(module_name, globals(), locals(), ["XXX"], 0);
                for exportFuncName in ltExportFuncNames:
                    getattr(module, exportFuncName); 
                moduleList.append(module);
                g_logger.info("Loaded:" + module_file);
            except Exception, e:
                #g_logger.error("ImportError:"+str(e)+"\nMay no __init__.py OR no exportFuncName");
                g_logger.error(">>>"+ traceback.format_exc());
                pass

        if os.path.isdir(module_file):
            moduleList += LoadPlugins(module_file, ltExportFuncNames);
            pass; 

    return moduleList;


class WaitAnimation():
    def __init__(self, Interval = 1):
        self.__index = 0;
        self.__chars = ["|", "/", "-", "\\"];
        self.__WaitFlag = True;
        self.Interval = Interval;
        pass 
 
    def __Animation(self, Animation, Rate):
        if(Animation.upper() == 'P'):
            STEP_NUM = 77;
            sys.stdout.write("[");
            for i in range(STEP_NUM - int(STEP_NUM * Rate)):
                sys.stdout.write(">");
            for i in range(int(STEP_NUM * Rate)):
                sys.stdout.write("-");
            sys.stdout.write("]\r");
            pass
        elif(Animation.upper() == 'C'):
            sys.stdout.write(self.__chars[self.__index] + " DC [" +str(Rate*100) + "%]     \r");
            self.__index = (self.__index+1) % len(self.__chars);
            pass 

    def __WaitFor(self, max_sleep=1, Animation="C", expr="False"):
        self.__WaitFlag = True;
        remainder = max_sleep;
        ExprCond = eval(expr);
        print " ";
        while(remainder>0 and self.__WaitFlag and not ExprCond):
            self.__Animation(Animation, remainder*1.0/max_sleep);
            time.sleep(self.Interval);
            remainder -= self.Interval;
            ExprCond = eval(expr);
        print "\rAfter WaitFor" + " "* (79 - len("After WaitFor"));

    def WaitFor(self,max_sleep=1, expr="False"):
        return self.__WaitFor(max_sleep, "c", expr);

    def Process(self, max_sleep=1, expr="False"):
        return self.__WaitFor(max_sleep, "p", expr); 

    def Break(self):
        self.__WaitFlag = False;
        pass

def __test():
    return 5;
    pass

if "__main__"==__name__:
    WaitAnimationObj = WaitAnimation();
    #WaitAnimationObj.WaitFor(expr="__test()>10", max_sleep=10);
    #WaitAnimationObj.Process(10);
    WaitAnimationObj.WaitFor(10);

    print "Over ================>";
    pass
