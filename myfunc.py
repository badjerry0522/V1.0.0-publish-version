# -- coding: utf-8 -
# -- coding: utf-8 -
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
######################################################
#本文件由郭科睿创建
######################################################

#排序
def sort_(list0):
    """
    根据y值对circle冒泡排序
    :param list0: 针对circle
    :return: 排序好的结果
    """
    list = list0[0].copy()
    for i in range(len(list)):
        for j in range(0, len(list) - i - 1):
            if list[j][1] > list[j + 1][1]:
                temp = list[j].copy()
                list[j] = list[j + 1].copy()
                list[j + 1] = temp.copy()
    #print(list)
    return list


def find_circle(img, r_min, r_max, para4Hough):
    """

    :param img: 输入的rgb图片
    :param r_min: 最小半径
    :param r_max: 最大半径
    :param para4Hough: HoughCircle的param2
    :return: circles,识别结果;output,可视化结果
    """
    img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    output = img.copy()
    circles = cv2.HoughCircles(img_g,
                               cv2.HOUGH_GRADIENT,
                               1,
                               10,
                               param1=100,
                               param2=para4Hough,
                               minRadius=r_min,
                               maxRadius=r_max)

    if circles is not None:
        #("共检测", len(circles[0]), "个台球")
        circles_ = sort_(circles)  # 根据y值进行冒泡排序
        #print(circles_)
        #print("not none")
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(output,(x,y),r,(0,255,0),1)
            cv2.rectangle(output, (x - 1, y - 1), (x + 1, y + 1), (0, 128, 255), -1)
        return circles_,output
    else:
        return None,img


def xyxy_to_xywh(xyxy):
    center_x = (xyxy[0] + xyxy[2]) / 2
    center_y = (xyxy[1] + xyxy[3]) / 2
    w = xyxy[2] - xyxy[0]
    h = xyxy[3] - xyxy[1]
    return (center_x, center_y, w, h)


def plot_one_box(xyxy, img, color=(0, 200, 0), target=False):
    xy1 = (int(xyxy[0]), int(xyxy[1]))
    xy2 = (int(xyxy[2]), int(xyxy[3]))
    if target:
        color = (0, 0, 255)
    cv2.rectangle(img, xy1, xy2, color, 1, cv2.LINE_AA)  # filled


def plot_information(trace_list_all):
    """
    由完整的trace_list绘制速度-时间曲线 + 曲线线性程度
    :param trace_list_all: 完整的trace_list
    :return: NONE
    """
    velocity = []
    velocity_av =[]
    orientation = []
    orientation_av = []
    x_before = trace_list_all[0][0]
    y_before = trace_list_all[0][1]
    print(trace_list_all)
    for [x,y] in trace_list_all:
        dis = ((x - x_before) ** 2 + (y - y_before) ** 2) ** 0.5
        if (y - y_before) != 0:
            k = (x - x_before)/(y - y_before)
            orientation.append(k)
        #认为摄像头为固定帧率
        velocity.append(dis)
        x_before = x
        y_before = y
    #print(velocity)
    i = 0
    v_ = 0
    for v in velocity:
        i = i + 1
        v_ = v_+ v
        if i % 3 ==0:
            velocity_av.append(v_ / 5)
            v_ = 0
    i = 0
    o_ = 0
    for o in orientation:
        i = i + 1
        o_ = o_ + o
        if i % 3 ==0:
            orientation_av.append(o_ / 3)
            o_ = 0
    fig1 = plt.figure(1)
    plt.plot(velocity_av)
    plt.title("velocity of ball (px/frame)")
    fig2 = plt.figure(2)
    plt.plot(orientation)
    plt.title("orientation of ball (px/frame)")
    plt.show()


def updata_trace_list(box_center, trace_list, max_list_len=1000):
    if len(trace_list) <= max_list_len:
        trace_list.append(box_center)
    else:
        trace_list.pop(0)
        trace_list.append(box_center)
    return trace_list


def draw_trace(img, trace_list):
    """
    更新trace_list,绘制trace
    :param trace_list:
    :param max_list_len:
    :return:
    """
    for i, item in enumerate(trace_list):

        if i < 1:
            continue
        cv2.line(img,
                 (trace_list[i][0], trace_list[i][1]), (trace_list[i - 1][0], trace_list[i - 1][1]),
                 (255, 255, 0), 3)


