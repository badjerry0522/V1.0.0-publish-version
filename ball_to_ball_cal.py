# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 00:50:16 2022

@author: ASUS
"""
import numpy as np
import cv2 as cv 
import reflection as ref
import math
import data_structures
'''
picturesize=[480,640]

sita0=0
sita1=0
sita=[sita0,sita1]

impoint0=[0,0]  #原小球碰撞位置
impoint1=[0,0]  #被碰小球位置
impoint2=[0,0]  #原小球与边界交点
impoint3=[0,0]  #被碰撞球与边界交点
impoint=[impoint0,impoint1,impoint2,impoint3] #单次碰撞四条边数组




#otherball=[25,80,5,0]#普通球z
otherball=[254,234,6,0]#普通球
whiteball=[218,208,6,1] #白球
cue=[218,208,2.08994]#球杆
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

rcue=math.cos(cue[2])*cue[0]+math.sin(cue[2])*cue[1]
d=(math.cos(cue[2])*otherball[0]+math.sin(cue[2])*otherball[1]-rcue)


otherball=[186,206,6,0]#普通球
whiteball=[146,192,6,1] #白球
cue=[146,192,1.78145]#球杆
rcue=math.cos(cue[2])*cue[0]+math.sin(cue[2])*cue[1]
d=(math.cos(cue[2])*otherball[0]+math.sin(cue[2])*otherball[1]-rcue)



impoint[0]=[otherball[0],otherball[1]]

bd0=[0,math.pi/2]
bd1=[640,0]
bd2=[480,math.pi/2]
bd3=[0,math.pi]
bd=[bd0,bd1,bd2,bd3]#边界


impactpoint0=[0,0]
impactpoint1=[0,0]
impactpoint2=[0,0]
impactpoint3=[0,0]
impactpoint=[impactpoint0,impactpoint1,impactpoint2,impactpoint3]

bdpoint0=[0,0]
bdpoint1=[0,0]
bdpoint2=[0,0]
bdpoint3=[0,0]
bdpoint=[bdpoint0,bdpoint1,bdpoint2,bdpoint3]#球桌边界
'''


def compute_crosspoint(cue,ball,ball2,d,point_im,r_cue):
    '''
    r_d=math.cos(cue[2]+math.pi/2)*ball[0]+math.sin(cue[2]+math.pi/2)*ball[1]
    a=math.cos(cue[2]+math.pi/2)/math.cos(cue[2])
    y=(r_d-a*r_cue)/(math.sin(cue[2]+math.pi/2)-a*math.sin(cue[2]))
    x=(r_d-math.sin(cue[2]+math.pi/2)*y)/math.cos(cue[2]+math.pi/2)
    p=math.sqrt(4*ball[2]*ball[2]-d*d)
    y=y+math.cos(cue[2])*p
    x=x-math.sin(cue[2])*p
    point_im[1]=[x,y]
    print(point_im[1])
    '''
    if cue[2]>=math.pi:
        p=cue[2]-math.pi
    else:
        p=cue[2]
    r_d=math.cos(p+math.pi/2)*ball[0]+math.sin(p+math.pi/2)*ball[1]
    a=math.cos(p+math.pi/2)/math.cos(p)
    y=(r_d-a*r_cue)/(math.sin(p+math.pi/2)-a*math.sin(p))
    x=(r_d-math.sin(p+math.pi/2)*y)/math.cos(p+math.pi/2)
    v=math.sqrt(4*ball[2]*ball[2]-d*d)
    if ball2[0]<x and ball2[1]<y:
        y=y-abs(math.cos(p)*v)
        x=x-abs(math.sin(p)*v)
    if ball2[0]>x and ball2[1]<y:
        y=y-abs(math.cos(p)*v)
        x=x+abs(math.sin(p)*v)
    
    if ball2[0]<x and ball2[1]>y:
        y=y+abs(math.cos(p)*v)
        x=x-abs(math.sin(p)*v)
        
    if ball2[0]>x and ball2[1]>y:
        y=y+abs(math.cos(p)*v)
        x=x+abs(math.sin(p)*v)
    point_im[1]=[x,y]
    print(point_im[1])



def compute_sita1(d,ball,e,sita):
    print(((1-e)*4*math.pow(ball[2], 2)+(1+e)*math.pow(d, 2)))
    sita[1]=math.atan((1+e)*d*math.sqrt(4*math.pow(ball[2], 2)-math.pow(d, 2))/((1-e)*4*math.pow(ball[2], 2)+(1+e)*math.pow(d, 2)))
    print(sita[1])


def compute_sita2(d,ball,sita):
    sita[0]=math.asin(d/(2*ball[2]))
    

def compute_impoint(cue,ball,ball_white,d,point_im,sita,bdline,point,point_bd):
    if cue[2]>=math.pi:
        theta0=cue[2]-sita[0] #撞的小球
        print('::::::::',cue[2])
        theta1=cue[2]+sita[1] #原小球
        g=theta0-math.pi
    else:
        theta0=cue[2]+sita[0] #撞的小球
        print('::::::::',cue[2])
        theta1=cue[2]-sita[1] #原小球
        g=theta0
        
        
        
    if theta0>=2*math.pi:
        theta0=theta0-2*math.pi    
    if theta1>=2*math.pi:
        theta1=theta1-2*math.pi 
    if theta0>=math.pi:
        r_0=math.cos(theta0-math.pi)*point_im[0][0]+math.sin(theta0-math.pi)*point_im[0][1]
    else:
        r_0=math.cos(theta0)*point_im[0][0]+math.sin(theta0)*point_im[0][1]
    if theta1>=math.pi:
        r_1=math.cos(theta1-math.pi)*point_im[1][0]+math.sin(theta1-math.pi)*point_im[1][1]
    else:
        r_1=math.cos(theta1)*point_im[1][0]+math.sin(theta1)*point_im[1][1]
    
    for i in range(4):
        if theta0>=math.pi:
            p0=theta0-math.pi
        else:
            p0=theta0
        a=math.sin(p0)/math.sin(bdline[i][1])
        x=(r_0-a*bdline[i][0])/(math.cos(p0)-a*math.cos(bdline[i][1]))
        y=(r_0-math.cos(p0)*x)/math.sin(p0)
        point[i]=[x,y]
    print('pengzhuangkeneng',point)
    print('_______________________________')
    print('theta0',theta0,theta1)
    for i in range(2):
        if theta0>=(math.pi/2*i) and theta0<(math.pi/2*(i+1)):
            point[(i+2)%4]=point[(i+3)%4]=0
            if (point[i][0]<=point_bd[i][0] and point[i][0]>=point_bd[(i+3)%4][0] and point[i][1]<=point_bd[i][1] and point[i][1]>=point_bd[(i+3)%4][1])or(point[i][0]>=point_bd[i][0] and point[i][0]<=point_bd[(i+3)%4][0] and point[i][1]<=point_bd[i][1] and point[i][1]>=point_bd[(i+3)%4][1])or(point[i][0]>=point_bd[i][0] and point[i][0]<=point_bd[(i+3)%4][0] and point[i][1]>=point_bd[i][1] and point[i][1]<=point_bd[(i+3)%4][1])or(point[i][0]<=point_bd[i][0] and point[i][0]>=point_bd[(i+3)%4][0] and point[i][1]>=point_bd[i][1] and point[i][1]<=point_bd[(i+3)%4][1]):
                point[i+1]=0
            else:
                point[i]=0
    for i in range(2,4):
        if theta0>=(math.pi/2*i) and theta0<(math.pi/2*(i+1)):
            point[(i+2)%4]=point[(i+3)%4]=0
            if (point[i][0]<=point_bd[i][0] and point[i][0]>=point_bd[(i+3)%4][0] and point[i][1]<=point_bd[i][1] and point[i][1]>=point_bd[(i+3)%4][1])or(point[i][0]>=point_bd[i][0] and point[i][0]<=point_bd[(i+3)%4][0] and point[i][1]<=point_bd[i][1] and point[i][1]>=point_bd[(i+3)%4][1])or(point[i][0]>=point_bd[i][0] and point[i][0]<=point_bd[(i+3)%4][0] and point[i][1]>=point_bd[i][1] and point[i][1]<=point_bd[(i+3)%4][1])or(point[i][0]<=point_bd[i][0] and point[i][0]>=point_bd[(i+3)%4][0] and point[i][1]>=point_bd[i][1] and point[i][1]<=point_bd[(i+3)%4][1]):
                point[(i+1)%4]=0
            else:
                point[i]=0
    for i in range(4):
       if point[i] !=0:
           point_im[2]=point[i]
    print('pengzhuang 1',point_im[2])
           
    for i in range(4):
        if theta1>=math.pi:
            p1=theta1-math.pi
        else:
            p1=theta1
        a=math.sin(p1)/math.sin(bdline[i][1])
        x=(r_1-a*bdline[i][0])/(math.cos(p1)-a*math.cos(bdline[i][1]))
        y=(r_1-math.cos(p1)*x)/math.sin(p1)
        point[i]=[x,y]
    print('pengzhuangkeneng2222',point)
    print('_______________________________')
    for i in range(2):
        if theta1>=(math.pi/2*i) and theta1<(math.pi/2*(i+1)):
            point[(i+2)%4]=point[(i+3)%4]=0
            if (point[i][0]<=point_bd[i][0] and point[i][0]>=point_bd[(i+3)%4][0] and point[i][1]<=point_bd[i][1] and point[i][1]>=point_bd[(i+3)%4][1])or(point[i][0]>=point_bd[i][0] and point[i][0]<=point_bd[(i+3)%4][0] and point[i][1]<=point_bd[i][1] and point[i][1]>=point_bd[(i+3)%4][1])or(point[i][0]>=point_bd[i][0] and point[i][0]<=point_bd[(i+3)%4][0] and point[i][1]>=point_bd[i][1] and point[i][1]<=point_bd[(i+3)%4][1])or(point[i][0]<=point_bd[i][0] and point[i][0]>=point_bd[(i+3)%4][0] and point[i][1]>=point_bd[i][1] and point[i][1]<=point_bd[(i+3)%4][1]):
                point[i+1]=0
            else:
                point[i]=0
    for i in range(2,4):
        if theta1>=(math.pi/2*i) and theta1<(math.pi/2*(i+1)):
            point[(i+2)%4]=point[(i+3)%4]=0
            if (point[i][0]<=point_bd[i][0] and point[i][0]>=point_bd[(i+3)%4][0] and point[i][1]<=point_bd[i][1] and point[i][1]>=point_bd[(i+3)%4][1])or(point[i][0]>=point_bd[i][0] and point[i][0]<=point_bd[(i+3)%4][0] and point[i][1]<=point_bd[i][1] and point[i][1]>=point_bd[(i+3)%4][1])or(point[i][0]>=point_bd[i][0] and point[i][0]<=point_bd[(i+3)%4][0] and point[i][1]>=point_bd[i][1] and point[i][1]<=point_bd[(i+3)%4][1])or(point[i][0]<=point_bd[i][0] and point[i][0]>=point_bd[(i+3)%4][0] and point[i][1]>=point_bd[i][1] and point[i][1]<=point_bd[(i+3)%4][1]):
                point[(i+1)%4]=0
            else:
                point[i]=0
    for i in range(4):
       if point[i] !=0:
           point_im[3]=point[i]
    print('pengzhuang 2',point_im[3])

def draw(point_im,ball,point_bd,count,img_show,index):
    #img = np.zeros((picture_size[0],picture_size[1],3),np.uint8)
    #img=img_but
    drawpoint0=[0,0]
    drawpoint1=[0,0]
    drawpoint2=[0,0]
    drawpoint3=[0,0]
    drawpoint4=[ball[0],ball[1]]
    drawpoint=[drawpoint0,drawpoint1,drawpoint2,drawpoint3,drawpoint4]    
    for i in range(4):
        drawpoint[i][0]=round(point_im[i][0])
        drawpoint[i][1]=round(point_im[i][1])
    cv.line(img_show,(drawpoint[0][0],drawpoint[0][1]),(drawpoint[2][0],drawpoint[2][1]),(255,225,255),3,8,0)
    cv.line(img_show,(drawpoint[1][0],drawpoint[1][1]),(drawpoint[3][0],drawpoint[3][1]),(255,225,255),3,8,0)
    cv.line(img_show,(drawpoint[4][0],drawpoint[4][1]),(drawpoint[1][0],drawpoint[1][1]),(255,225,255),3,8,0)
    cv.imshow('result',img_show)
    cv.waitKey(1)

    file_path="./big_pool_result_e1/"+str(index)+".jpg"
    cv.imwrite(file_path,img_show)
    '''
    count += 1
    save_path='D:/work/picture_out/'
    cv.imwrite(save_path+'%d.jpg'%(count),img)
    cv.waitKey(0)
    cv.destroyAllWindows()
    '''

    

def btb_cal(boundary,cue_in,balls,b2b,img_but):  #叠加图层的名字
    white_ball=balls.white_ball()
    
    other_ball=b2b
    
    
    if(white_ball is None):
        return None

    picturesize=[720,1280]


    bd0=[boundary[0][0],boundary[0][1]]
    bd1=[boundary[3][0],boundary[3][1]]
    bd2=[boundary[1][0],boundary[1][1]]
    bd3=[boundary[2][0],boundary[2][1]]

    bd=[bd0,bd1,bd2,bd3]#边界


    cue=[cue_in.head_cue_x,cue_in.head_cue_y,cue_in.cue_theta]#球杆
    whiteball=[white_ball.x,white_ball.y,white_ball.r,white_ball.type] #白球
    otherball=[other_ball.x,other_ball.y,other_ball.r,other_ball.type] #被碰球
    
    
    
    
    '''
    机器学习训练的参数
    '''
    e=1
    #e=0.7485456192846609472
    
    
    
    sita0=0
    sita1=0
    sita=[sita0,sita1]

    impoint0=[0,0]  #原小球碰撞位置
    impoint1=[0,0]  #被碰小球位置
    impoint2=[0,0]  #原小球与边界交点
    impoint3=[0,0]  #被碰撞球与边界交点
    impoint=[impoint0,impoint1,impoint2,impoint3] #单次碰撞四条边数组



    #cue=(826,154,2.5841)
    #whiteball=(826,154,white_ball.r,white_ball.type)
    #otherball=(994.5,380.5,other_ball.r,other_ball.type)
    #otherball=[25,80,5,0]#普通球z
    #otherball=[254,234,6,0]#普通球
    #whiteball=[218,208,6,1] #白球
    #cue=[218,208,2.08994]#球杆
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
    if cue[2]>math.pi:
        rcue=math.cos(cue[2]-math.pi)*cue[0]+math.sin(cue[2]-math.pi)*cue[1]
    else:
        rcue=math.cos(cue[2])*cue[0]+math.sin(cue[2])*cue[1]#第一次碰撞方程r
    if cue[2]>math.pi:
        d=(math.cos(cue[2]-math.pi)*otherball[0]+math.sin(cue[2]-math.pi)*otherball[1]-rcue)
    else:
        d=(math.cos(cue[2])*otherball[0]+math.sin(cue[2])*otherball[1]-rcue)
    
    

    impoint[0]=[otherball[0],otherball[1]]


    impactpoint0=[0,0]
    impactpoint1=[0,0]
    impactpoint2=[0,0]
    impactpoint3=[0,0]
    impactpoint=[impactpoint0,impactpoint1,impactpoint2,impactpoint3]

    bdpoint0=[0,0]
    bdpoint1=[0,0]
    bdpoint2=[0,0]
    bdpoint3=[0,0]
    bdpoint=[bdpoint0,bdpoint1,bdpoint2,bdpoint3]#球桌边界
    
    if d>=whiteball[2]:
        return
    else:
        compute_sita1(d, otherball, e,sita)
        compute_sita2(d, otherball,sita)
        compute_crosspoint(cue, otherball,whiteball, d, impoint, rcue)
        ref.compute_bdpoint(bd,bdpoint)
        compute_impoint(cue,otherball,whiteball,d,impoint,sita,bd,impactpoint,bdpoint)
        b2b_result=data_structures.b2b_result(impoint,whiteball,bdpoint)
        
        #draw(impoint,whiteball, bdpoint, 1,img_but)
        return b2b_result


'''
print(sita)
print(impoint)
'''
'''
for i in range(45):
    
    p=i+1670
    #p=i+899
    a=str(p)
    file_name='F:/d/imgs_all/use/imgs/'+a+'.jpg'
    #file_name='F:/d/imgs_all/use/imgs/'+a+'.jpg'
    draw(picturesize, impoint,whiteball, bdpoint, 1,file_name)
    if(i==44):
        cv.waitKey(0)
        cv.destroyAllWindows()

'''