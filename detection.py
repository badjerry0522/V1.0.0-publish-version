# -- coding: utf-8
from calendar import c
import cv2
import math
import numpy as np
import data_structures
import myfunc
def sort_(list0):
    """
    根据y值对circle冒泡排序
    :param list0: 针对circle
    :return: 排序好的结果
    """
    list = list0[0].copy()
    #print(list[0][1])
    for i in range(len(list)):
        for j in range(0, len(list) - i - 1):
            if list[j][1] > list[j + 1][1]:
                temp = list[j].copy()
                list[j] = list[j + 1].copy()
                list[j + 1] = temp.copy()
    #print(list)
    return list
def ball_detection(img_blank, img_with_balls,length,width):
    """
    还不能识别球的类型
    :param img_blank: 设备开机时，自动拍摄的空白球桌（实际上不需要）
    :param img_with_balls: 运动检测模块识别所有球静止后，拍摄的照片
    :return:balls
    """
    img_ =img_blank
    img = img_with_balls
    #cv2.imshow("img",img)
    #cv2.waitKey()
    #output = img   

    img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 1.对img进行灰度化
    ret, img_b = cv2.threshold(img_g, 75, 255, cv2.THRESH_BINARY)
    # 2.对img进行二值化
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    circles = cv2.HoughCircles(img_g,
                               cv2.HOUGH_GRADIENT,
                               1,
                               17,  # 最小圆间距
                               param1=100,
                               param2=10,     # 严格程度   
                               minRadius=13,  # 最小圆半径
                               maxRadius=15)  # 最大圆半径
    # print(circles)
    if(circles is None):
        print("len of circle is 0")
        return None
    circles_ = sort_(circles)                 #根据y值进行冒泡排序
    balls_len = len(circles_)
    print("balls_len=",balls_len)
    #print(circles)
    balls = [data_structures.ball(circles_[i][0], circles_[i][1], circles_[i][2]) for i in range(balls_len)]

    for i in range(len(circles[0])):
        # 判断类型
        x = circles_[i][0]
        y = circles_[i][1]
        r = circles_[i][2]
        delta = 3 / 4 * r

        if(abs(y-width)<20 or abs(x-length)<20):
            continue
        
        bgr=img[round(y),round(x)]
        if(bgr[0]>190 and bgr[1]>190 and bgr[2]>190):
            balls[i].type=0
        else:
            balls[i].type=1

        '''
        if(abs(y-width)<20 or abs(x-length)<20):
            continue

        bgr = np.zeros((8, 3))
        bgr[0] = img[round(y - delta), round(x)]  # 上
        bgr[1] = img[round(y - delta / 2), round(x + delta / 2)]  # 右上
        bgr[2] = img[round(y + delta), round(x)]  # 下
        bgr[3] = img[round(y + delta / 2), round(x + delta / 2)]  # 右下
        bgr[4] = img[round(y), round(x - delta)]  # 左
        bgr[5] = img[round(y + delta / 2), round(x - delta / 2)]  # 左下
        bgr[6] = img[round(y), round(x + delta)]  # 右
        bgr[7] = img[round(y - delta / 2), round(x - delta / 2)]  # 左上

        hsv = np.zeros((8, 3))
        hsv[0] = img_hsv[round(y - delta), round(x)]  # 上
        hsv[1] = img_hsv[round(y - delta / 2), round(x + delta / 2)]  # 右上
        hsv[2] = img_hsv[round(y + delta), round(x)]  # 下
        hsv[3] = img_hsv[round(y + delta / 2), round(x + delta / 2)]  # 右下
        hsv[4] = img_hsv[round(y), round(x - delta)]  # 左
        hsv[5] = img_hsv[round(y + delta / 2), round(x - delta / 2)]  # 左下
        hsv[6] = img_hsv[round(y), round(x + delta)]  # 右
        hsv[7] = img_hsv[round(y - delta / 2), round(x - delta / 2)]  # 左上
        n = 0  # 黑色或白色
        for j in range(8):
            if hsv[j][1] < 30:  # 具体参数等实物到了，再调整
                n += 1
        if n > 6:
            if (bgr[0][1] > 30 and bgr[2][1] > 30 and bgr[4][1] > 30 and bgr[6][1] > 30):
                # 白球
                balls[i].type = 0
                #print(balls[i].x,balls[i].y,"123")
            else:
                # 黑8
                balls[i].type = 3
        else:
            if n > 3:
                # 大球，花色球
                balls[i].type = 2
            else:
                # 小球，纯色球
                balls[i].type = 1
        '''
    res = data_structures.balls_pos(balls_len,balls)
    return res

