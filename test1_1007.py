#边界检测
import cv2
import cv2
import numpy as np

Image_length=1920
Image_width=1080

def boundary_detection(img1):
    
    Image_length=640
    Image_width=480
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
    Error_angle_Horizontal_line=3*np.pi/180
    
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

    
    
    
    




test_img=cv2.imread("C:/Users/53075/Pictures/SMP_test/11.jpg",cv2.IMREAD_GRAYSCALE)
test_img=cv2.resize(test_img,dsize=(Image_length,Image_width))
new_result=boundary_detection(test_img)
    
     
   