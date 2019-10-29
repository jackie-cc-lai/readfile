import sys
import ffmpeg

#Test if file is mov/mp4 or not
if sys.argv[1].lower().endswith(('.mov', '.mp4')):
    print("Correct file!")
	
else:
    print("The program is intended for mov and mp4 files only, please try again")