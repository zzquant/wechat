from typing import List

import pymysql
import logging
import sys

# 加入日志
# 获取logger实例
logger = logging.getLogger("baseSpider")
# 指定输出格式
formatter = logging.Formatter('%(asctime)s\
              %(levelname)-8s:%(wechat)s')
# 文件日志
file_handler = logging.FileHandler("baseSpider.log")
file_handler.setFormatter(formatter)
# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# 为logge添加具体的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.setLevel(logging.INFO)


class DBHelper:
    # 构造函数
    def __init__(self, host='112.74.77.153', user='haochunqiu',pwd='Hcq@19901218', db='wx_mps'):
        #def __init__(self, host='localhost', user='root', pwd='1234', db='app4tao_v1'):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.conn = None
        self.cur = None

    # 连接数据库
    def connectDatabase(self):

        self.conn = pymysql.connect(self.host, self.user, self.pwd, self.db, charset='utf8')
        self.cur = self.conn.cursor()
        return True

    # 关闭数据库
    def close(self):
        # 如果数据打开，则关闭；否则没有操作
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
        return True

    # 执行数据库的sq语句,主要用来做插入操作
    def execute(self, sql, params=None,returnkey = False):
        # 连接数据库
        result = True
        self.connectDatabase()
        try:
            if self.conn and self.cur:
                # 正常逻辑，执行sql，提交操作
                self.cur.execute(sql, params)
                if returnkey:
                    result = self.cur.lastrowid
                self.conn.commit()
        except:
            logger.error("execute failed: " + sql)
            #logger.error("params: " + params)
            #self.close()
            return False
        return result

    def executemany(self,sql,params=None):
        self.connectDatabase()
        try:
            if self.conn and self.cur:
                self.cur.executemany(sql,params)
                self.conn.commit()
        except:
            logger.error("executemany failed: " + sql)
            logger.error("params: " + params)
            self.close()
            return False
        return True


    # 用来查询表数据
    def fetchall(self, sql, params=None):
        self.execute(sql, params)
        return self.cur.fetchall()

    def insert(self,table,arr,returnkey=False):
        keys = list(arr.keys())
        values = list(arr.values())
        keystr = '`{0}`'.format('`,`'.join(keys))
        valuestr = ",".join('%s' %'%s' for v in values)
        sql = 'insert into {0} ({1}) values ({2}) '.format(table,keystr,valuestr)
        return self.execute(sql,values,returnkey)

    def insertmany(self,table,arrs):
        valueslist = [[]]
        keys = list(arrs[0].keys())
        for arr in arrs:
            valueslist.append(list(arr.values()))
        valueslist[:1]=[]
        keystr = '`{0}`'.format('`,`'.join(keys))
        valuestr = ",".join('%s' % '%s' for v in keys)
        sql = 'insert into {0} ({1}) values ({2}) '.format(table, keystr, valuestr)
        return self.executemany(sql,valueslist)

    def update(self,table,arr,where):
        temp: List[str] = []
        for k,v in arr:
            temp.append("`{0}` = '{1}'".format(k,v))
        kandv = ','.join(temp)
        sql = 'update {0} set {1} where {2}'.format(table,kandv,where)
        return self.execute(sql)