def cue_detection_2(img_, white_ball_):
    """

    :param img_:
    :param white_ball:
    :return: cue 类
    """
    # 只关心white_ball的中心坐标
    white_ball = [white_ball_.x, white_ball_.y]
    if (img_ is None):
        print("img_with_cue=None")
        return None
    if (white_ball is None):
        print("white_ball==None")
        return None

    img = img_.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gaus = cv2.GaussianBlur(gray, (3, 3), 0)

    edges = cv2.Canny(gaus, 50, 150, apertureSize=3)

    minLineLength = 100
    maxLineGap = 10
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength, maxLineGap)
    # 找球杆轮廓
    line_cue_0, line_cue_1, return_flag = myfunc.find_best_line(lines, white_ball)
    if(return_flag==1):
        print("未指向球或未包含球杆边缘，返回空")
        return None
    # 绘制球杆轮廓
    cv2.line(img, (int(line_cue_0[0]), int(line_cue_0[1])), (int(line_cue_0[2]), int(line_cue_0[3])), (0, 0, 0), 2)
    cv2.line(img, (int(line_cue_1[0]), int(line_cue_1[1])), (int(line_cue_1[2]), int(line_cue_1[3])), (0, 0, 0), 2)

    # 线性拟合
    x = [line_cue_0[0], line_cue_0[2], line_cue_1[0], line_cue_1[2]]
    y = [line_cue_0[1], line_cue_0[3], line_cue_1[1], line_cue_1[3]]
    #parameter后续可能没用上
    parameter = np.polyfit(x, y, 1)
    # 比较距离，确保line_cue_0[0]和[1]离白球更近
    distance0 = (line_cue_0[0] - white_ball[0]) ** 2 + (line_cue_0[1] - white_ball[1]) ** 2
    distance1 = (line_cue_0[2] - white_ball[0]) ** 2 + (line_cue_0[3] - white_ball[1]) ** 2
    distance2 = (line_cue_1[0] - white_ball[0]) ** 2 + (line_cue_1[1] - white_ball[1]) ** 2
    distance3 = (line_cue_1[2] - white_ball[0]) ** 2 + (line_cue_1[3] - white_ball[1]) ** 2
    if distance0 > distance1:
        x = line_cue_0[0]
        y = line_cue_0[1]
        line_cue_0[0] = line_cue_0[2]
        line_cue_0[1] = line_cue_0[3]
        line_cue_0[2] = x
        line_cue_0[3] = y
    if distance2 > distance3:
        x = line_cue_1[0]
        y = line_cue_1[1]
        line_cue_1[0] = line_cue_1[2]
        line_cue_1[1] = line_cue_1[3]
        line_cue_1[2] = x
        line_cue_1[3] = y
    # 球杆头


    # 判断能否用两条轮廓的头的中点作为球杆头的中点
    distance = ((line_cue_0[0] - line_cue_1[0]) ** 2 + (line_cue_0[1] - line_cue_1[1]) ** 2) ** 0.5
    if distance < 16:
        print("采用两条轮廓判断球杆头")
        head_x = (line_cue_0[0] + line_cue_1[0]) / 2
        head_y = (line_cue_0[1] + line_cue_1[1]) / 2
    else:
        return None
        print("采用一条轮廓判断球杆头")
        head_x = line_cue_0[0]
        head_y = line_cue_0[1]
    tail_x = head_x * 2 - white_ball[0]
    tail_y = head_y * 2 - white_ball[1]

    #创建球杆对象
    if (head_x != tail_x):
        theta_0 = math.atan(abs((head_y - tail_y) / (head_x - tail_x)))
        if (head_y > tail_y):
            if (head_x > tail_x):
                theta = theta_0 + math.pi / 2
            else:
                theta = -theta_0 + math.pi * 1.5
        else:
            if (head_x > tail_x):
                theta = -theta_0 + math.pi / 2
            else:
                theta = theta_0 + 1.5 * math.pi
        theta_0 = abs(theta_0)
    else:
        if (head_y > tail_y):
            theta = math.pi
            theta_0 = theta
        else:
            theta = 0
            theta_0 = theta
        #

        # print(theta)
    res = data_structures.cue(head_x, head_y, theta, theta_0, tail_x, tail_y)
    #cv2.circle(img, (round(head_x), round(head_y)), 4, (255, 0, 0), 2)

    #cv2.imshow("1", img)
    #cv2.waitKey(0)
    return res

