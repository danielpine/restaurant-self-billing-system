from PIL import Image, ImageDraw, ImageFont
import base64
import sys
import cv2
import cv2
import numpy as np
sys.path.append("..")
sys.path.append(".")


def empty(a):
    pass


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(
                        imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(
                        imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(
                        imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(
                    imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(
                    imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


items = {
    'rect': '方形菜品',
    'circle': '圆形菜品',
    'eclipse': '椭圆菜品'
}


def getContours(img, imgContour, config, plates, texts):
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    minArea = config['minArea']
    maxArea = config['maxArea']
    for cnt in contours:
        # area = cv2.contourArea(cnt)
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.03 * peri, True)
        # compute the center of the contour
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        x, y, w, h = cv2.boundingRect(approx)
        area = w*h
        if area > minArea and area < maxArea and w/h < 2 and w/h > 0.5:
            # i=0
            # for p in approx:
            #     cv2.circle(imgContour, (p[0,0], p[0,1]), 5, (0, 0, 255), -1)
            #     cv2.putText(imgContour, str(i), (p[0,0], p[0,1]), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
            #     i+=1
            shape = detectShape((cX, cY), approx)
            # draw the center of the shape on the image
            # cv2.circle(imgContour, (cX, cY), 3, (255, 255, 255), -1)
            # cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 2)
            cv2.rectangle(imgContour, (x, y),
                          (x + w, y + h), (255, 144, 24), 1)
            cv2.rectangle(imgContour, (x, y),
                          (x + 70, y + 20), (255, 144, 24), -1)
            # cv2.putText(imgContour, "P: " + str(len(approx)), (x +
            #             20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 1)
            # cv2.putText(imgContour, "A: " + str(int(area)), (x + 20,
            #             y + 42), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 1)
            # cv2.putText(imgContour, "S: " + shape, (x + 20,
            #             y + 65), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
            # cv2.putText(imgContour,  items[shape], (x + 10, y + 10), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)
            texts.append([items[shape], (x+5, y+2)])
            plates.append(shape)
    return plates


def putText(img, text, xy):
    # 判断图片是否为ndarray格式，转为RGB图片
    if (isinstance(img, np.ndarray)):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    # 参数依次为 字体、字体大小、编码
    fontStyle = ImageFont.truetype("font/simsun.ttc", 16, encoding="utf-8")
    # 参数依次为位置、文本、颜色、字体
    draw.text((xy[0], xy[1]), text, font=fontStyle, fill='white')
    # 转回BGR图片、ndarray格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def detectShape(center, ponits):
    if len(ponits) <= 5:
        return 'rect'
    else:
        # compute the distance from every points to the center
        ds = [((p[0][0]-center[0])**2+(p[0][1]-center[1])**2)**0.5 for p in ponits]
        mins = min(ds)
        maxs = max(ds)
        # compute the delta
        delta = (maxs-mins)*2/(maxs+mins)
        # print(delta)
        if delta > 0.2:
            return 'eclipse'
        else:
            return 'circle'


def image_to_base64(image_np):
    image = cv2.imencode('.jpg', image_np)[1]
    image_code = str(base64.b64encode(image))[2:-1]
    return image_code


def base64_to_image(base64_code):
    # base64解码
    img_data = base64.b64decode(base64_code)
    # 转换为np数组
    img_array = np.fromstring(img_data, np.uint8)
    # 转换成opencv可用格式
    img = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
    return img


def detect(message):
    base64_code = message['image']
    config = message['config']
    img = base64_to_image(base64_code)
    imgContour = img.copy()
    imgBlur = cv2.GaussianBlur(
        img, (config['gaussianSize'], config['gaussianSize']), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    threshold1 = config['threshold1']
    threshold2 = config['threshold2']
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    kernel = np.ones((config['kernelSize'], config['kernelSize']))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
    plates = []
    texts = []
    getContours(imgDil, imgContour, config, plates, texts)
    # imgStack = stackImages(config['backScale']/100,
    #                        ([img, imgCanny],  [imgDil, imgContour]))
    for i in texts:
        imgContour = putText(imgContour, i[0], i[1])
    imgStack = stackImages(config['backScale']/100,  ([imgContour]))
    return {
        'plates': plates,
        'image': image_to_base64(imgStack)
    }
