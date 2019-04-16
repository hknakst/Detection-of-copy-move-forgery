import cv2
import numpy as np
import DetectionOfCopyMoveForgery


img = cv2.imread("indir.bmp" ,0)
height, width= img.shape

"""for i in range (512):
    for j in range(512):
        img[i][j]=0"""

imf = np.float32(img)/255.0
dst = cv2.dct(imf)
crop_img = img[10:10+50, 20:20+30]
#cv2.imshow("cropped", crop_img)

cv2.imshow("sonuc",dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
# cv2.imwrite("sonuc.bmp",img)
