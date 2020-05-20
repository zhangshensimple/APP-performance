#coding=utf-8
import csv,time,os

class App(object):
    def __init__(self):
        self.content =''
        self.startTime=0
    #启动app
    def LaunchApp(self):
        cmd = 'adb shell am start -W -n com.unicom.wopay/.app.MainActivity'
        self.content=os.popen(cmd)
    #停止app
    def StopApp(self):
        # cmd = 'adb shell am force-stop com.unicom.wopay' #强制退出app
        cmd='adb shell input keyevent 3'#按home键，使app进入后台运行
        os.popen(cmd)
    #获取启动时间
    def GetLaunchTime(self):
        for line in self.content.readlines():
            if 'ThisTime' in line:
                self.startTime=line.split(':')[1]
                break
        return self.startTime

#控制类
class Controller(object):
    def __init__(self,count):
        self.app = App()
        self.counter=count
        self.alldate=[('timeestamp','elapsedtime')]

    #单次启动过程
    def testprocess(self):
        self.app.LaunchApp()
        time.sleep(3)
        elapsedtime = self.app.GetLaunchTime()
        self.app.StopApp()
        time.sleep(3)
        currenttime = self.getCurrentTime()
        self.alldate.append((currenttime,elapsedtime))
    #多次执行过程
    def run(self):
        while self.counter>0:
            self.testprocess()
            self.counter=self.counter-1
    #获取当前时间戳
    def getCurrentTime(self):
        currentTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        return currentTime
    #时间数据存储
    def SaveDate(self):
        csvfile = open('starttime.csv','w')
        writer = csv.writer(csvfile)
        writer.writerows(self.alldate)
        csvfile.close()

if __name__ =='__main__':
    controller = Controller(4)
    controller.run()
    controller.SaveDate()