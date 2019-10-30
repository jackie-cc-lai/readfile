from ffmpy import ffmpeg
import ffmpy

def makemp4(file):
    fileName = file[:-4] #Remove the .mov designation
    fileName = fileName+'.mp4' #add the new suffix
    ff = ffmpy.FF(inputs={file:None}, outputs={fileName:'-c:v h264 -c:a ac3'})
    ff.cmd_str
    ff.run()