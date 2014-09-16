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

import math
import geohash
import csv
import sys

f = open('points.csv','w')


def distanceCal(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d
   
def main():
	points = []
	
	datafilename="processed_data_1978.csv"
	distance_radius = 50
	
	if len(sys.argv):
		datafilename = sys.argv[1]
	
	if len(sys.argv):
		distance_radius = sys.argv[2]


	f_raw = open(datafilename, 'rb')
	try:
		reader = csv.reader(f_raw)
		for row in reader:
			points = points + [row]
	finally:
		f_raw.close()
            
	selected_points = [points[0]];
	
	
	for p in points:
		is_valid = True
		origin  = [float(p[2]),float(p[3])]
		for x in selected_points:
			temp = []
			dest = [float(x[2]),float(x[3])]
			distance  = distanceCal(origin,dest)
			if distance<int(distance_radius):
				is_valid=False
				break

		if is_valid==True:
			selected_points = selected_points+[p]
	
  	for val in selected_points:
  		f.write(str(val[0])+","+str(val[1])+","+str(val[2])+","+str(val[3])+"\n")
  		
  	f.close()

	print "Original Stations Available: "+str(len(points))
	print "Reduced Clustered Stations: "+str(len(selected_points))

if __name__ == "__main__":
    main()
