# -*- coding: utf-8 -*-

import databaseHandler
import arrow
import utilities


class N900SMSHandler:

    def __init__(self, aPathToDb):
        self._filePath = aPathToDb
        self._myLastDate = arrow.get('1988-07-31')
        self._mySMS, self._myGroupUID = self._processSMS(
            databaseHandler.getSMSDataFromDb(self._filePath))

    def getLastDate(self):
        return self._myLastDate

    def _processSMS(self, aList):
        myHash = {}
        myGroupHash = {}
        for elem in aList:
            myData, myGid = self._getDataFromSMSTuple(elem)
            self._myLastDate = max(self._myLastDate, myData['date'])
            myGroupHash[myData['telno']] = myGid
            myHash[
                str(myData['date'].timestamp) + '_' + myData['telno']] = myData
        return myHash, myGroupHash

    def _getDataFromSMSTuple(self, aSMS):
        data = {}
        data['telno'] = utilities.normalizePhoneNumber(aSMS[13])
        # data['body'] = aSMS[15].replace("\r\n", "\n").rstrip('\n')
        data['body'] = aSMS[15]
        data['date'] = arrow.get(aSMS[3])
        # use storage time instead of start time
        # data['date'] = arrow.get(aSMS[5])
        if aSMS[7] == 1:
            data['sent'] = True
        myGUID = aSMS[16]
        return data, myGUID

    def getSMS(self):
        return self._mySMS

    def getGroupUIDHash(self):
        return self._myGroupUID

    def setSMS(self, aHash, aLastDateForNewHash):
        self._mySMS = aHash
        self._myLastDate = max(self._myLastDate, aLastDateForNewHash)
