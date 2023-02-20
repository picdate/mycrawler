import pymysql

class MysqlConnector:
    def __init__(self,mhost="localhost",mport=3306,muser="root",mpasswd="123456",mdb="test",mcharset="utf8"):
        self.db=pymysql.connect(host=mhost,port=mport,user=muser,passwd=mpasswd,db=mdb,charset=mcharset)
        
    def insert(self,sql):
        cursor=self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()
    def close(self):
        self.db.close()