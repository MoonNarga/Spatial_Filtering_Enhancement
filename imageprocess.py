import cv2 as cv
import numpy as np

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

if __name__ == '__main__':
    ip = imageProcess()
    ip.sharpen()