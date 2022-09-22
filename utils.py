import random
import time

from pydub import AudioSegment
from pydub.playback import play
import os
import pandas as pd
import numpy as np
import csv
'''
https://blog.csdn.net/wangxiaobei2017/article/details/93195120

https://blog.csdn.net/weixin_45263626/article/details/108428448
'''
# base_path=r'E:\\codes\\audio'
base_path=r'./audio'

def play_music():
    files=[]

    for dir_pth,dir_name,file_names in os.walk(os.path.join(base_path,'music')):
        print(dir_pth,dir_name,file_names)
        for file in file_names:
            files.append(os.path.join(dir_pth,file))

    print(len(files))
    print(files)
    rand_num=random.randint(0,len(files)-1)
    current_file=files[rand_num]
    print(current_file)
    format_file=current_file.split('.')[2]

    if format_file=='mp3':
        song = AudioSegment.from_mp3(current_file)
        play(song)

    elif format_file=='wav':
        song=AudioSegment.from_wav(current_file)
        play(song)

def write2csv(data,save_path='./sample.csv'):
    data=np.asarray(data)
    pd.DataFrame(data).to_csv(save_path)


def write_csv(path, data_row):
    with open(path,'a+') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(data_row)




if __name__ == '__main__':
    # play_music()
    # a = np.asarray([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    # write2csv(a)
    path = "file_name.csv"
    data_row=[1, 2, 3]
    data_row.append(time.asctime())
    write_csv(path, data_row)

    print(time.asctime())
    print(time.time())

    pass
