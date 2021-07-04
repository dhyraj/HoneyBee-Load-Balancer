
import threading
import socket
import random
import time

class Node:
    def __init__(self,conn,addr,power):
        self.node = conn
        self.ip = addr
        self.power = power
        self.tasks = []
        self.unLocked = 1
    
    def status(self):
        self.node.send(b"Status")
        data = self.node.recv(1024)
        print("\tIP: ",self.ip[0])
        print("\tPort: ", self.ip[1])
        print("\tAvailaable Power(%): ",(self.power*100.0)%100,"%")
        print("\tTotal tasks: ", len(self.tasks))
        print("\tStatus: ",end="")
        if data != None:
            print("Active")
        else:
            print("Inactive")
    def task(self):
        # snd = "Task"
        self.node.send(b"Task")
        self.node.send(b"Power")
        threading.Thread(target = self.reciever,daemon =True)
        threading.Thread(target = self.reciever,daemon = True)

    def reciever(self):
        # while True:
        data = self.node.recv(1024).decode()
        data.split(":")
        if data[0] == "Power":
            print("powerUpdated:",self.ip)
            self.power = float(data[1])
            self.unLocked = 1
        elif data[0] == "TaskDone":
            print("taskDone",data[1])
            self.tasks.append(float(data[1]))

def dotask():
    # print("doing task")
    counter = 1001
    fib = [0]*counter
    fib[1] = 1
    # for i in range(counter):
    #     for j in range(counter):
    for k in range(counter):
        fib[k] = (fib[k-1]+fib[k-2])
    slp = 2 #random.randint(1,4)
    # print("Sleeping for",slp)
    time.sleep(slp)

def connector(sock):
    global workers
    while True:
        conn,addr = sock.accept()
        print(f"new node connect @{addr[0]}:{addr[1]}")
        data = conn.recv(1024)
        workers.append(Node(conn,addr,float(data.decode())))

if __name__ == "__main__":
    global workers
    workers = []

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(("127.0.0.1",9952))
    s.listen(10)
    t = threading.Thread(target = connector, args = (s,))
    t.daemon = True
    t.start()

    while True:
        print()
        print("1. Status")
        print("2. Tasks")
        print("3. Exit")
        choise = int(input())
        if choise==1:
            print("Total Present Workers: {}".format(len(workers)))
            for i in range(len(workers)):
                print()
                print("Node {}:".format(i+1))
                workers[i].status()

        elif choise == 2:
            tscomplete = []
            n = int(input("Enter no. of Tasks: "))
            s = time.time()
            for w in workers: w.unLocked = 1

            for i in range(n):
                trig = 1
                while True:
                    w = sorted(workers, key = lambda x: x.power * x.unLocked, reverse =True)[0]
                    if w.unLocked ==1:
                        trig = 1
                        w.node.send(b"Task")
                        w.unLocked = 0
                        # w.node.send(b"Power")
                        w.power = float(w.node.recv(1024).decode().split(":")[1]) #*random.randint(1,3)
                        t1 = threading.Thread(target = w.reciever,daemon=True)
                        t1.start()
                        # t2 = threading.Thread(target = w.reciever,daemon = True)
                        # t2.start()
                        tscomplete.extend([t1])
                        print("Task",i+1,"task assigned to",w.ip)
                        break
                    else:
                        if trig:
                            # print("wait")
                            for x in workers:
                                x.unLocked=1
            for i in range(0,n):
                tscomplete[i].join()
                print("Task",i+1,"completed")
            e= time.time()
            print("Total Time Taken: ",e-s,"s")
                # print(w.status())

            print("Rigging same amout of task in a single node:")
            st = time.time()
            for i in range(n):
                dotask()
                print(i+1,"complete")
            en = time.time()
            print("Single server takes:",en-st)
        else:
            for i in workers:
                i.node.close()
            exit()