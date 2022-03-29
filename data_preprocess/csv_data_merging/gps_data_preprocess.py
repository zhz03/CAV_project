import pandas as pd 
import numpy as np
import csv
import os

def single_file_output(CSVfile_abs_path,target_path):
    # CSVfile = '/media/carma/easystore8/2nd deployment/Day11/CSV/Tesla_CAV_2022_01_31_104428_cavgt.csv'
    # target_path = './csv_dataset/'
    CSV_paths = CSVfile_abs_path.split('/')
    file_name = CSV_paths[-1]
    file_path = target_path + CSV_paths[-3] + '/' + CSV_paths[-2] + '/'
    print('-'*20)
    print(file_path)
    
    if not os.path.exists(file_path):
        os.makedirs(file_path)
        print('make a new path')
    
    CAV = pd.read_csv(CSVfile_abs_path)
    #CAV_old = pd.read_csv(file_old)
    rows,columns = len(CAV.axes[0]),len(CAV.axes[1])
    Rostime = CAV['ROSTimeMS']
    Rostime_dewe = CAV['ROSTimeMS_Time']
    
    print("#"*20)

    #CAV = pd.read_csv('GPS_info_1_python.csv')

    Rostime_1 = Rostime[Rostime>0.0]
    Num_RosTime=len(Rostime_1)
    print(Num_RosTime)
    # create info
    acc_x=np.zeros((Num_RosTime,1))
    acc_y=np.zeros((Num_RosTime,1))
    acc_z=np.zeros((Num_RosTime,1))
    gyro_x=np.zeros((Num_RosTime,1))
    gyro_y=np.zeros((Num_RosTime,1))
    gyro_z=np.zeros((Num_RosTime,1))
    vn=np.zeros((Num_RosTime,1))
    ve=np.zeros((Num_RosTime,1))
    vd=np.zeros((Num_RosTime,1))
    roll=np.zeros((Num_RosTime,1))
    pitch=np.zeros((Num_RosTime,1))
    heading=np.zeros((Num_RosTime,1))
    lati=np.zeros((Num_RosTime,1))
    longi=np.zeros((Num_RosTime,1))
    alti=np.zeros((Num_RosTime,1))
    ins_sec=np.zeros((Num_RosTime,1))
    ins_nsec=np.zeros((Num_RosTime,1))
    # find corresponding time
    ins_time=CAV["PosAlt_Time"]
    for i in range(Num_RosTime):
      #intermedia_variable=np.array(abs(Rostime_dewe[i]-ins_time))
      intermedia_variable=np.array(abs(Rostime_dewe[i]-ins_time))
      min_value = min(intermedia_variable)
      min_index = np.argmin(intermedia_variable)
      #print(min_index)
      ros_time = Rostime_1[i]
      
      ins_sec[i]=(ros_time-(ros_time%1000))/1000
      ins_nsec[i]=round(ros_time%1000)
      
      acc_x[i]=CAV['AccelX'][min_index]
      acc_y[i]=CAV['AccelY'][min_index]
      acc_z[i]=CAV['AccelZ'][min_index]
      gyro_x[i]=CAV['AngRateX'][min_index] #M(p,56);
      gyro_y[i]=CAV['AngRateY'][min_index]# M(p,58);
      gyro_z[i]=CAV['AngRateZ'][min_index]#M(p,60);
      vn[i]=CAV['VelNorth'][min_index]#M(p,24);
      ve[i]=CAV['VelEast'][min_index]#M(p,26);
      vd[i]=CAV['VelDown'][min_index]#M(p,28);
      roll[i]=CAV['AngleRoll'][min_index]#M(p,84);
      pitch[i]=CAV['AnglePitch'][min_index]#M(p,82);
      heading[i]=CAV['AngleHeading'][min_index]#M(p,80);
      lati[i]=CAV['PosLat'][min_index]#M(p,18);
      longi[i]=CAV['PosLon'][min_index]#M(p,20);
      alti[i]=CAV['PosAlt'][min_index]#M(p,22);

    # write header and data
    header = ['HunterAccelX', 'HunterAccelY', 'HunterAccelZ', 'HunterAngRateX', 'HunterAngRateY', 'HunterAngRateZ', 'HunterVelNorth', 'HunterVelEast', 'HunterVelDown', 'HunterIsoRollAngle', 'HunterIsoPitchAngle', 'HunterIsoYawAngle', 'HunterPosLat', 'HunterPosLon', 'HunterPosAlt', 'ins_sec', 'ins_secn']


    file = open(file_path + file_name, "w")
    writer = csv.writer(file)
    #writer.writerow(header)
    for w in range(Num_RosTime):
      writer.writerow([acc_x[w][0], acc_y[w][0], acc_z[w][0], gyro_x[w][0], gyro_y[w][0], gyro_z[w][0], vn[w][0], ve[w][0], vd[w][0], roll[w][0], pitch[w][0], heading[w][0], lati[w][0], longi[w][0], alti[w][0], ins_sec[w][0], ins_nsec[w][0]])

    file.close()
    print(file_path + file_name)
    print("Process Done")
    

def batch_files(data_path,target_path):
    dayfolder_list = []
    for subfolder in os.listdir(data_path):
        if subfolder[:3] == 'Day':
            dayfolder_list.append(subfolder)
    
    for i,item in enumerate(dayfolder_list):
        dayfolder = data_path + item + '/CSV/'
        for sub_file in os.listdir(dayfolder):
            if sub_file[:5] == 'Tesla':
                # print(sub_file)
                CSVfile_abs_path = dayfolder + sub_file
                single_file_output(CSVfile_abs_path,target_path)
                # print(CSVfile_abs_path)
        print(item + ' is finish!!!')
    
if __name__ == "__main__":
    CSVfile = '/home/zhaoliang/Data_ZZL/mobility_lab/CAV_project/data/Day11/CSV/Tesla_CAV_2022_01_31_104428_cavgt.csv'
    
    target_path = './csv_dataset/' # local folder 
    
    data_path = '/home/zhaoliang/Data_ZZL/mobility_lab/CAV_project/2nd deployment/'
    
    batch_files(data_path,target_path)
                
    # single_file_output(CSVfile,target_path)
    # file_path = './csv_dataset/Day12/'
    # print(os.path.exists(file_path))
