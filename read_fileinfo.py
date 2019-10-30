import sys
import ffmpeg
import re
from ffpyplayer.player import MediaPlayer
import subprocess
import shlex
import json
import csv

#Use regex to test if file is mp4/mov or not (use regex because we need to make sure files like ..mp4 isn't passed through)
file_true = re.search('^[^.]*(?:.mp4|.mov)$', sys.argv[1].lower())

def getMetaData(file):
    cmd = "ffprobe -v quiet -print_format json -show_streams"
    args = shlex.split(cmd) #I was hoping I didn't need this but I need to actually split it instead of changing the command to an array on its own
    args.append(file)
    metadata = subprocess.check_output(args)
    metadata = json.loads(metadata)
    return metadata
 
 
class fileMeta:
    def __init__(self, res, duration, codec, bitrate, encoder, fps):
        self.res = res
        self.duration = duration
        self.codec = codec
        self.bitrate = bitrate
        self.encoder = encoder   
        self.fps = fps
    


if (file_true):
    if(sys.argv[1].lower() == '.mp4' or sys.argv[1].lower() == '.mov'):
        print("The program is intended for mov and mp4 files only, please try again") #Edge case - if the entry is literally just the suffix itself (since thats just not a file)
    else:
        #We now read the metadata via ffmpeg/ffprobe
        filemeta = getMetaData(sys.argv[1])
        
        #get the hours, min, sec, ms from the duration variable
        fileLength = filemeta['streams'][0]['duration']
        fileLength = float(fileLength)
        fileHours = int(fileLength / 3600)
        fileMin = int(fileLength/60 - fileHours*60)
        fileSec = int(fileLength - fileMin*60 - fileHours*3600)
        fileMs = int((fileLength - fileSec - fileMin*60 - fileHours*3600)*1000)
        filefps = filemeta['streams'][0]['r_frame_rate']
        
        filefps = filefps.split("/")
        filefps = round(int(filefps[0])/int(filefps[1]))

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
        duration = fileHours+ " hr "+fileMin+" m " + fileSec+" s " + fileMs + " ms"
        res = str(filemeta['streams'][0]['width'])+ "px width "+ str(filemeta['streams'][0]['height']) +"px height"
        
        #storing into class
        fileData = fileMeta(res, duration, filemeta['streams'][0]['codec_type'], filemeta['streams'][0]['bit_rate'], filemeta['streams'][0]['codec_long_name'], filefps)

        #writing to csv file
        with open('video_info.csv', 'a') as csvWrite:
            file_write = csv.writer(csvWrite, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            file_write.writerow( [fileData.res, fileData.duration,fileData.bitrate,fileData.codec,fileData.encoder, fileData.fps])
            
else: #file is not of type mov or mp4
    print("The program is intended for mov and mp4 files only, please try again")