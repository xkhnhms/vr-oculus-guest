# -*- coding:utf-8 -*-
# author:WHJ\TZM
from time import sleep
from Master import *
#from modbus_tk import modbus_rtu
#import multiprocessing
#from threading import Thread

class _RG2():  
    def __init__(self,master=MTCPMaster,id=1):
        self._master=master
        self._id=id
        #Write
        self._target_force=0
        self._target_width=0
        self._Set_Fingertip_offset=0
        #Read
        self._Fingertip_offset=0
        self._Actual_depth=0
        self._Actual_relative_depth=0
        self._Actual_width=0
        self._Status=0
        self._Actual_width_with_offset=0
        self.address_num = 3
        self.function_list = [i for i in range(1101,1108)]
        print ("Run RG2...")
        
    #select mode
    def function_select(self,mode,command):
        if mode == 1101: return self.wait_free(command)
        elif mode == 1102: return self.reset()
        elif mode == 1103: return self.get_status()
        elif mode == 1104: return self.grip(command,1)#不带偏置运动
        elif mode == 1105: return self.stop()
        elif mode == 1106: return self.grip(command,16)#带偏置运动
        elif mode == 1107: return self.set_Fingertip_offset(command)
        
    # Function 1
    def wait_free(self,command):
        '''阻塞等待'''
        try :
            num = command[0]
        except: 
            num = command
        a=0
        while(a<num):
            a+=0.1
            ret=self._master.read_AO(self._id,268,1)
            if(ret[0]!=1):
                return False
            sleep(0.1)
        return True
    # Function 2
    def reset(self):
        '''重启电源'''
        ret=self._master.read_AO(self._id,268,1)
        if(ret[0]>2):
            print("command:Reset RG2")
            self._master.write_AO(63,0,[2])
            sleep(3)
            self._target_force=0
            self._target_width=0
            self._Set_Fingertip_offset=0
            print("command:Reset RG2 OK")
        return 0
    #Function 3
    def get_status(self):
        '''获取夹爪参数'''
        ret=self._master.read_AO(self._id,258,1)
        self._Fingertip_offset=ret[0]

        ret=self._master.read_AO(self._id,263,2)
        self._Actual_depth=ret[0]
        self._Actual_relative_depth=ret[1]

        ret=self._master.read_AO(self._id,267,2)
        self._Actual_width=ret[0]
        self._Status=ret[1]

        ret=self._master.read_AO(self._id,275,1)
        self._Actual_width_with_offset=ret[0]

        info_opt = ['busy','detected','S1_pushed','S1_trigged','S2_pushed','S2_trigged','Safety_error']
        status_code = bin(self._Status)[2:]
        info_status = [bool(int(status_code[0-i])) for i in range(len(status_code))]
        information = {}
        for i in range(len(info_opt)):
            try:
                information[info_opt[i]] = info_status[i]
            except:
                information[info_opt[i]]  = False

        status ={"Fingertip_offset":self._Fingertip_offset,
                "Actual_depth":self._Actual_depth, 
                "Actual_relative_depth":self._Actual_relative_depth,
                "Actual_width":self._Actual_width,
                "Status":information,
                "Actual_width_with_offset":self._Actual_width_with_offset}
        return status
    #Function 4
    def grip(self,command,offest):
        '''夹爪动作，
        若 command[2] == 1，加16s阻塞等待'''
        ret=0
        force = command[0]
        width = command[1]
        block = command[2]
        if(self._target_force!=force):
            self._target_force=force
            ret=1
        if(self._target_width!=width):
            self._target_width=width
            ret=1
        if(ret==1):
            print("command:grip")
            self.wait_free(30)
            self._master.write_AO(self._id,0,[force,width,offest])
            if block:
                self.wait_free(16)
        else:
            print("command:nothing")
        return 0
    #Function 5
    def stop(self):
        '''夹爪停止运动'''
        print("command:stop")
        self._master.write_AO(self._id,2,[8])
        return 0
    #Funcion 7
    def set_Fingertip_offset(self,command):
        '''设置手指偏置'''
        offset = command[0]
        print ("command:set_Fingertip_offset")
        self._master.write_AO(self._id,1031,[offset])
        return 0
    
if __name__ == '__main__':
    pass
    