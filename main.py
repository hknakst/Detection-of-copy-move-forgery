from DetectionOfCopyMoveForgery import *





img = cv2.imread("aa" ,0)
height, width= img.shape

asd = DetectionofCopyMoveForgery(img,height,width,16,16)
asd.dct_of_img()
# z=[[0,1,2,3,4],[5,6,7,8,9],[10,11,12,13,14],[15,16,17,18,19],[20,21,22,23,24]]
# zz= np.array([[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]])
# zz1=np.array([[0,1,2],[3,4,5],[6,7,8]])
# print(zigzag(z))






#mask = np.ones((8,8)) print(mask)


cv2.waitKey(0)
cv2.destroyAllWindows()
# cv2.imwrite("sonuc.bmp",img)
