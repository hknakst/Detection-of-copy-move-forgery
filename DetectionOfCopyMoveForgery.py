import cv2
import numpy as np


class DetectionofCopyMoveForgery:

    def __init__(self,img,height,width,blocksize_r,blocksize_c):
        self.img = img
        self.height=height
        self.width=width
        self.blocksize_r = blocksize_r
        self.blocksize_c = blocksize_c
        self.vector=[]



    def dct_of_img(self):

        for r in range(0, self.height - self.blocksize_r, self.blocksize_r):
            for c in range(0, self.width - self.blocksize_c, self.blocksize_c):
                block = self.img[r:r + self.blocksize_r, c:c + self.blocksize_c]
                imf = (block) / 255.0  #0 ile 1 arasında normalize ediyoruz
                dst = np.round(cv2.dct(imf),6)      # block block dst uyguluyoruz ve virgülden sonraki 6. basamağı yumarlıyoruz
                self.vector=self.zigzag(dst)
                self.vector.append(c)   #blogun baslangıc kordinatının x noktası vektorun sonuna ekleniyor
                self.vector.append(r)   #aynı sekilde y noktası ekleniyor
                print(self.vector)
                print("asd")
                # cv2.imshow("sonuc",block)
                # cv2.waitKey(0)

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

    def lexicographically_sort_of_vectors(self):
        pass

    def correlation_of_vectors(self,threshold):
        pass

