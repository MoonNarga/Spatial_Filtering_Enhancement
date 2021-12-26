import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

class imageProcess():

    def sharpen(self):
        src = cv.imread("./flowerGray.jpg", cv.IMREAD_GRAYSCALE)
        window1 = cv.namedWindow('1', cv.WINDOW_NORMAL)
        window2 = cv.namedWindow('2', cv.WINDOW_NORMAL)
        window3 = cv.namedWindow('3', cv.WINDOW_NORMAL)
        window4 = cv.namedWindow('4', cv.WINDOW_NORMAL)
        kernal1 = np.array([[-2, -1, 0], [-1, 0, 1], [0, 1, 2]], np.float64)
        kernal2 = np.array([[0, -1, -2], [1, 0, -1], [2, 1, 0]], np.float64)
        dst1 = cv.filter2D(src, -1, kernal1)
        dst2 = cv.filter2D(src, -1, kernal2)
        dst3 = dst1 + dst2
        cv.imshow('1', src)
        cv.imshow('2', dst1)
        cv.imshow('3', dst2)
        cv.imshow('4', dst3)
        cv.waitKey(0)

    def DFTtrans(self):
        src = cv.imread("./flowerGray.jpg", cv.IMREAD_GRAYSCALE)
        dft = cv.dft(np.float32(src), flags = cv.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)
        magnitude_spectrum = 20*np.log(cv.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
        plt.subplot(121),plt.imshow(src, cmap = 'gray')
        plt.title('Input Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
        plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
        plt.show()

if __name__ == '__main__':
    ip = imageProcess()
    ip.DFTtrans()