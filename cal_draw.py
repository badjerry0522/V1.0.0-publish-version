# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 11:05:49 2022

@author: ASUS
"""

import reflection as ref
import math
import numpy as np
import cv2 as cv 
import data_structures

'''
input:
'''

def draw(point_impact,ball,point_bd,count,img_show,index):
        #img = np.zeros((picture_size[0],picture_size[1],3),np.uint8)
        drawpoint0=[round(ball[0]),round(ball[1])]
        drawpoint1=[0,0]
        drawpoint2=[0,0]
        drawpoint3=[0,0]
        drawpoint=[drawpoint0,drawpoint1,drawpoint2,drawpoint3]
        
        
        #img=img_with_route.copy()
        #cv.namedWindow('image',cv.WND_PROP_FULLSCREEN)
        for i in range(1,4):
            drawpoint[i][0]=round(point_impact[i-1][0])
            drawpoint[i][1]=round(point_impact[i-1][1])
        for i in range(3):
            cv.line(img_show,(drawpoint[i][0],drawpoint[i][1]),(drawpoint[i+1][0],drawpoint[i+1][1]),(255,225,255),3,8,0)
            cv.line(img_show,(round(point_bd[i][0]),round(point_bd[i][1])),(round(point_bd[i+1][0]),round(point_bd[i+1][1])),(255,225,255),3,8,0)
        cv.line(img_show,(round(point_bd[3][0]),round(point_bd[3][1])),(round(point_bd[0][0]),round(point_bd[0][1])),(255,225,255),3,8,0)
        cv.imshow('result',img_show)
        cv.waitKey(1)
        file_path="./big_pool_result_e1/"+str(index)+".jpg"
        cv.imwrite(file_path,img_show)


        '''
        for index in range(124,140):
            file_name="./imgs/"+str(index)+".jpg"
            img=cv.imread(file_name)
            for i in range(1,4):
                drawpoint[i][0]=round(point_impact[i-1][0])
                drawpoint[i][1]=round(point_impact[i-1][1])
            for i in range(3):
                cv.line(img,(drawpoint[i][0],drawpoint[i][1]),(drawpoint[i+1][0],drawpoint[i+1][1]),(255,225,255),3,8,0)
                cv.line(img,(round(point_bd[i][0]),round(point_bd[i][1])),(round(point_bd[i+1][0]),round(point_bd[i+1][1])),(255,225,255),3,8,0)
            cv.line(img,(round(point_bd[3][0]),round(point_bd[3][1])),(round(point_bd[0][0]),round(point_bd[0][1])),(255,225,255),3,8,0)
            cv.imshow('image',img)
            cv.waitKey(0)
        
        
        count += 1
        save_path="test_result"
        cv.imwrite(save_path+'%d.jpg'%(count),img_with_route)
        '''


def cal(boundary,cue_in,balls,img_with_route):
    white_ball=balls.white_ball()
    if(white_ball is None):
        return None

    picturesize=[720,1280]

    print("boundary=",boundary)

    bd0=[boundary[0][0],boundary[0][1]]
    bd1=[boundary[3][0],boundary[3][1]]
    bd2=[boundary[1][0],boundary[1][1]]
    bd3=[boundary[2][0],boundary[2][1]]

    bd=[bd0,bd1,bd2,bd3]#边界
    print("bd=",bd)

    cue=[cue_in.head_cue_x,cue_in.head_cue_y,cue_in.cue_theta]#球杆

    print(cue_in.cue_theta)
    ball=[white_ball.x,white_ball.y,white_ball.r,white_ball.type] #球


    '''
    bd0=[50,math.pi*7/4]
    bd1=[250,math.pi/4]
    bd2=[50,math.pi*3/4]
    bd3=[50,math.pi/4]
    cue=[35.3,35.3,math.pi/2]
    bd=[bd0,bd1,bd2,bd3]#边界
    '''
    if cue[2]>math.pi:
        rcue=math.cos(cue[2]-math.pi)*cue[0]+math.sin(cue[2]-math.pi)*cue[1]
    else:
        rcue=math.cos(cue[2])*cue[0]+math.sin(cue[2])*cue[1]#第一次碰撞方程r

    imnumb0=0 #碰撞次数
    imnumb=[imnumb0]
    bdnumb0=0 #碰撞边界编号
    bdnumb1=0
    bdnumb2=0
    bdnumb=[bdnumb0,bdnumb1,bdnumb2]


    impoint0=[0,0]
    impoint1=[0,0]
    impoint2=[0,0]
    impoint3=[0,0]
    impoint=[impoint0,impoint1,impoint2,impoint3] #单次碰撞四条边数组

    bdpoint0=[0,0]
    bdpoint1=[0,0]
    bdpoint2=[0,0]
    bdpoint3=[0,0]
    bdpoint=[bdpoint0,bdpoint1,bdpoint2,bdpoint3]#球桌边界

    impactpoint0=[0,0]
    impactpoint1=[0,0]
    impactpoint2=[0,0]
    impactpoint=[impactpoint0,impactpoint1,impactpoint2]  #总共最多三次碰撞

    rrefline0=rcue
    rrefline1=0
    rrefline2=0
    rrefline=[rrefline0,rrefline1,rrefline2]#碰撞方程

    refline0=cue
    refline1=[0,0,0]
    refline2=[0,0,0]
    refline=[refline0,refline1,refline2]#碰撞轨迹参数同球杆



    






    ref.compute_bdpoint(bd,bdpoint)
    ref.compute_impoint(bd, rrefline, refline,impoint,imnumb)
    ref.compute_bdpoint(bd,bdpoint)
    ref.judge_point_im(bdpoint, impoint, impactpoint, bdnumb, imnumb, refline)
    ref.compute_ref_sita(bd, bdnumb, imnumb, refline)
    ref.compute_ref_line(impactpoint, bd, rrefline, refline, imnumb)


    ref.compute_impoint(bd, rrefline, refline,impoint,imnumb)
    ref.judge_point_im(bdpoint, impoint, impactpoint, bdnumb, imnumb, refline)
    ref.compute_ref_sita(bd, bdnumb, imnumb, refline)
    ref.compute_ref_line(impactpoint, bd, rrefline, refline, imnumb)


    ref.compute_impoint(bd, rrefline, refline,impoint,imnumb)
    ref.judge_point_im(bdpoint, impoint, impactpoint, bdnumb, imnumb, refline)


    cal_result=data_structures.cal_result(impactpoint,ball,bdpoint)
    
    #draw(impactpoint,ball,bdpoint,1,img_with_route)
    return cal_result
