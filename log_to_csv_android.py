# -*- coding:utf-8 -*-

import re
import os
import csv
import sys

log_file = sys.argv[1]
# log_file = r"csv.log"
# csv_content = []
# new_csv = sys.argv[2]
# new_csv = r"result.csv"
csv_name = os.path.splitext(log_file)[0] + ".csv"
csvfile = file(csv_name, 'wb')
writer = csv.writer(csvfile)

"""
12-12 16:46:39.942 I/TimeCal Stop <---(27363): Current Time: 1386837999947 ms.\
 Time delta: 91 ms
12-12 16:46:40.047 I/TimeCal Close <---(27363): Current Time: \
1386838000050 ms. Time delta: 103 ms
12-12 16:46:40.142 I/TimeCal Open <---(27363): Current Time: \
1386838000148 ms. Time delta: 98 ms
12-12 16:46:55.087 I/TimeCal Run <---(27363): Current Time: \
1386838015092 ms. Time delta: 4 ms
12-12 16:48:41.217 I/TimeCal Receive VOOSMP_CB_VideoStopBuff <---(27363): \
Current Time: 1386838121220 ms. Time delta: 15200 ms
12-12 16:48:41.217 I/TimeCal Receive VideoRenderStart <---(27363): \
Current Time: 1386838121220 ms. Time delta: 0 ms
"""

# pattern_Stop = """"(\d{2}-\d{2}:\d{2}:\d{2}.\d{3}\D* )(Stop)( <---.*)\
# (Time delta: )(\d+) ms$"""
# pattern_Stop = "(.*)(Stop)( <---.*)(Time delta: )(\d+) ms$"
# pattern_Close = "(.*)(Close)( <---.*)(Time delta: )(\d+) ms$"
# pattern_Open = "(.*)(Open)( <---.*)(Time delta: )(\d+) ms$"
# pattern_Run = "(.*)(Run)( <---.*)(Time delta: )(\d+) ms$"
# pattern_VideoStopBuff = """(.*Receive )(VOOSMP_CB_VideoStopBuff)( <---.*)\
# (Time delta: )(\d+) ms$"""
# pattern_VideoRenderStart = """(.*Receive )(VideoRenderStart)( <---.*)\
# (Time delta: )(\d+) ms$"""
# pattern_Drm = "(.*)(Init Drm server.*)( <---.*)(Time delta: )(\d+) ms$"
pattern_Stop = "(Stop) <---.* Time delta: (\d*) ms"
pattern_Close = "(Close) <---.* Time delta: (\d*) ms"
pattern_Open = "(Open) <---.* Time delta: (\d*) ms"
pattern_Run = "(Run) <---.* Time delta: (\d*) ms"
pattern_VideoStopBuff = "(VOOSMP_CB_VideoStopBuff) <---.* Time delta: (\d*)"
pattern_VideoRenderStart = "(Receive VideoRenderStart) <---.*Time delta: (\d*)"
# pattern_Drm = "(Init Drm server.*) <---.*Time delta: (\d*) ms$"

patternDic = {"Stop": pattern_Stop,
              "Close": pattern_Close,
              "Open": pattern_Open,
              "Run": pattern_Run,
              "VideoStopBuff": pattern_VideoStopBuff,
              "VideoRenderStart": pattern_VideoRenderStart}

patternList = ["Stop", "Close", "Open", "Run",
               "VideoRenderStart", "VideoStopBuff"]

writer.writerow(patternList)


def segmentLog(logfile):
    f = open(logfile, "rb")
    flag = 1  # flag for readline
    segment_mark = ".*VideoRenderStart <---.*"
    tempList = []  # counter for readline
    content = []

    while flag:
        line = f.readline()
        tempList.append(line)
        if re.search(segment_mark, line):  # keyword is in that line
            temp = ''.join(tempList)
            content.append(temp)
            tempList = []
        else:
            pass
        if not line:
            flag = 0
            break
    return content


def text2list(log_file):
    """translate text segment to new dictionary: {"Stop":xx, "Close":yy..}"""
    # content = open("1.txt", "rb").read()
    content = segmentLog(log_file)
    segmentDicList = {}
    segmentList = []
    for segment in content:
        # print segment
        for key, vaule in patternDic.items():
            # print key
            # print vaule
            result = re.search(vaule, str(segment))
            # print result
            if result:
                segmentDicList[key] = result.group(2)
                # print result.group(2)
            else:
                segmentDicList[key] = " "
        segmentList.append([segmentDicList[key] for key in patternList])
    return segmentList


if __name__ == '__main__':
    line_list = text2list(log_file)
    for i in line_list:
        # print i
        writer.writerow(i)
    csvfile.close()
