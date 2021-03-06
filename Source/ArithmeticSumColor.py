import math
import numpy
import collections
from PIL import Image

from ImageDecoder import ImageDecoder
from Unification import Unification
from ImageHelper import ImageHelper
from Commons import Commons

class ArithmeticSumColor(object):
    def __init__(self, firstPath, secondPath, imageType):
        self.firstDecoder = ImageDecoder(firstPath, imageType)
        self.secondDecoder = ImageDecoder(secondPath, imageType)
        self.imageType = imageType

    # Ex3.1
    def sumWithConst(self, constValue):
        print('Sum color image {} with const {}'.format(self.firstDecoder.name, constValue))
        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()

        maxSum = float(numpy.amax(numpy.add(image.astype(numpy.uint32), constValue)))
        maxValue = float(numpy.iinfo(image.dtype).max)
        scaleFactor = (maxSum - maxValue) / maxValue if maxSum > maxValue else 0

        result = numpy.ones((height, width, 3), numpy.uint8)
        for h in range(height):
            for w in range(width):
                R = (image[h, w, 0] - (image[h, w, 0] * scaleFactor)) + (constValue - (constValue * scaleFactor))
                G = (image[h, w, 1] - (image[h, w, 1] * scaleFactor)) + (constValue - (constValue * scaleFactor))
                B = (image[h, w, 2] - (image[h, w, 2] * scaleFactor)) + (constValue - (constValue * scaleFactor))
                result[h, w] = [numpy.ceil(R), numpy.ceil(G), numpy.ceil(B)]

        ImageHelper.Save(result, self.imageType, 'sum-color-const', False, self.firstDecoder, None, constValue)
        result = Commons.Normalization(image, result)
        ImageHelper.Save(result, self.imageType, 'sum-color-const', True, self.firstDecoder, None, constValue)
        
    # Ex3.1
    def sumImages(self):
        print('Sum color image {} with image {}'.format(self.firstDecoder.name, self.secondDecoder.name))
        unification = Unification(self.firstDecoder.name, self.secondDecoder.name, self.imageType)
        firstImage, secondImage = unification.colorUnification()
        width, height = firstImage.shape[0], firstImage.shape[1]
        
        maxSum = float(
            numpy.amax(
                numpy.add(firstImage.astype(numpy.uint32), 
                          secondImage.astype(numpy.uint32))))
        maxValue = float(numpy.iinfo(firstImage.dtype).max)
        scaleFactor = (maxSum - maxValue) / maxValue if maxSum > maxValue else 0
        
        result = numpy.ones((height, width, 3), numpy.uint8)
        for h in range(height):
            for w in range(width):
                R = (firstImage[h, w, 0] - (firstImage[h, w, 0] * scaleFactor)) + (secondImage[h, w, 0] - (secondImage[h, w, 0] * scaleFactor))
                G = (firstImage[h, w, 1] - (firstImage[h, w, 1] * scaleFactor)) + (secondImage[h, w, 1] - (secondImage[h, w, 1] * scaleFactor))
                B = (firstImage[h, w, 2] - (firstImage[h, w, 2] * scaleFactor)) + (secondImage[h, w, 2] - (secondImage[h, w, 2] * scaleFactor))
                result[h, w] =  [numpy.ceil(R), numpy.ceil(G), numpy.ceil(B)]

        ImageHelper.Save(result, self.imageType, 'sum-color-images', False, self.firstDecoder, self.secondDecoder)
        result = Commons.Normalization(firstImage, result)
        ImageHelper.Save(result, self.imageType, 'sum-color-images', True, self.firstDecoder, self.secondDecoder)

    # Ex3.2
    def multiplyWithConst(self, constValue):
        print('Multiply color image {} with const {}'.format(self.firstDecoder.name, constValue))
        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()
        maxValue = numpy.iinfo(image.dtype).max
        result = numpy.ones((height, width, 3), numpy.uint8)
        
        for h in range(height):
            for w in range(width):
                R = image[h, w, 0] * constValue
                G = image[h, w, 1] * constValue
                B = image[h, w, 2] * constValue
                result[h, w, 0] = R if R <= maxValue else maxValue
                result[h, w, 1] = G if G <= maxValue else maxValue
                result[h, w, 2] = B if B <= maxValue else maxValue

        ImageHelper.Save(result, self.imageType, 'multiply-color-const', False, self.firstDecoder, None, constValue)
        result = Commons.Normalization(image, result)
        ImageHelper.Save(result, self.imageType, 'multiply-color-const', True, self.firstDecoder, None, constValue)

    # Ex3.2
    def multiplyImages(self):
        print('Multiply color image {} with image {}'.format(self.firstDecoder.name, self.secondDecoder.name))
        unification = Unification(self.firstDecoder.name, self.secondDecoder.name, self.imageType)
        firstImage, secondImage = unification.colorUnification()
        width, height = firstImage.shape[0], firstImage.shape[1]
        
        maxValue = float(numpy.iinfo(firstImage.dtype).max)
        result = numpy.ones((height, width, 3), numpy.uint8)
        for h in range(height):
            for w in range(width):
                result[h, w, 0] = int(firstImage[h, w, 0]) * int(secondImage[h, w, 0]) / maxValue
                result[h, w, 1] = int(firstImage[h, w, 1]) * int(secondImage[h, w, 1]) / maxValue
                result[h, w, 2] = int(firstImage[h, w, 2]) * int(secondImage[h, w, 2]) / maxValue

        ImageHelper.Save(result, self.imageType, 'multiply-color-images', False, self.firstDecoder, self.secondDecoder)
        result = Commons.Normalization(firstImage, result)
        ImageHelper.Save(result, self.imageType, 'multiply-color-images', True, self.firstDecoder, self.secondDecoder)

    # Ex3.3
    def blendImages(self, ratio):
        print('Blending color image {} with image {} and ratio {}'.format(self.firstDecoder.name, self.secondDecoder.name, ratio))
        if ratio < 0 or ratio > 1.0:
            raise ValueError('ratio is wrong')

        unification = Unification(self.firstDecoder.name, self.secondDecoder.name, self.imageType)
        firstImage = unification.scaleUpColor(self.firstDecoder)
        secondImage = unification.scaleUpColor(self.secondDecoder)
        width, height = firstImage.shape[0], firstImage.shape[1]
        
        result = numpy.ones((height, width, 3), numpy.uint8)
        for h in range(height):
            for w in range(width):
                result[h, w, 0] = ratio * firstImage[h, w, 0] + (1 - ratio) * secondImage[h, w, 0]
                result[h, w, 1] = ratio * firstImage[h, w, 1] + (1 - ratio) * secondImage[h, w, 1]
                result[h, w, 2] = ratio * firstImage[h, w, 2] + (1 - ratio) * secondImage[h, w, 2]

        ImageHelper.Save(result, self.imageType, 'blend-color-images', False, self.firstDecoder, None, ratio)

    # Ex3.4
    def powerFirstImage(self, powerIndex):
        print('Power color image {} with image {} and index {}'.format(self.firstDecoder.name, self.secondDecoder.name, powerIndex))
        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()
        
        maxValue = float(numpy.iinfo(image.dtype).max)
        result = numpy.ones((height, width, 3), numpy.uint32)
        for h in range(height):
            for w in range(width):
                result[h, w, 0] = 0 if result[h,w,0] == 0 else 255 * math.pow(image[h,w,0]/maxValue, powerIndex)
                result[h, w, 1] = 0 if result[h,w, 1] == 0 else 255 * math.pow(image[h,w,1]/maxValue, powerIndex)
                result[h, w, 2] = 0 if result[h,w,2 == 0] else 255 * math.pow(image[h,w,2]/maxValue, powerIndex)

        ImageHelper.Save(result.astype(numpy.uint8), self.imageType, 'power-color', False, self.firstDecoder, None, powerIndex)
        result = Commons.Normalization(image, result)
        ImageHelper.Save(result.astype(numpy.uint8), self.imageType, 'power-color', True, self.firstDecoder, None, powerIndex)

    # Ex3.5
    def divideWithConst(self, constValue):
        print('Divide color image {} with const {}'.format(self.firstDecoder.name, constValue))
        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()
        maxValue = numpy.iinfo(image.dtype).max
        result = numpy.ones((height, width, 3), numpy.uint8)
        
        for h in range(height):
            for w in range(width):
                result[h, w, 0] = image[h, w, 0] / constValue
                result[h, w, 1] = image[h, w, 1] / constValue
                result[h, w, 2] = image[h, w, 2] / constValue

        ImageHelper.Save(result, self.imageType, 'divide-color-const', False, self.firstDecoder, None, constValue)
        result = Commons.Normalization(image, result)
        ImageHelper.Save(result, self.imageType, 'divide-color-const', True, self.firstDecoder, None, constValue)

    # Ex3.5
    def divideImages(self):
        print('Divide color image {} with image {}'.format(self.firstDecoder.name, self.secondDecoder.name))
        unification = Unification(self.firstDecoder.name, self.secondDecoder.name, self.imageType)
        firstImage, secondImage = unification.colorUnification()
        width, height = firstImage.shape[0], firstImage.shape[1]
        
        maxValue = float(numpy.iinfo(firstImage.dtype).max)
        sumR = float(
            numpy.amax(
                numpy.add(firstImage[:, :, 0].astype(numpy.uint32), 
                          secondImage[:, :, 0].astype(numpy.uint32))))
        sumG = float(
            numpy.amax(
                numpy.add(firstImage[:, :, 1].astype(numpy.uint32), 
                          secondImage[:, :, 1].astype(numpy.uint32))))
        sumB = float(
            numpy.amax(
                numpy.add(firstImage[:, :, 2].astype(numpy.uint32), 
                          secondImage[:, :, 2].astype(numpy.uint32))))
        scaleR = maxValue / sumR
        scaleG = maxValue / sumG
        scaleB = maxValue / sumB

        result = numpy.ones((height, width, 3), numpy.uint8)
        for h in range(height):
            for w in range(width):
                R = (int(firstImage[h, w, 0]) + int(secondImage[h, w, 0])) * scaleR
                G = (int(firstImage[h, w, 1]) + int(secondImage[h, w, 1])) * scaleG
                B = (int(firstImage[h, w, 2]) + int(secondImage[h, w, 2])) * scaleB
                result[h, w, 0] = numpy.ceil(R)
                result[h, w, 1] = numpy.ceil(G)
                result[h, w, 2] = numpy.ceil(B)

        ImageHelper.Save(result, self.imageType, 'divide-color-images', False, self.firstDecoder, self.secondDecoder)
        result = Commons.Normalization(firstImage, result)
        ImageHelper.Save(result, self.imageType, 'divide-color-images', True, self.firstDecoder, self.secondDecoder)

    # Ex3.6
    def rootFirstImage(self, rootIndex):
        print('Root color image {} with image {} and index {}'.format(self.firstDecoder.name, self.secondDecoder.name, rootIndex))
        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()
        
        maxValue = float(numpy.iinfo(image.dtype).max)
        result = numpy.ones((height, width, 3), numpy.uint32)
        for h in range(height):
            for w in range(width):
                result[h, w, 0] = image[h, w, 0]**(1.0/rootIndex)
                result[h, w, 1] = image[h, w, 1]**(1.0/rootIndex)
                result[h, w, 2] = image[h, w, 2]**(1.0/rootIndex)

        ImageHelper.Save(result.astype(numpy.uint8), self.imageType, 'root-color', False, self.firstDecoder, None, rootIndex)
        result = Commons.Normalization(image, result)
        ImageHelper.Save(result.astype(numpy.uint8), self.imageType, 'root-color', True, self.firstDecoder, None, rootIndex)

    # Ex3.7
    def logarithm(self):
        print('Logarithm color image {}'.format(self.firstDecoder.name))
        height, width = self.firstDecoder.height, self.firstDecoder.width
        image = self.firstDecoder.getPixels()
        
        maxValue = float(numpy.iinfo(image.dtype).max)
        maxR = numpy.amax(image[:, :, 0])
        maxG = numpy.amax(image[:, :, 1])
        maxB = numpy.amax(image[:, :, 2])
        result = numpy.ones((height, width, 3), numpy.uint32)
        for h in range(height):
            for w in range(width):
                result[h, w, 0] = maxValue * (math.log10(1 + image[h, w, 0]) / math.log10(1 + maxR))
                result[h, w, 1] = maxValue * (math.log10(1 + image[h, w, 1]) / math.log10(1 + maxG))
                result[h, w, 2] = maxValue * (math.log10(1 + image[h, w, 2]) / math.log10(1 + maxB))

        ImageHelper.Save(result.astype(numpy.uint8), self.imageType, 'logarithm-color', False, self.firstDecoder)