def cue_detection(img_with_balls, img_with_cue, white_ball):
    """
    还不能识别球杆头
    :param img_with_balls:运动检测模块识别所有球静止后，拍摄的照片
    :param img_with_cue:有球杆时的照片
    :return: cue类的实例
    """

    
    if(img_with_balls is None):
        print("img_with_balls=None")
        return None
    if(img_with_cue is None):
        print("img_with_cue=None")
        return None
    if(white_ball is None):
        print("white_ball==None")
        return None
    


    cue1 = img_with_balls
    cue2 = img_with_cue
    img = cv2.absdiff(cue1, cue2)

    #cv2.imshow("abs",img)
    #cv2.waitKey()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gaus = cv2.GaussianBlur(gray, (3, 3), 0)

    edges = cv2.Canny(gaus, 50, 150, apertureSize=3)

    minLineLength = 50
    maxLineGap = 10
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength, maxLineGap)
    if(lines is None):
        print("no cue detected\n")
        return None
    
    print(lines)


    
    min_d=99999999999

    head_x=0
    head_y=0
    tail_x=0
    tail_y=0
    for content in lines:
        distance1 = (white_ball.x - content[0][0]) ** 2 + (white_ball.y -  content[0][1]) ** 2
        distance2 = (white_ball.x -  content[0][2]) ** 2 + (white_ball.y -  content[0][3]) ** 2
        index_head=0
        index_tail=2
        if(distance1 < distance2):
            min_dis_1_2=distance1
            index_head=0
            index_tail=2
        else:
            min_dis_1_2=distance2
            index_head=2
            index_tail=0
        if(min_dis_1_2<min_d):
            min_d=min_dis_1_2
            head_x=content[0][index_head]
            head_y=content[0][index_head+1]
            tail_x=content[0][index_tail]
            tail_y=content[0][index_tail+1]

    theta=0
    theta_original=0

    print(math.atan((head_y - tail_y) / (head_x - tail_x)))


#
    if(head_x!=tail_x):
        theta_0=math.atan(abs((head_y - tail_y) / (head_x - tail_x)))
        if(head_y>tail_y):
            if(head_x>tail_x):
                theta=theta_0+math.pi/2
            else:
                theta=-theta_0+math.pi*1.5
        else: 
            if(head_x>tail_x):
                theta=-theta_0+math.pi/2
            else:
                theta=theta_0+1.5*math.pi
        theta_0=abs(theta_0)
    else:   
        if(head_y>tail_y):
            theta = math.pi 
            theta_0=theta
        else:
            theta = 0 
            theta_0=theta
#


    #print(theta)
    res=data_structures.cue(head_x,head_y,theta,theta_0,tail_x,tail_y)
    
    
    '''
    cv2.circle(img,(res.head_cue_x,res.head_cue_y),3,(2,30,200),6)
    cv2.line(img, (head_x, head_y), (tail_x, tail_y), (255, 255, 255), 2)
    cv2.imshow("cue",img)
    #cv2.imshow("abs",img)
    #cv2.waitKey()
    '''
    return res

