#!/usr/bin/python

'''
The MIT License (MIT)

Copyright (c) 2014 Karthikeya Udupa K M

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import sys
import webbrowser
import os
from datetime import date

minyear = '1978'
distance = 50

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    
def main():

	global minyear
	if len(sys.argv):
		minyear = sys.argv[1]

	global distance
	if len(sys.argv):
		distance = sys.argv[2]
	
	print  bcolors.WARNING + "------------------------------------------------"
	print  bcolors.WARNING + "Finding stations with data: "+ str(minyear) + " - " + str(date.today().year)
	print  bcolors.WARNING + "------------------------------------------------"	
	print  bcolors.WARNING
	
	os.system("./relevant_data_extractor.py "+minyear)
	
	print  bcolors.WARNING + "Clustering stations by area - " + str(distance) + "km"
	print  bcolors.WARNING + "------------------------------------------------"	
	print  bcolors.WARNING
	
	os.system("python map_points.py "+"processed_location_detailed_"+minyear+".csv "+str(distance))
	print  bcolors.WARNING + "------------------------------------------------"	
	print  bcolors.WARNING
	
	# open an HTML file on my own (Windows) computer
	url = "data_points.html?radius="+distance
	webbrowser.open("file://"+os.path.dirname(os.path.abspath(url))+"/"+url)


if __name__ == "__main__":
    main()