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

            if data.decode() == "Status":
                print("status asked")
                s.send(b"Running")
            elif data.decode() == "Task":
                print("Task Assigned")
                start = time.time()
                dotask()
                end = time.time()
                result = f"TaskDone:{end-start}"
                print(result)
                s.send(result.encode())
            elif data != None:
                pass
            else:
                s.send(b"random")

threading.Thread(target = listener,daemon=True,args=(s,)).start()
while True:
        data = s.recv(1024)
        tasks.insert(0,data)
        

        # s.send(b"Just Checking")
        # time.sleep(5)
        # s.send(b"Just Checking")
        # time.sleep(5)
        # s.send(b"Just Checking")