'''
    for x1, y1, x2, y2 in lines[0]:
        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
    #print(x1, y1, x2, y2)
    # 注意！像素点的原点在左上角，所以斜率应取反
    distace1 = (white_ball.x - x1) ** 2 + (white_ball.y - y1) ** 2
    #print(distace1)
    distace2 = (white_ball.x - x2) ** 2 + (white_ball.y - y2) ** 2
    #print(distace2)
    if distace2 > distace1:
        print("1是球杆头")
        if x2 == x1:
            if y2 > y1:
                theta = - math.pi / 2
            if y2 == y1:
                print("waring:cue_dection may wrong")
            else :
                theta = math.pi / 2
        else:
            if y2 > y1:
                theta = - math.atan((y2 - y1) / (x2 - x1))
            else :
                thetba = math.atan((y2 - y1) / (x2 - x1))
        res = data_structures.cue(x1, y1, theta)
    else:
        print("2是球杆头")
        if x2 == x1:
            if y2 > y1:
                theta = math.pi / 2
            if y2 == y1:
                print("waring:cue_dection may wrong")
            else :
                theta = - math.pi / 2
        else:
            if y2 > y1:
                theta = math.atan((y2 - y1) / (x2 - x1))
            else :
                theta = - math.atan((y2 - y1) / (x2 - x1))
        res = data_structures.cue(x2, y2, theta)


    return res
'''


