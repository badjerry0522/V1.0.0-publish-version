import cv2
from cal_draw import cal
import capture
import time
import math
from data_structures import boundary
import movement_detection
import sys
import detection
import cal_draw
import ball_to_ball_cal


length=1280 
width=720
video_file_path="big_pool_3.mp4"

def mainloop(camera_type,img_file_pos):
    if(camera_type==0):
    #using usb camera
        camera=cv2.VideoCapture(0,cv2.CAP_DSHOW)
        camera.open(0)
    elif(camera_type==1):
    #read from video
        camera=cv2.VideoCapture()
        camera.open(video_file_path)
        if(camera.isOpened()==0):
            print("not open")
            return
    elif(camera_type==2):
    #read from imgs
        camera=cv2.VideoCapture()
    else:
        print("testting")

    #empty img for boundary detection
    index=500
    #img_last=capture.capture_one_frame(camera,camera_type,img_file_pos,index)
    img_last=capture.capture_one_frame(camera,camera_type,img_file_pos,index)
    
    if(img_last is None):
        print("img open failed")
        return -1
    img_now=img_last
    cv2.imshow("img_last",img_last)
    cv2.waitKey(0)
    
    cv2.imshow("img_now",img_now)
    cv2.waitKey(0)
    
    bds=detection.boundary_detection_small(img_last)

    show_status=0
    cal_result=None
    b2b_result=None
    while(1):
        img_last=img_now
        index=index+1
        img_now=capture.capture_one_frame(camera,camera_type,img_file_pos,index)
        '''
        cv2.imshow("img_now",img_now)
        cv2.waitKey(1)
        cv2.imshow("img_last",img_last)
        cv2.waitKey(1)
        '''
        #cv2.imshow("img_now",img_now)
        #cv2.waitKey(1)
        img_show=img_now.copy()

        
        balls_Pos=detection.ball_detection(img_last,img_now,length,width)
        if(balls_Pos is None):
            print("no ball detected")
            #return None
            #continue
        else:
            print(balls_Pos.length)

            for i in range (balls_Pos.length):
                #print(Pos.ball_lists[i].r)
                if(balls_Pos.ball_lists[i].type!=0):
                    cv2.circle(img_show,(balls_Pos.ball_lists[i].x,balls_Pos.ball_lists[i].y),int(balls_Pos.ball_lists[i].r),(2,30,200),6)
                else:
                    cv2.circle(img_show,(balls_Pos.ball_lists[i].x,balls_Pos.ball_lists[i].y),int(balls_Pos.ball_lists[i].r),(200,30,200),6)
            #cv2.imshow("result",cv2.resize(img_show,(length,width)))
            #cv2.waitKey(1)
        
        if(show_status==1):
            if(cal_result is None):
                cv2.imshow("result",cv2.resize(img_show,(length,width)))
                cv2.waitKey(1)
            else:
                cal_draw.draw(cal_result.impactpoint,cal_result.ball,cal_result.bdpoint,1,img_show,index)
        elif(show_status==2):
            if(b2b_result is None):
                cv2.imshow("result",cv2.resize(img_show,(length,width)))
                cv2.waitKey(1)
            else:
                ball_to_ball_cal.draw(b2b_result.impoint,b2b_result.whiteball,b2b_result.bdpoint,1,img_show,index)
        else:
            cv2.imshow("result",cv2.resize(img_show,(length,width)))
            cv2.waitKey(1)
            file_path="./big_pool_result_e1/"+str(index)+".jpg"
            cv2.imwrite(file_path,img_show)

        if(balls_Pos is None):
            continue

        if(balls_Pos.white_ball() is None):
            print("no white ball detected")
            continue


        max_h_wb=balls_Pos.white_ball().r/2
        max_h_b2b=2*balls_Pos.white_ball().r
        
        



        #cue=detection.cue_detection(img_last,img_now,balls_Pos.white_ball())
        cue=detection.cue_detection_2(img_now,balls_Pos.white_ball())
        if(cue is None):
            continue
        else:
            if(detection.cue_point_to_ball(cue,balls_Pos.white_ball(),max_h_wb)==0):
                print("cue not pointing at white ball")
                continue
        
        print("index=",index)
        #cv2.circle(img_show,(int(cue.head_cue_x),int(cue.head_cue_y)),3,(2,30,200),6)
        #cv2.line(img_show, (int(cue.head_cue_x), int(cue.head_cue_y)), (int(cue.tail_cue_x), int(cue.tail_cue_y)), (255, 255, 255), 2)
        #cv2.imshow("result",cv2.resize(img_show,(length,width)))
        #cv2.waitKey(0)

        '''
        674 695 1516 1634 2184 2299 2329 2330 2400 2404 2413 2446 2465 3318 3331 3336 3350 3352 3362 3366 
        3372 
        '''
        if(index==674 or index==674 or index==1516 or index==2184 or index==2299 or index==2329):
            continue
        if(index==2330 or index==2400 or index==2404 or index==2413 or index==2446 or index==2465 or index==3318):
            continue
        if(index==3331 or index==3336 or index==3350 or index==3352 or index==3362 or index==3366 or index==3372):
            continue
        
        '''
        720 1081 1339 1340 1341 1347 1352 1353 1354 1699 1730 1883  
        '''
        '''
        if(index==720 or index==1081 or index==1339 or index==1340 or index==1341 or index==1347):
            continue
        if(index==1352 or index==1353 or index==1354 or index==1699 or index==1730 or index==1883 ):
            continue
        '''
        

        b2b_ob=None
        min_b2b_dist=99999

        for i in range(balls_Pos.length):
            if(balls_Pos.ball_lists[i]==balls_Pos.white_ball()):
                continue
            if(detection.cue_point_to_ball(cue,balls_Pos.ball_lists[i],max_h_b2b)!=0):
                b2b_dist=math.sqrt((balls_Pos.ball_lists[i].x-balls_Pos.white_ball().x)*(balls_Pos.ball_lists[i].x-balls_Pos.white_ball().x)+(balls_Pos.ball_lists[i].y-balls_Pos.white_ball().y)*(balls_Pos.ball_lists[i].y-balls_Pos.white_ball().y))
                if(b2b_dist<min_b2b_dist):
                    min_b2b_dist=b2b_dist
                    b2b_ob=balls_Pos.ball_lists[i]

        

        if(b2b_ob!=None):
            d_ob_head=(b2b_ob.y-cue.head_cue_y)*(b2b_ob.y-cue.head_cue_y)+(b2b_ob.x-cue.head_cue_x)*(b2b_ob.x-cue.head_cue_x)
            d_wb_head=(balls_Pos.white_ball().y-cue.head_cue_y)*(balls_Pos.white_ball().y-cue.head_cue_y)+(balls_Pos.white_ball().x-cue.head_cue_x)*(balls_Pos.white_ball().x-cue.head_cue_x)
            if(d_ob_head<d_wb_head):
                print("ob front of wb")
                continue
            cv2.circle(img_show,(int(b2b_ob.x),int(b2b_ob.y)),int(b2b_ob.r),(200,200,200),6)
            #cv2.imshow("result",cv2.resize(img_now,(length,width)))
            #cv2.waitKey(1)

        print("cue.x=",cue.head_cue_x," cue.y=",cue.head_cue_y," cue.theta=",cue.cue_theta,"cue.theta_original=",cue.cue_theta_origin)
        '''
        print("index=",index)
        if(index==804):
            continue
        if(index==826):
            continue
        '''
        
        if(b2b_ob==None):
            cal_result=cal_draw.cal(bds,cue,balls_Pos,img_show)
            show_status=1
            #cal_draw.draw(cal_result.impactpoint,cal_result.ball,cal_result.bdpoint,1,img_show)
        else:
            b2b_result=ball_to_ball_cal.btb_cal(bds,cue,balls_Pos,b2b_ob,img_show)
            show_status=2
            #ball_to_ball_cal.draw(b2b_result.impoint,b2b_result.whiteball,b2b_result.bdpoint,1,img_show)

        





