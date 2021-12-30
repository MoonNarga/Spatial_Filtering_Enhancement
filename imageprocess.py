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
        dft = cv.dft(np.float32(src), flags=cv.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)
        return dft_shift

    def magnitude_spectrum(self, src):
        dft_shift = imageProcess.dft(self, src)
        magnitude_spectrum = 20 * \
            np.log(cv.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))
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
        img_back = cv.magnitude(img_back[:, :, 0], img_back[:, :, 1])
        return img_back

    def dct(self, src, quantization_table):
        imgTrans = np.ndarray(src.shape, dtype=np.float64)
        dct = np.ndarray(src.shape, dtype=np.float64)
        dctTrans = np.ndarray(src.shape, dtype=np.float64)
        row, col = src.shape
        htable, wtable = quantization_table.shape
        rrow, ccol = int(row / htable), int(col / wtable)
        for i in range(0, rrow):
            for j in range(0, ccol):
                block = src[htable*i:htable*(i+1), wtable*j:wtable*(j+1)]
                Yb = cv.dct(block.astype(np.float64))
                dct[htable*i:htable*(i+1), wtable*j:wtable*(j+1)] = Yb
                Yb *= quantization_table
                dctTrans[htable*i:htable*(i+1), wtable*j:wtable*(j+1)] = Yb
                iblock = cv.idct(Yb)
                imgTrans[htable*i:htable*(i+1), wtable*j:wtable*(j+1)] = iblock
        return dct, dctTrans, imgTrans

    def encode(self, src):
        row, col = src.shape
        stretching = np.ndarray((row*col), dtype=np.uint8)
        predict = np.ndarray((row*col), dtype=np.int16)
        for i in range(0, row):
            for j in range(0, col):
                stretching[i*col+j] = src[i][j]
        bef3, bef2, bef1 = 0, 0, 0
        for i in range(0, row):
            for j in range(0, col):
                predict[i*col+j] = np.int16(stretching[i*col+j]) - np.int16(
                    bef1 + np.int16(((np.float32(bef1) - np.float32(bef3)) / 2)))
                bef3, bef2, bef1 = bef2, bef1, stretching[i*col+j]
        imgcompress = np.empty(shape=src.shape, dtype=np.uint8)
        for i in range(0, row):
            for j in range(0, col):
                if (predict[i*col+j] < 0):
                    imgcompress[i][j] = 0
                else:
                    imgcompress[i][j] = predict[i*col+j]
        runlength = np.empty((row*col), dtype=np.int16)
        codelen = 0
        temp = predict[0]
        count = 0
        for i in range(0, row*col):
            if (predict[i] == temp):
                count += 1
                if (count == 127 or i == row*col):
                    code = np.int16(0)
                    code |= (count << 9)
                    if (temp < 0):
                        code |= 0x0100
                    code |= abs(temp)
                    runlength[codelen] = code
                    codelen += 1
                    count = 0
            else:
                code = np.int16(0)
                code |= (count << 9)
                if (temp < 0):
                    code |= 0x0100
                code |= abs(temp)
                runlength[codelen] = code
                codelen += 1
                if (i == row*col):
                    code = np.int16(0)
                    code |= (count << 9)
                    if (predict[i] < 0):
                        code |= 0x0100
                    code |= abs(predict[i])
                    runlength[codelen] = code
                    codelen += 1
                else:
                    temp = predict[i]
                    count = 1
        return runlength, imgcompress, row, col

    def decode(self, runlength, row, col):
        imgdecode = np.ndarray((row*col), dtype=np.uint8)
        bef3, bef2, bef1 = np.uint8(0), np.uint8(0), np.uint8(0)
        pos = 0
        length = runlength.shape[0]
        for i in range(0, length):
            code = np.int16(runlength[i])
            count = np.int16(code >> 9)
            value = np.int16(code & 0x00ff)
            sign = np.int16((code & 0x0100) >> 8)
            if (sign == 1):
                value = -value
            for i in range(0, count):
                imgdecode[pos] = np.int16(
                    value + bef1 + np.int16((np.float32(bef1) - np.float32(bef3)) / 2))
                bef3, bef2, bef1 = bef2, bef1, imgdecode[pos]
                pos += 1
        imgdecode = imgdecode.reshape((row, col))
        return imgdecode

    def savelikeJPEG(self, src, quantization_table):
        dct, _, _ = self.dct(src, quantization_table)
        row, col = src.shape
        htable, wtable = quantization_table.shape
        rrow, ccol = int(row / htable), int(col / wtable)
        stretching = np.ndarray((rrow*ccol, htable*wtable), dtype=np.float64)
        pos = 0
        for i in range(0, rrow):
            for j in range(0, ccol):
                dctblock = dct[htable*i:htable*(i+1), wtable*j:wtable*(j+1)]
                ii, jj = 0, 0
                pnum = 0
                while (ii < htable and jj < wtable):
                    stretching[pos][pnum] = dctblock[ii][jj]
                    pnum += 1
                    if ((ii + jj) % 2 == 0):
                        if (ii == 0):
                            if (jj == wtable - 1):
                                ii += 1
                            else:
                                jj += 1
                        elif (jj == wtable - 1):
                            ii += 1
                        else:
                            ii -= 1
                            jj += 1
                    else:
                        if (jj == 0):
                            if (ii == htable - 1):
                                jj += 1
                            else:
                                ii += 1
                        elif (ii == htable - 1):
                            jj += 1
                        else:
                            ii += 1
                            jj -= 1
                pos += 1
        return stretching, row, col, htable, wtable

    def loadlikeJPEG(self, stretching, row, col, htable, wtable):
        blocknum, pix = stretching.shape
        imgload = np.ndarray((row, col), dtype=np.float64)
        dctblock = np.ndarray((htable, wtable), dtype=np.float64)
        rrow, ccol = int(row / htable), int(col / wtable)
        for i in range(0, rrow):
            for j in range(0, ccol):
                ii, jj = 0, 0
                for p in range(0, pix):
                    dctblock[ii][jj] = stretching[i*ccol+j][p]
                    if ((ii + jj) % 2 == 0):
                        if (ii == 0):
                            if (jj == wtable - 1):
                                ii += 1
                            else:
                                jj += 1
                        elif (jj == wtable - 1):
                            ii += 1
                        else:
                            ii -= 1
                            jj += 1
                    else:
                        if (jj == 0):
                            if (ii == htable - 1):
                                jj += 1
                            else:
                                ii += 1
                        elif (ii == htable - 1):
                            jj += 1
                        else:
                            ii += 1
                            jj -= 1
                imgload[htable*i:htable *
                        (i+1), wtable*j:wtable*(j+1)] = cv.idct(dctblock)
        return imgload

    def segmentation01(self, src):
        row, col = src.shape
        for i in range(0, row):
            for j in range(0, col):
                if (src[i][j] < 150):
                    src[i][j] = 0
                else:
                    src[i][j] = 255
        return src

    def segmentationMin(self, src):
        graySum = np.zeros((256), dtype=np.uint16)
        row, col = src.shape
        for i in range(0, row):
            for j in range(0, col):
                graySum[src[i][j]] += 1
        minlist = [0]
        maxgray = 0
        for i in range(1, 255):
            if (i == 127):
                minlist.append(127)
                continue
            if (graySum[i] < graySum[i-1] and graySum[i] > graySum[i-1]):
                minlist.append(i)
            if (graySum[i]>maxgray):
                maxgray = i
        minlist.append(255)
        n = len(minlist)
        if (n == 2):
            minlist[1] = maxgray
            minlist.append(255)
        print(minlist)
        for i in range(0, row):
            for j in range(0, col):
                for k in range(1, n):
                    if (src[i][j] >= minlist[k-1] and src[i][j]<= minlist[k]):
                        src[i][j] = np.uint8((minlist[k-1] + minlist[k]) / 2)
        return src