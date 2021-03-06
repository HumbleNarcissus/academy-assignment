import numpy
import collections
from PIL import Image

from ImageDecoder import ImageDecoder
from ImageHelper import ImageHelper

class Unification(object):
    def __init__(self, firstPath, secondPath, imageType):
        self.firstDecoder = ImageDecoder(firstPath, imageType)
        self.secondDecoder = ImageDecoder(secondPath, imageType)
        self.imageType = imageType
        self.maxHeight, self.maxWidth = self._findMaxSize()
        
    def _findMaxSize(self):
        self.maxHeight = max([self.firstDecoder.height, self.secondDecoder.height])
        self.maxWidth = max([self.firstDecoder.width, self.secondDecoder.width])
        print('max size: ' + str(self.maxWidth) + 'x' + str(self.maxHeight))
        return self.maxHeight, self.maxWidth

    # Ex1.1
    def geometricGray(self):
        firstResult, secondResult = self.grayUnification()
        ImageHelper.Save(firstResult.astype(numpy.uint8), self.imageType, 'geometric-gray', False, self.firstDecoder, self.secondDecoder)
        ImageHelper.Save(secondResult.astype(numpy.uint8), self.imageType, 'geometric-gray', False, self.secondDecoder, self.firstDecoder)

    def grayUnification(self):
        firstResult = numpy.zeros((self.maxHeight, self.maxWidth), numpy.uint8)
        width, height = self.firstDecoder.width, self.firstDecoder.height
        if width < self.maxWidth or height < self.maxHeight:
            startWidthIndex = int(round((self.maxWidth - width) / 2))
            startHeightIndex = int(round((self.maxHeight - height) / 2))
            pixelsBuffer = self.firstDecoder.getPixels()
            for h in range (0, height):
                for w in range (0, width):
                    firstResult[h + startHeightIndex, w + startWidthIndex] = pixelsBuffer[h, w]
        else:
            firstResult = self.firstDecoder.getPixels()
        
        secondResult = numpy.zeros((self.maxHeight, self.maxWidth), numpy.uint8)
        width, height = self.secondDecoder.width, self.secondDecoder.height
        if width < self.maxWidth or height < self.maxHeight:
            startWidthIndex = int(round((self.maxWidth - width) / 2))
            startHeightIndex = int(round((self.maxHeight - height) / 2))
            pixelsBuffer = self.secondDecoder.getPixels()
            for h in range (0, height):
                for w in range (0, width):
                    secondResult[h + startHeightIndex, w + startWidthIndex] = pixelsBuffer[h, w]
        else:
            secondResult = self.secondDecoder.getPixels()

        return firstResult, secondResult

    # Ex1.2
    def rasterGray(self):
        print('Raster gray unification for image {} and {}'.format(self.firstDecoder.name, self.secondDecoder.name))
        firstResult = self.scaleUpGray(self.firstDecoder)
        secondResult = self.scaleUpGray(self.secondDecoder)
        ImageHelper.Save(firstResult.astype(numpy.uint8), self.imageType, 'raster-gray', False, self.firstDecoder, self.secondDecoder)
        ImageHelper.Save(secondResult.astype(numpy.uint8), self.imageType, 'raster-gray', False, self.secondDecoder, self.firstDecoder)
        
    def scaleUpGray(self, decoder):
        width, height = decoder.width, decoder.height
        scaleFactoryW = float(self.maxWidth) / width
        scaleFactoryH = float(self.maxHeight) / height
        if width < self.maxWidth or height < self.maxHeight:
            pixelsBuffer = decoder.getPixels()
            result = numpy.zeros((self.maxHeight, self.maxWidth), numpy.uint8)
            # Fill values
            for h in range(height - 1):
                for w in range(width - 1):
                    if w%2 == 0:
                        result[int(scaleFactoryH * h), int(round(scaleFactoryW * w)) + 1] = pixelsBuffer[h, w]
                    if w%2 == 1:
                        result[int(round(scaleFactoryH * h)) + 1, int(scaleFactoryW * w)] = pixelsBuffer[h, w]
            # Interpolate
            self._interpolateGray(result)
            return result
        else: 
            return decoder.getPixels()
    
    def _interpolateGray(self, result):
        for h in range(self.maxHeight):
            for w in range(self.maxWidth):
                value = 0
                count = 0
                if result[h, w] == 0:
                    for hOff in range(-1, 2):
                        for wOff in range(-1, 2):
                            hSafe = h if ((h + hOff) > (self.maxHeight - 2)) | ((h + hOff) < 0) else (h + hOff)
                            wSafe = w if ((w + wOff) > (self.maxWidth - 2)) | ((w + wOff) < 0) else (w + wOff)
                            if result[hSafe, wSafe] != 0:
                                value += result[hSafe, wSafe]
                                count += 1
                    result[h, w] = value / count

    # Ex1.3
    def geometricColor(self):
        print('Geometric color unification for image {} and {}'.format(self.firstDecoder.name, self.secondDecoder.name))
        firstResult, secondResult = self.colorUnification()
        ImageHelper.Save(firstResult.astype(numpy.uint8), self.imageType, 'geometric-color', False, self.firstDecoder, self.secondDecoder)
        ImageHelper.Save(secondResult.astype(numpy.uint8), self.imageType, 'geometric-color', False, self.secondDecoder, self.firstDecoder)

    def colorUnification(self):
        width, height = self.firstDecoder.width, self.firstDecoder.height
        if width < self.maxWidth or height < self.maxHeight:
            firstResult = self._paintInMiddleColor(self.firstDecoder)
        else:
            firstResult = self.firstDecoder.getPixels()

        width, height = self.secondDecoder.width, self.secondDecoder.height
        if width < self.maxWidth or height < self.maxHeight:
            secondResult = self._paintInMiddleColor(self.secondDecoder)
        else:
            secondResult = self.secondDecoder.getPixels()

        return firstResult, secondResult

    def _paintInMiddleColor(self, decoder):
        result = numpy.full((self.maxHeight, self.maxWidth, 3), 0, numpy.uint8)
        # Copy smaller image to bigger
        width, height = decoder.width, decoder.height
        startWidthIndex = int(round((self.maxWidth - width) / 2))
        startHeightIndex = int(round((self.maxHeight - height) / 2))
        pixelsBuffer = decoder.getPixels()
        for h in range (0, height):
            for w in range (0, width):
                result[h + startHeightIndex, w + startWidthIndex] = pixelsBuffer[h, w]
        return result

    # Ex1.4
    def rasterColor(self):
        print('Raster color unification for image {} and {}'.format(self.firstDecoder.name, self.secondDecoder.name))
        firstResult = self.scaleUpColor(self.firstDecoder)
        secondResult = self.scaleUpColor(self.secondDecoder)
        ImageHelper.Save(firstResult.astype(numpy.uint8), self.imageType, 'raster-color', False, self.firstDecoder, self.secondDecoder)
        ImageHelper.Save(secondResult.astype(numpy.uint8), self.imageType, 'raster-color', False, self.secondDecoder, self.firstDecoder)

    def scaleUpColor(self, decoder):
        width, height = decoder.width, decoder.height
        scaleFactoryW = float(self.maxWidth) / width
        scaleFactoryH = float(self.maxHeight) / height
        if width < self.maxWidth or height < self.maxHeight:
            pixelsBuffer = decoder.getPixels()
            result = numpy.full((self.maxHeight, self.maxWidth, 3), 1, numpy.uint8)
            # Fill values
            for h in range(height):
                for w in range(width):
                    if w%2 == 0:
                        result[int(scaleFactoryH * h), int(round(scaleFactoryW * w)) + 1] = pixelsBuffer[h, w]
                    if w%2 == 1:
                        result[int(round(scaleFactoryH * h)) + 1, int(scaleFactoryW * w)] = pixelsBuffer[h, w]
            # Interpolate
            self._interpolateColor(result)
            return result;
        else: 
            return decoder.getPixels()

    def _interpolateColor(self, result):
        for h in range(self.maxHeight):
            for w in range(self.maxWidth):
                r, g, b = 0, 0, 0
                n = 0
                if (result[h, w][0] == 1) & (result[h, w][1] == 1) & (result[h, w][2] == 1):
                    for hOff in range(-1, 2):
                        for wOff in range(-1, 2):
                            hSafe = h if ((h + hOff) > (self.maxHeight - 2)) | ((h + hOff) < 0) else (h + hOff)
                            wSafe = w if ((w + wOff) > (self.maxWidth - 2)) | ((w + wOff) < 0) else (w + wOff)
                            if (result[hSafe, wSafe][0] > 1) | (result[hSafe, wSafe][1] > 1) | (result[hSafe, wSafe][2] > 1):
                                r += result[hSafe, wSafe][0]
                                g += result[hSafe, wSafe][1]
                                b += result[hSafe, wSafe][2]
                                n += 1
                    result[h, w] = (r/n, g/n, b/n)