# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 17:11:03 2019

@author: lstaichakcarvalh
"""

import config
from lxml import etree
import pandas as pd
import pickle
sensor_database = '.\california_config.xml'

#vdstypes = ['CD','CH','FF','FR','HV','ML','OR']

tree = etree.parse(sensor_database)#cria elemento tree contendo rede em branco.
root = tree.getroot() #define a raiz do arquivo

#getting all freeway ids
sensordict={}
#for sensortype in vdstypes:
#    sensordict[sensortype]={}
for element in root:
    if element.tag == 'district':
        for s1 in element:
            if s1.tag == 'detector_stations':
                for s2 in s1:
                    if s2.tag == 'vds':
#                        sensortype = s2.get('type')
                        dictio=s2.attrib
                        sensordict[int(s2.get('id'))]=dictio

#list of sensors
sensorlist = list(sensordict.keys())

#list of sensors attributes
sensorattribs = list(sensordict[sensorlist[0]].keys())

#sorting information to create the sensor dataframe
layer1dict = {}
for attribute in sensorattribs:
    layer1dict[attribute] = []
for i in sensordict:
    for attribute in sensordict[i]:
        layer1dict[attribute].append(sensordict[i][attribute])

sensor_info = pd.DataFrame(layer1dict)

print('basic sensor info gotten')
#list of unique entries by attribute
attribs_list={}
dfbyattribute = {}
for attribute in sensorattribs:
    print('now getting attribute %s information' %attribute)
    attribs_list[attribute] = list(set(layer1dict[attribute]))
    dfbyattribute[attribute]={}
#setting thematic dataframes based on each attribute
    for uniqueatt in attribs_list[attribute]:
        dfbyattribute[attribute][uniqueatt] = pd.DataFrame(sensor_info.loc[sensor_info[attribute] == uniqueatt])
        if attribute == 'freeway_id':
            dfbyattribute[attribute][uniqueatt]=dfbyattribute[attribute][uniqueatt].drop(['name',
             'last_modified',
             'latitude',
             'longitude',
             'county_id',
             'cal_pm',
             'city_id'],axis=1)


#now working on ordering each freeway and taking the basic segments
attribute = 'freeway_id'
freeway='170'

one_mile_equals_to = 5280 #ft


#separating freeway movements
base_sensor_list=[]
fr_mov = {}
for freeway in dfbyattribute[attribute]:
    fr_mov[freeway]={}
    u_directions = list(set(dfbyattribute[attribute][freeway]['freeway_dir']))
    for direction in u_directions:
        fr_mov[freeway][direction]=dfbyattribute[attribute][freeway].loc[
                        dfbyattribute[attribute][freeway]['freeway_dir'] == direction]
        
        fr_mov[freeway][direction]['abs_pm']=pd.to_numeric(fr_mov[freeway][direction]['abs_pm'])
        fr_mov[freeway][direction]['abs_ft']=fr_mov[freeway][direction]['abs_pm']*one_mile_equals_to
        
        fr_mov[freeway][direction]['rel_posft']=fr_mov[freeway][direction]['abs_ft']-fr_mov[freeway][direction]['abs_ft'].min()


        if config.options['%s_abspos' %direction] == 'ascending':
            fr_mov[freeway][direction] = fr_mov[freeway][direction].sort_values(by=['abs_pm'], ascending=True)    
            fr_mov[freeway][direction]['rel_posft_ascend'] = fr_mov[freeway][direction]['rel_posft']
        else:
            fr_mov[freeway][direction] = fr_mov[freeway][direction].sort_values(by=['abs_pm'], ascending=False)    
            fr_mov[freeway][direction]['rel_posft_ascend']=fr_mov[freeway][direction]['rel_posft'].max()+fr_mov[freeway][direction]['rel_posft']*-1
        fr_mov[freeway][direction].reset_index(drop=True,inplace=True)
      
#detecting potential basic segments
#        for i in range(0,len(fr_mov[freeway][direction])):
        #locating mainline segments
        mainsegs = fr_mov[freeway][direction].loc[ (
                fr_mov[freeway][direction]['rel_posft_ascend'] >1500) & (
                fr_mov[freeway][direction]['rel_posft_ascend'] < (fr_mov[freeway][direction]['rel_posft_ascend'].max()-1500) ) & (
                fr_mov[freeway][direction]['type'] == 'ML')
                ]
        
        #checking sensors right before and right after the main segments
        for index in mainsegs.iterrows():
            sensorbefore=fr_mov[freeway][direction].loc[index[0]-1]
            sensorafter =fr_mov[freeway][direction].loc[index[0]+1]
            #calculating the distance between ML sensor and those nearby
            dist_bef = mainsegs.at[index[0],'rel_posft_ascend'] - sensorbefore['rel_posft_ascend']
            dist_post = (mainsegs.at[index[0],'rel_posft_ascend'] - sensorafter['rel_posft_ascend'])*-1
            
            if dist_bef >=1500 and dist_post >= 1500:
                base_sensor_list.append(mainsegs.at[index[0],'id'])
            
            
#            print(a['type'])
#            print(row['c1'], row['c2'])
        
#            if fr_mov[freeway][direction].at[i,'relposft_ascend'] >=1500 and fr_mov[freeway][direction].at[
#                    i,'relposft_ascend'] <= (fr_mov[freeway][direction]['relposft_ascend'].max()-1500):
#                print(i)
base_df = sensor_info[sensor_info['id'].isin(base_sensor_list)]  
base_df['lanes'] = pd.to_numeric(base_df['lanes'])
#base_df=base_df.drop(['name','latitude','longitude'],axis=1)
 
baseperlane ={}
for nlanes in range(base_df['lanes'].min(),base_df['lanes'].max()+1):
    baseperlane[nlanes] = base_df.loc[base_df['lanes']==nlanes]
    baseperlane[nlanes] = baseperlane[nlanes].drop(['name',
         'last_modified',
         'latitude',
         'longitude',
         'county_id',
         'cal_pm',
         'city_id'],axis=1)
    
output = open('.\\database_pickle\\baseperlane.pkl', 'wb')
pickle.dump(baseperlane, output)
output.close()

    


output = open('.\\database_pickle\\sensor_info.pkl', 'wb')
pickle.dump(sensor_info, output)
output.close()

#output = open('.\\database_pickle\\base_df.pkl', 'wb')
#pickle.dump(base_df, output)
#output.close()




