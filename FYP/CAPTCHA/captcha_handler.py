import cv2
import numpy as np
import pytesseract
from PIL import Image

file_name = 'new_captcha.png'

"""
read the image
"""
greyscale_captcha = cv2.imread(file_name, 0)

"""
binarization
"""
_ ,binarized_captcha = cv2.threshold(greyscale_captcha,127,255,cv2.THRESH_BINARY)

cv2.imwrite('greyscale_captcha.jpg', greyscale_captcha)
cv2.imwrite('binarized_captcha.jpg', binarized_captcha)
image = Image.open('binarized_captcha.jpg')

image_height = binarized_captcha.shape[0]
image_width = binarized_captcha.shape[1]

"""
character recognition for image as a whole
"""
print pytesseract.image_to_string(Image.open('binarized_captcha.jpg'))

"""
segmentation
"""
character_width = 47
starting_index = 24
first_char = image.crop((starting_index, 0, starting_index + character_width, image_height))
starting_index = starting_index + character_width
second_char = image.crop((starting_index, 0, starting_index + character_width, image_height))
starting_index = starting_index + character_width
third_char = image.crop((starting_index, 0, starting_index + character_width, image_height))
starting_index = starting_index + character_width
fourth_char = image.crop((starting_index, 0, starting_index + character_width, image_height))
starting_index = starting_index + character_width
fifth_char = image.crop((starting_index, 0, starting_index + character_width, image_height))

first_char.save('first_char.jpg')
second_char.save('second_char.jpg')
third_char.save('third_char.jpg')
fourth_char.save('fourth_char.jpg')
fifth_char.save('fifth_char.jpg')

"""
character recognition for each character image
"""
print pytesseract.image_to_string(Image.open('first_char.jpg'), config="-psm 10")
print pytesseract.image_to_string(Image.open('second_char.jpg'), config="-psm 10")
print pytesseract.image_to_string(Image.open('third_char.jpg'), config="-psm 10")
print pytesseract.image_to_string(Image.open('fourth_char.jpg'), config="-psm 10")
print pytesseract.image_to_string(Image.open('fifth_char.jpg'), config="-psm 10")
