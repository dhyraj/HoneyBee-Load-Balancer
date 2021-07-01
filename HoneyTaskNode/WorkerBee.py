import threading
import socket
import time
import random
import psutil as pt
def dotask():
    print("here")
    counter = 1001
    fib = [0]*counter
    fib[1] = 1
    # for i in range(counter):
    #     for j in range(counter):
    for k in range(counter):
        fib[k] = (fib[k-1]+fib[k-2])
    slp = random.randint(1,4)
    print("Sleeping for",slp)
    time.sleep(slp)

def powerCalc():
    cpuStat =  pt.virtual_memory()
    return cpuStat.available/cpuStat.total

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("localhost",9952))
pow = f"{powerCalc()}"
s.send(pow.encode()) #power of cpu
print(s)

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
            s.send(res.encode())

threading.Thread(target = listener,daemon=True,args=(s,)).start()
while True:
        data = s.recv(1024)
        if data.decode()=="Power":
            pow = f"Power:{powerCalc()}"
            print(pow)
            s.send(pow.encode())
        elif data.decode() == "Status":
            s.send(b"Running")
        elif data.decode() == "Task":
            print("task!!!")
            t = threading.Thread(target = dotask,daemon = True)
            tasks.append(t)

