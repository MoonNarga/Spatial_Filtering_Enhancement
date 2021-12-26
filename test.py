import imageProcess
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

ip = imageProcess.imageProcess()

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

if __name__ == '__main__':
    src = "./flowerGray.jpg"
    test = test()
    test.dftTest(src)