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
        imgTrans = np.ndarray(src.shape, dtype=np.float64)
        dct = np.ndarray(src.shape, dtype=np.float64)
        dctTrans = np.ndarray(src.shape, dtype=np.float64)
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
        plt.subplot(221), plt.imshow(src, cmap='gray')
        plt.title('src'), plt.xticks([]), plt.yticks([])
        plt.subplot(222), plt.imshow(dct, cmap='gray')
        plt.title('dct'), plt.xticks([]), plt.yticks([])
        plt.subplot(223), plt.imshow(dctTrans, cmap='gray')
        plt.title('dctTrans'), plt.xticks([]), plt.yticks([])
        plt.subplot(224), plt.imshow(imgTrans, cmap='gray')
        plt.title('imgTrans'), plt.xticks([]), plt.yticks([])
        plt.show()

    def encode(self, src):
        src = cv.imread(src, cv.IMREAD_GRAYSCALE)
        src = src[:256, :256]
        row, col = src.shape
        stretching = np.ndarray((row*col), dtype=np.uint8)
        predict = np.ndarray((row*col), dtype=np.int16)
        for i in range(0, row):
            for j in range(0, col):
                stretching[i*col+j] = src[i][j]
        bef3, bef2, bef1 = 0, 0, 0
        for i in range(0, row):
            for j in range(0, col):
                predict[i*col+j] = np.int16(stretching[i*col+j]) - (np.float32(bef1 )+ (np.float32(bef1) - np.float32(bef3)) / 2)
                bef3, bef2, bef1 = bef2, bef1, stretching[i*col+j]
        imgcompress = np.empty(shape=src.shape, dtype=np.uint8)
        for i in range(0, row):
            for j in range(0, col):
                if (predict[i*col+j] < 0):
                    imgcompress[i][j] = 0
                else:
                    imgcompress[i][j] = predict[i*col+j]
        runlength = np.empty(shape=(0), dtype=np.int16)
        temp = predict[0]
        count = 1
        flag = False
        for i in range(1, row*col):
            if (predict[i] != temp):
                code = np.int16(0)
                code |= (count << 9)
                if (temp < 0):
                    code |= 0x0100
                code |= abs(temp)
                flag = True
            else:
                count += 1
            if (count == 127):
                code = np.int16(0)
                code |= (count << 9)
                if (temp < 0):
                    code |= 0x0100
                code |= abs(temp)
                flag = True
            if (flag == True):
                if (i != row*col):


    def segmentation(self, src):
        dict = {}
        img = cv.imread(src)
        cv.imshow("origin", img)
        dict['origin'] = img
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        dict['gray'] = gray
        ret, thresh = cv.threshold(
            gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
        dict['thresh'] = thresh

        # 去掉噪音
        kernel = np.ones((3, 3), np.uint8)
        opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=2)
        dict['opening'] = opening

        # 寻找确定的背景
        sure_bg = cv.dilate(opening, kernel, iterations=3)
        dict['sure_bg'] = sure_bg

        # 寻找确定的前景区域
        dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
        ret, sure_fg = cv.threshold(
            dist_transform, 0.7 * dist_transform.max(), 255, 0)
        dict['dist_transform'] = dist_transform
        dict['sure_fg'] = sure_fg

        # 用背景减前景，得到不确定的区域
        sure_fg = np.uint8(sure_fg)
        unknown = cv.subtract(sure_bg, sure_fg)
        dict['unknown'] = unknown

        # 创建标记（它是一个与原始图像大小相同的数组，但数据类型为 int32）并标记其中的区域。
        # 标记背景、不确定对象（默认背景为0，其他为1）
        ret, markers = cv.connectedComponents(sure_fg)
        dict['markers'] = markers

        # 对所有标签加1，将得到背景为1
        markers = markers + 1

        # 标记未知区域为0
        markers[unknown == 255] = 0

        # 应用分水岭算法，然后标记图像，边界区域将被标记为-1
        markers = cv.watershed(img, markers)
        img[markers == -1] = [255, 0, 0]
        cv.imshow("watershed res", img)
        cv.waitKey(0)
        cv.destroyAllWindows()
        dict['marker boundaries'] = markers
        dict['res'] = img

        size = len(dict)
        print(size, '\n')
        for i, key in enumerate(dict):
            print(i + 1, key, len(list(dict[key].shape)))
            plt.subplot(3, 4, i + 1)
            # 由于matplot需要RGB以显示彩色图，而OpenCV是用BGR来表示彩色图的
            if (len(list(dict[key].shape)) > 2):
                # 为确保正确显示RGB图，进行颜色空间转换
                plt.imshow(cv.cvtColor(dict[key], cv.COLOR_BGR2RGB))
            else:
                plt.imshow(dict[key])
            plt.title(key)  # 图片的标题
            plt.xticks([])  # 去掉x轴的刻度
            plt.yticks([])  # 去掉y轴的刻度
        plt.show()


if __name__ == '__main__':
    src = "./lena.jpg"
    test = test()
    test.encode(src)
