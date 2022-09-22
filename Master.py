import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
class MTCPMaster():
    def __init__(self, host='127.0.0.1',port=502):
        self.master = modbus_tcp.TcpMaster(host,port,0.5)
        self.master.open()
           
    def open(self):
        self.master.open()

    def close(self):
        self.master.close()

    def read_DI(self,id,address,length):
        try:
            return self.master.execute(id, cst.READ_DISCRETE_INPUTS, address, length)  
        except:
            print('no master')
            return [9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999]

    def write_DO(self,id,address,value):
        try:
            self.master.execute(id, cst.WRITE_MULTIPLE_COILS,address,output_value = value)
        except:
            print('no master')

    def read_AI(self,id,address,length):
        try:
            return self.master.execute(id,cst.READ_INPUT_REGISTERS,address,length)
        except:
            print('no master')
            return [9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999]

    def write_AO(self,id,address,value):
        try:
            # self.master.execute(id, cst.WRITE_SINGLE_REGISTER, address,output_value= value)
            self.master.execute(id, cst.WRITE_MULTIPLE_REGISTERS, address,output_value= value)
        except:
            print('write ao no master: ',id,address,value)

    def read_DO(self,id,address,length):
        try:
            return self.master.execute(id,cst.READ_COILS,address,length)
        except:
            print('no master')
            return [9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999]

    def read_AO(self,id,address,length):
        try:
            return self.master.execute(id,cst.READ_HOLDING_REGISTERS,address,length)
        except:
            print(id,address,length)
            print('read ao no master')
            return [9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999,9999]

if __name__=='main':
    master = MTCPMaster('1111')
    import RG2
    grippper = RG2._RG2(master, 65)
    force = 0 # 20~100
    width = 0 # 0~1100
    grippper.grip([force,width,True])
