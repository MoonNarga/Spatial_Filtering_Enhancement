import imageprocess
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

ip = imageprocess.imageProcess()

class test():
    
    def sharpenTest(self, src):
        src = cv.imread(src, cv.IMREAD_GRAYSCALE)
        dst1 = ip.sharpen(src, [[-2, -1, 0], [-1, 0, 1], [0, 1, 2]])
        dst2 = ip.sharpen(src, [[0, -1, -2], [1, 0, -1], [2, 1, 0]])
        dst = dst1 + dst2
        plt.subplot(221),plt.imshow(src, cmap = 'gray')
        plt.title('Input Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(222),plt.imshow(dst1, cmap = 'gray')
        plt.title('Sharpen1'), plt.xticks([]), plt.yticks([])
        plt.subplot(223),plt.imshow(dst2, cmap = 'gray')
        plt.title('Sharpen2'), plt.xticks([]), plt.yticks([])
        plt.subplot(224),plt.imshow(dst, cmap = 'gray')
        plt.title('SharpenSum'), plt.xticks([]), plt.yticks([])
        plt.show()

    def dftTest(self, src):
        src = cv.imread(src, cv.IMREAD_GRAYSCALE)
        magnitude_spectrum = ip.magnitude_spectrum(src)
        high_back = ip.addMask(src, 'high')
        low_back = ip.addMask(src, 'low')
        plt.subplot(221),plt.imshow(src, cmap = 'gray')
        plt.title('Input Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(222),plt.imshow(magnitude_spectrum, cmap = 'gray')
        plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
        plt.subplot(223),plt.imshow(high_back, cmap = 'gray')
        plt.title('Magnitude Spectrum_high'), plt.xticks([]), plt.yticks([])
        plt.subplot(224),plt.imshow(low_back, cmap = 'gray')
        plt.title('Magnitude Spectrum_low'), plt.xticks([]), plt.yticks([])
        plt.show()

    def dctTest(self, src):
        src = cv.imread(src, cv.IMREAD_GRAYSCALE)
        imgTrans = np.ndarray(src.shape,dtype=np.float64)
        dct = np.ndarray(src.shape,dtype=np.float64)
        dctTrans = np.ndarray(src.shape,dtype=np.float64)
        row, col = src.shape
        rrow, ccol = int(row / 8), int(col / 8)
        mask = np.zeros((8, 8), dtype=np.float64)
        mask[:3, :3] = [[1, 1, 1], [1, 1, 0], [1, 0, 0]]
        for i in range(0, rrow):
            for j in range(0, ccol):
                block = src[8*i:8*(i+1), 8*j:8*(j+1)]
                # plt.subplot(131),plt.imshow(block, cmap = 'gray')
                # plt.title('Input block'), plt.xticks([]), plt.yticks([])
                Yb = cv.dct(block.astype(np.float64))
                dct[8*i:8*(i+1), 8*j:8*(j+1)] = Yb
                Yb *= mask
                dctTrans[8*i:8*(i+1), 8*j:8*(j+1)] = Yb
                # plt.subplot(132),plt.imshow(Yb, cmap = 'gray')
                # plt.title('dct'), plt.xticks([]), plt.yticks([])
                iblock = cv.idct(Yb)
                imgTrans[8*i:8*(i+1), 8*j:8*(j+1)] = iblock
                # plt.subplot(133),plt.imshow(iblock, cmap = 'gray')
                # plt.title('idct'), plt.xticks([]), plt.yticks([])
                # plt.show()
        plt.subplot(221),plt.imshow(src, cmap='gray')
        plt.title('src'), plt.xticks([]), plt.yticks([])
        plt.subplot(222),plt.imshow(dct, cmap='gray')
        plt.title('dct'), plt.xticks([]), plt.yticks([])
        plt.subplot(223),plt.imshow(dctTrans, cmap='gray')
        plt.title('dctTrans'), plt.xticks([]), plt.yticks([])
        plt.subplot(224),plt.imshow(imgTrans, cmap='gray')
        plt.title('imgTrans'), plt.xticks([]), plt.yticks([])
        plt.show()


if __name__ == '__main__':
    src = "./flowerGray.jpg"
    test = test()
    test.dctTest(src)