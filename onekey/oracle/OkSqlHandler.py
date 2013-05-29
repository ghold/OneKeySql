import cx_Oracle
import logging

class OkSqlHandler(object):
    @classmethod
    def setupConn(cls):
        dsn = cx_Oracle.makedsn("10.0.44.99", "1521", "ompdb")
        conn = cx_Oracle.connect('omp', 'omp', dsn)
        return conn
        
    @classmethod
    def insertAction(cls, sql):
        conn = cls.setupConn()
        cursor = conn.cursor()
        #logging
        logging.basicConfig(filename='onkey.log',level=logging.DEBUG, format='%(asctime)s %(message)s')
        logging.info(sql)
        cursor.execute(sql)
        cursor.close()
        conn.commit()
        conn.close()
        
#if __name__ == "__main__":
#    OkSqlHandler.insertAction("insert into omp.tt_bar_record (BAR_RECORD_ID, OP_CODE, ZONE_CODE, WAYBILL_NO, CONTNR_CODE, OP_ATTACH_INFO, STAY_WHY_CODE, BAR_SCAN_TM, BAR_OPR_CODE, COURIER_CODE, PHONE_ZONE, PHONE, SUBBILL_PIECE_QTY, BAR_UPLOAD_TYPE_CODE, WEIGHT_QTY, OTHER_INFO, AUTOLOADING, OBJ_TYPE_CODE, CREATE_TM) values (1989012000004, '30', '755R', '960837100044', '333124100065', '755R021R0430', '', to_date('05-12-2013 04:10:39', 'mm-dd-yyyy hh24:mi:ss'), '243099', '', '', '', 0, 0, 0.00, '', '1', 30, to_date('05-12-2013 04:35:39', 'mm-dd-yyyy hh24:mi:ss'))")
