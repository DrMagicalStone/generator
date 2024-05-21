from PIL import Image, ImageFont, ImageDraw, ImageTransform, ImageFilter

from shapely import Point, MultiPoint, transform

from numpy import matrix, array, cross, asarray, maximum, minimum, concatenate, identity

from random import randint, normalvariate, random

from math import pi, cos, sin

from character import generateRandomString
from util import clamp
from TextInfo import TextInfo

font = ImageFont.truetype("MadokaRunes.ttf", 32)

def generateMultilineText() -> str:
    text = ""

    for i in range(0, randint(1, 4)):
        text = text + generateRandomString(int(clamp(normalvariate(mu=32, sigma=8), 16, 48))).strip() + "\n"
    
    return text.strip()

def makeTextRect() -> tuple[Image.Image, str]:
    text = generateMultilineText()
    
    scaler = ImageDraw.Draw(Image.new("1", (0, 0), 0))

    (_, _, textWidth, textHeight) = scaler.multiline_textbbox((0, 0), text, font=font)
    
    im = Image.new("1", (textWidth, textHeight), )
    
    drawer = ImageDraw.Draw(im)

    drawer.multiline_text((0, 0), text, font=font, fill=1, align="center")
    
    return im, text

def trapezoide(im: Image.Image) -> Image.Image:
    
    size = im.size
    
    a = array([0, 0])
    b = array([0, size[1]])
    c = array([size[0], size[1]])
    d = array([size[0], 0])
    
    fixB = b[1] * 1 / 4 * random()
    
    angleB = random() * pi / 2
    
    b = b + array([-cos(angleB), sin(angleB)]) * fixB
    
    fixCX = c[0] * 1 / 4 * random()
    fixCY = c[1] * 1 / 4 * random()
    
    angleC = random() * pi / 2
    
    c = c + array([cos(angleC) * fixCX, sin(angleC) * fixCY])
    
    fixD = d[0] * 1 / 4 * random()
    
    angleD = random() * pi / 2
    
    d = d + array([cos(angleD), -sin(angleD)]) * fixD
    
    return im.transform(size=im.size, method=ImageTransform.QuadTransform((a[0], a[1], b[0], b[1], c[0], c[1], d[0], d[1])), fillcolor=(0, 0, 0, 0))

