# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 15:36:26 2019

@author: lstaichakcarvalh
"""
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import pickle
import numpy as np
#import pandas as pd
from data_downloader import number_of_lanes,sensor_download_list
import config

import vanaerde

#van aerde calculated density
#calc_kmodel
#    return (c1 + c2 / (s_f - speed) + c3*speed)**(-1)


#file_input = open('.\\PeMS_specific\\%s\\database_pickle\\treated_sensors.pkl' %config.options['pems_state'], 'rb')
#treated_df = pickle.load(file_input)
#file_input.close()



#plottingdf['L%ihourFlow'%lane] = copy.deepcopy( df['L%ihourFlow'%lane])
#plottingdf['L%iSpeed'%lane] = copy.deepcopy( df['L%iSpeed'%lane])    


#evaldf['flowdiff'] = errorfn(evaldf['L%ihourFlow'%lane],evaldf['L%imodelflow'%lane])

   

        



colors = ['b','g','r','darkmagenta']
fig=plt.figure(figsize=(8,5),dpi=900)


#for i in vanaerde.lanelist[:-1]: 
#    speedplot=np.arange(0,bestind[i]['genes']['s_f'],1)
##    speedplot.append(bestind[i]['genes']['s_f'])
#    
#    plottingdf = pd.DataFrame()
#    #    if calibrationmode == 'lane':      
#    #        for lane in range(1,config.options['number_of_lanes']+1):
#    kandq= vanaerde.eval_model_q_k(bestind[i]['genes'],speedplot)
#    #            evaldf['L%imodeldensity'%lane] = kandq[0]
#    plottingdf['L%imodelflow'%i] = kandq[1]    
#    
#    plt.plot(plottingdf['L%imodelflow'%i],speedplot,c=colors[i-1])
#    
#    
#    plt.scatter(treated_df[sensor]['L%ihourFlow'%i],
#                treated_df[sensor]['L%iSpeed'%i],
#                label='Lane %i Hourly Flow' %i,
#                alpha=0.3,
#                s = 10,
#                c=colors[i-1])            
#    #        plt.plot()
#    plt.title('Sensor %s \n Ini Date %s, End Date %s' %(sensor,
#                                                       treated_df[sensor]['tini'].min(),
#                                                       treated_df[sensor]['tend'].max()))
#    plt.xlabel('Flow [veh./h]')
#    plt.ylabel('Speed (mph)')
#
#plt.grid()
#plt.xlim(0,2600)
#plt.ylim(0,90)
#plt.legend()
#plt.show()

##########################################################################
#fig=plt.figure(figsize=(8,5),dpi=900)
#
#for i in vanaerde.lanelist[-1:]:
#    speedplot=np.arange(0,bestind[i]['genes']['s_f'],1)
##    speedplot.append(bestind[i]['genes']['s_f'])
#    
#    plottingdf = pd.DataFrame()
#    #    if calibrationmode == 'lane':      
#    #        for lane in range(1,config.options['number_of_lanes']+1):
#    kandq= vanaerde.eval_model_q_k(bestind[i]['genes'],speedplot)
#    #            evaldf['L%imodeldensity'%lane] = kandq[0]
#    plottingdf['modelflow'] = kandq[1]    
#    
#    plt.plot(plottingdf['modelflow'],speedplot,c='k')
#    
#    
#    plt.scatter(treated_df[sensor]['HourFlow'],
#                treated_df[sensor]['Speed'],
#                label='Segment Hourly Flow',
#                alpha=0.3,
#                s = 10,
#                c='gray')            
#    #        plt.plot()
#    plt.title('Sensor %s \n Ini Date %s, End Date %s' %(sensor,
#                                                       treated_df[sensor]['tini'].min(),
#                                                       treated_df[sensor]['tend'].max()))
#    plt.xlabel('Flow [veh./h]')
#    plt.ylabel('Speed (mph)')
#
#plt.grid()
##plt.xlim(0,2600)
#plt.ylim(0,90)
#plt.legend()
##plt.show()
#





#    plt.show()
#    pdf.savefig(fig,dpi=900)
#plt.close()#out_pdf = 'figuras\\%ilanes_%isensors.pdf' %(number_of_lanes,len(sensor_download_list))
#pdf = matplotlib.backends.backend_pdf.PdfPages(out_pdf)
#for stationnumber in sensor_download_list:
stationnumber = sensor

#    

fig=plt.figure(figsize=(8,5))
for i in range(1,number_of_lanes+1): 
    plt.scatter(treated_df[stationnumber]['L%ihourFlow'%i]/bestind[i]['genes']['v_c'],
                treated_df[stationnumber]['L%iRatio'%i],
                label='Lane %i Flow' %i,
                alpha=0.5,
                s = 10,
                c=colors[i-1])            
#        plt.plot()
plt.title('Sensor %s \n Ini Date %s, End Date %s' %(stationnumber,
                                                   treated_df[stationnumber]['tini'].min(),
                                                   treated_df[stationnumber]['tend'].max()))
plt.xlabel('Volume/Capacity')
plt.ylabel('[(Lane flow) / (Total flow)]')
plt.grid()
#plt.xlim(0,1)
plt.ylim(0,1)
plt.legend()
plt.show()
#    pdf.savefig(fig,dpi=900)
plt.close()
#pdf.close()     