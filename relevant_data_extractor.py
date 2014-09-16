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

import json
import urllib
import urllib2
import httplib
import sys
import datetime
from dateutil import parser
from bs4 import BeautifulSoup

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    

minyear = '1978'
url = "http://badc.nerc.ac.uk/cgi-bin/midas_stations/search_by_county.cgi.py?county=%s&minyear="+minyear+"&maxyear=2014&current=y&db=midas_stations&orderby=start"

cities = ['ABERDEENSHIRE','ANGUS','ANTRIM','ARGYLL (IN HIGHLAND REGION)','ARGYLL (IN STRATHCLYDE REGION)','ARGYLLSHIRE','ARMAGH','AVON','AYRSHIRE','BANFFSHIRE','BEDFORDSHIRE','BERKSHIRE','BERWICKSHIRE','BORDERS','BRECKNOCKSHIRE','BUCKINGHAMSHIRE','BUTESHIRE','CAERNARFONSHIRE','CAITHNESS','CAMBRIDGESHIRE','CARDIGANSHIRE','CARLOW','CARMARTHENSHIRE','CAVAN','CENTRAL','CHESHIRE','CLACKMANNANSHIRE','CLARE','CLEVELAND','CLWYD','CORK','CORNWALL','CUMBERLAND','CUMBRIA','DENBIGHSHIRE','DERBYSHIRE','DEVON','DONEGAL','DORSET','DOWN','DUBLIN','DUMFRIES & GALLOWAY','DUMFRIESSHIRE','DUNBARTONSHIRE','DURHAM','DYFED','EAST LOTHIAN','EAST SUSSEX','ESSEX','FERMANAGH','FIFE','FLINTSHIRE','FORFARSHIRE','GALWAY','GLAMORGANSHIRE','GLOUCESTERSHIRE','GRAMPIAN','GREATER LONDON','GREATER MANCHESTER','GWENT','GWYNEDD','HAMPSHIRE','HEREFORD','HEREFORD & WORCESTER','HERTFORDSHIRE','HIGHLAND','HUMBERSIDE','HUNTINGDONSHIRE','INVERNESS-SHIRE','ISLE OF ANGLESEY','ISLE OF WIGHT','KENT','KERRY','KILDARE','KILKENNY','KINCARDINESHIRE','KINROSS-SHIRE','KIRKCUDBRIGHTSHIRE','LANARKSHIRE','LANCASHIRE','LAOIS','LEICESTERSHIRE','LEITRIM','LIMERICK','LINCOLNSHIRE','LONDONDERRY','LONGFORD','LOTHIAN','LOUTH','MAYO','MEATH','MERIONETHSHIRE','MERSEYSIDE','MIDDLESEX','MID GLAMORGAN','MIDLOTHIAN','MIDLOTHIAN (IN BORDERS REGION)','MIDLOTHIAN (IN LOTHIAN REGION)','MONAGHAN','MONMOUTHSHIRE','MONTGOMERYSHIRE','MORAY','MORAY (IN GRAMPIAN REGION)','MORAY (IN HIGHLAND REGION)','NAIRNSHIRE','NORFOLK','NORTHAMPTONSHIRE','NORTHUMBERLAND','NORTH YORKSHIRE','NOTTINGHAMSHIRE','OFFALY','ORKNEY','OXFORDSHIRE','PEEBLESHIRE','PEMBROKESHIRE','PERTHSHIRE','PERTHSHIRE (IN CENTRAL REGION)','PERTHSHIRE (IN TAYSIDE REGION)','POWYS','POWYS (NORTH)','POWYS (SOUTH)','RADNORSHIRE','RENFREWSHIRE','ROSCOMMON','ROSS & CROMARTY','ROXBURGHSHIRE','RUTLAND','SELKIRKSHIRE','SHETLAND','SHROPSHIRE','SLIGO','SOMERSET','SOUTH GLAMORGAN','SOUTH YORKSHIRE','STAFFORDSHIRE','STIRLING','STIRLING (IN CENTRAL REGION)','STIRLING (IN STRATHCLYDE REGION)','STRATHCLYDE','SUFFOLK','SURREY','SUSSEX','SUTHERLAND','TAYSIDE','TIPPERARY','TYNE & WEAR','TYRONE','WARWICKSHIRE','WATERFORD','WESTERN ISLES','WEST GLAMORGAN','WEST LOTHIAN','WEST LOTHIAN (IN CENTRAL REGION)','WEST LOTHIAN (IN LOTHIAN REGION)','WESTMEATH','WEST MIDLANDS','WESTMORLAND','WEST SUFFOLK','WEST SUSSEX','WEST YORKSHIRE','WEXFORD','WICKLOW','WIGTOWNSHIRE','WILTSHIRE','WORCESTERSHIRE','YORKSHIRE']

