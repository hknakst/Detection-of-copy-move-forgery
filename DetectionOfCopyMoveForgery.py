import cv2
import numpy as np
from math import sqrt


class DetectionofCopyMoveForgery:

    def __init__(self, img, height, width, blocksize,oklid_threshold,correlation_threshold,vec_len_threshold,num_ofvector_threshold):
        self.img = img
        self.height=height
        self.width=width
        self.blocksize = blocksize
        self.oklid_threshold = oklid_threshold
        self.correlation_threshold = correlation_threshold
        self.vec_len_threshold = vec_len_threshold
        self.num_ofvector_threshold=num_ofvector_threshold

        self.block_vector=[]
        self.sizeof_vector=8;
        self.hough_space = (self.height, self.width)
        self.hough_space = np.zeros(self.hough_space)
        self.shiftvector=[]


    def detection_forgery(self):
        self.dct_of_img()
        self.lexicographically_sort_of_vectors()
        self.correlation_of_vectors()

        #son olarakan belirlenen esik degerine gore ayni dogrultudaki shift vektor sayisina gore sahte alanlar belirleniyor.
        for i in range(self.height):
            for j in range(self.width):
                if (self.hough_space[i][j]) >self.num_ofvector_threshold:
                    for k in range(len(self.shiftvector)):
                        if self.shiftvector[k][0]==j and self.shiftvector[k][1]==i:
                            cv2.line(self.img, (self.shiftvector[k][2], self.shiftvector[k][3]), (self.shiftvector[k][4], self.shiftvector[k][5]), (0), 2)
        cv2.imshow("sonuc",self.img)
        cv2.waitKey(0)


    def dct_of_img(self):

        for r in range(0, self.height, self.blocksize):
            for c in range(0, self.width, self.blocksize):
                block = self.img[r:r + self.blocksize, c:c + self.blocksize]
                # imf = np.float32(block)  #0 ile 1 arasında normalize ediyoruz
                # dct = cv2.dct(imf)      # block block dst uyguluyoruz ve virgülden sonraki 6. basamağı yumarlıyoruz
                img2 = np.zeros((self.blocksize, self.blocksize), dtype=np.float32)
                img2 = img2 + block[:self.blocksize, :self.blocksize]
                dct = cv2.dct(img2)

                QUANTIZATION_MAT_50 = np.array([[16, 11, 10, 16, 24, 40, 51, 61], [12, 12, 14, 19, 26, 58, 60, 55],
                                             [14, 13, 16, 24, 40, 57, 69, 56], [14, 17, 22, 29, 51, 87, 80, 62],
                                             [18, 22, 37, 56, 68, 109, 103, 77], [24, 35, 55, 64, 81, 104, 113, 92],
                                             [49, 64, 78, 87, 103, 121, 120, 101], [72, 92, 95, 98, 112, 100, 103, 99]])
                QUANTIZATION_MAT_10 = np.array([[80, 60, 50, 80, 120, 200, 255, 255], [55, 60, 70, 95, 130, 255, 255,255],
                                             [70, 65, 80, 120, 200, 255, 255, 255], [70, 85, 110, 145, 255, 255,255,255],
                                             [90, 110, 185,  255, 255,255,255,255], [120, 175, 255, 255,255,255, 255,255],
                                             [255, 255,255,255, 255,255,255,255], [255, 255,255,255, 255,255,255,255]])
                #dct donusumu quantalama matrisine bolerek sıkıstırırız iliskilere baktigimiz icin buna gerek olmayabilir..
                dct= np.divide(dct, QUANTIZATION_MAT_50).astype(int)
                self.significant_part_extraction(self.zigzag(dct),self.sizeof_vector,c,r)



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
        for i in range((self.blocksize * self.blocksize), significant_size, -1):
            vector.pop()

        vector.append(x)  # blogun baslangıc kordinatının x noktası vektorun sonuna ekleniyor
        vector.append(y)  # aynı sekilde y noktası ekleniyor
        # her block sonucunu vector listemize atiyoruz.
        self.block_vector.append(vector)


    def lexicographically_sort_of_vectors(self,):
        #sutun siralaması oldugu icin ters cevirip siralamamiz lazim
        #ayni zamanda son iki yani ters cevirince ilk iki satirida koordinat bilgimiz var bunları sıralamicaz.
        self.block_vector=np.array(self.block_vector)
        self.block_vector= self.block_vector[np.lexsort(np.rot90(self.block_vector)[2:(self.sizeof_vector + 1) + 2 , :])]
        self.block_vector=np.round(self.block_vector, 3)

        # for i in range(sort_size):
        #     for j in range(len(vector)):
        #         for k in range(len(vector) - 1):
        #             if (i == 0):
        #                 if (vector[k + 1][i] < vector[k][i]):
        #                     temp = vector[k]
        #                     vector[k] = vector[k + 1]
        #                     vector[k + 1] = temp
        #
        #             else:
        #                 sum =0
        #                 for h in range(1,i+1):
        #                     if (vector[k + 1][i - h] == vector[k][i - h]):
        #                         sum +=1
        #
        #                 if(sum==i):
        #                     if (vector[k + 1][i] < vector[k][i]):
        #                         temp = vector[k]
        #                         vector[k] = vector[k + 1]
        #                         vector[k + 1] = temp



    def correlation_of_vectors(self):

        for i in range(len(self.block_vector)):
            if(i+self.correlation_threshold >= len(self.block_vector)):
                self.correlation_threshold -=1
                #vektorleri asagiya dogru belirlenen esik kadar oklid benzerliklerine gore inceliyoruz.
            for j in range(i+1, i + self.correlation_threshold + 1):
                if(self.oklid(self.block_vector[i], self.block_vector[j], self.sizeof_vector) <= self.oklid_threshold):
                    #birbirlerine benzeyelen vektorlerin son indislerinde bulunan konumlarini yeni bir vektorde tutuyoruz.
                    v1=[]
                    v2=[]
                    v1.append(int(self.block_vector[i][-2])) #x1
                    v1.append(int(self.block_vector[i][-1])) #y1
                    v2.append(int(self.block_vector[j][-2])) #x2
                    v2.append(int(self.block_vector[j][-1])) #y2
                    self.elimination_of_weak_vectors(v1,v2,2)


    def elimination_of_weak_vectors(self,vector1,vector2,size):
        #iliskili vektorlerlerin oklid ile uzunluklarini bularak belirlenen esik degerine gore kisa olanlari eliyoruz.
        if(self.oklid(vector1,vector2,size) >= self.vec_len_threshold):
            self.elimination_of_weak_area(vector1,vector2)

    def elimination_of_weak_area(self,vector1,vector2):
        #son olarak belirlenen vektorlerin dogrultulari hesaplanarak , bu dogrultunun hough uzayindaki konumu bir arttırıliyor
        #hangi blockvektorlerin hangi dogrultuyu arttirdigini kaybetmemek icin yeni bir vektor olusturularak once dogrultu sonra
        #kendi koordinatlari vektorde tutuluyor ve bu vektorlerde block block shift vektore atiliyor.
        c = abs(vector2[0]-vector1[0])
        r = abs(vector2[1]-vector1[1])
        self.hough_space[r][c] +=1
        vector=[]
        vector.append(c)
        vector.append(r)
        vector.append(vector1[0])
        vector.append(vector1[1])
        vector.append(vector2[0])
        vector.append(vector2[1])
        self.shiftvector.append(vector)


    def oklid(self,vector1,vector2,size):
        sum=0
        for i in range(size):
            sum += (vector2[i]-vector1[i])**2

        return sqrt(sum)