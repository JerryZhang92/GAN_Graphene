# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 23:31:02 2018

@author: Herman Wu
"""
from keras.models import load_model
import os
import numpy as np
import re


def GAN_predict(Model,Latent_size,Data_num,Type='4by4'):
    Noise=np.random.normal(0,0.5,(Data_num,latent_size))
#    Gen_label=np.random.randint(0,20,Data_num)
    Gen_label=np.random.randint(1,2,1000)
    Gen_data=Gen.predict([Noise,Gen_label],verbose=0)
    if Type=='4by4':
        Gen_data=Gen_data.reshape(Data_num,4,4,1)
        for c in range(len(Gen_data)):
            for i in range(4):
                for j in range(4):
                    if Gen_data[c,i,j]>0.5:
                        Gen_data[c,i,j]=1
                    else:
                        Gen_data[c,i,j]=0            
    elif Type=='5by5':
        Gen_data=Gen_data.reshape(Data_num,5,5,1)
        for c in range(len(Gen_data)):
            for i in range(5):
                for j in range(5):
                    if Gen_data[c,i,j]>0.5:
                        Gen_data[c,i,j]=1
                    else:
                        Gen_data[c,i,j]=0            
    return Gen_data,Gen_label
 
def ConvertToNumber(Dataset,size):
    number=[]
    for data in Dataset:
        temp=[]
        for i in range(size):
            for j in range(size):
                temp.append(str(int(data[i,j,:])))
        temp=(''.join(temp))
        temp_10=int(temp,2)
        number.append(temp_10)
    return number
    
if __name__=='__main__':
    Base_dir = os.path.dirname(__file__)
    Base_dir=(Base_dir.split('Script'))[0]
#    Label=1.0
    latent_size=100
    Data_num=1000
    Type='5by5'
    Mode='processed'
    
# =============================================================================
    Gen_dir=Base_dir+'GANs_result/H5_file/Gen_V1_Best_'+Type+'.h5'
    Gen=load_model(Gen_dir)
    kk=re.compile(r'\d+')
    kk1=re.findall(kk,Type)
    size=int(kk1[0])
        
    if Mode=='Unprocessed':
        Gen_data,Gen_label=GAN_predict(Gen,latent_size,Data_num,Type=Type)
        generate_labels=(Gen_label+6)/10 
        generate_labels=generate_labels.reshape(Data_num,1)   
#        for index,i in enumerate(Gen_data):
#            i=i.reshape(size,size)            
#            save_dir_x=Base_dir+'GANs_result/Predict_result/Unprocessed/InputX/InputX_'+str(index+1)+'.csv'
#            save_dir_y=Base_dir+'GANs_result/Predict_result/Unprocessed/InputY/InputY_'+str(index+1)+'.csv'
#            np.savetxt(save_dir_x,i,fmt='%10.5f',delimiter=',')
#            np.savetxt(save_dir_y,generate_labels[index],fmt='%10.5f',delimiter=',')

    elif Mode=='processed':
        Pre_dir=Base_dir+'predict_h5file/GANs_Test/'+Type+'.h5'  
        Pre=load_model(Pre_dir)         
        count=0
        save_data=[]
        save_label=[]
        while count<1000:
            Gen_data,Gen_label=GAN_predict(Gen,latent_size,Data_num,Type=Type)
            generate_labels=(Gen_label+6)/10 
            generate_labels=generate_labels.reshape(Data_num,1)   
            Result=(Pre.predict(Gen_data))*4.6
            error=Result-generate_labels
            for index,i in enumerate(error):
                if abs(i)<=0.25:
                    count+=1
                    if save_data==[]:
                        save_data=Gen_data[index,:,:,:]
                        save_data=save_data.reshape(1,size,size,1)
                    else:
                        temp=Gen_data[index,:,:,:]
                        temp=temp.reshape(1,size,size,1)
                        save_data=np.concatenate((save_data,temp),axis=0)
                    save_label.append(float(generate_labels[index]))
                    if count==1000:
                        break
                    
    number=ConvertToNumber(save_data,size)
    a=set(number)
    temp_count=0
    for i in a:
        temp_count+=1
    #a=np.array(a)
    
#    number=number.reshape(Data_num,1)
#    save_label=save_label.reshape(Data_num,1)

#    save_csv=pd.DataFrame(np.transpose(np.array((number,save_label))))    
    
#        for index,i in enumerate(save_data):
#            i=i.reshape(size,size)
#            save_dir_x=Base_dir+'GANs_result/Predict_result/Processed/InputX/InputX_'+str(index+1)+'.csv'
#            save_dir_y=Base_dir+'GANs_result/Predict_result/Processed/InputY/InputY_'+str(index+1)+'.csv'
#            np.savetxt(save_dir_x,i,fmt='%10.5f',delimiter=',')
#            np.savetxt(save_dir_y,save_label[index],fmt='%10.5f',delimiter=',')


# =============================================================================
#     Gen=load_model(h5_dir)
#     noise_Gen=np.random.randint(-1,1,(Data_num,latent_size))    
#     labels=np.ones(Data_num)*label
#     labels=labels.reshape(Data_num,1)
#     Generate_data=Gen.predict([noise_Gen,labels])
#     Generate_data=Generate_data.reshape(Data_num,4,4)
#     for c in range(len(Generate_data)):
#         for i in range(4):
#             for j in range(4):
#                 if Generate_data[c,i,j]>0.5:
#                     Generate_data[c,i,j]=1
#                 else:
#                     Generate_data[c,i,j]=0
#         Gen_data=Generate_data[c,:,:]
# =============================================================================

#        csv_file=Base_dir+'GANs_result/Predict_result/Label_'+str(Label)+'/'+str(c+1)+'.csv'
#        np.savetxt(csv_file,temp,fmt='%10.5f',delimiter=',')    
    