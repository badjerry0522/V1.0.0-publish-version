import multi_thread
import cv2
import threading
import time
import data_structures
length=640
width=480
frame_count=500
a=multi_thread.prodcons()

def get_time_diff(last_time,cur_time):
    return (cur_time-last_time)


def producer():
    print("producer begin")
    
    camera=cv2.VideoCapture(0)
    camera.set(3,length)
    camera.set(4,width)
    camera.set(cv2.CAP_PROP_FPS,60)

    last_time=0
    print("camera init complete")
    
    for i in range(frame_count):
        flag,img=camera.read()
        st=time.time()
        buffer_now=data_structures.buffer(img,length,width,st,i,0)
        multi_thread.push(a,buffer_now)
        print("read time=",get_time_diff(last_time,st))
        last_time=st
        
    
    img=camera.read()
    st=time.time()
    buffer_now=data_structures.buffer(img,length,width,st,i,1)
    multi_thread.push(a,buffer_now)
    multi_thread.push(a,buffer_now)
    multi_thread.push(a,buffer_now)
    multi_thread.push(a,buffer_now)


def consumer():
    print("consumer begin")
    last_time=0
    while(1):
        buffer_rcv=multi_thread.get(a)
        if(buffer_rcv.isOver==1):
            break
        file_pos="../imgs/"+str(buffer_rcv.index)+".jpg"
        cv2.imwrite(file_pos,buffer_rcv.img)
        print("writing",buffer_rcv.index)
        
        time_consumed=(buffer_rcv.cur_time-last_time)
        print("write time=",time_consumed)
        last_time=buffer_rcv.cur_time

def main():
    thread1=threading.Thread(target=producer)
    thread2=threading.Thread(target=consumer)
    thread3=threading.Thread(target=consumer)
    thread4=threading.Thread(target=consumer)
    thread5=threading.Thread(target=consumer)
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()

main()