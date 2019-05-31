from DetectionOfCopyMoveForgery import *

def getFmeasure(orginal_img, test_img, width, height):

    DP=0
    YP=0
    YN=0
    for i in range(height):
        for j in range(width):
            if orginal_img[i][j]==255 and test_img[i][j]==255:
                DP +=1
            if orginal_img[i][j]==0 and test_img[i][j]==255:
                YP +=1
            if orginal_img[i][j]==255 and test_img[i][j]==0:
                YN +=1

    precision =DP/(DP+YP)
    recall =DP/(DP+YN)

    return 2*((precision*recall)/(precision+recall))




# for i in range(160,0,-2):
#     path ="forged_images/"+str(i)+".png"
#     img = cv2.imread(path ,0)
#     height, width= img.shape
#     # (img, height, width, blocksize, oklid_threshold, correlation_threshold, vec_len_threshold, num_ofvector_threshold)
#     asd = DetectionofCopyMoveForgery(img, height, width, 8,3.5,8,100,5)
#     asd.detection_forgery()
#     cv2.waitKey(0)
#     path = "forged_images/" + str(i-1) + ".png"
#     original_img = cv2.imread(path,0)
#     print(getFmeasure(original_img,img,width,height))



img = cv2.imread("example_photo/foto4_gj90.png" ,0)
height, width= img.shape
# (img, height, width, blocksize, oklid_threshold, correlation_threshold, vec_len_threshold, num_ofvector_threshold)
asd = DetectionofCopyMoveForgery(img, height, width, 8,3.5,8,100,5)
asd.detection_forgery()
cv2.waitKey(0)

original_img = cv2.imread("photo/foto4_sonuc.png",0)
print(getFmeasure(original_img,img,width,height))
cv2.destroyAllWindows()









