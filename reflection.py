# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 08:14:34 2022

@author: ASUS


input:
    1.boundary:(r,sita)  r2,sita2
    2.cue:[x,y,sita]  r1,sita1
    3.ball(x,y,r,type)
output:
    1.impact_point[x,y]
    2.trail
"""

'''
变量参数bdline表示边界线，point点坐标，line表示轨迹，r_line表示轨迹
'''
'''
data1:斜着的桌子45
bd0=[5,math.pi*7/4]
bd1=[25,math.pi/4]
bd2=[5,math.pi*3/4]
bd3=[5,math.pi/4]
cue=[3.53,3.53,math.pi/2]


data2:正桌子
bd0=[0,math.pi/2]
bd1=[20,0]
bd2=[10,math.pi/2]
bd3=[0,math.pi]
cue=[0,5,math.pi*3/4]
'''
import math
import numpy as np
import cv2 as cv 

def compute_bdpoint(bdline,point):  #计算边界交点
    for i in range(4):
        if math.sin(bdline[i][1])==0:
            bdline[i][1]=(i+1)*1e-5
            
    for i in range(4):
        a=math.sin(bdline[i][1])/math.sin(bdline[(i+1)%4][1])
        x=(bdline[i][0]-a*bdline[(i+1)%4][0])/(math.cos(bdline[i][1])-a*math.cos(bdline[(i+1)%4][1]))
        y=(bdline[i][0]-math.cos(bdline[i][1])*x)/math.sin(bdline[i][1])
        point[i]=[x,y]
    print('111111',point)


def compute_impoint(bdline,r_line,line,point,numb_im):    #计算碰撞交点(边界，轨迹方程r，轨迹参数)
    for i in range(4):
        if bdline[i][1]==0:
            y=(r_line[numb_im[0]]-math.cos(line[numb_im[0]][2])*bdline[i][0])/math.sin(line[numb_im[0]][2])
            x=bdline[i][0]
            point[i]=[x,y]
        else:
            if line[numb_im[0]][2]>math.pi:
                p=line[numb_im[0]][2]-math.pi
            else:
                p=line[numb_im[0]][2]
            if p==0:
                p=p+0.00002
            a=math.sin(p)/math.sin(bdline[i][1])
            x=(r_line[numb_im[0]]-a*bdline[i][0])/(math.cos(p)-a*math.cos(bdline[i][1]))
            y=(r_line[numb_im[0]]-math.cos(p)*x)/math.sin(p)
            point[i]=[x,y]
    
    
    
def judge_point_im(point_bd,point_im,point_impact,numb_bd,numb_im,line):   #判断碰撞交点
    for i in range(2):
        if line[numb_im[0]][2]>=(math.pi/2*i) and line[numb_im[0]][2]<(math.pi/2*(i+1)):
            point_im[(i+2)%4]=point_im[(i+3)%4]=0
            if (point_im[i][0]<=point_bd[i][0] and point_im[i][0]>=point_bd[(i+3)%4][0] and point_im[i][1]<=point_bd[i][1] and point_im[i][1]>=point_bd[(i+3)%4][1])or(point_im[i][0]>=point_bd[i][0] and point_im[i][0]<=point_bd[(i+3)%4][0] and point_im[i][1]<=point_bd[i][1] and point_im[i][1]>=point_bd[(i+3)%4][1])or(point_im[i][0]>=point_bd[i][0] and point_im[i][0]<=point_bd[(i+3)%4][0] and point_im[i][1]>=point_bd[i][1] and point_im[i][1]<=point_bd[(i+3)%4][1])or(point_im[i][0]<=point_bd[i][0] and point_im[i][0]>=point_bd[(i+3)%4][0] and point_im[i][1]>=point_bd[i][1] and point_im[i][1]<=point_bd[(i+3)%4][1]):
                point_im[i+1]=0
                #print('AAAAAAAAAAAA')
            else:
                point_im[i]=0
                #print('bbbbbbbbbb')
    for i in range(2,4):
        if line[numb_im[0]][2]>=(math.pi/2*i) and line[numb_im[0]][2]<(math.pi/2*(i+1)):
            point_im[(i+2)%4]=point_im[(i+3)%4]=0
            if (point_im[i][0]<=point_bd[i][0] and point_im[i][0]>=point_bd[(i+3)%4][0] and point_im[i][1]<=point_bd[i][1] and point_im[i][1]>=point_bd[(i+3)%4][1])or(point_im[i][0]>=point_bd[i][0] and point_im[i][0]<=point_bd[(i+3)%4][0] and point_im[i][1]<=point_bd[i][1] and point_im[i][1]>=point_bd[(i+3)%4][1])or(point_im[i][0]>=point_bd[i][0] and point_im[i][0]<=point_bd[(i+3)%4][0] and point_im[i][1]>=point_bd[i][1] and point_im[i][1]<=point_bd[(i+3)%4][1])or(point_im[i][0]<=point_bd[i][0] and point_im[i][0]>=point_bd[(i+3)%4][0] and point_im[i][1]>=point_bd[i][1] and point_im[i][1]<=point_bd[(i+3)%4][1]):
                point_im[(i+1)%4]=0
            else:
                point_im[i]=0
    for i in range(4):
       if point_im[i] !=0:
           point_impact[numb_im[0]]=point_im[i]
           numb_bd[numb_im[0]]=i
    numb_im[0]=numb_im[0]+1
    
    
    

    
 #sita1是桌子角度,sita2是球运动角度   
def compute_ref_sita(bdline,numb_bd,numb_im,line):
    sita=bdline[numb_bd[numb_im[0]-1]][1]*2-line[numb_im[0]-1][2]
   
    if sita<0:
        sita=2*math.pi+sita
    line[numb_im[0]][2]=sita
    print('sita',sita)
def compute_ref_line(point_impact,bdline,r_line,line,numb_im):
    if line[numb_im[0]][2]>=math.pi:
        sita=line[numb_im[0]][2]-math.pi
    else:
        sita=line[numb_im[0]][2]
    r_line[numb_im[0]]=math.cos(sita)*point_impact[numb_im[0]-1][0]+math.sin(sita)*point_impact[numb_im[0]-1][1]
    line[numb_im[0]]=[point_impact[numb_im[0]-1][0],point_impact[numb_im[0]-1][1],line[numb_im[0]][2]]    
    
'''
picturesize=[100,200]


bd0=[0,math.pi/2]
bd1=[200,0]
bd2=[100,math.pi/2]
bd3=[0,math.pi]
bd=[bd0,bd1,bd2,bd3]#边界
cue=[10,60,math.pi*3/4]#球杆
ball=[20,70,2,1] #球


bd0=[50,math.pi*7/4]
bd1=[250,math.pi/4]
bd2=[50,math.pi*3/4]
bd3=[50,math.pi/4]
cue=[35.3,35.3,math.pi/2]
bd=[bd0,bd1,bd2,bd3]#边界
'''
'''
bd0=[95,1.6]
bd1=[551,0.034]
bd2=[335,1.6]
bd3=[41,0.034]
bd=[bd0,bd1,bd2,bd3]#边界
cue=[146,270,1.86]#球杆
ball=[146,270,2,1] #球

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
    

compute_bdpoint(bd,bdpoint)
compute_impoint(bd, rrefline, refline,impoint,imnumb)
compute_bdpoint(bd,bdpoint)
judge_point_im(bdpoint, impoint, impactpoint, bdnumb, imnumb, refline)
compute_ref_sita(bd, bdnumb, imnumb, refline)
compute_ref_line(impactpoint, bd, rrefline, refline, imnumb)

print("第",imnumb[0],"次碰撞的碰撞点：",impactpoint[imnumb[0]-1])
print("碰撞的桌边编号为：",bdnumb[0])


compute_impoint(bd, rrefline, refline,impoint,imnumb)
judge_point_im(bdpoint, impoint, impactpoint, bdnumb, imnumb, refline)
compute_ref_sita(bd, bdnumb, imnumb, refline)
compute_ref_line(impactpoint, bd, rrefline, refline, imnumb)

print("第",imnumb[0],"次碰撞的碰撞点：",impactpoint[imnumb[0]-1])
print("碰撞的桌边编号为：",bdnumb[1])
print("反射线参数",refline)

compute_impoint(bd, rrefline, refline,impoint,imnumb)
judge_point_im(bdpoint, impoint, impactpoint, bdnumb, imnumb, refline)
print("第",imnumb[0],"次碰撞的碰撞点：",impactpoint[imnumb[0]-1])
print("碰撞的桌边编号为：",bdnumb[2])

def draw(picture_size,point_impact,ball,point_bd,count):
    img = np.zeros((picture_size[0],picture_size[1],3),np.uint8)
    drawpoint0=[round(ball[0]),round(ball[1])]
    drawpoint1=[0,0]
    drawpoint2=[0,0]
    drawpoint3=[0,0]
    drawpoint=[drawpoint0,drawpoint1,drawpoint2,drawpoint3]
    for i in range(4):
        point_bd[i]=[round(point_bd[i][0]),round(point_bd[i][1])]
    for i in range(1,4):
        drawpoint[i][0]=round(point_impact[i-1][0])
        drawpoint[i][1]=round(point_impact[i-1][1])
    for i in range(3):
        cv.line(img,drawpoint[i],drawpoint[i+1],(255,225,255),3,8,0)
    for i in range(4):
        cv.line(img,point_bd[i],point_bd[(i+1)%4],(255,225,255),3,8,0)
    cv.imshow('image',img)
    cv.waitKey(0)

picturesize=[480,640]
draw(picturesize,impactpoint,ball,bdpoint,1)
'''