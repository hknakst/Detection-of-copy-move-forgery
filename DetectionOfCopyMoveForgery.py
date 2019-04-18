import cv2
import numpy as np
from math import sqrt


class DetectionofCopyMoveForgery:

    def __init__(self,img,height,width,blocksize_r,blocksize_c):
        self.img = img
        self.height=height
        self.width=width
        self.blocksize_r = blocksize_r
        self.blocksize_c = blocksize_c
        self.vector=[]
        self.sizeof_vector=16;


    def detection_forgery(self):
        self.dct_of_img()
        self.lexicographically_sort_of_vectors(self.vector,self.sizeof_vector)
        self.correlation_of_vectors(0.1 ,5)
        cv2.imshow("sonuc",self.img)
        cv2.waitKey(0)


    def dct_of_img(self):

        for r in range(0, self.height - self.blocksize_r, self.blocksize_r):
            for c in range(0, self.width - self.blocksize_c, self.blocksize_c):
                block = self.img[r:r + self.blocksize_r, c:c + self.blocksize_c]
                imf = np.float32(block) / 255.0  #0 ile 1 arasında normalize ediyoruz
                dst = np.round(cv2.dct(imf),6)      # block block dst uyguluyoruz ve virgülden sonraki 6. basamağı yumarlıyoruz
                self.significant_part_extraction(self.zigzag(dst),self.sizeof_vector,c,r)



    def zigzag(self,matrix):
        """Scan matrix of zigzag algorithm"""
        vector = []
        n = len(matrix) - 1
        i = 0
        j = 0

        for _ in range(n * 2):
            vector.append(matrix[i][j])

            if j == n:   # right border
                i += 1     # shift
                while i != n:   # diagonal passage
                    vector.append(matrix[i][j])
                    i += 1
                    j -= 1
            elif i == 0:  # top border
                j += 1
                while j != 0:
                    vector.append(matrix[i][j])
                    i += 1
                    j -= 1
            elif i == n:   # bottom border
                j += 1
                while j != n:
                    vector.append(matrix[i][j])
                    i -= 1
                    j += 1
            elif j == 0:   # left border
                i += 1
                while i != 0:
                    vector.append(matrix[i][j])
                    i -= 1
                    j += 1

        vector.append(matrix[i][j])
        return vector

    def significant_part_extraction(self,vector,significant_size,x,y):

        # 1x64 boyutundaki vectorden sadece alcak freans yani anlamli kismini cikarmak icin belirlenen(16) degere kadar pop islemi yapilir.
        for i in range((self.blocksize_c * self.blocksize_r),significant_size, -1):
            vector.pop()

        vector.append(x)  # blogun baslangıc kordinatının x noktası vektorun sonuna ekleniyor
        vector.append(y)  # aynı sekilde y noktası ekleniyor
        # her block sonucunu vector listemize atiyoruz.
        self.vector.append(vector)

    def lexicographically_sort_of_vectors(self,vector,sort_size):

        for i in range(sort_size):
            for j in range(len(vector)):
                for k in range(len(vector) - 1):
                    if (i == 0):
                        if (vector[k + 1][i] < vector[k][i]):
                            temp = vector[k]
                            vector[k] = vector[k + 1]
                            vector[k + 1] = temp

                    else:
                        if (vector[k + 1][i - 1] == vector[k][i - 1]):
                            if (vector[k + 1][i] < vector[k][i]):
                                temp = vector[k]
                                vector[k] = vector[k + 1]
                                vector[k + 1] = temp



    def correlation_of_vectors(self,oklid_threshold,correlation_threshold):

        for i in range(len(self.vector)):
            if(i+correlation_threshold >= len(self.vector)):
                correlation_threshold -=1
            for j in range(i+1,i+correlation_threshold+1):
                if(self.oklid(self.vector[i],self.vector[j],self.sizeof_vector) <= oklid_threshold):
                    v1=[]
                    v2=[]
                    v1.append(self.vector[i][-2]) #x1
                    v1.append(self.vector[i][-1]) #y1
                    v2.append(self.vector[j][-2]) #x2
                    v2.append(self.vector[j][-1]) #y2
                    self.elimination_of_weak_vectors(v1,v2,2,10)


    def elimination_of_weak_vectors(self,vector1,vector2,size,threshold_lenght):
        if(self.oklid(vector1,vector2,size) >= threshold_lenght):
            print(self.oklid(vector1,vector2,size))
            cv2.line(self.img,(vector1[0],vector1[1]),(vector2[0],vector2[1]),(0),2)
            self.elimination_of_weak_area(vector1,vector2,10)

    def elimination_of_weak_area(self,vector1,vector2,threshold_num_ofvectors):
        pass

    def oklid(self,vector1,vector2,size):
        sum=0
        for i in range(size):
            sum += (vector2[i]-vector1[i])**2

        return sqrt(sum)