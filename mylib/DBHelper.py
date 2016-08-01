#-*- encoding=utf-8 -*-  

############################################

def singleton(cls, *args, **kw):  
    instances = {}  
    def _singleton(*args, **kw):  
        if cls not in instances:  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]  
    return _singleton

#@singleton
class DBHelper:
 
    def __init__(self, SQLiteFileName=None, MySQLHost=None, MySQLPort=3306, MySQLUser=None, MySQLPasswd=None, MySQLDBName=None, NowConnect=False, DBCharset='utf8'):
        self.context_ = None;
        self.cursor_  = None;
        
        self.SQLiteFileName = SQLiteFileName; 
        self.MySQLHost      = MySQLHost; 
        self.MySQLPort      = 3306 if not MySQLPort else MySQLPort; 
        self.MySQLUser      = MySQLUser; 
        self.MySQLPasswd    = MySQLPasswd; 
        self.MySQLDBName    = MySQLDBName;
        self.DBCharset      = DBCharset;
        if(NowConnect):
            self.__Connect();

    def __del__(self):
        self.Disconnect();          
        

    def Disconnect(self):
        if(self.context_):
            self.Commit();
            self.context_.close();
            self.context_ = None;
            self.cursor_  = None;
        pass 

    def __Connect(self):
        if(not self.cursor_ or not self.context_):
            #For SQLite
            if(self.SQLiteFileName):
                exec("import sqlite3")
                self.context_ = sqlite3.connect(self.SQLiteFileName);
            #For Mysql!
            elif(self.MySQLHost and self.MySQLPort and self.MySQLUser and self.MySQLPasswd and self.MySQLDBName):
                exec("import MySQLdb")
                self.context_= MySQLdb.connect(
                    host     = self.MySQLHost,
                    port     = int(self.MySQLPort),
                    user     = self.MySQLUser,
                    passwd   = self.MySQLPasswd,
                    db       = self.MySQLDBName,
                    charset  = self.DBCharset
                );
               
            if(self.context_):
                self.cursor_ = self.context_.cursor();
            else:
                raise Exception("*** (DBHelper)Failed to connect DB! ***");
        pass


    
    def Exec(self, sql, param=None):
        self.__Connect();
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

    def Lock(self, TableName, Flag="write"):
        sql = "lock table "+TableName+ " "+Flag;
        self.Exec(sql);
        pass

    def Unlock(self):
        sql = "unlock tables";
        self.Exec(sql);
        pass


