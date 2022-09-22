from ctypes import c_bool
import socket, threading
import msvcrt
import numpy as np
import time
import datetime
import sys
import math
sys.path.insert(0,r'C:\Users\fs\Desktop\vr-oculus-guest-master\SDK') #JAKA SDK path
import jkrc
from numpy import *
from utils import *
import threading


from Master import *
import RG2

# global msg
# 90.908
###########Robot thread
class Robot():                             ##创建机器人线程类
    def __init__(self):                                    ##初始化创建机器人并登录
        self.ABS = 0 # 绝对运动
        self.INCR = 1 # 增量运动
        # self.robot = jkrc.RC('192.168.156.128')
        # self.robot = jkrc.RC('10.5.5.100')
        self.robot = jkrc.RC('192.168.1.100')
        self.robot.login()
        self.robot.power_on()
        self.robot.enable_robot()
        
    def run(self):                                         ##start时机器人回到设定的初始位置
        self.robot.servo_move_enable(False) #关闭伺服使能
        time.sleep(0.1)
        # self.robot.servo_move_use_joint_MMF(max_buf=8, kp=0.2, kv=0.3 ,ka=0.6)
        # 【0-1】 参数越小 滤波率的越恨  跟随性和复现性就越差
        self.robot.servo_move_use_joint_LPF(0.1)
        # self.robot.set_user_frame_id(0)
        time.sleep(0.1)


        # joint_pos = [0.04398210451818206, 1.5808151070257108, 2.084332306298577, 1.0353411372029384, -1.51052762936927, -1.499921590541316] #zu
        # joint_pos = [-0.9168449881032902,2.3991903861175707,1.9772282312428453,0.33597024935007097,-1.5707963,-1.5655552757820648]
        joint_pos = [-0.02400230395981029, 0.20732320934987822, 1.5600457020782084, 3.1415925996353495, -1.374223703468782, -0.024002324962014616] #mini
        # joint_pos = [-0.02400230395981029, 0.20732320934987822, 1.5600457020782084, 3.1415925996353495,-1.374223703468782, 0.791002324962014616]
        # joint_pos = [-4.77785728754739, -0.42632917278613436, 1.4017536495986367, 3.37637592685837, -0.6481290005918211, -0.29341111038335194]
        self.robot.joint_move(joint_pos,move_mode = self.ABS ,is_block = True ,speed = 3)
        
    def setting(self,quaternion):
        #quaternion to rpy
        self.robot.set_user_frame_id(0)

        time.sleep(0.3)
        ret,status = self.robot.get_robot_status()

        ret,rot = self.robot.quaternion_to_rot_matrix (quaternion)

        ret,rpy = self.robot.rot_matrix_to_rpy(rot)

        #设置用户坐标系
        Fram_date = list(status[18])                              ##将当前tcp位置设置为用户坐标系

        print(Fram_date)
        print("我是用户坐标系：{}".format(Fram_date))
        self.robot.set_user_frame_data(2,Fram_date, 'realsense2')

        #初始化rpy
        self.rpyl_x = rpy[0]
        self.rpyl_y = rpy[1]
        self.rpyl_z = rpy[2]
        #开启伺服滤波
        # print("ready")
        self.robot.servo_move_enable(True)
        time.sleep(0.1)
        self.robot.set_user_frame_id(2)
        time.sleep(0.1)

        
        self.posc_x = 0
        self.posc_y = 0
        self.posc_z = 0
        
    def move(self,pos_x,pos_y,pos_z,quaternion):           ##机器人运动
        ret,status = self.robot.get_robot_status()
        self.robot.set_user_frame_id(2)
        #四元数变化欧拉角
        ret,rot = self.robot.quaternion_to_rot_matrix (quaternion)
        ret,rpy = self.robot.rot_matrix_to_rpy(rot)

        #统一坐标轴
        pos_rx = 0
        pos_ry = 0 
        pos_rz = 0

        if abs(self.posc_x - pos_x) < 0.5:   ##posc_x 上一次的坐标  pos_x新的坐标 : origin:1
            self.posc_x = self.posc_x           ##如果差小于1mm 值还等于上次的
        else:
            self.posc_x = pos_x            ##如果大于1mm 坐标等于新的值
        if abs(self.posc_y - pos_y) < 0.5:
            self.posc_y = self.posc_y
        else:
            self.posc_y = pos_y
        if abs(self.posc_z - pos_z) < 0.5:
            self.posc_z = self.posc_z
        else:
            self.posc_z = pos_z
        
        #设置用户坐标系并逆解
        # cartesian_pose = [-self.posc_x,-self.posc_z,-self.posc_y,-pos_rx,-pos_ry,-pos_rz]
        # cartesian_pose = [self.posc_z, -self.posc_x, -self.posc_y, -pos_rx, -pos_ry, -pos_rz]  # zu
        cartesian_pose = [-self.posc_z, self.posc_x, -self.posc_y, -pos_rx, -pos_ry, -pos_rz]  #minicobo

        # print("我是Rpos{}".format(cartesian_pose))
        
        ret,pos = self.robot.kine_inverse(status[19],cartesian_pose)
        self.robot.servo_j(joint_pos = pos, move_mode = self.ABS)
    
    def gripper(self, iotype, index,state):
        self.robot.set_digital_output(iotype, index, state)
        num_val = self.robot.get_digital_output(iotype, index)
        print(num_val)

    def run_program(self, program):
        self.robot.program_load(program)
        self.robot.get_loaded_program()
        self.robot.program_run()

    def greet(self):

        ret,pos = self.robot.get_joint_position()

        ratioa=[0.986509421,0.926847625,0.780530599,1.779319484,0.998265933,1.01682883]
        # ratioa = [0.990526821,0.993808235,0.80422894,1.320692079,0.998795554,1.011601975]
        up_pos =[pos[i]*ratioa[i] for i in range(len(pos))]

        # self.robot.servo_move_enable(True)

        # self.robot.joint_move(up_pos, self.ABS,False, 1)
        self.robot.servo_j(joint_pos=up_pos, move_mode=self.ABS)

        # self.robot.joint_move(pos, self.INCR, False, 1)
        # self.robot.linear_move(pos, self.INCR, False, 1)
        # self.robot.joint_move(pos, self.ABS,False, 1)
        # self.robot.joint_move(pos, self.ABS, False, 1)

        # self.robot.servo_move_enable(True)
        self.robot.servo_j(joint_pos=pos, move_mode=self.ABS)


    def sixJoint(self):
        global msg
        jointP = self.robot.get_joint_position()
        if jointP[0] == 0:
            #print("the jointposition is", jointP[1]*180/math.pi)
            msg = jointP[1] 
            msg = [i * 180 / math.pi for i in msg]
            print(msg)
            msg = " ".join(map(str, msg))
            print(msg)
        #     return  msg
        # return None
    
    def _del_(self):
        self.robot.logout()      