if len(sys.argv):
	minyear = sys.argv[1]

f = open('processed_data_'+minyear+'.dat','w')
f2 = open('processed_location_detailed_'+minyear+'.csv','w')
f3 = open('links_'+minyear+'.html','w')

##should be stations.
total_valid_stations = 0
total_stations = 0
total_valid_counties = 0
contentHTML = '<html><h1>Valid Counties With Valid Stations</h1><ul>'
v_print = None

    
def main():

	global total_valid_counties

	ctr = 0;
	total = len(cities)
	
	global total_valid_counties
	total_valid_counties = 0
	
	global total_valid_stations 
	total_valid_stations = 0
	
	global total_stations
	total_stations = 0
	
	
	for _city in cities:
		current_url =  url %_city
		req = urllib2.Request(current_url)
		opener = urllib2.build_opener()
		req.get_method = lambda: 'GET'
		f = opener.open(req)
		res = urllib2.urlopen(req)
		ctr=ctr+1
		print bcolors.OKGREEN + _city + ": " + str(ctr) + " of " + str(total)
		process(res.read(), _city)

	f.close()
	f2.close()
	f3.write(contentHTML+"</ul></html>\n")
	f3.close()
	print  bcolors.OKGREEN
	print  bcolors.OKGREEN
	print  bcolors.OKGREEN + "------------------------------------------------"	
	print  bcolors.OKGREEN + "Total Counties: " + str(ctr)
	print  bcolors.OKGREEN + "Total Valid Counties: " + str(total_valid_counties)
	print  bcolors.OKGREEN + "Total Stations: " + str(total_stations)
	print  bcolors.OKGREEN + "Total Valid Stations: " + str(total_valid_stations)
	print  bcolors.OKGREEN + "------------------------------------------------"	
def process(html_content, city_name):
	
	global total_stations
	global total_valid_stations
	global minyear
	
	soup = BeautifulSoup(html_content)
	table = soup.find_all('table')

	rows = table[2].findAll('tr')
	usablevar = ''
	if(len(rows)>0):
		rows.pop(0)

	
		for tr in rows:
		  cols = tr.findAll('td')
		  if len(cols):
			new_format = "%d-%m-%Y"
			total_stations=total_stations+1
			dt = parser.parse(cols[4].find(text=True))
			if(dt<=parser.parse('01-01-'+minyear)):
				total_valid_stations=total_valid_stations+1
				usablevar = usablevar+str(cols[0].find(text=True))+" "
				
				lat = 	str(cols[6].find(text=True))
				lng = 	str(cols[7].find(text=True))
				station_code = str(cols[0].find(text=True))
				
				f2.write(station_code.strip()+","+ city_name.strip() +","+ lat.strip() +","+ lng.strip() + "\n")
			
	usablevar = usablevar.strip()
	if len(usablevar) != 0:
		f.write(city_name + "\n"+ usablevar + "\n\n");
		writeToHTML(usablevar, city_name)
		print bcolors.OKGREEN + str(len(usablevar)) + " Valid Stations."
		print
	else:
		print bcolors.WARNING + "No Valid Stations."
		print

def writeToHTML(stations, county):
    
    global total_valid_counties
    total_valid_counties=total_valid_counties+1
    
    global contentHTML
    content  = '%2Fwps%3FRequest%3DExecute%26Identifier%3DExtractUKStationData%26Format%3Dtext%2Fxml%26Inform%3Dtrue%26Store%3Dfalse%26Status%3Dfalse%26DataInputs%3DStationIDs%3D'+urllib.quote_plus(stations.replace(' ','|'))+'%3BEndDateTime%3D2014-01-01T00%253A00%253A00%3BDelimiter%3Dcomma%3BObsTableName%3DWH%3BOutputTimeChunk%3Dyear%3BBBox%3D-12.00%257C49.00%257C3.00%257C61.00%3BStartDateTime%3D'+minyear+'-01-01T00%253A00%253A00%3BInputJobId%3D%3BCounties%3D'+urllib.quote_plus(county)
    contentHTML = contentHTML + '<li><a href="http://ceda-wps2.badc.rl.ac.uk/submitter?wps_request_url='+content+'&proc_id=ExtractUKStationData" target="_blank">'+county+'</a></li>'+'\n\n'
		
if __name__ == "__main__":
    main()