'''
def boundary_detection_small(img):
    Image_length=640
    Image_width=480
    #result=cv2.Canny(img,50,125,None,3)
    result=cv2.Canny(img,50,120,None,3)
    cresult=cv2.cvtColor(result,cv2.COLOR_GRAY2BGR)
    cresultP=np.copy(cresult)
    
    cv2.imshow('result.jpg', result)
    cv2.waitKey(0)
    
    
    #line_result=cv2.HoughLines(result,1,np.pi/180,175)[:,0,:]
    line_result=cv2.HoughLines(result,1,np.pi/180,140)[:,0,:]
    N=line_result.shape[0]  #线条总数
    
    #角度检测,分成横线集合和竖线集合
    Error_angle_Vertical_line=5*np.pi/180  #允许的倾斜角度
    Error_angle_Horizontal_line=5*np.pi/180
    
    Horizontal_line=np.zeros((N,2))
    Vertical_line=np.zeros((N,2))
    
    for i in range(N):
        if((line_result[i,1]<Error_angle_Vertical_line)|(np.pi-Error_angle_Vertical_line<line_result[i,1])):
            Vertical_line[i]=line_result[i]
        if(np.pi/2-Error_angle_Horizontal_line<line_result[i,1]<np.pi/2+Error_angle_Horizontal_line): 
            Horizontal_line[i]=line_result[i]
            

    #计算与图像中心的距离
    Horizontal_line_Distance_1=np.zeros(N)
    Horizontal_line_Distance_2=np.zeros(N)
    
    for i in range(N):
        r=Horizontal_line[i,0]
        theta=Horizontal_line[i,1]
        distance=0.5*Image_width*np.sin(theta)-r+0.5*Image_length*np.cos(theta)
        if distance>0:
            Horizontal_line_Distance_1[i]=distance
        if distance<0:
            Horizontal_line_Distance_2[i]=abs(distance)
        
    #寻找最靠近的水平线
    Horizontal_line_Distance_1_min_index=0
    Horizontal_line_Distance_1_min=9999999
    for i in range (N-1):
        if (Horizontal_line_Distance_1[i]!=0)and(Horizontal_line_Distance_1[i]<Horizontal_line_Distance_1_min):
            Horizontal_line_Distance_1_min_index=i
            Horizontal_line_Distance_1_min=Horizontal_line_Distance_1[i]

    Horizontal_line_Distance_2_min_index=0
    Horizontal_line_Distance_2_min=9999999
    for i in range (N-1):
        if (Horizontal_line_Distance_2[i]!=0)and(Horizontal_line_Distance_2[i]<Horizontal_line_Distance_2_min):
            Horizontal_line_Distance_2_min_index=i
            Horizontal_line_Distance_2_min=Horizontal_line_Distance_2[i]


    Vertical_line_Distance_1=np.zeros(N)
    Vertical_line_Distance_2=np.zeros(N)
    
    for i in range(N):
        r=Vertical_line[i,0]
        theta=Vertical_line[i,1]
        distance=0.5*Image_width*np.sin(theta)-r+0.5*Image_length*np.cos(theta)
        if theta>np.pi/2:
            distance=-distance
        if distance>0:
            Vertical_line_Distance_1[i]=distance
        if distance<0:
            Vertical_line_Distance_2[i]=abs(distance)
        
    #寻找最靠近的竖直线
    Vertical_line_Distance_1_min_index=0
    Vertical_line_Distance_1_min=9999999
    for i in range (N-1):
        if (Vertical_line_Distance_1[i]!=0)and(Vertical_line_Distance_1[i]<Vertical_line_Distance_1_min)and(Vertical_line_Distance_1[i]>0.2*Image_length):
            Vertical_line_Distance_1_min_index=i
            Vertical_line_Distance_1_min=Vertical_line_Distance_1[i]

    Vertical_line_Distance_2_min_index=0
    Vertical_line_Distance_2_min=9999999
    for i in range (N-1):
        if (Vertical_line_Distance_2[i]!=0)and(Vertical_line_Distance_2[i]<Vertical_line_Distance_2_min)and(Vertical_line_Distance_2[i]>0.2*Image_length):
            Vertical_line_Distance_2_min_index=i
            Vertical_line_Distance_2_min=Vertical_line_Distance_2[i]

    new_result=np.array([line_result[Horizontal_line_Distance_1_min_index],
                                  line_result[Horizontal_line_Distance_2_min_index],
                                  line_result[Vertical_line_Distance_1_min_index],
                                  line_result[Vertical_line_Distance_2_min_index]])

    #打印最终结果line_result
    #for r,theta in line_result[:,:]:
    #for r,theta in Horizontal_line[:,:]:
    #for r,theta in Vertical_line[:,:]:
    
    
    for r,theta in new_result[:,:]:
        #if (theta==0)&(r>1000):
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * r
            y0 = b * r
            pt1 = (int(x0 + 2000*(-b)), int(y0 + 2000*(a)))
            pt2 = (int(x0 - 2000*(-b)), int(y0 - 2000*(a)))
            cv2.line(cresult,pt1, pt2, (0,0,255),2,cv2.LINE_AA)
            print(r,"$$")
    #cv2.line(img,(300,0), (0,400), (0,0,255),2)
    
    cv2.imshow('houghlines3.jpg', cresult)


    
     
    # print(line_result)
    # print(hough_result[1])
    # print(hough_result[2])
    ##cv2.imshow("image",result)
    
    print("展示result")
    cv2.waitKey(0)   # 按任意按键关闭窗口  这里使用的opencv-contrib-python版本要用4.1.2.30
    cv2.destroyAllWindows()  #否则关闭窗口后无法自动退出该程序
    
    return new_result
'''
def boundary_detection_small(img):
    Image_length=640
    Image_width=360
    #result=cv2.Canny(img,50,125,None,3)
    result=cv2.Canny(img,20,100,None,3)
    cresult=cv2.cvtColor(result,cv2.COLOR_GRAY2BGR)
    cresultP=np.copy(cresult)
    
    #cv2.imshow('result.jpg', result)
    #cv2.waitKey(0)
    
    
    #line_result=cv2.HoughLines(result,1,np.pi/180,175)[:,0,:]
    line_result=cv2.HoughLines(result,1,np.pi/180,140)[:,0,:]
    N=line_result.shape[0]  #线条总数
    
    #角度检测,分成横线集合和竖线集合
    Error_angle_Vertical_line=10*np.pi/180  #允许的倾斜角度
    Error_angle_Horizontal_line=5*np.pi/180
    
    Horizontal_line=np.zeros((N,2))
    Vertical_line=np.zeros((N,2))
    
    for i in range(N):
        if((line_result[i,1]<Error_angle_Vertical_line)|(np.pi-Error_angle_Vertical_line<line_result[i,1])):
            Vertical_line[i]=line_result[i]
        if(np.pi/2-Error_angle_Horizontal_line<line_result[i,1]<np.pi/2+Error_angle_Horizontal_line): 
            Horizontal_line[i]=line_result[i]
            

    #计算与图像中心的距离
    Horizontal_line_Distance_1=np.zeros(N)
    Horizontal_line_Distance_2=np.zeros(N)
    
    for i in range(N):
        r=Horizontal_line[i,0]
        theta=Horizontal_line[i,1]
        distance=0.5*Image_width*np.sin(theta)-r+0.5*Image_length*np.cos(theta)
        if distance>0:
            Horizontal_line_Distance_1[i]=distance
        if distance<0:
            Horizontal_line_Distance_2[i]=abs(distance)
        
    #寻找最靠近的水平线
    Horizontal_line_Distance_1_min_index=0
    Horizontal_line_Distance_1_min=9999999
    for i in range (N-1):
        if (Horizontal_line_Distance_1[i]!=0)and(Horizontal_line_Distance_1[i]<Horizontal_line_Distance_1_min):
            Horizontal_line_Distance_1_min_index=i
            Horizontal_line_Distance_1_min=Horizontal_line_Distance_1[i]

    Horizontal_line_Distance_2_min_index=0
    Horizontal_line_Distance_2_min=9999999
    for i in range (N-1):
        if (Horizontal_line_Distance_2[i]!=0)and(Horizontal_line_Distance_2[i]<Horizontal_line_Distance_2_min):
            Horizontal_line_Distance_2_min_index=i
            Horizontal_line_Distance_2_min=Horizontal_line_Distance_2[i]


    Vertical_line_Distance_1=np.zeros(N)
    Vertical_line_Distance_2=np.zeros(N)
    
    for i in range(N):
        r=Vertical_line[i,0]
        theta=Vertical_line[i,1]
        distance=0.5*Image_width*np.sin(theta)-r+0.5*Image_length*np.cos(theta)
        if theta>np.pi/2:
            distance=-distance
        if distance>0:
            Vertical_line_Distance_1[i]=distance
        if distance<0:
            Vertical_line_Distance_2[i]=abs(distance)
        
    #寻找最靠近的竖直线
    Vertical_line_Distance_1_min_index=0
    Vertical_line_Distance_1_min=9999999
    for i in range (N-1):
        if (Vertical_line_Distance_1[i]!=0)and(Vertical_line_Distance_1[i]<Vertical_line_Distance_1_min)and(Vertical_line_Distance_1[i]>0.2*Image_length):
            Vertical_line_Distance_1_min_index=i
            Vertical_line_Distance_1_min=Vertical_line_Distance_1[i]

    Vertical_line_Distance_2_min_index=0
    Vertical_line_Distance_2_min=9999999
    for i in range (N-1):
        if (Vertical_line_Distance_2[i]!=0)and(Vertical_line_Distance_2[i]<Vertical_line_Distance_2_min)and(Vertical_line_Distance_2[i]>0.2*Image_length):
            Vertical_line_Distance_2_min_index=i
            Vertical_line_Distance_2_min=Vertical_line_Distance_2[i]

    new_result=np.array([line_result[Horizontal_line_Distance_1_min_index],
                                  line_result[Horizontal_line_Distance_2_min_index],
                                  line_result[Vertical_line_Distance_1_min_index],
                                  line_result[Vertical_line_Distance_2_min_index]])

    #打印最终结果line_result
    #for r,theta in line_result[:,:]:
    #for r,theta in Horizontal_line[:,:]:
    #for r,theta in Vertical_line[:,:]:
    
    
    for r,theta in new_result[:,:]:
        #if (theta==0)&(r>1000):
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * r
            y0 = b * r
            pt1 = (int(x0 + 2000*(-b)), int(y0 + 2000*(a)))
            pt2 = (int(x0 - 2000*(-b)), int(y0 - 2000*(a)))
            cv2.line(cresult,pt1, pt2, (0,0,255),2,cv2.LINE_AA)
            print(r,"$$")
    #cv2.line(img,(300,0), (0,400), (0,0,255),2)
    cv2.namedWindow("img",0)
    cv2.resizeWindow("img",640,480)
    #cv2.resize(img,(640,480))
    cv2.imshow('img', cresult)


    
     
    # print(line_result)
    # print(hough_result[1])
    # print(hough_result[2])
    ##cv2.imshow("image",result)
    
    print("展示result")
    cv2.waitKey(0)   # 按任意按键关闭窗口  这里使用的opencv-contrib-python版本要用4.1.2.30
    cv2.destroyAllWindows()  #否则关闭窗口后无法自动退出该程序
    
    return new_result