#################             主程序                ###################
PORT = 5500
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
print(ADDR)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(ADDR)

force = 30  # 20~100
offest = 500
master=MTCPMaster('192.168.1.1',502)
grippper = RG2._RG2(master, 65)

done = False
#启动机器人线程
Rb = Robot()
Rb.run()
print("i will run")
time.sleep(0.1)
num = 0
OC = 0
# quaternions=[]

if msvcrt.kbhit():
    key = msvcrt.getch()
    if(key == b'a'):
        print("you pressed",key,"so now i will quit")
        done = True
        del(Rb)
        s.close()
#循环体
while not done:
    Rb.sixJoint()
    data, addr = s.recvfrom(1024)  # 返回数据和接入连接的（服务端）地址,得到服务端发来的数据和地址
    # get_data_time1=time.asctime() # get current time
    get_data_time1=time.time()
    data = data.decode()  # 解码数据
    s.sendto(msg.encode('gbk'), ("127.0.0.1", 5501))

    if(len(data) > 4):
        lis_data = data.replace('(', '')
        lis_data = lis_data.replace(')', ',').split(',')
    else:
        OC = data
    if OC == "O":
        Rb.gripper(1,0, state = True)
        # Rb.gripper(0, 1, state=True)
        width = 1200
        grippper.grip([force, width, True], offest)
        OC = 0
    if OC == "C":
        Rb.gripper(1,0, state = False)
        # Rb.gripper(0, 1, state=False)
        width = 300
        grippper.grip([force, width, True], offest)
        OC = 0
    if OC == "D": #DANCE
        print('---music----------')
        thread_open = threading.Thread(target=play_music)
        # play_music()
        thread_open.start()
        OC = 0
    if OC == "G": # GREET
        print('---greet----')
        # Rb.greet()
        # Rb.setting(quaternions[3])
        # Rb.move(quaternions[0], quaternions[1], quaternions[2], quaternions[3])
        OC = 0
    if lis_data:
    #格式化坐标信息
        pos_x = float(lis_data[0]) * 500
        pos_y = float(lis_data[1]) * 500
        pos_z = float(lis_data[2]) * 500
        quaternion_x = float(lis_data[3])
        quaternion_y = float(lis_data[4])
        quaternion_z = float(lis_data[5])
        quaternion_w = float(lis_data[6])
        quaternion = [quaternion_w,quaternion_x,quaternion_y,quaternion_z]

    #执行一次机器人setting
        if num == 0 :
            print("i will set")
            Rb.setting(quaternion)
            num = num + 1
            time.sleep(0.2)
        # print(pos_z, -pos_x, -pos_y, quaternion) #Zu
        print(-pos_z, pos_x, -pos_y, quaternion)

        Rb.move(pos_x, pos_y, pos_z,quaternion)

print('over')


