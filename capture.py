import cv2

def capture_one_frame(camera,camera_type,file_pos,index):
    if(camera_type==0):
        flag,img=camera.read()
        return img
    if(camera_type==1):
        flag,img=camera.read()
        return cv2.resize(img,(1280,720))
    if(camera_type==2):
        img=cv2.imread(file_pos+str(index)+".jpg")
        return img