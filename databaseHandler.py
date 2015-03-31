# -*- coding: utf-8 -*-

import sqlite3
import utilities


def getSMSDataFromDb(aPathToDB):
    try:
        myDb = sqlite3.connect(aPathToDB)
        myCursor = myDb.cursor()
        myRequest = myCursor.execute(
            "select * from Events where event_type_id='11'")
        myList = myRequest.fetchall()
        return myList
    except Exception as e:
        raise e
    finally:
        myDb.close()


def deleteAllSmsFromDatabase(aPathToDB):
    try:
        myDb = sqlite3.connect(aPathToDB)
        myCursor = myDb.cursor()
        myCursor.execute("delete from Events where event_type_id='11'")
        myDb.commit()
    except Exception as e:
        myDb.rollback()
        raise e
    finally:
        myDb.close()
        # print('fail')


def deleteGroupCacheFromDatabase(aPathToDB):
    try:
        myDb = sqlite3.connect(aPathToDB)
        myCursor = myDb.cursor()
        myCursor.execute("delete from GroupCache where service_id='3'")
        myDb.commit()
    except Exception as e:
        myDb.rollback()
        raise e
    finally:
        myDb.close()


def copyDatabaseAndAddSms(aPathToDB, aPathToEDB, aHash, aGroupHash):
    utilities.copyFile(aPathToDB, aPathToEDB)
    deleteAllSmsFromDatabase(aPathToEDB)
    deleteGroupCacheFromDatabase(aPathToEDB)
    addSmsToDatabase(aPathToEDB, aHash, aGroupHash)


def addSmsToDatabase(aPathToDB, aHash, aGroupHash):
    try:
        myDb = sqlite3.connect(aPathToDB)
        myCursor = myDb.cursor()
        myList = utilities.hashToListOfTuples(aHash, aGroupHash)
        # for elem in aHash.values():
        #     myCursor.execute("""insert into Events(service_id,\
        #         event_type_id,storage_time,start_time,end_time,\
        #         is_read,outgoing,local_uid,local_name,\
        #         remote_uid,free_text,group_uid)\
        #          values (?,?,?,?,?,?,?,?,?,?,?,?)""",
        #                      ('3', '11', elem['date'].timestamp,
        #                       elem['date'].timestamp, elem['date'].timestamp,
        #                          0 if 'sent' in elem else 1,
        #                          1 if 'sent' in elem else 0,
        #                          'ring/tel/ring', '<SelfHandle>',
        #                          elem['telno'], elem['body'],
        #                          aGroupHash[elem['telno']] if elem['telno'] in aGroupHash else None))
        myCursor.executemany("""insert into Events(service_id,\
                event_type_id,storage_time,start_time,end_time,\
                is_read,outgoing,local_uid,local_name,\
                remote_uid,free_text,group_uid)\
                 values (?,?,?,?,?,?,?,?,?,?,?,?)""", myList)
        myDb.commit()
    except Exception as e:
        myDb.rollback()
        raise e
    finally:
        myDb.close()
        # print('something went awfully wrong')
        # print('Exception %s' % e.strerror)
