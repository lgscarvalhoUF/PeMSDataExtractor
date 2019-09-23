# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 12:58:33 2019

@author: lstaichakcarvalh
"""

#import config
import os
import pandas as pd
import pickle
import time
import config
import copy
#import shutil
#import matplotlib.pyplot as plt
from data_downloader import lanefolder,segtype,starttimes,endtimes,ddir,descriptionsheet
#import matplotlib.backends.backend_pdf

#number_of_lanes = config.options["number_of_lanes"]
#segtype = config.options["segmenttype"]
#download_list=list(pd.read_excel('sensordownloadlist.xlsx')['Sensor_name'].tolist())

#lanefolder = 'segment_%s_lanes_%s' %(segtype,number_of_lanes)


#plt.rcParams['axes.formatter.use_locale'] = True
#plt.rcParams["font.family"] ='sans-serif'
#plt.rcParams["font.sans-serif"] = 'arial'
#font = {'family' : 'sans-serif',
##        'weight' : 'bold',
#        'size'   : '15'}
#plt.rc('font', **font)
#
#axessetup = {'titlesize':15,
#        'titleweight':'bold'}
#plt.rc('axes',**axessetup)
partialoutpath = (config.options['treated_files_dir'] +'\\' +config.options['segmenttype']+ '\\'+ lanefolder + '\\')


sensor_download_list = config.options['sensor_list']
number_of_lanes = config.options['number_of_lanes']
if __name__ == "__main__":

    if config.options['segmenttype'] == 'Basic':
        
        if config.invalidflag == 0:
            
            errorcount = 0
            #if config.options['sensor_list'] == 'custom':
            #    download_list = sensor_download_list
            #else:
            #    download_list = config.options['sensor_list']
            
            
            for stationnumber in sensor_download_list:
                outpath =  partialoutpath+str(config.options['project_sensor_id']).rjust(3,'0') + '\\' + str(stationnumber)
        
                dirpath = (ddir +'\\' + lanefolder + '\\' + str(config.options['project_sensor_id']).rjust(3,'0') + '\\' + str(stationnumber))
            
                for i,j in zip(starttimes,endtimes):
                    
                    gi=time.gmtime(i)
                    ge=time.gmtime(j)
            
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
                    filepath=os.path.join(dirpath,'%s.xlsx' %newfilename)
                    
                    #checking consistency
                    
                    descript_table = pd.read_excel(filepath, sheet_name =descriptionsheet,skiprows=1,usecols=[1,2])
                    if config.options['pems_state'] == 'VA': 
                        weblink = descript_table.at[2,'Aggregates>Time Series']
    
                    elif config.options['pems_state'] == 'UT': 
                        weblink = descript_table.at[2,'Aggregates>Time Series']
    
                    else: 
                        weblink = descript_table.at[0,'Aggregates>Time Series']
            
                    variables=weblink.split('&')
                    #checking each variable
                    if variables[4] != 'station_id=%s' %stationnumber and (
                            variables[6] != 's_time_id_f=%s%%2F%s%%2F%s+%s%%3A%s' %(str(gi[1]).rjust(2,'0'),
                                                                    str(gi[2]).rjust(2,'0'),
                                                                    str(gi[0]).rjust(2,'0'),
                                                                    str(gi[3]).rjust(2,'0'),
                                                                    str(gi[4]).rjust(2,'0'),
                                                                    )) and (
                                     variables[8] != 'e_time_id_f=%s%%2F%s%%2F%s+%s%%3A%s' %(str(ge[1]).rjust(2,'0'),
                                                                    str(ge[2]).rjust(2,'0'),
                                                                    str(ge[0]).rjust(2,'0'),
                                                                    str(ge[3]).rjust(2,'0'),
                                                                    str(ge[4]).rjust(2,'0'),
                                                                    )
                                     ):
            #            print('Files for station %s is incorrect' %stationnumber)
                        errorcount+=1
                        os.remove(filepath)
                    
            
            print('%i files with error were removed' %errorcount)
            
            #surfing and aggregating data
            
            #out_pdf = 'figuras\\%ilanes_%isensors.pdf' %(number_of_lanes,len(download_list))
            #pdf = matplotlib.backends.backend_pdf.PdfPages(out_pdf)
            
            
            
            os.makedirs(outpath,exist_ok=True)
            #os.makedirs(config.options['treated_files_dir'],exist_ok=True)
            
            treated_df=dict()
            
            for stationnumber in sensor_download_list:
                dfsensor = pd.DataFrame()
                dirpath = (ddir +'\\' + lanefolder + '\\' + str(config.options['project_sensor_id']).rjust(3,'0') + '\\' + str(stationnumber))
                
                for i,j in zip(starttimes,endtimes):
                
                    gi=time.gmtime(i)
                    ge=time.gmtime(j)
                
                    filename = '%s_%i_%s%s%s%s%s_%s%s%s%s%s.xlsx' %(
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
            
            #    for file in next(os.walk(dirpath))[2]:
                    df = pd.read_excel(os.path.join(dirpath,filename))
                    df=df.drop(['# Lane Points',
                                ],axis=1)
                    collist = []
            #        collist.append('index')
                    collist.append('time')
                    for i in range(1,number_of_lanes+1):
                        collist.append('L%iVolume'%i)
                        collist.append('L%iSpeed'%i)
                    collist.append('TotalVolume')
                    collist.append('AvgSpeed')
                    collist.append('% Observed')
                    df.columns=collist
                    
                    df['time'] = pd.to_datetime(df['time'])
                    
                    df.loc[0,'interv'] =5
                    for i in range(1,len(df)):
                        df.loc[i, 'interv'] = ((df.loc[i, 'time'] -df.loc[i-1, 'time']).value)/60/10e8
                        
                    #aggregating in 15 minutes intervals
                    totalrows = len(df)/3
            #        print(totalrows)
                    dfag = pd.DataFrame()
                    for tagreg in range(0,int(totalrows)):
            #            print((tagreg * 3),(tagreg *3 +3))
                        dftemp = df[(tagreg * 3):(tagreg *3 +3)]
                        dfag.loc[tagreg,'tini'] = df.loc[tagreg*3,'time']
                        dfag.loc[tagreg,'tend'] = df.loc[(tagreg*3+2),'time']
                        
                        
                        for lane in range(1,number_of_lanes+1):
                            column = 'L%iVolume'%lane
                            dfag.loc[tagreg,column] = dftemp[column].sum()
                        
                        for lane in range(1,number_of_lanes+1):
                            column = 'L%iSpeed'%lane
                            dfag.loc[tagreg,column] = dftemp[column].mean()
            
                        
                        dfag.loc[tagreg,'% Observed'] = dftemp['% Observed'].mean()
                        dfag.loc[tagreg,'interv'] = dftemp['interv'].sum()
                        dfag.loc[tagreg,'Volume15min'] = dftemp['TotalVolume'].sum()
                        dfag.loc[tagreg,'AvgSpeed'] = dftemp['AvgSpeed'].mean()
            
                    dfsensor=dfsensor.append(dfag, ignore_index=True)
                    
            #    dfsensor['tperc']=dfsensor['TFlow']/dfsensor['AFlow']
                
                
                
            #    fig=plt.figure(figsize=(8,5))
                for i in range(1,number_of_lanes+1): 
                    dfsensor['L%iRatio'%i]=dfsensor['L%iVolume'%i]/dfsensor['Volume15min']
                    dfsensor['L%ihourFlow'%i]=dfsensor['L%iVolume'%i]*4
            #Calculating density
                    dfsensor['L%iDensity'%i] = dfsensor['L%ihourFlow'%i]/dfsensor['L%iSpeed'%i]
                
                dfsensor['Density'] = dfsensor['Volume15min']*4/dfsensor['AvgSpeed']
                dfsensor['Flow_vph'] = dfsensor['Volume15min']*4
                treated_df[stationnumber] = copy.deepcopy(dfsensor)
                
            
    #            output = open(outpath+'\\treated_%i.pkl' %stationnumber, 'wb')
    #            pickle.dump(treated_df[stationnumber], output)
    #            output.close()
    
        if config.invalidflag == 1:
            if config.options["pems_state"] in ['MN','WI','FL']:
                stationnumber = config.options['sensor_list'][0]
                
                outpath =  partialoutpath+str(config.options['project_sensor_id']).rjust(3,'0') + '\\' + str(stationnumber)
                dirpath = (ddir +'\\' + lanefolder + '\\' + str(config.options['project_sensor_id']).rjust(3,'0') + '\\' + str(stationnumber))
        
        
                os.makedirs(outpath,exist_ok=True)
                treated_df=dict()
        
        #    for file in next(os.walk(dirpath))[2]:
                dfsensor = pd.read_excel(os.path.join(dirpath,next(os.walk(dirpath))[2][0]))
                
    #            dfsensor=dfsensor.drop(['# Lane Points',
    #                        ],axis=1)
                collist = []
        #        collist.append('index')
                collist.append('time')
                for i in range(1,number_of_lanes+1):
                    collist.append('L%iVolume'%i)
                    collist.append('L%iSpeed'%i)
                collist.append('Volume15min')
                collist.append('AvgSpeed')
    #            collist.append('% Observed')
                dfsensor.columns=collist
                        
                dfsensor['time'] = pd.to_datetime(dfsensor['time'])
        
        
        #        dfsensor = dfsensor.rename(index=str, columns={"Date": "time"})
                
                dfsensor['time'] = pd.to_datetime(dfsensor['time'])
        
        #        dropping invalid data
                dfsensor = dfsensor.drop(dfsensor[dfsensor.Volume15min < 0].index,axis=0)
                dfsensor = dfsensor.drop(dfsensor[dfsensor.AvgSpeed < 0].index,axis=0)
        #L1Volume	L1Speed	L2Volume	L2Speed	Volume15min	AvgSpeed
                for lane in range(1,config.options['number_of_lanes']+1):
                    dfsensor = dfsensor.drop(dfsensor[dfsensor['L%iSpeed' %lane] > 85].index,axis=0)
                    dfsensor = dfsensor.drop(dfsensor[dfsensor['L%iSpeed' %lane] < 0].index,axis=0)
                    
                    
                dfsensor = dfsensor.reset_index(drop=True)
                
                dfsensor.loc[0,'interv'] =15
        
                for i in range(1,len(dfsensor)):
                    dfsensor.loc[i, 'interv'] = ((dfsensor.loc[i, 'time'] -dfsensor.loc[i-1, 'time']).value)/60/10e8
                
                
        
                
                dfsensor['tini'] = dfsensor['time']
                dfsensor['tend'] = 0
        #        df=df.drop(['# Lane Points',
        #                    ],axis=1)
        #        collist = []
        ##        collist.append('index')
        #        collist.append('time')
        #        for i in range(1,number_of_lanes+1):
        #            collist.append('L%iVolume'%i)
        #            collist.append('L%iSpeed'%i)
        #        collist.append('TotalVolume')
        #        collist.append('AvgSpeed')
        #        collist.append('% Observed')
        #        df.columns=collist
        #        
        #        df['time'] = pd.to_datetime(df['time'])
        #        
        #        df.loc[0,'interv'] =5
        #        for i in range(1,len(df)):
        #            df.loc[i, 'interv'] = ((df.loc[i, 'time'] -df.loc[i-1, 'time']).value)/60/10e8
                    
        #        #aggregating in 15 minutes intervals
        #        totalrows = len(df)/3
        ##        print(totalrows)
        #        dfag = pd.DataFrame()
        #        for tagreg in range(0,int(totalrows)):
        ##            print((tagreg * 3),(tagreg *3 +3))
        #            dftemp = df[(tagreg * 3):(tagreg *3 +3)]
        #            dfag.loc[tagreg,'tini'] = df.loc[tagreg*3,'time']
        #            dfag.loc[tagreg,'tend'] = df.loc[(tagreg*3+2),'time']
        #            
        #            
        #            for lane in range(1,number_of_lanes+1):
        #                column = 'L%iVolume'%lane
        #                dfag.loc[tagreg,column] = dftemp[column].sum()
        #            
        #            for lane in range(1,number_of_lanes+1):
        #                column = 'L%iSpeed'%lane
        #                dfag.loc[tagreg,column] = dftemp[column].mean()
        
                    
        #            dfag.loc[tagreg,'% Observed'] = dftemp['% Observed'].mean()
        #            dfag.loc[tagreg,'interv'] = dftemp['interv'].sum()
        #            dfag.loc[tagreg,'Volume15min'] = dftemp['TotalVolume'].sum()
        #            dfag.loc[tagreg,'AvgSpeed'] = dftemp['AvgSpeed'].mean()
        #
        #        dfsensor=dfsensor.append(dfag, ignore_index=True)
                
        #    dfsensor['tperc']=dfsensor['TFlow']/dfsensor['AFlow']
            
            
            
        #    fig=plt.figure(figsize=(8,5))
                for i in range(1,number_of_lanes+1): 
                    dfsensor['L%iRatio'%i]=dfsensor['L%iVolume'%i]/dfsensor['Volume15min']
                    dfsensor['L%ihourFlow'%i]=dfsensor['L%iVolume'%i]*4
            #Calculating density
                    dfsensor['L%iDensity'%i] = dfsensor['L%ihourFlow'%i]/dfsensor['L%iSpeed'%i]
                
                dfsensor['Density'] = dfsensor['Volume15min']*4/dfsensor['AvgSpeed']
                dfsensor['Flow_vph'] = dfsensor['Volume15min']*4
                
                
    #            fixing minnesota reversed lane positioning
                for i in range(1,number_of_lanes+1):
                    dfsensor['L%iVolume' %(i+10)] = dfsensor['L%iVolume' %(i)]
                    dfsensor['L%iSpeed' %(i+10)] = dfsensor['L%iSpeed' %(i)]
                    dfsensor['L%iRatio' %(i+10)] = dfsensor['L%iRatio' %(i)]
                    dfsensor['L%ihourFlow' %(i+10)] = dfsensor['L%ihourFlow' %(i)]
                    dfsensor['L%iDensity' %(i+10)] = dfsensor['L%iDensity' %(i)]
    
                for i,j in zip(range(1,number_of_lanes+1),reversed(range(1,number_of_lanes+1))):
    #                print(i,j)
                    dfsensor['L%iVolume' %(j)] = dfsensor['L%iVolume' %(i+10)]
                    dfsensor['L%iSpeed' %(j)] = dfsensor['L%iSpeed' %(i+10)]
                    dfsensor['L%iRatio' %(j)] = dfsensor['L%iRatio' %(i+10)]
                    dfsensor['L%ihourFlow' %(j)] = dfsensor['L%ihourFlow' %(i+10)]
                    dfsensor['L%iDensity' %(j)] = dfsensor['L%iDensity' %(i+10)]
                
                for i in range(1,number_of_lanes+1):
                    dfsensor=dfsensor.drop(['L%iVolume' %(i+10)],axis=1)
                    dfsensor=dfsensor.drop(['L%iSpeed' %(i+10)],axis=1)
                    dfsensor=dfsensor.drop(['L%iRatio' %(i+10)] ,axis=1)
                    dfsensor=dfsensor.drop(['L%ihourFlow' %(i+10)],axis=1)
                    dfsensor=dfsensor.drop(['L%iDensity' %(i+10)],axis=1)
                
                
                
                treated_df[stationnumber] = copy.deepcopy(dfsensor)
            
        
                output = open(outpath+'\\treated_%i.pkl' %stationnumber, 'wb')
                pickle.dump(treated_df[stationnumber], output)
                output.close()
                 
                treated_df[stationnumber].to_excel(outpath+'\\treated_%i.xlsx' %stationnumber)
###################################################################################################

    if config.options['segmenttype'] in ['Merge','Diverge','Weaving']:
        
        if config.invalidflag == 0:
            
            #os.makedirs(config.options['treated_files_dir'],exist_ok=True)
            
            treated_df=dict()
            

            if segtype == 'Diverge':
                customrange = [0,2]
            else:
                customrange = range(0,len(sensor_download_list))
            
            for dlistid in customrange:
                stationnumber = sensor_download_list[dlistid]
                
                outpath =  partialoutpath+str(config.options['project_sensor_id']).rjust(3,'0') + '\\' + str(stationnumber)
    
                dirpath = (ddir +'\\' + lanefolder + '\\' + str(config.options['project_sensor_id']).rjust(3,'0') + '\\' + str(stationnumber))
                
                os.makedirs(outpath,exist_ok=True)

                
                if dlistid < 2:
                    number_of_lanes = int(config.detectorinfo.loc[config.detectorinfo['Number'] == (config.options["project_sensor_id"]),'# Lanes'].iloc[0])


                    dfsensor = pd.DataFrame()
                    dirpath = (ddir +'\\' + lanefolder + '\\' + str(config.options['project_sensor_id']).rjust(3,'0') + '\\' + str(stationnumber))
                    
                    for i,j in zip(starttimes,endtimes):
                    
                        gi=time.gmtime(i)
                        ge=time.gmtime(j)
                    
                        filename = '%s_%i_%s%s%s%s%s_%s%s%s%s%s.xlsx' %(
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
                
                #    for file in next(os.walk(dirpath))[2]:
                        df = pd.read_excel(os.path.join(dirpath,filename))
                        df=df.drop(['# Lane Points',
                                    ],axis=1)
                        collist = []
                #        collist.append('index')
                        collist.append('time')
                        for i in range(1,number_of_lanes+1):
                            collist.append('L%iVolume'%i)
                            collist.append('L%iSpeed'%i)
                        collist.append('TotalVolume')
                        collist.append('AvgSpeed')
                        collist.append('% Observed')
                        df.columns=collist
                        
                        df['time'] = pd.to_datetime(df['time'])
                        
                        df.loc[0,'interv'] =5
                        for i in range(1,len(df)):
                            df.loc[i, 'interv'] = ((df.loc[i, 'time'] -df.loc[i-1, 'time']).value)/60/10e8
                            
                        #aggregating in 15 minutes intervals
                        totalrows = len(df)/3
                #        print(totalrows)
                        dfag = pd.DataFrame()
                        for tagreg in range(0,int(totalrows)):
                #            print((tagreg * 3),(tagreg *3 +3))
                            dftemp = df[(tagreg * 3):(tagreg *3 +3)]
                            dfag.loc[tagreg,'tini'] = df.loc[tagreg*3,'time']
                            dfag.loc[tagreg,'tend'] = df.loc[(tagreg*3+2),'time']
                            
                            
                            for lane in range(1,number_of_lanes+1):
                                column = 'L%iVolume'%lane
                                dfag.loc[tagreg,column] = dftemp[column].sum()
                            
                            for lane in range(1,number_of_lanes+1):
                                column = 'L%iSpeed'%lane
                                dfag.loc[tagreg,column] = dftemp[column].mean()
                
                            
                            dfag.loc[tagreg,'% Observed'] = dftemp['% Observed'].mean()
                            dfag.loc[tagreg,'interv'] = dftemp['interv'].sum()
                            dfag.loc[tagreg,'Volume15min'] = dftemp['TotalVolume'].sum()
                            dfag.loc[tagreg,'AvgSpeed'] = dftemp['AvgSpeed'].mean()
                
                        dfsensor=dfsensor.append(dfag, ignore_index=True)
                        
                #    dfsensor['tperc']=dfsensor['TFlow']/dfsensor['AFlow']
                    
                    
                    
                #    fig=plt.figure(figsize=(8,5))
                    for i in range(1,number_of_lanes+1): 
                        dfsensor['L%iRatio'%i]=dfsensor['L%iVolume'%i]/dfsensor['Volume15min']
                        dfsensor['L%ihourFlow'%i]=dfsensor['L%iVolume'%i]*4
                #Calculating density
                        dfsensor['L%iDensity'%i] = dfsensor['L%ihourFlow'%i]/dfsensor['L%iSpeed'%i]
                    
                    dfsensor['Density'] = dfsensor['Volume15min']*4/dfsensor['AvgSpeed']
                    dfsensor['Flow_vph'] = dfsensor['Volume15min']*4
                    treated_df[stationnumber] = copy.deepcopy(dfsensor)
                    
                    output = open(outpath+'\\treated_%i.pkl' %stationnumber, 'wb')
                    pickle.dump(treated_df[stationnumber], output)
                    output.close()
                     
                    treated_df[stationnumber].to_excel(outpath+'\\treated_%i.xlsx' %stationnumber)
            
                else:
                    if segtype == 'Weaving':
                    
#        elif segtype == 'Weaving':
                        if dlistid == 2:
                            number_of_lanes = int(config.detectorinfo.loc[config.detectorinfo['Number'] == (config.options["project_sensor_id"]),'# Ramp Lanes'].iloc[0])
                        elif dlistid == 3:
                            number_of_lanes = int(config.detectorinfo.loc[config.detectorinfo['Number'] == (config.options["project_sensor_id"]),'#RampLanesDetec4'].iloc[0])

                        else:
                            number_of_lanes = int(config.detectorinfo.loc[config.detectorinfo['Number'] == (config.options["project_sensor_id"]),'# Ramp Lanes'].iloc[0])
                    
#                    number_of_lanes = int(config.detectorinfo.loc[config.detectorinfo['Number'] == (config.options["project_sensor_id"]),'# Ramp Lanes'].iloc[0])

                    dfsensor = pd.DataFrame()
                    dirpath = (ddir +'\\' + lanefolder + '\\' + str(config.options['project_sensor_id']).rjust(3,'0') + '\\' + str(stationnumber))
                    
                    for i,j in zip(starttimes,endtimes):
                    
                        gi=time.gmtime(i)
                        ge=time.gmtime(j)
                    
                        filename = '%s_%i_%s%s%s%s%s_%s%s%s%s%s.xlsx' %(
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
                
                #    for file in next(os.walk(dirpath))[2]:
                        df = pd.read_excel(os.path.join(dirpath,filename))
                        df=df.drop(['# Lane Points',
                                    ],axis=1)
                        collist = []
                #        collist.append('index')
                        collist.append('time')
                        for i in range(1,number_of_lanes+1):
                            collist.append('L%iVolume'%i)
#                            collist.append('L%iSpeed'%i)
                        collist.append('TotalVolume')
#                        collist.append('AvgSpeed')
                        collist.append('% Observed')
                        df.columns=collist
                        
                        df['time'] = pd.to_datetime(df['time'])
                        
                        df.loc[0,'interv'] =5
                        for i in range(1,len(df)):
                            df.loc[i, 'interv'] = ((df.loc[i, 'time'] -df.loc[i-1, 'time']).value)/60/10e8
                            
                        #aggregating in 15 minutes intervals
                        totalrows = len(df)/3
                #        print(totalrows)
                        dfag = pd.DataFrame()
                        for tagreg in range(0,int(totalrows)):
                #            print((tagreg * 3),(tagreg *3 +3))
                            dftemp = df[(tagreg * 3):(tagreg *3 +3)]
                            dfag.loc[tagreg,'tini'] = df.loc[tagreg*3,'time']
                            dfag.loc[tagreg,'tend'] = df.loc[(tagreg*3+2),'time']
                            
                            
                            for lane in range(1,number_of_lanes+1):
                                column = 'L%iVolume'%lane
                                dfag.loc[tagreg,column] = dftemp[column].sum()
                            
#                            for lane in range(1,number_of_lanes+1):
#                                column = 'L%iSpeed'%lane
#                                dfag.loc[tagreg,column] = dftemp[column].mean()
                
                            
                            dfag.loc[tagreg,'% Observed'] = dftemp['% Observed'].mean()
                            dfag.loc[tagreg,'interv'] = dftemp['interv'].sum()
                            dfag.loc[tagreg,'Volume15min'] = dftemp['TotalVolume'].sum()
#                            dfag.loc[tagreg,'AvgSpeed'] = dftemp['AvgSpeed'].mean()
                
                        dfsensor=dfsensor.append(dfag, ignore_index=True)
                        
                #    dfsensor['tperc']=dfsensor['TFlow']/dfsensor['AFlow']
                    
                    
                    
                #    fig=plt.figure(figsize=(8,5))
                    for i in range(1,number_of_lanes+1): 
                        dfsensor['L%iRatio'%i]=dfsensor['L%iVolume'%i]/dfsensor['Volume15min']
                        dfsensor['L%ihourFlow'%i]=dfsensor['L%iVolume'%i]*4
                #Calculating density
#                        dfsensor['L%iDensity'%i] = dfsensor['L%ihourFlow'%i]/dfsensor['L%iSpeed'%i]
                    
#                    dfsensor['Density'] = dfsensor['Volume15min']*4/dfsensor['AvgSpeed']
                    dfsensor['Flow_vph'] = dfsensor['Volume15min']*4
                    treated_df[stationnumber] = copy.deepcopy(dfsensor)

                    output = open(outpath+'\\treated_%i.pkl' %stationnumber, 'wb')
                    pickle.dump(treated_df[stationnumber], output)
                    output.close()
                     
                    treated_df[stationnumber].to_excel(outpath+'\\treated_%i.xlsx' %stationnumber)
                    
        if config.invalidflag == 1:
            if config.options["pems_state"] in ['MN','WI','FL']:
                

                if segtype == 'Diverge':
                    customrange = [0,2]
                else:
                    customrange = range(0,len(sensor_download_list))
                
                for dlistid in customrange:
                    print(dlistid)
                    stationnumber = sensor_download_list[dlistid]
                    if dlistid < 2:
                        number_of_lanes = config.detectorinfo.loc[config.detectorinfo['Number'] == (config.options["project_sensor_id"]),'# Lanes'].iloc[0]
                    else:
                        number_of_lanes = config.detectorinfo.loc[config.detectorinfo['Number'] == (config.options["project_sensor_id"]),'# Ramp Lanes'].iloc[0]
                                                              
                
                
#                stationnumber = config.options['sensor_list'][0]
                
                    outpath =  partialoutpath+str(config.options['project_sensor_id']).rjust(3,'0') + '\\' + str(stationnumber)
                    dirpath = (ddir +'\\' + lanefolder + '\\' + str(config.options['project_sensor_id']).rjust(3,'0') + '\\' + str(stationnumber))
            
            
                    os.makedirs(outpath,exist_ok=True)
                    treated_df=dict()
            
            #    for file in next(os.walk(dirpath))[2]:
                    dfsensor = pd.read_excel(os.path.join(dirpath,next(os.walk(dirpath))[2][0]))
                    
        #            dfsensor=dfsensor.drop(['# Lane Points',
        #                        ],axis=1)
                    collist = []
            #        collist.append('index')
                    collist.append('time')
                    for i in range(1,number_of_lanes+1):
                        collist.append('L%iVolume'%i)
                        collist.append('L%iSpeed'%i)
                    collist.append('Volume15min')
                    collist.append('AvgSpeed')
        #            collist.append('% Observed')
                    dfsensor.columns=collist
                            
                    dfsensor['time'] = pd.to_datetime(dfsensor['time'])
            
            
            #        dfsensor = dfsensor.rename(index=str, columns={"Date": "time"})
                    
                    dfsensor['time'] = pd.to_datetime(dfsensor['time'])
            
            #        dropping invalid data
                    dfsensor = dfsensor.drop(dfsensor[dfsensor.Volume15min < 0].index,axis=0)
                    dfsensor = dfsensor.drop(dfsensor[dfsensor.AvgSpeed < 0].index,axis=0)
            #L1Volume	L1Speed	L2Volume	L2Speed	Volume15min	AvgSpeed
                    for lane in range(1,number_of_lanes+1):
                        dfsensor = dfsensor.drop(dfsensor[dfsensor['L%iSpeed' %lane] > 85].index,axis=0)
                        dfsensor = dfsensor.drop(dfsensor[dfsensor['L%iSpeed' %lane] < 0].index,axis=0)
                        
                        
                    dfsensor = dfsensor.reset_index(drop=True)
                    
                    dfsensor.loc[0,'interv'] =15
            
                    for i in range(1,len(dfsensor)):
                        dfsensor.loc[i, 'interv'] = ((dfsensor.loc[i, 'time'] -dfsensor.loc[i-1, 'time']).value)/60/10e8
                    
                    
            
                    
                    dfsensor['tini'] = dfsensor['time']
                    dfsensor['tend'] = 0
            #        df=df.drop(['# Lane Points',
            #                    ],axis=1)
            #        collist = []
            ##        collist.append('index')
            #        collist.append('time')
            #        for i in range(1,number_of_lanes+1):
            #            collist.append('L%iVolume'%i)
            #            collist.append('L%iSpeed'%i)
            #        collist.append('TotalVolume')
            #        collist.append('AvgSpeed')
            #        collist.append('% Observed')
            #        df.columns=collist
            #        
            #        df['time'] = pd.to_datetime(df['time'])
            #        
            #        df.loc[0,'interv'] =5
            #        for i in range(1,len(df)):
            #            df.loc[i, 'interv'] = ((df.loc[i, 'time'] -df.loc[i-1, 'time']).value)/60/10e8
                        
            #        #aggregating in 15 minutes intervals
            #        totalrows = len(df)/3
            ##        print(totalrows)
            #        dfag = pd.DataFrame()
            #        for tagreg in range(0,int(totalrows)):
            ##            print((tagreg * 3),(tagreg *3 +3))
            #            dftemp = df[(tagreg * 3):(tagreg *3 +3)]
            #            dfag.loc[tagreg,'tini'] = df.loc[tagreg*3,'time']
            #            dfag.loc[tagreg,'tend'] = df.loc[(tagreg*3+2),'time']
            #            
            #            
            #            for lane in range(1,number_of_lanes+1):
            #                column = 'L%iVolume'%lane
            #                dfag.loc[tagreg,column] = dftemp[column].sum()
            #            
            #            for lane in range(1,number_of_lanes+1):
            #                column = 'L%iSpeed'%lane
            #                dfag.loc[tagreg,column] = dftemp[column].mean()
            
                        
            #            dfag.loc[tagreg,'% Observed'] = dftemp['% Observed'].mean()
            #            dfag.loc[tagreg,'interv'] = dftemp['interv'].sum()
            #            dfag.loc[tagreg,'Volume15min'] = dftemp['TotalVolume'].sum()
            #            dfag.loc[tagreg,'AvgSpeed'] = dftemp['AvgSpeed'].mean()
            #
            #        dfsensor=dfsensor.append(dfag, ignore_index=True)
                    
            #    dfsensor['tperc']=dfsensor['TFlow']/dfsensor['AFlow']
                
                
                
            #    fig=plt.figure(figsize=(8,5))
                    for i in range(1,number_of_lanes+1): 
                        dfsensor['L%iRatio'%i]=dfsensor['L%iVolume'%i]/dfsensor['Volume15min']
                        dfsensor['L%ihourFlow'%i]=dfsensor['L%iVolume'%i]*4
                #Calculating density
                        dfsensor['L%iDensity'%i] = dfsensor['L%ihourFlow'%i]/dfsensor['L%iSpeed'%i]
                    
                    dfsensor['Density'] = dfsensor['Volume15min']*4/dfsensor['AvgSpeed']
                    dfsensor['Flow_vph'] = dfsensor['Volume15min']*4
                    
                    
        #            fixing minnesota reversed lane positioning
                    if config.options['lanenumbering'] != 'Left':
                        for i in range(1,number_of_lanes+1):
                            dfsensor['L%iVolume' %(i+10)] = dfsensor['L%iVolume' %(i)]
                            dfsensor['L%iSpeed' %(i+10)] = dfsensor['L%iSpeed' %(i)]
                            dfsensor['L%iRatio' %(i+10)] = dfsensor['L%iRatio' %(i)]
                            dfsensor['L%ihourFlow' %(i+10)] = dfsensor['L%ihourFlow' %(i)]
                            dfsensor['L%iDensity' %(i+10)] = dfsensor['L%iDensity' %(i)]
            
                        for i,j in zip(range(1,number_of_lanes+1),reversed(range(1,number_of_lanes+1))):
            #                print(i,j)
                            dfsensor['L%iVolume' %(j)] = dfsensor['L%iVolume' %(i+10)]
                            dfsensor['L%iSpeed' %(j)] = dfsensor['L%iSpeed' %(i+10)]
                            dfsensor['L%iRatio' %(j)] = dfsensor['L%iRatio' %(i+10)]
                            dfsensor['L%ihourFlow' %(j)] = dfsensor['L%ihourFlow' %(i+10)]
                            dfsensor['L%iDensity' %(j)] = dfsensor['L%iDensity' %(i+10)]
                        
                        for i in range(1,number_of_lanes+1):
                            dfsensor=dfsensor.drop(['L%iVolume' %(i+10)],axis=1)
                            dfsensor=dfsensor.drop(['L%iSpeed' %(i+10)],axis=1)
                            dfsensor=dfsensor.drop(['L%iRatio' %(i+10)] ,axis=1)
                            dfsensor=dfsensor.drop(['L%ihourFlow' %(i+10)],axis=1)
                            dfsensor=dfsensor.drop(['L%iDensity' %(i+10)],axis=1)
                    
                    
                    
                    treated_df[stationnumber] = copy.deepcopy(dfsensor)
            

                    output = open(outpath+'\\treated_%i.pkl' %stationnumber, 'wb')
                    pickle.dump(treated_df[stationnumber], output)
                    output.close()
                     
                    treated_df[stationnumber].to_excel(outpath+'\\treated_%i.xlsx' %stationnumber)
                        