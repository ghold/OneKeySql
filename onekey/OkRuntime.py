from oracle.OkSqlHandler import OkSqlHandler
import re
import time
from threading import Thread

class OkExecProcess(Thread):
    def __init__(self, sql, daemon=True):
        Thread.__init__(self, daemon=daemon)
        self.sql = sql
        
    def run(self):
        step_pattern = r";\n/\*Step [0-9 ]+.+\*/\n"
        step_compiler = re.compile(step_pattern)
        step_list = step_compiler.split(self.sql)
        sql_pattern = r";\n|/\*Step [0-9 ]+.+\*/\n|\n"
        sql_compiler = re.compile(sql_pattern)
        for val in step_list:
            val = sql_compiler.sub(r' ', val)
            #Don't need to add " at start or at end
            if 'INSERT' in val:
                OkSqlHandler.insertAction(val.strip())
                time.sleep(1)
            else:
                exec(val.strip())
