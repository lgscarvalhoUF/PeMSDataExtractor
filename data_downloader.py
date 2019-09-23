# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 15:08:55 2019

@author: lstaichakcarvalh
"""

import config #imports the config file with the options dictionary
import time #used for time operations
import datetime #used for time operations as well
import os #used to access and to do basic operations related to folders and files
import numpy as np #used for several commands related to numeric structures
import webbrowser #used to declare basic commands involving web browsers
import shutil #used with os to deal with folders and files
import glob #used to access specific information regarding file storage 
import pandas as pd #used to work with sheet-like structures
import random #provides several randomizing operations
#import sys

#if config.invalidflag == 1:
#    sys.exit("Invalid config file. Please look at check up procedure at the config file.")

number_of_lanes = config.options["number_of_lanes"] #loads the 
segtype = config.options["segmenttype"]

tablesheet = 'Report Data'
descriptionsheet = 'PeMS Report Description'

os.environ['TZ'] = config.options['time_zone']
ddir = config.options['download_directory']+'\\'+config.options['segmenttype']
os.makedirs(ddir,exist_ok=True)

#C:\PeMSFiles\Basic\4L\001\413373\001_413373_201706240000_201706302359.xlsx

dirname = config.options['download_chromedir']

def timelimitsplitter(date,hour):
    sday=int(date.split('/')[1])
    smonth=int(date.split('/')[0])
    syear=int(date.split('/')[2])
    
    shour=int(hour.split(':')[0])
    sminute=int(hour.split(':')[1])
    ssecond=int(hour.split(':')[2])
    
    dtini=datetime.datetime(
            syear,
            smonth,
            sday,
            shour,
            sminute,
            ssecond
            )
    epochtime = int((dtini-datetime.datetime(1970,1,1)).total_seconds())
    inihumandate = time.gmtime(epochtime)
    return [epochtime,inihumandate]

tstart = timelimitsplitter(config.options['start_date'],config.options['start_hour'])
tend =  timelimitsplitter(config.options['end_date'],config.options['end_hour'])

#fullweeks=int((tend[0]-tstart[0])/(7*24*3600))
weekduration = (7*24*3600)

starttimes = np.arange(tstart[0],tend[0],weekduration)
endtimes = np.arange(tstart[0]+weekduration-60,tend[0],weekduration)


#file_input = open('.\\database_pickle\\sensor_info.pkl', 'rb')
#sensorinfo = pickle.load(file_input)
#file_input.close()
#
#
#file_input = open('.\\database_pickle\\baseperlane.pkl', 'rb')
#baseperlane = pickle.load(file_input)
#file_input.close()
#
#baseperlane[number_of_lanes]['id']=pd.to_numeric(baseperlane[number_of_lanes]['id'])

#slist = sorted(list(set(baseperlane[number_of_lanes]['id'])))

if isinstance(config.options['sensor_list'], list) == False:
    if config.options['sensor_list'] == 'all':
#            print('opt a')
        sensor_download_list = slist
    if config.options['sensor_list'] == 'custom':
#            print('opt b')
        if config.options['draw_opt'] == 'first':
            sensor_download_list = slist[0:(config.options['draw_number'])]
        if config.options['draw_opt'] == 'first':
            sensor_download_list = slist[-(config.options['draw_number']):]
        if config.options['draw_opt'] == 'random':
            random.shuffle(slist)
            sensor_download_list = slist[0:(config.options['draw_number'])]            
            slist = sorted(list(set(baseperlane[number_of_lanes]['id'])))
else:
#        print('opt c')
    sensor_download_list = config.options['sensor_list']


#sensor_download_list = [175,1173]

lanefolder = '%iL' %(number_of_lanes)
if __name__ == "__main__":

    #saving the sensor download list to an excel file
    dfsens = pd.DataFrame({'Sensor_name':sensor_download_list})
    pd.DataFrame.to_excel(dfsens,'sensordownloadlist.xlsx')
    
        
        
    os.makedirs(ddir,exist_ok=True)
    timenow =  time.localtime(time.time())
    
#    timenowstring = '%s%s%s%s%s' %(str(timenow[0]).rjust(2,'0'),
#                                       str(timenow[1]).rjust(2,'0'),
#                                       str(timenow[2]).rjust(2,'0'),
#                                       str(timenow[3]).rjust(2,'0'),
#                                       str(timenow[4]).rjust(2,'0'))
    os.makedirs(ddir +'\\' + lanefolder,exist_ok=True)
    
    os.makedirs(ddir +'\\' + lanefolder + '\\' + str(config.options['project_sensor_id']).rjust(3,'0'), exist_ok=True)
    
    if config.options['sensor_list'] == 'custom':
        download_list = sensor_download_list
    else:
        download_list = config.options['sensor_list']
    
    if segtype == 'Diverge':
        customrange = [0,2]
    else:
        customrange = range(0,len(download_list))
#    for dlistid in [1]:
    for dlistid in customrange:
        stationnumber = download_list[dlistid]
        if dlistid < 2:
            number_of_lanes = int(config.detectorinfo.loc[config.detectorinfo['Number'] == (config.options["project_sensor_id"]),'# Lanes'].iloc[0])

        elif segtype == 'Weaving':
            if dlistid == 2:
                number_of_lanes = int(config.detectorinfo.loc[config.detectorinfo['Number'] == (config.options["project_sensor_id"]),'# Ramp Lanes'].iloc[0])
            elif dlistid == 3:
                number_of_lanes = int(config.detectorinfo.loc[config.detectorinfo['Number'] == (config.options["project_sensor_id"]),'#RampLanesDetec4'].iloc[0])

        else:
            number_of_lanes = int(config.detectorinfo.loc[config.detectorinfo['Number'] == (config.options["project_sensor_id"]),'# Ramp Lanes'].iloc[0])
        
#        print('station %s'%stationnumber)
        dirpath = (ddir +'\\' + lanefolder + '\\' + str(config.options['project_sensor_id']).rjust(3,'0') + '\\' + str(stationnumber))
        if os.path.exists(dirpath):
            shutil.rmtree(dirpath,ignore_errors = True)
        os.makedirs(dirpath,exist_ok=True)
        if tend[0] > endtimes[-1]:
            print('false')
            starttimes= np.append(starttimes,(endtimes[-1]+60))
            endtimes = np.append(endtimes,(tend[0]))
        
        for i,j in zip(starttimes,endtimes):
            
            gi=time.gmtime(i)
            ge=time.gmtime(j)
            
            
            
        #s_time_id=int(time.mktime(dt.timetuple()))
            s_time_id_f='%s%%2F%s%%2F%s+%s%%3A%s' %(str(gi[1]).rjust(2,'0'),
                                                    str(gi[2]).rjust(2,'0'),
                                                    str(gi[0]).rjust(2,'0'),
                                                    str(gi[3]).rjust(2,'0'),
                                                    str(gi[4]).rjust(2,'0'),
                                                    )
        
            e_time_id_f='%s%%2F%s%%2F%s+%s%%3A%s' %(str(ge[1]).rjust(2,'0'),
                                                    str(ge[2]).rjust(2,'0'),
                                                    str(ge[0]).rjust(2,'0'),
                                                    str(ge[3]).rjust(2,'0'),
                                                    str(ge[4]).rjust(2,'0'),
                                                    )
        

            
            if config.options['pems_state'] == 'CA':
                website = 'http://pems.dot.ca.gov/?report_form=1&dnode=VDS&content=loops&tab=det_timeseries&export=xls'
                
            if config.options['pems_state'] == 'UT':
                website = 'https://udot.iteris-pems.com/?report_form=1&dnode=VDS&content=loops&tab=det_timeseries&export=xls'

            if config.options['pems_state'] == 'VA':
                website = 'https://vdot.iteris-pems.com/?report_form=1&dnode=VDS&content=loops&tab=det_timeseries&export=xls'
                
            website = website + '&station_id=%s' %stationnumber
            website = website + '&s_time_id=%i' %i
            website = website + '&s_time_id_f=%s' %s_time_id_f
            website = website + '&e_time_id=%i' %j
            website = website + '&e_time_id_f=%s' %e_time_id_f
            website = website + '&tod=all&tod_from=0&tod_to=0&dow_2=on&dow_3=on&dow_4=on&q=flow&q2=speed&gn=5min&agg=on'
            

            
            for lane in range(1,number_of_lanes+1):
                website = website +'&lane%i=on' %lane
#            print(website)
            newfilename = '%s_%i_%s%s%s%s%s_%s%s%s%s%s' %(
                                                    str(config.options['project_sensor_id']).rjust(3,'0'),
                                                    stationnumber,
                                                    str(gi[0]).rjust(2,'0'),
                                                    str(gi[1]).rjust(2,'0'),
                                                    str(gi[2]).rjust(2,'0'),
                                                    str(gi[3]).rjust(2,'0'),
                                                    str(gi[4]).rjust(2,'0'),
                                                    str(ge[0]).rjust(2,'0'),
                                                    str(ge[1]).rjust(2,'0'),
                                                    str(ge[2]).rjust(2,'0'),
                                                    str(ge[3]).rjust(2,'0'),
                                                    str(ge[4]).rjust(2,'0')
                                                    )
    
    
            files = glob.glob(dirname+'\\*.xlsx')
            
            
    #        print('opening website') 
            
            
    #        print('waiting for download')
            if config.options['pems_state'] in ['VA','UT']:
                timeout = 30
            else:
                timeout = 15
            period = 0.4
            mustend = time.time() + timeout
            
            errorcount = 0
            variables=[]
            while errorcount != 1:
#                print('inside errorcount while')
                files = glob.glob(dirname+'\\*.xlsx')
                lastfile = max(files , key = os.path.getctime)    
                webbrowser.open(website)
                mustend = time.time() + timeout
                while time.time() < mustend:
#                    print('inside mustend while')
                    files = glob.glob(dirname+'\\*.xlsx')
                    newfile = max(files , key = os.path.getctime)
                    if newfile !=lastfile: break
                    time.sleep(period)
                    
#                print('end of new file search')
#                filepath=os.path.join(dirpath,'%s.xlsx' %newfilename)
                #checking consistency
                try:
#                    print('inside try procedure')
                    descript_table = pd.read_excel(newfile, sheet_name =descriptionsheet,skiprows=1,usecols=[1,2])
#                    print(errorcount)
                except:
                    print('exception occurred in sheet name')
                    errorcount = 2
#                    descript_table = pd.read_excel(filepath, sheet_name =descriptionsheet,skiprows=1,usecols=[1,2])
                    mustend = time.time() + timeout
                if errorcount != 2:
#                    print('checking website info')
                    if config.options['pems_state'] == 'VA': 
                        weblink = descript_table.at[2,'Aggregates>Time Series']
#                        print(weblink)
                        
                    elif config.options['pems_state'] == 'UT': 
                        weblink = descript_table.at[2,'Aggregates>Time Series']
                    else: 
                        weblink = descript_table.at[0,'Aggregates>Time Series']
                    variables=weblink.split('&')
                    #checking each variable
                    
                    if len(variables) >9 and variables[4] == 'station_id=%s' %stationnumber and (
                            variables[6] == 's_time_id_f=%s%%2F%s%%2F%s+%s%%3A%s' %(str(gi[1]).rjust(2,'0'),
                                                                    str(gi[2]).rjust(2,'0'),
                                                                    str(gi[0]).rjust(2,'0'),
                                                                    str(gi[3]).rjust(2,'0'),
                                                                    str(gi[4]).rjust(2,'0'),
                                                                    )) and (
                                     variables[8] == 'e_time_id_f=%s%%2F%s%%2F%s+%s%%3A%s' %(str(ge[1]).rjust(2,'0'),
                                                                    str(ge[2]).rjust(2,'0'),
                                                                    str(ge[0]).rjust(2,'0'),
                                                                    str(ge[3]).rjust(2,'0'),
                                                                    str(ge[4]).rjust(2,'0'),
                                                                    )
                                     ):                                
                        
                        shutil.move(newfile,os.path.join(dirpath,'%s.xlsx' %newfilename))
#                        print('before os')
#                        os.remove(newfile)
                        
                        
                        errorcount=1
    
                    else:
                        print('File for station %s is incorrect' %stationnumber)
                        errorcount=0
    #                        os.remove(newfile)
                        mustend = time.time() + timeout
                
                
#                except:
#                    print('exception occurred')
#                    errorcount = 0    
#                
                
                    