def cue_point_to_ball(cue,ball,max_h):
    if(cue is None):
        print("in cue check, cue is None")
        return None

    if(ball is None):
        print("No ball")
        return None

    a=math.sqrt((cue.head_cue_y-cue.tail_cue_y)*(cue.head_cue_y-cue.tail_cue_y)+(cue.head_cue_x-cue.tail_cue_x)*(cue.head_cue_x-cue.tail_cue_x))
    b=math.sqrt((cue.tail_cue_y-ball.y)*(cue.tail_cue_y-ball.y)+(cue.tail_cue_x-ball.x)*(cue.tail_cue_x-ball.x))
    c=math.sqrt((cue.head_cue_y-ball.y)*(cue.head_cue_y-ball.y)+(cue.head_cue_x-ball.x)*(cue.head_cue_x-ball.x))

    cos_theta=(a*a+b*b-c*c)/2/a/b
    if(cos_theta > 1):
        print("cos theta > 1")
        return 0

    if(cos_theta < 0):
        print("ball close to tail")
        return 0

    h=b*math.sqrt(1-cos_theta*cos_theta)
    if(h<max_h):
        return 1
    else:
        return 0
'''
def cue_point_to_ball(cue,white_ball,max_theta_diff):
    if(cue is None):
        print("in cue check, cue is None")
        return None

    if(white_ball is None):
        print("No ball")
        return None

    theta_two_points=math.atan(abs((white_ball.y-cue.head_cue_y)/(white_ball.x-cue.head_cue_x)))
    diff_theta=abs(abs(cue.cue_theta_origin)-theta_two_points)

    print("two points: x=",white_ball.x," y=",white_ball.y)
    print("theta_two_points=",theta_two_points)
    print("theta_origin=",cue.cue_theta_origin)
    print("diff_theta=",diff_theta)

    if(diff_theta>max_theta_diff):
        return 0
    else:
        return 1
'''
'''
def boundary_detection(img1):
    
    Image_length=1920
    Image_width=1080
    img=cv2.resize(img1,(Image_length,Image_width))
    
    #result=cv2.Canny(img,50,125,None,3)
    result=cv2.Canny(img,75,125,None,3)
    cresult=cv2.cvtColor(result,cv2.COLOR_GRAY2BGR)
    cresultP=np.copy(cresult)
    
    cv2.imshow('result.jpg', result)
    cv2.waitKey(0)
    
    
    #line_result=cv2.HoughLines(result,1,np.pi/180,175)[:,0,:]
    line_result=cv2.HoughLines(result,1,np.pi/180,125)[:,0,:]
    N=line_result.shape[0]  #线条总数
    
    #角度检测,分成横线集合和竖线集合
    Error_angle_Vertical_line=5*np.pi/180  #允许的倾斜角度
    Error_angle_Horizontal_line=1.3*np.pi/180
    
    Horizontal_line=np.zeros((N,2))
    Vertical_line=np.zeros((N,2))
    
    for i in range(N):
        if((line_result[i,1]<Error_angle_Vertical_line)|(np.pi-Error_angle_Vertical_line<line_result[i,1])):
            Vertical_line[i]=line_result[i]
        if(np.pi/2-Error_angle_Horizontal_line<line_result[i,1]<np.pi/2+Error_angle_Horizontal_line): 
            Horizontal_line[i]=line_result[i]
            

    #计算与图像中心的距离
    Horizontal_line_Distance_1=np.zeros(N)
    Horizontal_line_Distance_2=np.zeros(N)
    
    for i in range(N):
        r=Horizontal_line[i,0]
        theta=Horizontal_line[i,1]
        distance=0.5*Image_width*np.sin(theta)-r+0.5*Image_length*np.cos(theta)
        if distance>0:
            Horizontal_line_Distance_1[i]=distance
        if distance<0:
            Horizontal_line_Distance_2[i]=abs(distance)
        
    #寻找最靠近的水平线
    Horizontal_line_Distance_1_min_index=0
    Horizontal_line_Distance_1_min=9999999
    for i in range (N-1):
        if (Horizontal_line_Distance_1[i]!=0)and(Horizontal_line_Distance_1[i]<Horizontal_line_Distance_1_min):
            Horizontal_line_Distance_1_min_index=i
            Horizontal_line_Distance_1_min=Horizontal_line_Distance_1[i]

    Horizontal_line_Distance_2_min_index=0
    Horizontal_line_Distance_2_min=9999999
    for i in range (N-1):
        if (Horizontal_line_Distance_2[i]!=0)and(Horizontal_line_Distance_2[i]<Horizontal_line_Distance_2_min):
            Horizontal_line_Distance_2_min_index=i
            Horizontal_line_Distance_2_min=Horizontal_line_Distance_2[i]


    Vertical_line_Distance_1=np.zeros(N)
    Vertical_line_Distance_2=np.zeros(N)
    
    for i in range(N):
        r=Vertical_line[i,0]
        theta=Vertical_line[i,1]
        distance=0.5*Image_width*np.sin(theta)-r+0.5*Image_length*np.cos(theta)
        if theta>np.pi/2:
            distance=-distance
        if distance>0:
            Vertical_line_Distance_1[i]=distance
        if distance<0:
            Vertical_line_Distance_2[i]=abs(distance)
        
    #寻找最靠近的竖直线
    Vertical_line_Distance_1_min_index=0
    Vertical_line_Distance_1_min=9999999
    for i in range (N-1):
        if (Vertical_line_Distance_1[i]!=0)and(Vertical_line_Distance_1[i]<Vertical_line_Distance_1_min)and(Vertical_line_Distance_1[i]>0.4*Image_length):
            Vertical_line_Distance_1_min_index=i
            Vertical_line_Distance_1_min=Vertical_line_Distance_1[i]

    Vertical_line_Distance_2_min_index=0
    Vertical_line_Distance_2_min=9999999
    for i in range (N-1):
        if (Vertical_line_Distance_2[i]!=0)and(Vertical_line_Distance_2[i]<Vertical_line_Distance_2_min)and(Vertical_line_Distance_2[i]>0.4*Image_length):
            Vertical_line_Distance_2_min_index=i
            Vertical_line_Distance_2_min=Vertical_line_Distance_2[i]

    new_result=np.array([line_result[Horizontal_line_Distance_1_min_index],
                                  line_result[Horizontal_line_Distance_2_min_index],
                                  line_result[Vertical_line_Distance_1_min_index],
                                  line_result[Vertical_line_Distance_2_min_index]])

    #打印最终结果line_result
    #for r,theta in line_result[:,:]:
    #for r,theta in Horizontal_line[:,:]:
    #for r,theta in Vertical_line[:,:]:
    for r,theta in new_result[:,:]:
        #if (theta==0)&(r>1000):
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * r
            y0 = b * r
            pt1 = (int(x0 + 2000*(-b)), int(y0 + 2000*(a)))
            pt2 = (int(x0 - 2000*(-b)), int(y0 - 2000*(a)))
            cv2.line(cresult,pt1, pt2, (0,0,255),2,cv2.LINE_AA)
            print(r,"$$")
    #cv2.line(img,(300,0), (0,400), (0,0,255),2)
    #cv2.namedWindow('input',cv2.WINDOW_NORMAL)
    cv2.imshow('imput', cresult)
    
     
    # print(line_result)
    # print(hough_result[1])
    # print(hough_result[2])
    ##cv2.imshow("image",result)
    print("展示result")
    cv2.waitKey(0)   # 按任意按键关闭窗口  这里使用的opencv-contrib-python版本要用4.1.2.30
    cv2.destroyAllWindows()  #否则关闭窗口后无法自动退出该程序
    return new_result
'''

    
