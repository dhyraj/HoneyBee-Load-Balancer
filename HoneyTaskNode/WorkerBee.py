import threading
import socket
import time
import random
import psutil as pt
def dotask():
    print("doing task")
    counter = 1001
    fib = [0]*counter
    fib[1] = 1
    # for i in range(counter):
    #     for j in range(counter):
    for k in range(counter):
        fib[k] = (fib[k-1]+fib[k-2])
    slp = 2 #random.randint(1,4)
    print("Sleeping for",slp)
    time.sleep(slp)

def powerCalc():
    cpuStat =  pt.virtual_memory()
    return cpuStat.available/cpuStat.total

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("localhost",9952))
pow = f"{powerCalc()}"
s.send(pow.encode()) #power of cpu
print(s,pow)

tasks = []
def listener(s):
    while True:
        if len(tasks)>0:   
            data = tasks.pop()
            st = time.time()
            data.start()
            data.join()
            en = time.time()
            res = f"taskDone:{en-st}"
            print(res)
            s.send(res.encode())
            print("completed")

threading.Thread(target = listener,daemon=True,args=(s,)).start()
while True:
        data = s.recv(1024).decode()
        if data =="Power":
            pow = f"Power:{powerCalc()}"
            print(pow)
            s.send(pow.encode())
            print("power sent")
        elif data == "Status":
            s.send(b"Running")
        elif data == "Task":
            print("task!!!")
            t = threading.Thread(target = dotask,daemon = True)
            tasks.append(t)
            pow = f"Power:{powerCalc()}"
            s.send(pow.encode())