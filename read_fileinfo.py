import sys
import ffmpeg
import re
from ffpyplayer.player import MediaPlayer
import time
import csv
import os
import logging
from logFilter import LogFilter
from fileMeta import fileMeta
from fileMeta import getMetaData
from convertmov import makemp4

start_time = time.time()
#Use regex to test if file is mp4/mov or not (use regex because we need to make sure files like ..mp4 isn't passed through - in other cases the OS itself would likely disallow such)
file_true = re.search('^[\w\W]+ *(?:.mp4|.mov)$', sys.argv[1].lower())
# create loggers
logger = logging.getLogger('info')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
nf = logging.FileHandler('info.log')
nf.setLevel(logging.DEBUG)
# create console handler with a higher log level
er = logging.FileHandler('error.log')
er.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
nf.setFormatter(formatter)
er.setFormatter(formatter)
# add the handlers to the logger
nf.addFilter(LogFilter(logging.INFO))
er.addFilter(LogFilter(logging.ERROR))
logger.addHandler(nf)
logger.addHandler(er)

logger.info("Program started")

def getFinalTime():
    logger.info('Program terminated')
    dur = str(time.time() - start_time)
    logger.info('Duration: ' + dur)
    
if (file_true):
    if ( not os.path.exists(sys.argv[1]) ): #If the filename is wrong with the right suffix to prevent error when trying to read the file
        print("File does not exist, please try again")
        logger.error('File does not exist')
        getFinalTime()
    else:
        #We now read the metadata via ffmpeg/ffprobe
        logger.info('Retrieving metadata from file for processing')
        filemeta = getMetaData(sys.argv[1])
        if filemeta != '':  
            #get the hours, min, sec, ms from the duration variable
            logger.info('Parsing file duration')
            fileLength = filemeta['streams'][0]['duration']
            fileLength = float(fileLength)
            fileHours = int(fileLength / 3600)
            fileMin = int(fileLength/60 - fileHours*60)
            fileSec = int(fileLength - fileMin*60 - fileHours*3600)
            fileMs = int((fileLength - fileSec - fileMin*60 - fileHours*3600)*1000)
            # Standardize how it looks
            if fileHours == 0:
                fileHours = '00'
            else: 
                fileHours = str(fileHours)
            if fileMin == 0:
                fileMin = '00'
            else: 
                fileMin = str(fileMin)
            if fileSec == 0:
                fileSec = '00'
            else: 
                fileSec = str(fileSec)
            if fileMs == 0:
                fileMs = '00'
            else: 
                fileMs = str(fileMs)
             
            #changing int to string now that the operations are done
            duration = fileHours+ " hr "+fileMin+" min " + fileSec+" sec " + fileMs + " ms"
            logger.info('Parsing video frames per second')
            filefps = filemeta['streams'][0]['r_frame_rate']
            filefps = filefps.split("/")
            filefps = round(int(filefps[0])/int(filefps[1]))
            logger.info('parsing file resolution')
            res = str(filemeta['streams'][0]['width'])+ "px width "+ str(filemeta['streams'][0]['height']) +"px height"
            bitrate = filemeta['streams'][0]['bit_rate']
            bitrate = round(int(bitrate)/1000)
            bitrate = str(bitrate) + "kb/s"
            #storing into class
            logger.info('parsing all data into class')
            fileData = fileMeta(res, duration, filemeta['streams'][0]['codec_type'], bitrate, filemeta['streams'][0]['codec_long_name'], filefps)
            #writing to csv file
            logger.info('Writing to csv file')
            with open('video_info.csv', 'a', newline='') as csvWrite:
                file_write = csv.writer(csvWrite, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                file_write.writerow([fileData.res, fileData.duration,fileData.bitrate,fileData.codec,fileData.encoder, fileData.fps])
                
            if sys.argv[1].endswith('.mov'):
                logger.info('mov file initiating conversion')
                makemp4(sys.argv[1])
                logger.info('mov file finished conversion')
                
            getFinalTime()
        else:
            print("File corrupted")
            logger.error("File corrupted")
            getFinalTime()
            
else: #file is not of type mov or mp4
    print("The program is intended for mov and mp4 files only, please try again")
    logger.error('Filetype Incorrect')
    getFinalTime()