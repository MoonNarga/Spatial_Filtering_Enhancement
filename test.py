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
        plt.subplot(221), plt.imshow(src, cmap='gray')
        plt.title('Input Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(222), plt.imshow(dst1, cmap='gray')
        plt.title('Sharpen1'), plt.xticks([]), plt.yticks([])
        plt.subplot(223), plt.imshow(dst2, cmap='gray')
        plt.title('Sharpen2'), plt.xticks([]), plt.yticks([])
        plt.subplot(224), plt.imshow(dst, cmap='gray')
        plt.title('SharpenSum'), plt.xticks([]), plt.yticks([])
        plt.show()

    def dftTest(self, src):
        src = cv.imread(src, cv.IMREAD_GRAYSCALE)
        magnitude_spectrum = ip.magnitude_spectrum(src)
        high_back = ip.addMask(src, 'high')
        low_back = ip.addMask(src, 'low')
        plt.subplot(221), plt.imshow(src, cmap='gray')
        plt.title('Input Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(222), plt.imshow(magnitude_spectrum, cmap='gray')
        plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
        plt.subplot(223), plt.imshow(high_back, cmap='gray')
        plt.title('Magnitude Spectrum_high'), plt.xticks([]), plt.yticks([])
        plt.subplot(224), plt.imshow(low_back, cmap='gray')
        plt.title('Magnitude Spectrum_low'), plt.xticks([]), plt.yticks([])
        plt.show()

    def dctTest(self, src):
        src = cv.imread(src, cv.IMREAD_GRAYSCALE)
        quantization_table = np.zeros((8, 8), dtype=np.float64)
        quantization_table[:3, :3] = [[1, 1, 1], [1, 1, 0], [1, 0, 0]]
        dct, dctTrans, imgTrans = ip.dct(src, quantization_table)
        plt.subplot(221), plt.imshow(src, cmap='gray')
        plt.title('src'), plt.xticks([]), plt.yticks([])
        plt.subplot(222), plt.imshow(dct, cmap='gray')
        plt.title('dct'), plt.xticks([]), plt.yticks([])
        plt.subplot(223), plt.imshow(dctTrans, cmap='gray')
        plt.title('dctTrans'), plt.xticks([]), plt.yticks([])
        plt.subplot(224), plt.imshow(imgTrans, cmap='gray')
        plt.title('imgTrans'), plt.xticks([]), plt.yticks([])
        plt.show()
    
    def encodeTest(self, src):
        src = cv.imread(src, cv.IMREAD_GRAYSCALE)
        runlength, imgcompress, row, col = ip.encode(src)
        imgdecode = ip.decode(runlength, row, col)
        plt.subplot(131), plt.imshow(src, cmap='gray')
        plt.title('Src'), plt.xticks([]), plt.yticks([])
        plt.subplot(132), plt.imshow(imgcompress, cmap='gray')
        plt.title('Imgcompress'), plt.xticks([]), plt.yticks([])
        plt.subplot(133), plt.imshow(imgdecode, cmap='gray')
        plt.title('Imgdecode'), plt.xticks([]), plt.yticks([])
        plt.show()

    def jpegTest(self, src):
        src = cv.imread(src, cv.IMREAD_GRAYSCALE)
        quantization_table = np.zeros((8, 8), dtype=np.float64)
        quantization_table[:3, :3] = [[1, 1, 1], [1, 1, 0], [1, 0, 0]]
        stretching, row, col, htable, wtable = ip.savelikeJPEG(src, quantization_table)
        imgload = ip.loadlikeJPEG(stretching, row, col, htable, wtable)
        plt.subplot(121), plt.imshow(src, cmap='gray')
        plt.title('ImgSrc'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(imgload, cmap='gray')
        plt.title('Imgload'), plt.xticks([]), plt.yticks([])
        plt.show()

    def segmentationTest(self, src):
        src = cv.imread(src, cv.IMREAD_GRAYSCALE)
        seg01 = ip.segmentation01(src)
        plt.subplot(121), plt.imshow(seg01, cmap='gray')
        plt.title('Segmentation01'), plt.xticks([]), plt.yticks([])
        segmin = ip.segmentationMin(src)
        plt.subplot(122), plt.imshow(segmin, cmap='gray')
        plt.title('SegmentationMin'), plt.xticks([]), plt.yticks([])
        plt.show()


if __name__ == '__main__':
    src = "./flowerGray.jpg"
    test = test()
    test.segmentationTest(src)