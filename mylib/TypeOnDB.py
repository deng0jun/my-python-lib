#-*- encoding=utf-8 -*-  

from DBHelper import DBHelper;
import time;

#子类对应的数据库表必须包含key、keyType这两个域！
class __DataType(object):
    def __init__(self, DBInfo="DataType.db", tableName="tableName"):
        if(isinstance(DBInfo, str)):
            self.DBObj = DBHelper(DBInfo);
        else:
            self.DBObj = DBInfo;
        self.tableName = tableName;
    
    def RestoreDataType(self, strVal, strTypeInfo):
        if(strTypeInfo==str(str)):
            return str(strVal);
        if(strTypeInfo==str(bool)):
            return bool(strVal);
        if(strTypeInfo==str(int)):
            return int(strVal);
        if(strTypeInfo==str(long)):
            return long(strVal);
        if(strTypeInfo==str(float)):
            return float(strVal);
        if(strTypeInfo==str(complex)):
            return complex(strVal);
        if(strTypeInfo==str(list)):
            return list(strVal);
        if(strTypeInfo==str(tuple)):
            return tuple(strVal);
        if(strTypeInfo==str(type(None))):
            return None;
        return strVal;

    def clear(self): 
        '''Clear all data of this obj'''
        try:
            self.DBObj.Exec("delete from "+self.tableName);
        except Exception, e:
            print "clear-Exception:", e

    def __len__(self):
        '''x.__len__() <==> len(x)'''
        try:
            sql = "select count(*) from "+self.tableName;
            self.DBObj.Exec(sql);
            ltRet = self.DBObj.Fetch();
            return long(ltRet[0][0]);
        except:
            return 0;

    def empty(self):
        '''empty return True, else return False'''
        return self.__len__()==0;

    def remove(self, key):
        '''Remove one record'''
        try:
            sql = "delete from "+self.tableName+" where key=\"" +str(key) +"\" and keyType=\""+str(type(key))+ "\"";
            self.DBObj.Exec(sql);
            self.DBObj.Commit();
        except Exception, e:
            print "remove-Exception:", e 

    def __iter__(self): 
        try:
            PageStart=0;
            PageSize =100;
            while(True):
                self.DBObj.Exec("select key,keyType from "+self.tableName+" limit "+str(PageStart)+","+str(PageSize));
                ltRes = self.DBObj.Fetch();
                for val in ltRes:
                    yield self.RestoreDataType(val[0], val[1]);
                if(len(ltRes)<PageSize):
                    break;
                PageStart += PageSize;
        except Exception, e:
            print "__iter__-Exception:", e

    def __contains__(self, key):
        '''x.__contains__(y) <==> y in x '''
        try:
            sql = "select * from "+self.tableName+" where key=\""+str(key)+"\" and keyType=\""+str(type(key))+"\"";
            self.DBObj.Exec(sql);
            ltRes = self.DBObj.Fetch();
            if(len(ltRes)>0):
                return True;
        except:
            pass
        return False;

##############################################################
#数据存储在数据库中的Set
class DBSet(__DataType):
    def __init__(self, DBInfo="DBSet.db", tableName="SetInfo", OverWriteExistTable=False, CreateTableFlag=True):
        super(DBSet, self).__init__(DBInfo, tableName);
        if(CreateTableFlag):
            if(OverWriteExistTable):
                sql = "drop table if exists "+self.tableName ;
                self.DBObj.Exec(sql);
            sql = "create table if not exists "+self.tableName+" (key varchar(2048), keyType varchar(64), primary key(key,keyType))"
            self.DBObj.Exec(sql);

    def add(self, val):
        try:
            sql = "insert into "+self.tableName+" (key, keyType) values (\"" +str(val)+ "\",\"" +str(type(val))+ "\")"
            #print ">>>", sql;
            self.DBObj.Exec(sql);
            self.DBObj.Commit();
        except Exception, e:
            print "add-Exception:", e

    def pop(self):
        for key in self:
            self.remove(key);
            return key; 
        raise KeyError;
 
    def copy(self):
        try:
            setObj = set();
            self.DBObj.Exec("select key,keyType from "+self.tableName);
            ltRes = self.DBObj.Fetch();
            for val in ltRes:
                setObj.add(self.RestoreDataType(val[0], val[1]));
            return setObj;
        except Exception, e:
            print "copy-Exception:", e

 

