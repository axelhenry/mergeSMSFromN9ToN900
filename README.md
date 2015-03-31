# mergeSMSFromN9ToN900

##Goal:

Providing a way to merge back your sms from a backup of your dead N9 to your working N900

##Usage:

./launcher.py -n900_first_db 'path/to/el-v1.db' -n9_folder 'path/to/vmg/files' -osql 'path/to/new/db'

or if you have multiple n900 databases

./launcher.py -n900_first_db 'files/el-v1_before_import_in_N9.db' -n900_last_db 'files/el-v1_31_07_2015.db' -n9_folder 'files/N9/' -osql 'files/test_export.db'

##Dependencies:

To use this script you'll need :
- python3
- arrow (pip install arrow, see http://crsmithdev.com/arrow/#quickstart)
- sqlite3

##Sidenotes:

- The database holding sms in your n900 can be found in /home/user/.rtcomm-eventlogger/
- Use NbuExplorer on one of your n9 backup to extract sms, each sms will be in .vmg file
- First version of this utility, works with french mobile phone numbers only. Can be changed by modifying the regular expression in utilities.py

##Thanks to:
- pyvmg's developers