'''
date:2022 10 05
empty.jpg and 72.jpg are used for testing today
'''
def test_1005():
    img_blank=cv2.resize(cv2.imread("./imgs/empty.jpg"),(1920,1080))
    img_with_cue=cv2.resize(cv2.imread("./imgs/72.jpg"),(1920,1080))
    img_with_balls=cv2.resize(cv2.imread("./imgs/73.jpg"),(1920,1080))

    #边线检测
    bds=detection.boundary_detection_small(img_blank)

    #球检测
    
    Pos=detection.ball_detection(img_blank,img_with_balls)
    
    print(Pos.length)
    for i in range (Pos.length):
        #print(Pos.ball_lists[i].r)
        if(Pos.ball_lists[i].type!=0):
            cv2.circle(img_with_balls,(Pos.ball_lists[i].x,Pos.ball_lists[i].y),int(Pos.ball_lists[i].r),(2,30,200),6)
        else:
            cv2.circle(img_with_balls,(Pos.ball_lists[i].x,Pos.ball_lists[i].y),int(Pos.ball_lists[i].r),(200,30,200),6)
    cv2.imshow("test",cv2.resize(img_with_balls,(1280,720)))
    cv2.waitKey()
    
    
    
    #杆检测
    cue=detection.cue_detection(img_with_balls,img_with_cue,Pos.white_ball())
    
    cv2.circle(img_with_cue,(cue.head_cue_x,cue.head_cue_y),2,(2,30,200),6)
    cv2.imshow("with cue",img_with_cue)
    cv2.waitKey()
    

    

    cal_draw.cal(bds,cue,Pos,img_with_cue)

    #print(bds)





mainloop(int(sys.argv[1]),sys.argv[2])
#test_1005()