#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import N900SMSHandler as N900
import N9SMSHandler as N9
import databaseHandler as DB
import SMSMerger as SMS


parser = argparse.ArgumentParser(
    description='Merge sms from n900 and n9 in a new n900 database')
parser.add_argument(
    '--n900_last_db', '-n900l',
    help='path to our sqlite file', required=False)
parser.add_argument(
    '--n9_folder', '-n9f',
    help="""path to a folder containing .vmg\
     exported from a n9\'s backup with nbuexplorer""", required=True)
parser.add_argument(
    '--output_sql_file', '-osql',
    help='path to our output sqlite file',
    required=True)
parser.add_argument(
    '--n900_first_db', '-n900f',
    help='path to our output sqlite file',
    required=True)
args = parser.parse_args()

if args.n900_last_db:
    myLastDb = args.n900_last_db
else:
    myLastDb = None
if args.n9_folder:
    myFolder = args.n9_folder
if args.output_sql_file:
    myNewDb = args.output_sql_file
if args.n900_first_db:
    myFirstDb = args.n900_first_db


myFN900 = N900.N900SMSHandler(myFirstDb)
myN9 = N9.N9SMSHandler(myFolder)
mySMSMerger = SMS.SMSMerger(myFN900, myN9)
myGroupUIDHash = myFN900.getGroupUIDHash
myPathToDbToBeCopied = myFirstDb
if myLastDb:
    myN9.setSMS(mySMSMerger.getSMS(), myN9.getLastDate())
    myLN900 = N900.N900SMSHandler(myLastDb)
    mySMSMerger = SMS.SMSMerger(myN9, myLN900)
    myGroupUIDHash = myLN900.getGroupUIDHash()
    myPathToDbToBeCopied = myLastDb
    # myN9.setSMS(mySMSMerger.getSMS(), myN9.getLastDate())
else:
    myLastDb = myFirstDb
mySMSMerger = SMS.SMSMerger(myN9, myLN900)
DB.copyDatabaseAndAddSms(
    myPathToDbToBeCopied, myNewDb, mySMSMerger.getSMS(), myGroupUIDHash)