##########################################################
#数据存储在数据库中的字典
class DBDict(__DataType):
    def __init__(self, DBInfo="DBDict.db", tableName="DictInfo", OverWriteExistTable=False, CreateTableFlag=True):
        super(DBDict, self).__init__(DBInfo, tableName);
        if(CreateTableFlag):
            if(OverWriteExistTable):
                sql = "drop table if exists "+self.tableName ;
                self.DBObj.Exec(sql);
            sql = "create table if not exists "+self.tableName+" (key varchar(2048), keyType varchar(64), value varchar(4096), valueType varchar(64), primary key(key,keyType))"
            self.DBObj.Exec(sql);

    def __setitem__(self, key, value): 
        '''Overload sequence element set'''   
        try:
            try:
                if(self.has_key(key)):
                    self.DBObj.Exec("update "+self.tableName+" set value=\""+str(value)+"\", valueType=\""+str(type(value))+"\" where key=\""+str(key)+"\" and keyType=\""+str(type(key))+"\"");
                else:
                    self.DBObj.Exec("insert into "+self.tableName+" (key, keyType, value, valueType) values (" +str(key) +", \""+str(type(key))+ "\", \""+str(value)+"\", \"" +str(type(value))+ "\")");
            except Exception, e:
                print "__setitem__-Exception 1:", e
            finally:
                self.DBObj.Commit();

        except Exception, e:
            print "__setitem__-Exception 2 :", e
 

    def get(self, key, defVal=None):
        '''D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.'''
        if(self.has_key(key)):
            return self.__getitem__(key);
        return defVal;

    def __getitem__(self, key): 
        '''x.__getitem__(y) <==> x[y]''' 
        try:
            sql = "select value,valueType from "+self.tableName+" where key=\""+str(key)+"\" and keyType=\""+str(type(key))+"\"";
            print "__getitem__-sql", sql;
            self.DBObj.Exec(sql);
            ltRes = self.DBObj.Fetch();
            print "ltRes", key, type(key), ltRes
            for val in ltRes:
                return self.RestoreDataType(val[0], val[1]);
            raise KeyError;
        except KeyError, e:
            print "__getitem__-Exception 1:", e
            raise e;
        except Exception, e:
            print "__getitem__-Exception 2:", e

    def __delitem__(self, key):
        '''x.__delitem__(y) <==> del x[y]'''
        self.remove(key);


    def copy(self):
        '''D.copy() -> a shallow copy of D'''
        dictObj = {};
        try:            
            self.DBObj.Exec("select key,keyType, value,valueType from "+self.tableName);
            ltRes = self.DBObj.Fetch();
            for val in ltRes:
                _key = self.RestoreDataType(val[0], val[1]);
                _val = self.RestoreDataType(val[2], val[3]);
                print _key,type(_key),  _val;
                dictObj[_key] = _val;
            return dictObj;
        except Exception, e:
            print "copy-Exception:", e
            return dictObj;  

    def items(self): 
        ltRet = [];
        try:
            for key, val in self.iteritems():
                ltRet.append((key, val));
        except Exception, e:
            print "items-Exception:", e 
        finally:
            return ltRet; 

    def iteritems(self): 
        try:
            self.DBObj.Exec("select key,keyType, value,valueType from "+self.tableName);
            ltRes = self.DBObj.Fetch();
            for val in ltRes:
                yield self.RestoreDataType(val[0], val[1]), self.RestoreDataType(val[2], val[3]);
        except Exception, e:
            print "iteritems-Exception:", e;
            

    def __getColVals(self, ColName):
        ltRet= [];
        try:
            self.DBObj.Exec("select "+ColName +","+ColName+"Type from "+self.tableName);
            ltRes = self.DBObj.Fetch();            
            for val in ltRes:
                ltRet.append(self.RestoreDataType(val[0], val[1]));
            return ltRet
        except Exception, e:
            print "keys-Exception:", e
            return ltRet;        

    def keys(self):
        '''D.keys() -> list of D's keys'''
        return self.__getColVals("key");

    def values(self):
        '''D.values() -> list of D's values'''
        return self.__getColVals("value");
        
    def has_key(self, key): 
        return self.__contains__(key);


