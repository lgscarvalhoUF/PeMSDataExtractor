# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 18:36:45 2019

@author: lstaichakcarvalh


options dictionary entries and properties:

-------------------
#Sensor list setup:   
- draw_number:   the number of sensors to be extracted using a 'draw_opt' option.    
                Input: integer           

- draw_opt:     choose a draw setting for choosing sensors.
                Input options: 'first','last','random'
    - 'first':  will extract the first 'draw_number' elements of the seg. class set.
    - 'last':   will extract the last 'draw_number' elements of the seg. class set.
    - 'random': will extract 'draw_number' random sensors from the seg. class set.

- number_of_lanes: the number of lanes for all segments being evaluated.
                Input: integer

- segmenttype:  the segment class set you want to use.
                Input options: 'basic'
    
- sensor_list:  these are the sensors you want to download. 
                Input options: list, 'custom', 'all'
    - list:     a list of integer numbers, each number corresponding to a sensor;
    - 'all':    will download data for all sensors corresponding to segmenttype 
                class entry;
    - 'custom': will download a custom set of sensors, according to 'draw_opt' 
                and 'draw_number' entries;
--------------------
#Data treatment setup
    The following options indicate the ascending order for evaluating the absolute
    position of each sensor in each freeway.
    - N_abspos
    - S_abspos
    - E_abspos
    - W_abspos
--------------------
#Date setup
    The following options indicate the start and end date for the data collection.
    Please notice that the algorithm will look inside this interval in order to
    select VALID dates (no holidays, not weekends, etc.)
    Input: string. Format: month(2digits)/day(2digits)/year(4digits). Example: 02/01/2019 
    - start_date
    - end_date
    
    The following options indicate the start and end hours for the data collection.
    Input: string. Format (24 hours): hour(2digits):minutes(2digits):seconds(2digits). Example: 17:50:00
    - start_hour
    - end_hour
    
- time_zone:This string should inform the local time zone of the data collection site.
            It might not be needed anymore. Please refer to 
            https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
            for a list of time zone codes.
            Input: string.
--------------------
"""
import pandas as pd

options={
#    'pems_state':'mn',
    'download_directory':r'C:\Users\lstaichakcarvalh\Documents\NCHRPData\Field data for validation',
    'treated_files_dir':r'C:\Users\lstaichakcarvalh\Documents\NCHRPData\Treated sensors',
    'download_chromedir': 'C:\\Users\\lstaichakcarvalh\Downloads',
    #--------------------
    #Sensor list setup:     
    'draw_number': 10,
    'draw_opt': 'random',    
    "number_of_lanes":3, 
    'segmenttype':'Weaving',
#    "sensor_list":[500014082],
    "project_sensor_id":98,
#    "upstream_detector":1000500,
    #--------------------
    #Data treatment setup
    'N_abspos':'ascending',
    'S_abspos':'descending',
    'E_abspos':'ascending',
    'W_abspos':'descending',
    #--------------------
    #Date setup
#     'days_range':7, 
#    "start_date":str(start_date),
    "start_hour":'00:00:00',
#    "end_date":str(end_date),   
    "end_hour":'23:59:00',    
    "time_zone": 'America/Tijuana',
#    "time_correction":18000, #due t1o local time issues
   #--------------------
   # Capacity Analysis Parameters
	"SpeedLimQuantile":0.9,
	'SpeedDropTreshold':0.15,
	'CapacityAdoptPercentile':0.85,
}


detectorinfo = pd.read_excel('inputs\HCSProject.xlsx',sheet_name='Detector Info')
#print(len(detectorinfo))
detectorinfo = detectorinfo.dropna(subset=['Number'])
#print(len(detectorinfo))
detectorinfo['Number'] = detectorinfo['Number'].astype('int64')
#detectorinfo['Number'] = detectorinfo['Number'].astype('str')
#detectorinfo['Initial_date'].astype('datetime64[ns]') 
startdate = detectorinfo.loc[detectorinfo['Number'] == (options["project_sensor_id"]),'Initial_date'].iloc[0]
enddate = detectorinfo.loc[detectorinfo['Number'] == (options["project_sensor_id"]),'Final_Date'].iloc[0]

options["start_date"]='%s/%s/%s' %(str(startdate.month).rjust(2,'0'),
                                   str(startdate.day).rjust(2,'0'),
                                   str(startdate.year).rjust(4,'0'))
       
options["end_date"]='%s/%s/%s' %(str(enddate.month).rjust(2,'0'),
                                   str(enddate.day).rjust(2,'0'),
                                   str(enddate.year).rjust(4,'0'))


if options['segmenttype'] in ['Merge','Diverge']:
    sensor_ids = []
    sensor_ids.append(int(detectorinfo.loc[detectorinfo['Number'] == (options["project_sensor_id"]),'Detector 1 (Upstream/ML)'].iloc[0]))
    sensor_ids.append(int(detectorinfo.loc[detectorinfo['Number'] == (options["project_sensor_id"]),'Detector 2 (Downstream)'].iloc[0]))
    sensor_ids.append(int(detectorinfo.loc[detectorinfo['Number'] == (options["project_sensor_id"]),'Detector 3 (Ramp)'].iloc[0]))
    options["sensor_list"]=sensor_ids
elif options['segmenttype'] == 'Weaving':
    sensor_ids = []
    sensor_ids.append(int(detectorinfo.loc[detectorinfo['Number'] == (options["project_sensor_id"]),'Detector 1 (Upstream/ML)'].iloc[0]))
    sensor_ids.append(int(detectorinfo.loc[detectorinfo['Number'] == (options["project_sensor_id"]),'Detector 2 (Downstream)'].iloc[0]))
    sensor_ids.append(int(detectorinfo.loc[detectorinfo['Number'] == (options["project_sensor_id"]),'Detector 3 (Ramp)'].iloc[0]))
    sensor_ids.append(int(detectorinfo.loc[detectorinfo['Number'] == (options["project_sensor_id"]),'Detector 4'].iloc[0]))
    options["sensor_list"]=sensor_ids
    
else:
    sensor_ids = detectorinfo.loc[detectorinfo['Number'] == (options["project_sensor_id"]),'Detector 1 (Upstream/ML)'].iloc[0]
    options["sensor_list"]=[sensor_ids]

options["pems_state"] = detectorinfo.loc[detectorinfo['Number'] == (options["project_sensor_id"]),'State'].iloc[0]

options["lanenumbering"] = detectorinfo.loc[detectorinfo['Number'] == (options["project_sensor_id"]),'Lane1'].iloc[0]

#checking if config is valid
invalidflag = 0
validstates = ['CA','UT','VA']
if options['pems_state'] not in validstates:
    invalidflag = 1
#    print('Invalid State!!!')
