# -*- coding: utf-8 -*-

import collections
from difflib import SequenceMatcher as SeqM, Differ
from pprint import pprint
from operator import itemgetter


def isR(c):
    return c in "\r"


def ignore_ws_nl(c):
    return c in " \t\n\r"


class SMSMerger:

    def __init__(self, N900SMSHash, N9SMSHash):
        self._myMergedHash = self._mergeHashes(N900SMSHash, N9SMSHash)
        self._mySortedHash = self._sortHash(self._myMergedHash)

    def getSMS(self):
        return self._mySortedHash

    def _getSmsPosteriorTo(self, aDate, aN900, aN9):
        myHash = {}
        # myN900Date = aN900.getLastDate()
        for key, values in aN9.getSMS().items():
            if values['date'] > aDate:
                myHash[key] = values
        print('unique elements : ', len(myHash))
        return myHash

    def _mergeHashes(self, aN900, aN9):
        myHash = self._getSmsPosteriorTo(aN900.getLastDate(), aN900, aN9)
        myN900SMS = aN900.getSMS().copy()
        for key, value in myHash.items():
            myN900SMS[key] = value
        return myN900SMS

    # def _mergeHashes(self, aFstHash, aSndHash):
    #     if len(aSndHash) <= len(aFstHash):
    #         aShorterHash = aSndHash
    #         aLongerHash = aFstHash
    #     else:
    #         aShorterHash = aFstHash
    #         aLongerHash = aSndHash

    #     myDuplicate = 0
    #     myHash = {}
    #     for elem in aLongerHash:
    #         if elem in aShorterHash:
    #             fstStr = """""".join([aShorterHash[elem]['body']])
    # fstStr = aShorterHash[elem]['body']
    #             sndStr = """""".join([aLongerHash[elem]['body']])
    # sndStr = aLongerHash[elem]['body']
    # print('N9 Body : ', fstStr)
    # print('N900 body : ', sndStr)
    # RE_STR = re.compile(''.join(['^', fstStr, '$']))
    # if RE_STR.search(sndStr):
    #             myRatio = SeqM(None, fstStr, sndStr).ratio()
    # print('myratio : ', myRatio)
    #             if myRatio != 1.0:
    # if fstStr != sndStr:
    # if aShorterHash[elem]['body'] !=
    # aLongerHash[elem]['body']:
    #                 myDiffer = Differ(linejunk=ignore_ws_nl)
    #                 pprint(
    #                     list(myDiffer.compare(fstStr.splitlines(1), sndStr.splitlines(1))))
    #                 myHash[elem] = aShorterHash[elem]
    #                 print('N9 Body : \n', aShorterHash[elem]['body'])
    #                 print('---')
    #                 print('N900 body : \n', aLongerHash[elem]['body'])
    #             else:
    #                 myDuplicate += 1
    #         else:
    #             myHash[elem] = aLongerHash[elem]
    #     print('Duplicate elements found : ', myDuplicate)
    #     return myHash

    def _sortHash(self, aHash):
        myL = [tuple(elem.split('_')) for elem in aHash]
        # print('myL : ', myL)
        myL = sorted(myL, key=itemgetter(0))
        myDict = collections.OrderedDict()
        for elem in myL:
            key = elem[0] + '_' + elem[1]
            myDict[key] = aHash[key]
        return myDict
