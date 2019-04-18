from DetectionOfCopyMoveForgery import *



img = cv2.imread("a.png" ,0)
height, width= img.shape

asd = DetectionofCopyMoveForgery(img,height,width,8,8)
asd.detection_forgery()
#z=[[1,1,22,3,4],[5,6,7,8,9],[1,11,12,13,14],[1,1,17,18,19],[5,6,2,23,24],[1,1,18,1,1],[0,0,0,1000,0],[0,0,0,10,100],[0,0,0,1000,-1]]
#zz= np.array([[0,1,2],[4,5,6],[8,9,10],[12,13,14]])
#zz1=np.array([[0,1,5],[3,4,5],[6,7,8]])
# print(zigzag(z))





#mask = np.ones((8,8)) print(mask)


cv2.waitKey(0)
cv2.destroyAllWindows()
# cv2.imwrite("sonuc.bmp",img)
