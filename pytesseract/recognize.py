'''
Created on 2022年6月6日

@author: b
'''
import cv2
import pytesseract
try:
    from PIL import Image
except ImportError:
    import Image

print(pytesseract.get_languages(config=''))

image = cv2.imread("./num.png")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

text = pytesseract.image_to_string(binary, lang='chi_sim+eng')

print("识别结果", text)