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
        self.sizeof_vector=16;
        self.hough_space = (self.height, self.width,2)
        self.hough_space = np.zeros(self.hough_space)
        self.shiftvector=[]


    def detection_forgery(self):

        self.dct_of_img()
        self.lexicographically_sort_of_vectors()
        self.correlation_of_vectors()

        #son olarakan belirlenen esik degerine gore ayni dogrultudaki shift vektor sayisina gore sahte alanlar belirleniyor.
        max=-1
        for i in range(self.height):
            for j in range(self.width):
                for h in range(2):
                    if(self.hough_space[i][j][h]) > max:
                        max = self.hough_space[i][j][h]
        for i in range(self.height):
            for j in range(self.width):
                self.img[i][j]=0

        for i in range(self.height):
            for j in range(self.width):
                for h in range(2):
                    if (self.hough_space[i][j][h]) >= (max - (max*self.num_ofvector_threshold/100)):
                        for k in range(len(self.shiftvector)):
                            if (self.shiftvector[k][0]==j and self.shiftvector[k][1]==i and self.shiftvector[k][2]==h):
                                cv2.rectangle(self.img,(self.shiftvector[k][3], self.shiftvector[k][4]),(self.shiftvector[k][3]+self.blocksize, self.shiftvector[k][4]+self.blocksize), (255), -1)
                                cv2.rectangle(self.img, (self.shiftvector[k][5], self.shiftvector[k][6]),(self.shiftvector[k][5] + self.blocksize, self.shiftvector[k][6] + self.blocksize), (255), -1)
        cv2.imshow("sonuc",self.img)


    def dct_of_img(self):

        for r in range(0, self.height-self.blocksize, 1):
            for c in range(0, self.width-self.blocksize,1):

                block = self.img[r:r + self.blocksize, c:c + self.blocksize]
                imf = np.float32(block)
                dct = cv2.dct(imf)      # block block dst uyguluyoruz
                dct =  np.round(dct/16).astype(int)


                # QUANTIZATION_MAT_10 = np.array([[80, 60, 50, 80, 120, 200, 255, 255], [55, 60, 70, 95, 130, 255, 255,255],
                #                              [70, 65, 80, 120, 200, 255, 255, 255], [70, 85, 110, 145, 255, 255,255,255],
                #                              [90, 110, 185,  255, 255,255,255,255], [120, 175, 255, 255,255,255, 255,255],
                #                              [255, 255,255,255, 255,255,255,255], [255, 255,255,255, 255,255,255,255]])
                QUANTIZATION_MAT_50 = np.array([[16, 11, 10, 16, 24, 40, 51, 61], [12, 12, 14, 19, 26, 58, 60, 55],
                                             [14, 13, 16, 24, 40, 57, 69, 56], [14, 17, 22, 29, 51, 87, 80, 62],
                                             [18, 22, 37, 56, 68, 109, 103, 77], [24, 35, 55, 64, 81, 104, 113, 92],
                                             [49, 64, 78, 87, 103, 121, 120, 101], [72, 92, 95, 98, 112, 100, 103, 99]])

                QUANTIZATION_MAT_90 = np.array([[3, 2, 2, 3, 5, 8, 10, 12], [2, 2, 3, 4, 5, 12, 12, 11],
                                               [3, 3, 3, 5 ,8, 11, 14, 11], [3, 3, 4, 6, 10, 17, 16, 12],
                                               [4, 4, 7, 11, 14, 22, 21, 15], [5, 7, 11, 13, 16, 12, 23, 18],
                                               [10, 13, 16, 17, 21, 24, 24, 21], [14, 18, 19, 20, 22, 20, 20, 20]])

                # QUANTIZATION_MAT_50_16 = np.array([[2*16, 2.5*11, 2.5*10, 2.5*16,2.5*24,2.5*40,2.5*51,2.5*61,1,1,1,1,1,1,1,1],
                #                                    [2.5*12,2.5*12,2.5*14,2.5*19,2.5*26,2.5*58,2.5*60,2.5*55, 1,1,1,1,1,1,1,1],
                #                                    [2.5*14,2.5*13,2.5*16,2.5*24,2.5*40,2.5*57,2.5*69,2.5*56, 1,1,1,1,1,1,1,1],
                #                                    [2.5*14,2.5*17,2.5*22,2.5*29,2.5*51,2.5*87,2.5*80,2.5*62, 1,1,1,1,1,1,1,1],
                #                                    [2.5*18,2.5*22,2.5*37,2.5*56,2.5*68,2.5*109,2.5*103,2.5*77, 1,1,1,1,1,1,1,1],
                #                                    [2.5*24,2.5*35,2.5*55,2.5*64,2.5*81,2.5*104,2.5*113,2.5*92, 1,1,1,1,1,1,1,1],
                #                                    [2.5*49,2.5*64,2.5*78,2.5*87,2.5*103,2.5*121,2.5*120,2.5*101, 1,1,1,1,1,1,1,1],
                #                                    [2.5*72,2.5*92,2.5*95,2.5*98,2.5*112,2.5*100,2.5*103,2.5*99, 1,1,1,1,1,1,1,1],
                #                                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                #                                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                #                                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                #                                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                #                                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                #                                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                #                                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                #                                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])


                # dct donusumu quantalama matrisine bolerek sıkıstırırız iliskilere baktigimiz icin buna gerek olmayabilir..
                #dct= np.round(np.divide(dct, QUANTIZATION_MAT_90)).astype(int)
                self.significant_part_extraction(self.zigzag(dct),c,r)



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

    def significant_part_extraction(self,vector,x,y):

        # 1x64 boyutundaki vectorden sadece alcak freans yani anlamli kismini cikarmak icin belirlenen(16) degere kadar del islemi yapilir.
        del vector[self.sizeof_vector:(self.blocksize*self.blocksize)]
        vector.append(x)  # blogun baslangıc kordinatının x noktası vektorun sonuna ekleniyor
        vector.append(y)  # aynı sekilde y noktası ekleniyor
        # her block sonucunu vector listemize atiyoruz.
        self.block_vector.append(vector)


    def lexicographically_sort_of_vectors(self,):
        #sutun siralaması oldugu icin ters cevirip siralamamiz lazim
        #ayni zamanda son iki yani ters cevirince ilk iki satirida koordinat bilgimiz var bunları sıralamicaz.
        self.block_vector=np.array(self.block_vector)
        self.block_vector= self.block_vector[np.lexsort(np.rot90(self.block_vector)[2:(self.sizeof_vector + 1) + 2 , :])]


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
        if (vector2[0]>=vector1[0]):
            if(vector2[1]>=vector1[1]):
                z = 0
            else:
                z = 1

        if (vector1[0] > vector2[0]):
            if (vector1[1] >= vector2[1]):
                z = 0
            else:
                z = 1
        self.hough_space[r][c][z] +=1
        vector=[]
        vector.append(c)
        vector.append(r)
        vector.append(z)
        vector.append(vector1[0])
        vector.append(vector1[1])
        vector.append(vector2[0])
        vector.append(vector2[1])
        self.shiftvector.append(vector)  # sirasiyla hough kordinati , 1.vektorun kordinati, 2.vektorun kordinati


    def oklid(self,vector1,vector2,size):
        sum=0
        for i in range(size):
            sum += (vector2[i]-vector1[i])**2

        return sqrt(sum)
