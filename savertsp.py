#ffmpeg -loglevel debug -rtsp_transport tcp -i "rtsp://admin:admin12345@192.168.99.122:554/Streaming/tracks/101?starttime=20190119t224949z&endtime=20190119t225230z" -vcodec copy -an -t 00:01:00 foo.mp4
import sys
from datetime import datetime as dt
import os

RTSPURL = "rtsp://admin:zq888888@192.168.8.135:554/Streaming/tracks/"
FFMPEGEXPBEGIN = "ffmpeg -loglevel debug -rtsp_transport tcp -i"
FFMPEGEXPEND = "-vcodec copy -an -t"
SPACE = " "
FILEDIR = "~/videos/"

class Info:
  def __init__(self, line):
    list = line.split(",")
    self.channel = list[0]
    self.startTimeStr = list[1]
    self.endTimeStr = list[2]
    startTime = dt.strptime(self.startTimeStr, "%Y%m%dt%H%M%Sz")
    endTime = dt.strptime(self.endTimeStr, "%Y%m%dt%H%M%Sz")
    self.duration = endTime - startTime

def openFile():
  file_name = sys.argv[1]
  file = open(file_name)
  contents = file.read()
  file.close()
  return contents

def constructUrl(info):
  finalURL = RTSPURL + info.channel + "?" + "starttime=" + info.startTimeStr + "&" + "endtime=" + info.endTimeStr
  return finalURL

def transformToInfo(line):
  return Info(line)

def constructShell(info):
  url = constructUrl(info)
  name = info.channel + info.startTimeStr + "-" + info.endTimeStr + ".mp4"
  return FFMPEGEXPBEGIN + SPACE + "\"" + url + "\"" + SPACE + FFMPEGEXPEND + SPACE + str(info.duration) + SPACE + FILEDIR + name 

infoContents = openFile()
linelist = filter(lambda x: len(x) > 0, infoContents.split("\n"))
infoList = map(transformToInfo , linelist)
for info in infoList:
  shell = constructShell(info)
  os.system(shell)

