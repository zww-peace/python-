#协程:当程序遇见了I/O操作的时候，可以选择性的切换到其他任务上
#就像操作系统中讲的CPU不忙等
#在微观上是一个任务一个任务的切换，切换条件一般就是I/O操作
#在宏观上，我们能看到的其实是多个任务一起在执行
#多任务异步操作
#上方所讲的一切都是在单线程的条件下
import asyncio
import time

############################异步协程基本语法########################################
# async def func():
#     print("Hello")
#
# if __name__ =="__main__":
#     g=func() #异步协程函数执行得到的是一个协程对象
#     asyncio.run(g) #协程程序运行需要asyncio模块的支持

#############################异步实现#####################################################
async def func1():
    print("你好啊，我叫潘中聃")
    await asyncio.sleep(3) #异步操作有自己的代码，被切换的任务要被挂起await
    print("你好啊，我叫莎士比亚")
async def func2():
    print("你好啊，我叫安娜贝尔")
    await asyncio.sleep(2)
    print("你好啊，我叫村上春树")
async def func3():
    print("你好啊，我叫乡下野子")
    await asyncio.sleep(4)
    print("你好啊，我叫快乐宝贝")

#if __name__ == "__main__":
#     t1=time.time()
#     f1=func1()
#     f2=func2()
#     f3=func3()
#     tasks=[f1,f2,f3]
#     #一次性启动多个任务(协程)
#     asyncio.run(asyncio.wait(tasks))
#     t2=time.time()
#     print(t2-t1)

###################第二种写法##########################################################
async def main():
    #第一种
    #f1=func1()
    #await f1 #一般await挂起操作放在协程对象前面
    #第二种（推荐）
    tasks=[
        asyncio.create_task(func1()),
        asyncio.create_task(func2()),
        asyncio.create_task(func3())]
    await asyncio.wait(tasks)  #外面已经在run了
if __name__=="__main__":
    t1 = time.time()
    asyncio.run(main()) #这里在run
    t2=time.time()
    print(t2-t1)
