#coding:utf-8
import Queue;
import multiprocessing, threading, thread, time;

#Model:InputData&Func ==Queue==> [MultiTasksPool] ====> OutputData
#Usage: CreatePoolObject --> AddTasks --> GetResult --> Exit

class MultiTasksPool():
    def __init__(self, InputQueueSize=1024, OutputQueueSize=1024, TasksNum=12, UseThread=True):
        self.__InputQueue  = Queue.Queue(maxsize=InputQueueSize); #Create InputQeueue, it accept task info..
        self.__OutputQueue = Queue.Queue(maxsize=OutputQueueSize);#Create OutputQeueue, it cache result.
        self.__UseThread   = UseThread;#Task model: Multi-Thread or Multi-Process.
        self.__TaskNum     = TasksNum;
        self.__TaskHandlers= [];
        self.__RunningFlag  = True;
 
        WorkThreadNum = TasksNum if(self.__UseThread) else 1;
        for i in xrange(WorkThreadNum):
            #thread.start_new_thread(self.__Run__, ());
            handler = threading.Thread(target=self.__Run__, args=());            
            handler.setDaemon(True)
            handler.start();
            self.__TaskHandlers.append(handler);
            pass  

    def __del__(self):
        self.Exit();
        while(self.__RunningFlag is not None):
            time.sleep(0.1);
        for t in self.__TaskHandlers:
            t.join();
        pass

    def Exit(self):
        self.__RunningFlag = False;    
        pass;

    def AddTask(self, WorkFunc, Args=(), Block=False, TimeoutS=None):
        try:
            self.__InputQueue.put([WorkFunc, Args], block=Block, timeout=TimeoutS);
            return True;
        except Queue.Full, e:
            return False;

    def GetResult(self, Block=True, TimeoutS=None):
        '''
        TimeoutS is available only when Block is True
        '''
        try: 
            return self.__OutputQueue.get(block=Block, timeout=TimeoutS), True;
        except Queue.Empty, e:
            return None, False;
        pass


    def __Run__(self): 
        while(self.__RunningFlag):
            try:
                if(self.__UseThread):
                    WorkFunc, Args = self.__InputQueue.get(block=False);
                    ret = apply(WorkFunc, Args); 
                    self.__OutputQueue.put(ret, block=True);
                    pass
                else:
                    #Use process model!                    
                    while(True):                        
                        pool = multiprocessing.Pool(processes=self.__TaskNum);
                        result = [];
                        try:
                            for i in xrange(500):
                                WorkFunc, Args = self.__InputQueue.get(block=False);
                                result.append(pool.apply_async(WorkFunc, Args));
                        finally:
                            #print "i===>", i
                            pool.close();
                            pool.join();                            

                            for ret in result:
                                if(ret.ready()):
                                    self.__OutputQueue.put(ret.get(), block=True);
                                    result.remove(ret);
                                pass
                            pass 
                        pass 
                    pass 
                pass     
            except Queue.Empty, e:                
                time.sleep(0.1);
                pass;

        else:
            self.__RunningFlag = None;
        pass
    pass

####################################################################
#Test:
def WorkFunc(k):
    #print i, "-->>";
    j=1;
    for i in xrange(k+99999):
        j = (i+j*3)%(2*i+j%3+2*j)%9; #计算密集型
        pass
    return str(k)+"__11111111111111_" + str(j);
    pass

def timeit(func):
    def wrapper():
        start = time.clock()
        func()
        end =time.clock()
        print 'used:', end - start
    return wrapper

'''
计算密集型，耗时情况：
单任务：386秒
3进程： 142秒
9线程： 795秒
对于计算不密集的任务（WorkFunc没有for循环），单任务效率最高，其次是多线程，多进程效率最差。
对于IO密集型任务，理论上多线程、多进程效率都高于单任务。
'''
@timeit
def Test():
    #最好AddTask使用非阻塞方式，而GetResult使用阻塞方式。
    pool = MultiTasksPool(InputQueueSize=1111, OutputQueueSize=1111, TasksNum=10, UseThread=False);
    for i in xrange(3999):
        WorkFunc(i);
        #print WorkFunc(i);
        continue;

        ret = pool.AddTask(WorkFunc, (i,), False);
        #print "AddTask-ret", ret;

        while(ret is False):
            retVal, retFlag = pool.GetResult(True);
            #print "retVal_1:", retVal;
            ret = pool.AddTask(WorkFunc, (i,), False);

    #return;
    while(True):
        retVal, retFlag = pool.GetResult(True, TimeoutS=13);
        if(retFlag is False):
            break;
        #print "retVal_2:", retVal;



if __name__=="__main__":
    s= time.time();
    Test()
    print ">>>", time.time()-s; 
    raw_input("...");
    pass
