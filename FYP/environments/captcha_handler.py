import cv2
import numpy as np
import thinning as th

file_name = raw_input('Enter file name: ')
#print(file_name)
greyscale_captcha = cv2.imread(file_name, 0)
#print(greyscale_captcha[0][0])
_ ,binarized_captcha = cv2.threshold(greyscale_captcha,127,255,cv2.THRESH_BINARY)
#print(binarized_captcha)
cv2.imwrite('greyscale_captcha.jpg', greyscale_captcha)
cv2.imwrite('binarized_captcha.jpg', binarized_captcha)

sobel_horizontal_edge_filter = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
sobel_vertical_edge_filter = np.array([[1, 0, -1],[2, 0, -2], [1, 0, -1]])

horizontal_edge_strength = th.MyConvolve(binarized_captcha, sobel_horizontal_edge_filter)
vertical_edge_strength = th.MyConvolve(binarized_captcha, sobel_vertical_edge_filter)
print(horizontal_edge_strength)
print(vertical_edge_strength)
edge_detected_array = th.combine_edges(horizontal_edge_strength, vertical_edge_strength, 'sobel')
thinned_edge = th.edge_thinning(edge_detected_array)
cv2.imwrite('edge_captcha.jpg', edge_detected_array)
cv2.imwrite('thinned_edge.jpg', thinned_edge)