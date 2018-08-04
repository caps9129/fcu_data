import pandas as pd
import datetime
import sys, traceback
import re
import matplotlib.pyplot as plt
import time,datetime

plt.rcParams['font.sans-serif']=['DFKai-SB']
plt.rcParams['axes.unicode_minus']=False

df_list = []


arr_Student_Objects = []


file_name = "./newdata/new20170213-{}.csv"

region_dict = {'行政一館':'aa', '忠勤樓':'ab', '語文大樓':'ac', '人言大樓':'ad', '理學院':'ae', '資訊電機館':'af',
               '商學院':'ah', '行政二館':'ba', '工學館':'bb', '建築館':'bc', '土水館':'bd', '圖書館':'be', '育樂館':'bg',
               '體育器材室':'bh', '紀念館':'bi', '科航館':'bj', '體育館':'bk', '電通館':'bm', '學思樓':'bn', '人社館':'bw',
               '男生宿舍':'bdorm', '文華創意中心':'cb', '女生宿舍':'gdorm', '中科校區':'zk'}


   

class Student(object):
    def __init__(self, mac, loc, time, count):
        self.mac = mac
        self.loc = loc
        self.time = time
        self.count = count

      
def add_column():

    for read_index in range(1, 3):

        df = pd.read_csv(file_name.format(read_index))
        df.loc[-1] = df.columns.values
        df.index = df.index + 1  # shifting index
        df = df.sort_index()
        df.columns = ['time', 'mac', 'loc']
        df_list.append(df)

    df = pd.concat(df_list)
    df = df.reset_index(drop=True)
  
    return df
 
def sort_by_time(df):

    df['time'] = pd.to_datetime(df.time)

    df = df.sort_values(by = 'time')

    df = df.reset_index(drop = True)

    return df




def erase_duplicate(arr_Object, Object):
    arr_Object.reverse()
    for index in range(len(arr_Object)):
        if(Object.mac == arr_Object[index].mac):
            # print("新加入:", Object.mac, ",", Object.time)
            # print("在原陣列:", arr_Object[index].mac, ",", arr_Object[index].time)
            after = pd.to_datetime(arr_Object[index].time, format = '%Y-%m-%d %H:%M:%S')
            before = pd.to_datetime(Object.time, format = '%Y-%m-%d %H:%M:%S')
            # now = (datetime.datetime(before_time) - datetime.datetime(nowa_time)).total_seconds()
            time = before-after
            if(time.total_seconds() >= 120):
                arr_Object.reverse()
                arr_Object.append(Object)
                # print(time.total_seconds())
                break      
            else:
                break
            # sys.exit(0)
            # if(arr_Object[index].time)
        else:
            if(index + 1 == len(arr_Object)):
                arr_Object.reverse()
                arr_Object.append(Object)
            continue

        
           



def unique_user(arr_Object):
   
    list_temp = list()

    global list_name
    list_name = list()

    global list_usercount
    list_usercount = list()

    for index in range(len(arr_Object)):
        list_temp.append(arr_Object[index].mac)
    # print(list_temp)    
    list_name = list(set(list_temp))
    # print(list_name)
    for list_name_index in range(len(list_name)):
        count = 0
        for list_temp_index in range(len(list_temp)):
        
            if(list_name[list_name_index] == list_temp[list_temp_index]):
                count = count + 1
         
            if(list_temp_index + 1 == len(list_temp)):
                list_usercount.append(count)
                break
    # print(list_count)

def unique_region(arr_Object):
    
    list_temp = list()

    global list_region
    list_region = list()

    global list_regioncount
    list_regioncount = list()

    for index in range(len(arr_Object)):
        if(arr_Object[index].loc[0:5].find("_") != -1):
            list_temp.append(arr_Object[index].loc[0:2])
        else:
            list_temp.append(arr_Object[index].loc[0:5])  

    list_region = list(set(list_temp))  

    for list_region_index in range(len(list_region)):
        count = 0
        for list_temp_index in range(len(list_temp)):
        
            if(list_region[list_region_index] == list_temp[list_temp_index]):
                count = count + 1
         
            if(list_temp_index + 1 == len(list_temp)):
                list_regioncount.append(count)
                break  



def main():
   
    df = add_column()
    df = sort_by_time(df)
    # print(df)
    for index, row in df.iterrows():
    # print(index)
        if(index == 0):
            continue
        elif(index == 1):
            arr_Student_Objects.append(Student(row[1], row[2], row[0], 0))    
            # print(arr_Student_Objects[index].time, ",", arr_Student_Objects[index].mac, ",", arr_Student_Objects[index].loc)
        else:
            Student_Objects = Student(row[1], row[2], row[0], 0)
            erase_duplicate(arr_Student_Objects, Student_Objects)

    # for arr_index in range(len(arr_Student_Objects)):
    #     print(arr_Student_Objects[arr_index].time, ",", arr_Student_Objects[arr_index].mac, ",", arr_Student_Objects[arr_index].loc)    

    unique_user(arr_Student_Objects)  # 每個使用者統計次數
    
    unique_region(arr_Student_Objects) # 每個地區統計次數
    
    for index in range(len(list_region)):
        list_region[index] = list(region_dict.keys())[list(region_dict.values()).index(list_region[index])]
    
    plt.plot(list_usercount)
    plt.show()


    plt.plot(list_region, list_regioncount)
    plt.show()



if __name__ == "__main__":
    main()

    sys.exit(0)
 


