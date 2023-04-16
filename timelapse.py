import PIL.ExifTags, PIL.Image
import os
import subprocess
from os import walk
import sys

directory = os.getcwd()
folder = sys.argv[1]

failed = []

for root, dirs, files in os.walk(directory + '/' + folder):
    for file in files:
        if file.endswith(".HEIC"):

            exists = os.path.isfile(directory + '/' + folder + '/' + file.replace("HEIC", "JPG")) or os.path.isfile(directory + '/' + folder + '/' + file.replace("HEIC", "jpg"))
            
            try:
                if not exists:
                    jpeg = subprocess.run(['heic-to-jpg', '-s', directory + '/' + folder, '--keep'])
            except:
                print("Failed to Convert: " + file)

try:
    lapse = subprocess.run(['ffmpeg', 
		            '-framerate', "12",
                            '-pattern_type', "glob",
                            '-i', folder + "/*.jpg",
                            '-s:v', "1440x1080",
			    '-c:v', "prores",
			    '-profile:v', "3",
   			    '-pix_fmt', "yuv422p10",
			    folder + '.mov'])
except Exception as e:
    print("Timelapse Creation Failed: ", e)

if len(failed) > 0:
    print()
    print("-------Failed--------")
    for file in failed:
        print(file['filename'] + file['error'])