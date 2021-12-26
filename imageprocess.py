import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

class imageProcess():

    def newKernelFromList(self, klist):
        return np.array(klist, np.float64)

    def sharpen(self, src, klist):
        kernel = imageProcess.newKernelFromList(self, klist)
        dst = cv.filter2D(src, -1, kernel)
        return dst

    def dft(self, src):
        dft = cv.dft(np.float32(src), flags = cv.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)
        return dft_shift

    def magnitude_spectrum(self, src):
        dft_shift = imageProcess.dft(self, src)
        magnitude_spectrum = 20*np.log(cv.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
        return magnitude_spectrum

    def addMask(self, src, mode):
        dft_shift = imageProcess.dft(self, src)
        row, col = src.shape
        crow = int(row / 2)
        ccol = int(col / 2)
        if mode == 'high':
            mask = np.ones((row, col, 2), np.uint8)
            mask[crow-25:crow+25, ccol-25:ccol+25] = 0
        if mode == 'low':
            mask = np.zeros((row, col, 2), np.uint8)
            mask[crow-10:crow+10, ccol-10:ccol+10] = 1
        fshift = dft_shift*mask
        f_ishift = np.fft.ifftshift(fshift)
        img_back = cv.idft(f_ishift)
        img_back = cv.magnitude(img_back[:,:,0],img_back[:,:,1])
        return img_back