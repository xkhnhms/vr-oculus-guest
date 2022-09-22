
import sys,os

# sys.path.append("./SDK")
sys.path.insert(0,r'C:\Users\fs\Desktop\vr-oculus-guest-master\SDK') #JAKA SDK path
# sys.path.insert(0,r'./SDK') #JAKA SDK path

# import jkrc

try:
    # from SDK import jkrc
    import jkrc
except:
    raise NameError("JAKA SDK path error! current work path: ",os.path.abspath('.'))

class Robot():  ##创建机器人线程类
    def __init__(self):  ##初始化创建机器人并登录
        self.ABS = 0  # 绝对运动
        self.INCR = 1  # 增量运动
        self.robot = jkrc.RC('192.168.156.128')
        # self.robot = jkrc.RC('10.5.5.100')
        # self.robot = jkrc.RC('192.168.1.100')
        self.robot.login()
        self.robot.power_on()
        self.robot.enable_robot()

    def run(self):  ##start时机器人回到设定的初始位置
        for i in range(20):
            self.robot.joint_move([1, 1, 1, 0, 0, 0], 0, True, 1)
            self.robot.joint_move([1, 1, 0, 0, 0, 0], 0, True, 1)


# address="192.168.156.128"
# robot = jkrc.RC(address)
# print("[JAKA] logining...")
#
# ret = robot.get_sdk_version()
# print("SDK version is:",ret[1])
#
#
# robot.login()
# print(1)
#
# ans=robot.power_on()
# print(ans)
# if not robot.power_on():
#     print("[JAKA] power_on successfully")
#
# robot.enable_robot()
#
# # test pos
# for i in range(20):
#     robot.joint_move([1,1,1,0,0,0],0,True,1)
#     robot.joint_move([1,1,0,0,0,0],0,True,1)

if __name__=="__main__":
    rb=Robot()
    rb.run()
