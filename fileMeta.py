import shlex
import json
import subprocess

class fileMeta:
    def __init__(self, res, duration, codec, bitrate, encoder, fps):
        self.res = res
        self.duration = duration
        self.codec = codec
        self.bitrate = bitrate
        self.encoder = encoder   
        self.fps = fps
        
def getMetaData(file, logger):
    cmd = "ffprobe -v quiet -print_format json -show_streams"
    args = shlex.split(cmd) #I was hoping I didn't need this but I need to actually split it instead of changing the command to an array on its own
    args.append(file)
    try:
        metadata = subprocess.check_output(args)
        metadata = json.loads(metadata)
        return metadata
    except:
        logger.error('Subprocess command returned non-zero exit status 1')
        metadata = ''
        return metadata