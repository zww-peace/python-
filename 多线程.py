#进程是资源的单位，每个进程至少有一个线程
#线程是执行单位

#启动每一个程序默认都会有一个主线程

#########################第一套写法############################
from threading import Thread
def func():
    for i in range(1000):
        print("func",i)
if __name__=="__main__":
    t=Thread(target=func)#创建线程并给线程分配任务
    t.start() #多线程状态为可以开始工作状态，具体的执行时间由CPU决定
    for i in range(1000):
        print("main",i)
#########################第二套写法#################################
class MyThread(Thread):
    def run(self): #固定的   ->线程被执行的时候，被执行的就是run()
        for i in range(1000):
            print("子线程",i)
if __name__=="__main__":
    t=MyThread()
    #t.run()  方法的调用->单线程
    t.start() #开启线程
    for i in range(1000):
        print("主线程",i)

#########################函数传参##################################
def func(name):
    for i in range(1000):
        print(name,i)
if __name__=="__main__":
    t1 = Thread(target=func,args=("周杰伦",)) #传参必须是元组
    t1.start()
    t2 = Thread(target=func, args=("王力宏",))#单个参数后面必须加逗号
    t2.start()