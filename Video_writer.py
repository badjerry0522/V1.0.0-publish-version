import cv2

fourcc = cv2.VideoWriter.fourcc('m', 'p', '4', 'v')
out = cv2.VideoWriter('big_pool_b2b_e1.mp4', fourcc, 20, (1280, 720))
index=501
while(1):
    print(index)
    img=cv2.imread("D:\\work\\pool\\src\\big_pool_result_e1\\"+str(index)+".jpg")
    #cv2.imshow("img",img)
    #cv2.waitKey(0)
    index=index+1
    if(img is None):
        continue
    out.write(img)
    if(index==3692):
        break
out.release()
