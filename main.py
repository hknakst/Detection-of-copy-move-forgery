from DetectionOfCopyMoveForgery import *


def oklida(vector1, vector2, size):
    sum = 0
    for i in range(size):
        sum = sum + (vector2[i] - vector1[i]) ** 2

    return sqrt(sum)

img = cv2.imread("aa" ,0)
height, width= img.shape

asd = DetectionofCopyMoveForgery(img,height,width,16,16)
#asd.detection_forgery()
#z=[[1,1,22,3,4],[5,6,7,8,9],[1,11,12,13,14],[1,1,17,18,19],[5,6,2,23,24],[1,1,18,1,1],[0,0,0,1000,0],[0,0,0,10,100],[0,0,0,1000,-1]]
zz= np.array([[0,1,2],[4,5,6],[8,9,10],[12,13,14]])
zz1=np.array([[0,1,5],[3,4,5],[6,7,8]])
# print(zigzag(z))

print(oklida(zz[1],zz1[1],3))



#mask = np.ones((8,8)) print(mask)


cv2.waitKey(0)
cv2.destroyAllWindows()
# cv2.imwrite("sonuc.bmp",img)