def cal_iou(box1, box2):
    """

    :param box1: xyxy 左上右下
    :param box2: xyxy
    :return:
    """
    x1min, y1min, x1max, y1max = box1[0], box1[1], box1[2], box1[3]
    x2min, y2min, x2max, y2max = box2[0], box2[1], box2[2], box2[3]
    # 计算两个框的面积
    s1 = (y1max - y1min + 1.) * (x1max - x1min + 1.)
    s2 = (y2max - y2min + 1.) * (x2max - x2min + 1.)

    # 计算相交部分的坐标
    xmin = max(x1min, x2min)
    ymin = max(y1min, y2min)
    xmax = min(x1max, x2max)
    ymax = min(y1max, y2max)

    inter_h = max(ymax - ymin + 1, 0)
    inter_w = max(xmax - xmin + 1, 0)

    intersection = inter_h * inter_w
    union = s1 + s2 - intersection

    # 计算iou
    iou = intersection / union
    return iou


def cal_distance(box1, box2):
    """
    计算两个box中心点的距离
    :param box1: xyxy 左上右下
    :param box2: xyxy
    :return:
    """
    center1 = ((box1[0] + box1[2]) // 2, (box1[1] + box1[3]) // 2)
    center2 = ((box2[0] + box2[2]) // 2, (box2[1] + box2[3]) // 2)
    dis = ((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2) ** 0.5

    return dis


def xywh_to_xyxy(xywh):
    x1 = xywh[0] - xywh[2]//2
    y1 = xywh[1] - xywh[3]//2
    x2 = xywh[0] + xywh[2] // 2
    y2 = xywh[1] + xywh[3] // 2

    return [x1, y1, x2, y2]

def get_distance_from_point_to_line(point, line_point1, line_point2):
    """

    :param point: 点
    :param line_point1: 直线上任意一点
    :param line_point2: 直线上任意另一点
    :return: 点到直线的距离
    """
    #对于两点坐标为同一点时,返回点与点的距离
    if line_point1[0] == line_point2[0] and line_point1[1] == line_point2[1]:
        point_array = np.array(point )
        point1_array = np.array(line_point1)
        return np.linalg.norm(point_array -point1_array )
    #计算直线的三个参数
    A = line_point2[1] - line_point1[1]
    B = line_point1[0] - line_point2[0]
    C = (line_point1[1] - line_point2[1]) * line_point1[0] + \
        (line_point2[0] - line_point1[0]) * line_point1[1]
    #根据点到直线的距离公式计算距离
    distance = np.abs(A * point[0] + B * point[1] + C) / (np.sqrt(A**2 + B**2))
    return distance

def find_best_line(lines,white_ball):
    """

    :param lines:[[x,y,x,y][x,y,x,y]]
    :param white_ball:[x,y]
    :return: lines中，球杆的轮廓
    """
    min_distance = [1000, 1000] #白球到直线距离
    line_cue_0 = np.zeros(4)
    line_cue_1 = np.zeros(4)
    i=0
    for line in lines:
        #print(line[0])
        point1 = np.array(line[0][0:2]) #0，1
        point2 = np.array(line[0][2:4]) #2，3
        distance = get_distance_from_point_to_line(white_ball, point1, point2)
        if distance < min(min_distance):
            min_distance[1] = min_distance[0]
            line_cue_1 = line_cue_0
            min_distance[0] =distance
            line_cue_0 = line[0]
    
    return_flag=0
    if min(min_distance) >= 100:
        print("球杆可能未指向球")
        return_flag=1
    if abs(min_distance[0] - min_distance[1]) >= 30:
        print("警告：Hough检测返回值可能未包含球杆的边缘")
        return_flag=1

    return line_cue_0,line_cue_1,return_flag



if __name__ == "__main__":
    box1 = [100, 100, 200, 200]
    box2 = [100, 100, 200, 300]
    iou = cal_iou(box1, box2)
    print(iou)
    box1.pop(0)
    box1.append(555)
    print(box1)
