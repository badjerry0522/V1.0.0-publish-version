import bdb
from re import X
from tkinter import Y


class boundary:
    def __init__(self,x1,x2,x3,x4,y1,y2,y3,y4):
        """
        注意，坐标原点在左上角
        :param x1:左下角
        :param x2:左上角
        :param x3:右上角
        :param x4:右下角
        :param y1:
        :param y2:
        :param y3:
        :param y4:
        """
        
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.x4 = x4
        self.y4 = y4



class ball:
    def __init__(self,x_centre,y_centre,radius,type=-1):
        """

        :param x_centre: 球心坐标
        :param y_centre: 球心坐标
        :param radius: 半径
        :param type: 0：白球；1：小球；2：大球 ；3：黑球；-1：未知
        """
        self.x = x_centre
        self.y = y_centre
        self.r = radius
        self.type = type
        if(type != 0 and type != 1 and type != 2 and type != 3 and type != -1):
            print("warning:球的类型无法识别")
    def showpos(self):
        print(self.x,self.y)
        res = [self.x, self.y]
        return res
class balls_pos:
    def __init__(self,length,balls):
        """

        :param length: 球的数量
        :param balls: ball对象数组（存了length个ball）
        """
        self.length =length
        self.ball_lists = balls
    def white_ball(self):
        """

        :return: 白球
        """
        res=None
        for i in range(self.length):
            if self.ball_lists[i].type == 0:
                #print(i)
                #print(self.ball_lists[i].type)
                res = self.ball_lists[i]
                #print("白球的球心:",self.ball_lists[i].x,self.ball_lists[i].y)
        return res
class cue:
    def __init__(self,cue_x,cue_y,cue_theta,cue_theta_origin,tail_cue_x,tail_cue_y):
        """

        :param cue_x: 杆头坐标x
        :param cue_y: 杆头坐标y
        :param cue_theta: 球杆角度,顺时针
        """
        self.head_cue_x = cue_x
        self.head_cue_y = cue_y
        self.tail_cue_x = tail_cue_x
        self.tail_cue_y = tail_cue_y
        self.cue_theta = cue_theta
        self.cue_theta_origin=cue_theta_origin
class route:
    def __init__(self,x0,y0,x1,y1):
        """

        :param x0: 线段起始点x坐标
        :param y0: 线段起始点y坐标
        :param x1: 线段终止点x坐标
        :param y1: 线段终止点y坐标
        """
        self.x_start = x0
        self.y_start = y0
        self.x_end = x1
        self.y_end = y1
class routes:
    def __init__(self):
        self.l:list
        self.num=0

class line:
    def __init__(self,x,y,theta):
        self.x=x
        self.y=y
        self.theta=theta

class lines:
    def __init__(self):
        self.l:list
        self.num=0

class buffer:
    def __init__(self,img,length,width,cur_time,index,isOver):
        self.img=img
        self.lengt=length
        self.width=width
        self.cur_time=cur_time
        self.index=index
        self.isOver=isOver

class cal_result:
    def __init__(self,impactpoint,ball,bdpoint):
        self.impactpoint=impactpoint
        self.ball=ball
        self.bdpoint=bdpoint

class b2b_result:
    def __init__(self,impoint,whiteball,bdpoint):
        self.impoint=impoint
        self.whiteball=whiteball
        self.bdpoint=bdpoint