from multiprocessing import Process
import time
def func():
    for i in range(1000):
        print("子进程",i)
        time.sleep(0.01) #在某些情况下，操作系统可能会优先调度主进程，使其先完成大部分或全部任务，然后再调度子进程
if __name__=="__main__":
    p=Process(target=func)
    p.start()
    for i in range(1000):
        print("主进程",i)
        time.sleep(0.01)