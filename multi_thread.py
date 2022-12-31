from asyncore import write
import time
import threading
import data_structures

#BUFFER_SIZE=20

class prodcons:
    buffers=[data_structures.buffer]*200
    lock=threading.Lock()
    isempty=threading.Condition(lock)
    isfull=threading.Condition(lock)
    write_pos=0
    read_pos=0


def push(b:prodcons,data:data_structures.buffer):
    b.lock.acquire()
    while((b.write_pos+1)%209 == b.read_pos):
        b.isfull.wait()
    b.buffers[b.write_pos]=data
    b.write_pos=b.write_pos+1
    if(b.write_pos>=200):
        b.write_pos=0
    b.isempty.notify()
    b.lock.release()

def get(b:prodcons):
    b.lock.acquire()
    while(b.write_pos==b.read_pos):
        b.isempty.wait()
    res=b.buffers[b.read_pos]
    b.read_pos=b.read_pos+1
    if(b.read_pos>=200):
        b.read_pos=0
    b.isfull.notify()
    b.lock.release()
    return res

'''
def producer():
    for i in range(10):
        push(a,i)
        print(i,"pushed")

def consumer():
    for i in range(10):
        get(a)
        print(i,"get")
'''

'''
def main():
    thread1 = threading.Thread(target=producer)
    thread2 = threading.Thread(target=consumer)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()    
    print('主线程完成了')

main()
'''

