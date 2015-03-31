# -*- coding: utf-8 -*-

import pyvmg
import utilities
import arrow


class N9SMSHandler:

    def __init__(self, aFolder, aDate=None):
        self._myFolder = aFolder
        self._mySMS = {}
        self._myLastDate = arrow.get('1988-07-31')
        self._myFiles = utilities.getListOfFilesForFolder(
            self._myFolder, True)
        # self._mySFiles = utilities.getListOfFilesForFolder(self._mySFolder)
        self._myVmgReader = pyvmg.VMGReader()
        self._processFiles(self._myFiles)

        # self._processFiles(self._mySFiles, True)

    def _processFiles(self, aListOfFiles):
        for aFile in aListOfFiles:
            if utilities.getFileExtension(aFile) == '.vmg':
                myData = self._processFile(aFile)
                self._myLastDate = max(self._myLastDate, myData['date'])
                if myData['telno']:
                    myData['telno'] = utilities.normalizePhoneNumber(
                        myData['telno'])
                    myData['body'] = myData['body'].replace(
                        "\r\n", "\n").rstrip('\n')
                    self._mySMS[
                        str(myData['date'].timestamp) + '_'
                        + myData['telno']] = myData

    def _processFile(self, aFile):
        self._myVmgReader.read(aFile, 'utf-16-le')
        return self._myVmgReader.process()

    def getSMS(self):
        return self._mySMS

    def getLastDate(self):
        return self._myLastDate

    def setSMS(self, aHash, aLastDateForNewHash):
        self._mySMS = aHash
        self._myLastDate = max(self._myLastDate, aLastDateForNewHash)