#With "short connect" to use DB
#@singleton 
class DBOperator:
    def __init__(self, DBHelperObj, TableName, FixedConnect=False, **kwFieldAttrs):
        assert(DBHelperObj is not None);
        self.DBHelperObj = DBHelperObj;
        self.TableName   = TableName; 
        self.FixedConnect= FixedConnect;

  
    def Create(self, TableName, OverWrite=False, **kwFieldAttrs):
        '''Create Table'''
        try:
            #self.PrimaryKeys = "";
            if(OverWrite is True):
                sql = "drop table if exists "+TableName;
                self.DBHelperObj.Exec(sql);
            sql = "create table if not exists "+TableName+" ( ";
            LastSql = ""
            for Field in kwFieldAttrs:
                if(not Field or not Field.strip() or Field=='_'):
                    LastSql += str(kwFieldAttrs[Field]) + ",";
                    #PrimaryIndex = str(kwFieldAttrs[Field]).upper().find("PRIMARY");
                    #if(str(kwFieldAttrs[Field]).upper().find("KEY")>PrimaryIndex and PrimaryIndex>=0):
                        #self.PrimaryKeys += str(kwFieldAttrs[Field]) + ";"
                else:
                    sql += str(Field) + " " + str(kwFieldAttrs[Field]) + ",";
                    #PrimaryIndex = str(Field).upper().find("PRIMARY");
                    #if(str(Field).upper().find("KEY")>PrimaryIndex and PrimaryIndex>=0):
                        #self.PrimaryKeys += str(Field) + ";"

            if(len(LastSql)<=0):
                sql = sql[:-1] + ")";
            else:
                sql = sql + LastSql[:-1] + ")";

            print "__init__ sql", sql
            if(len(kwFieldAttrs)>0):
                self.DBHelperObj.Exec(sql);
        finally:
            if(not self.FixedConnect):
                self.DBHelperObj.Disconnect();
        pass


    def Save(self, *Vals, **kwFieldVals):
        '''Svae data to Table'''
        #update catalog set name='Boy' where id = 0"
        #insert into Student (f1, f2) VALUES ('001', 'Bill1', '10', 'f');#comment
        try:
            if(len(Vals)>0):
                sql = 'insert into '+self.TableName+ " values (";
                for val in Vals:
                    sql += "\"" + str(val) + "\",";
                sql = sql[:-1]+")";
                self.DBHelperObj.Exec(sql);
                return True;
            
            if(len(kwFieldVals)>0):
                sql_condition = "";
                usql = 'update '+self.TableName+" set " ;
                isql = 'insert into '+self.TableName+ " (%s) values (";
                fields = "";
                for field in kwFieldVals:
                    fields += str(field)+",";
                    isql += "\"" + str(kwFieldVals[field]) + "\",";
                    if(field!='sql_condition'):
                        usql+= str(field)+"="+str(kwFieldVals[field])+",";
                    else:
                        sql_condition = str(kwFieldVals[field]);              
                
                if(len(sql_condition)>0):
                    usql = usql[:-1]+"  "+sql_condition;
                    #print "Update usql:", usql
                    self.DBHelperObj.Exec(usql);
                else:                    
                    isql = isql[:-1]+")";
                    #print "zzzz", fields[:-1]; 
                    #print "zzz2", isql;
                    #isql = isql % fields[:-1]; 
                    isql = isql.replace("%s", fields[:-1]); 
                    print "Insert sql:", isql 
                    self.DBHelperObj.Exec(isql);

            pass
        except Exception, e:
            print " *** Save Error :", e
            return False;
        finally:
            if(not self.FixedConnect):
                self.DBHelperObj.Disconnect();

    def Del(self, sql_condition='2>1'):
        '''Delete record'''
        if(not self.TableName):
            return False;
        sql = "delete from "+self.TableName+" "+sql_condition;
        #print "Delete sql:", sql 
        try:
            self.DBHelperObj.Exec(sql);
            return True;
        except Exception, e:
            print " *** Del Error:", e
            return False;
        finally:
            if(not self.FixedConnect):
                self.DBHelperObj.Disconnect();

    def Get(self, ltFields=[], sql_condition="", index=-1):
        '''Query info'''
        if(not self.TableName):
            return [];
        Predix = "select * ";
        if(isinstance(ltFields, list) and len(ltFields)>0):
            Predix = "select "
            for f in ltFields:
                Predix += str(f)+",";
        if(isinstance(ltFields, str) and len(ltFields)>0):
            Predix = "select " +ltFields;
            Predix = Predix.strip();
            if(not Predix.endswith(",")):
                Predix += " ,";
                
        if(sql_condition is None):
            sql_condition = "";

        sql = Predix[:-1]+" from "+self.TableName+ " " +sql_condition;
        print "Query sql:", sql 
        try:
            self.DBHelperObj.Exec(sql);
            return self.DBHelperObj.Fetch(index);
        except Exception, e:
            print " *** Get Error:", e
            return [];
        finally:
            if(not self.FixedConnect):
                self.DBHelperObj.Disconnect();

    def Flush(self):
        self.DBHelperObj.Commit();
                
if "__main__"==__name__:

    #²Ù×÷SQLite£º
    DBHelperObj = DBHelper("test_db.db");
    #DB.Exec("create table if not exists myTest ( age integer,id integer,name varchar(512) UNIQUE);")

    DBOperatorObj = DBOperator(DBHelperObj, "myTest", True, id='integer', name='varchar(512) UNIQUE', age="integer", _='primary key (id)' );
    DBOperatorObj.Save(id=1, age=20, name="A1");
    DBOperatorObj.Save(id=2, age=20, name="A2");
    DBOperatorObj.Save(id=3, age=20, name="A3");
    DBOperatorObj.Save(21, 4, "A4");
    DBOperatorObj.Save(age=52, sql_condition='id=4');
    DBOperatorObj.Save(id=4, age=36);
    DBOperatorObj.Del(sql_condition='id=2');
    print DBOperatorObj.Get('id=1');
    print DBOperatorObj.Get('id=2');
    print DBOperatorObj.Get('id=4');

    #²Ù×÷MySQL£º
    #DB = DBHelper(None, "localhost", 3306, 'root', '123456', 'chinamarket');
    #DB.Exec("select * from market_cucc limit 1");
    #print DB.Fetch();

############################################
 
