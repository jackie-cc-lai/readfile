## This repository is created as part of SavvyPro's coding question

The program gets a filename argument from command line, as such:

### >> python read_fileinfo.py \<filename\>

where \<filename\> is the file including its suffix, and returns video_info.csv, info.log, and error.log. Errors, including non-existing file, incorrect filetype, and error parsing files are stored into error.log, while all
other information is stored within info.log, including program start, duration, processes during runtime, and program termination.

The file in question must be stored in the same directory as read_fileinfo.py.