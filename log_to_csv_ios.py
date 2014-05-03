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
Dec 21 15:08:23 QAsiPod-touch5 Ericsson_SamplePlayer[8615] <Warning>: >>>>>>>>>>stop start  = 1387609703754.068848 ms 
Dec 21 15:08:23 QAsiPod-touch5 Ericsson_SamplePlayer[8615] <Warning>: >>>>>>>>>>stop end  = 1387609703936.304932 ms, stop using time: 182.255859 
Dec 21 15:08:23 QAsiPod-touch5 Ericsson_SamplePlayer[8615] <Warning>: >>>>>>>>>>close end  = 1387609703942.266846 ms, close using time: 1.860107 
Dec 21 15:08:24 QAsiPod-touch5 Ericsson_SamplePlayer[8615] <Warning>: >>>>>>>>>>open itself using  = 65.493896 ms 
Dec 21 15:08:24 QAsiPod-touch5 Ericsson_SamplePlayer[8615] <Warning>: >>>>>>>>>>run end  = 1387609704297.486084 ms run using time = 3.030029 
Dec 21 15:08:24 QAsiPod-touch5 Ericsson_SamplePlayer[8615] <Warning>: >>>>>>>>>>open to render time = 977.492988 ms 
Dec 21 15:08:24 QAsiPod-touch5 Ericsson_SamplePlayer[8615] <Warning>: >>>>>>>>>>render start  = 1387609704976.329102 ms 
"""

stop_start = "(.*>>>>>>>>>>stop start  = )(\d*\.\d*)( ms )?"
stop_using = "(.*>>>>>>>>>>stop end.*stop using time: )(\d*\.\d*)( ms )?"
close_using = "(.*>>>>>>>>>>close end.*close using time: )(\d*\.\d*)( ms )?"
open_using = "(.*>>>>>>>>>>open itself using  = )(\d*\.\d*)( ms )?"
run_using = "(.*>>>>>>>>>>run end.*run using time = )(\d*\.\d*) "
open_render = "(.*>>>>>>>>>>open to render time = )(\d*\.\d*)( ms )?"
render_start = "(.*>>>>>>>>>>render start  = )(\d*\.\d*)( ms )?"

patternDic = {"stop_start": stop_start,
              "stop_using": stop_using,
              "close_using": close_using,
              "open_using": open_using,
              "run_using": run_using,
              "open_render": open_render,
              "render_start": render_start}

patternList = ["stop_start", "stop_using", "close_using", "open_using",
               "run_using", "open_render", "render_start", "zapping_time"]

writer.writerow(patternList)


def segmentLog(logfile):
    f = open(logfile, "rb")
    flag = 1  # flag for readline
    segment_mark = ".*>>>>>>>>>>render start  =.*"
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
                segmentDicList[key] = float(result.group(2))
                # print result.group(2)
            else:
                segmentDicList[key] = ""
        segmentList.append([segmentDicList[key] for key in patternList])
    return segmentList


if __name__ == '__main__':
    line_list = text2list(log_file)
    for i in line_list:
        # print i
        writer.writerow(i)
    csvfile.close()
