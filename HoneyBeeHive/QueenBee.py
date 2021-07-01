
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
        print("\tAvailaable Power(%): ",self.power*100.0,"%")
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
            for i in range(n):
                w = sorted(workers, key = lambda x: x.power * x.unLocked, reverse =True)[0]
                w.node.send(b"Task")
                w.unLocked = 0
                w.node.send(b"Power")
                t1 = threading.Thread(target = w.reciever,daemon=True)
                t1.start()
                t2 = threading.Thread(target = w.reciever,daemon = True)
                t2.start()
                tscomplete.extend([t1,t2])
                print(i+1,"th task assigned to",w.ip)
            for i in range(n*2):
                tscomplete[i].join()
                print(i,"th completed")
            e= time.time()
            print("Total Time Taken: ",e-s,"s")
                # print(w.status())
        else:
            for i in workers:
                i.close()
            exit()