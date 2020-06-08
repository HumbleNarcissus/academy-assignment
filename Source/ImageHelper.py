import numpy
from PIL import Image

from ImageDecoder import ImageDecoder

class ImageHelper(object):
    @staticmethod
    def Save(result, imageType, operationName, isNorm, firstDecoder, secondDecoder = None, idValue = None):
        imageName = ImageHelper._composeName(operationName, isNorm, firstDecoder, secondDecoder, idValue)
        img = Image.fromarray(result, mode = imageType)
        img.save('Resources/result/' + imageName + '.png')
        
    @staticmethod
    def _composeName(operationName, isNorm, firstDecoder, secondDecoder = None, idValue = None):
        imageName = operationName + '-'
        imageName += firstDecoder.name.split('/')[1].split('.')[0]
        if secondDecoder != None:
            imageName += '-'
            imageName += secondDecoder.name.split('/')[1].split('.')[0]

        if idValue != None:
            imageName += '-'
            if isinstance(idValue, float):
                imageName += str(int(idValue*10))
            elif type(idValue) is tuple:
                imageName += str(idValue).replace(" ", "")
            else:
                imageName += str(idValue)

        if isNorm:
            imageName += '-norm'

        return imageName