########################################################
#数据库中实现队列
class DBQueue(__DataType):
    '''class DBQueue(__DataType)'''
    def __init__(self, MaxSize=0, FIFO=True, HPFO=False, ValUnique=False, DBInfo="DBQueue.db", tableName="QueueInfo", OverWriteExistTable=False, CreateTableFlag=True):
        super(DBQueue, self).__init__(DBInfo, tableName);
        self.FIFO = FIFO; #First In First Out
        self.HPFO = HPFO; #Higher Priority First Out
        self.MaxSize = MaxSize;
        self.ValUnique = ValUnique;

        if(CreateTableFlag):
            if(OverWriteExistTable):
                sql = "drop table if exists "+self.tableName ;
                self.DBObj.Exec(sql);
            sql = "create table if not exists "+self.tableName+" (id integer primary key autoincrement, key varchar(2048) not null , keyType varchar(64), come_time float, priority float)"
            self.DBObj.Exec(sql);
            #print "==>", sql

    def push(self, key, priority=10):
        return self.put(key, priority);

    def pop(self, DefaultRetVal=None):
        return self.get(DefaultRetVal);

    def put(self, key, priority=10):
        '''value of priority bigger indicate the priority of key higher'''
        try:
            if(self.ValUnique):
                sql = "select * from "+self.tableName+" where key=\""+str(key)+"\" and keyType=\""+str(type(key))+"\"";
                self.DBObj.Exec(sql);
                if(len(self.DBObj.Fetch())>0):
                    return False;
                pass
            sql = "insert into "+self.tableName+" (key,keyType,come_time,priority) values (\"" +str(key)+ "\",\"" +str(type(key))+ "\", "+ str(time.time()+time.clock()) +", "+str(priority)+")"
            self.DBObj.Exec(sql);
            self.DBObj.Commit();

            if(self.MaxSize>=1):
                if(self.__len__()>self.MaxSize):
                    self.get(FIFO=True);
                    #print "///>>", self.__len__(), self.MaxSize
            return True;
        except Exception, e:
            print "put-Exception:", e
            return False;

    def get(self, DefaultRetVal=None, FIFO=None):
        '''Get one value according to condition which given in func __init__'''
        #PrioSQL = "priority=(select min(priority) from "+self.tableName+")";
        PrioSQL = "priority>=-99999"; #Any 
        if(self.HPFO):
            PrioSQL = "priority=(select max(priority) from "+self.tableName+")";

        condSQL = "come_time=(select max(come_time) from "+self.tableName+" where "+PrioSQL +" )"
        
        if(FIFO is None):
            FIFO = self.FIFO;
        if(FIFO):
            condSQL = "come_time=(select min(come_time) from "+self.tableName+" where "+PrioSQL +" )"
        
        getSQL = "select id,key,keyType from "+self.tableName+" where "+ condSQL;
        self.DBObj.Exec(getSQL);
        ltRet = self.DBObj.Fetch();
        if(len(ltRet)<1):
            #raise KeyError;
            return DefaultRetVal;
        delSQL = "delete from "+self.tableName+" where id="+str(ltRet[0][0]);
        self.DBObj.Exec(delSQL);
        #print "Raw Data", ltRet;
        return self.RestoreDataType(ltRet[0][1], ltRet[0][2]);

#------------------------------------------------------
if "__main__"==__name__:
    #'''
    DBQueueObj = DBQueue(MaxSize=12);
    DBQueueObj.clear();
    DBQueueObj.put("sssss", 1);
    DBQueueObj.put(1, 1);
    DBQueueObj.put(1.2, 2);
    DBQueueObj.put("aaaa", 2);
    DBQueueObj.put("xxx", 1.5);
    DBQueueObj.put("xxx", 1.5);
    #print "Get ", DBQueueObj.get(), len(DBQueueObj);
    for i in DBQueueObj:
        print ">>>", i, type(i)
    #print help(DBQueue);
    #'''

    '''
    DBDictObj = DBDict();
    DBDictObj.clear();
    DBDictObj[1] = 1;
    DBDictObj[1] = 2;
    #print DBDictObj['1']
    DBDictObj['1'] = '1111111111';
    #print DBDictObj['1']
    DBDictObj[float(1)] = 1.1;
    print DBDictObj.keys();
    #DBDictObj.remove(1);

    for k, v in DBDictObj.iteritems():
        print "DBDictObj", k, type(k),  v, type(v);
        pass
    print "len(DBDictObj)", len(DBDictObj);

    DBDictObj = DBDictObj.copy();
    for k, v in DBDictObj.iteritems():
        print "DictObj", k, type(k),  v, type(v);
        pass
    '''

    '''
    DBSetObj = DBSet();
    #DBSetObj.clear();
    DBSetObj.add(2);
    DBSetObj.add(unicode("2"));
    DBSetObj.add(float(2));
    DBSetObj.add(float(3));
    DBSetObj.add(float(4));
    #DBSetObj.remove(float(2));
    #DBSetObj = DBSetObj.copy();
    for val in DBSetObj:
        print type(val), val
        pass
 
    #while True:
        #val = DBSetObj.pop();
        #print type(val), val
    #''' 
    