def rotateRect(im: Image.Image) -> tuple[Image.Image, tuple[Point, Point, Point, Point]] :
    rad = random() * 2 * pi
    rotationLinear = matrix([[cos(rad), sin(rad)], [-sin(rad), cos(rad)]]).T
    size = im.size
    length = int((size[0] ** 2 + size[1] ** 2) ** (1 / 2))
    
    center = matrix([[length, length]]).T / 2
    centerAffine = matrix([[length, length, 2]]).T / 2
    
    resizedIm = Image.new("1", (length, length), 0)
    
    resizedIm.paste(box=((length - size[0]) // 2, (length - size[1]) // 2), im = im, mask=im)
    
    rotationOffset = (identity(2) - rotationLinear) * center
    
    rotationAffine = concatenate((concatenate((rotationLinear, rotationOffset), axis=1), matrix([[0, 0, 1]])), axis=0)
    
    rotatedIm = resizedIm.transform(size=resizedIm.size, method=ImageTransform.AffineTransform(tuple(asarray(rotationAffine.flatten("C"))[0][0: 6])))
    
    rotationAffineI = rotationAffine.I
    
    diagonalH = matrix([[size[0], -size[1], 0]]).T / 2
    a = rotationAffineI * (centerAffine - maximum(diagonalH, -diagonalH))
    b = rotationAffineI * (centerAffine - diagonalH)
    c = rotationAffineI * (centerAffine + maximum(diagonalH, -diagonalH))
    d = rotationAffineI * (centerAffine + diagonalH)
    
    return (rotatedIm, (Point(tuple(asarray(a.T)[0][0: 2])), Point(tuple(asarray(b.T)[0][0: 2])), Point(tuple(asarray(c.T)[0][0: 2])), Point(tuple(asarray(d.T)[0][0: 2]))))

def perspectiveRect(im: Image.Image) -> Image.Image :
    yaw = random() * 0.00001 * 2 * pi
    pitch = (random() - 1 / 2) * 0.00001 * pi
    roll = random() * 0.1 * 2 * pi
    
    xAxis = array([cos(yaw), - sin(pitch) * sin(yaw), cos(pitch) * sin(yaw)])
    
    yAxis = array([0, cos(pitch), sin(pitch)])
    
    zAxis = cross(xAxis, yAxis)
    
    p = matrix([xAxis, yAxis, zAxis]).transpose()
    rotationOfRoll = matrix([[cos(roll), sin(roll), 0], [-sin(roll), cos(roll), 0], [0, 0, 1]]).transpose()
    
    
    rotation = p * rotationOfRoll * p
    
    fix = matrix([[im.width / 2, im.height / 2, 1]]).transpose()
    
    projector = matrix([0, 0, 1])
    
    a = - 2 * fix + projector.transpose()
    b = matrix([[2 * fix.item(0, 0), 0, 1]]).transpose()
    c = 2 * fix - projector.transpose()
    d = matrix([[0, 2 * fix.item(1, 0), 1]]).transpose()
    
    a = rotation * a
    b = rotation * b
    c = rotation * c
    d = rotation * d
    
    a = a / (projector * a)
    b = b / (projector * b)
    c = c / (projector * c)
    d = d / (projector * d)
    
    box = (a.item(0, 0), a.item(1, 0), a.item(0, 0), a.item(1, 0))
    box = (min(b.item(0, 0), box[0]), min(b.item(1, 0), box[1]), max(b.item(0, 0), box[2]), max(b.item(1, 0), box[3]))
    box = (min(c.item(0, 0), box[0]), min(c.item(1, 0), box[1]), max(c.item(0, 0), box[2]), max(c.item(1, 0), box[3]))
    box = (min(d.item(0, 0), box[0]), min(d.item(1, 0), box[1]), max(d.item(0, 0), box[2]), max(d.item(1, 0), box[3]))
    
    print(fix)
    
    fix = fix - matrix([[box[0], box[1], 0]]).transpose()
    
    print(fix)
    
    rotatedFix = rotation * fix
    
    fix = fix - (rotatedFix / (projector * rotatedFix))
    
    print(fix)
    
    rotationTranspose = rotation.transpose()
    
    resizedIm = Image.new("1", (int(box[2] - box[0]), int(box[3] - box[1])), 1)
    
    print(im.size, resizedIm.size)
    
    resizedIm.paste(im=im, mask=im, box=(int(-box[0]), int(-box[1])))
    
    matrixTransfer = matrix([asarray(rotationTranspose[0])[0], asarray(rotationTranspose[1])[0], asarray(rotationTranspose[2] + fix.transpose())[0]]).transpose()
    
    return resizedIm.transform(size=resizedIm.size, method=ImageTransform.PerspectiveTransform((matrixTransfer.item(0, 0), matrixTransfer.item(0, 1), matrixTransfer.item(0, 2), matrixTransfer.item(1, 0), matrixTransfer.item(1, 1), matrixTransfer.item(1, 2), matrixTransfer.item(2, 0), matrixTransfer.item(2, 1))), fillcolor=(0, 0, 0, 0))



def makeSample() -> tuple[Image.Image, list[TextInfo]]:
    mainIm = Image.new("1", (1920, 1080), 0)
    sizeOfMain = mainIm.size
    textInfos: list[TextInfo] = []

    for i in range(0, 5):
        (original, text) = makeTextRect()
        bended = trapezoide(original)
        (rotated, theBorder) = rotateRect(bended)
        bounds = MultiPoint(theBorder).bounds
        offset = Point((random() * (sizeOfMain[0] - bounds[2]), random() * (sizeOfMain[1] - bounds[3])))
        info = TextInfo(text, tuple(transform(theBorder, lambda p: p + [offset.x, offset.y])))
        for previousInfo in textInfos:
            if (previousInfo.intersects(info)):
                break
        else:
            textInfos.append(info)
            mainIm.paste(mask=rotated, im=rotated, box=(int(offset.x), int(offset.y)))
    
    return (mainIm, textInfos)
        
if (__name__ == "__main__"):
    (im, infos) = makeSample()
    print(infos)
    im.show()