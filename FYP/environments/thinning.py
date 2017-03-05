import numpy as np
import numpy.linalg as la
import cv2

def MyConvolve(img, ff):
    
    convoluted_array = np.zeros(img.shape)

    rows_for_img = len(img[:,0])
    columns_for_img = len(img[0,:])
    ff = np.fliplr(ff)
    ff = np.flipud(ff)
    """
    convoluted_array[0][0] = [0.0, 0.0, 0.0]
    convoluted_array[0][columns_for_img-1] = [0.0, 0.0, 0.0]
    convoluted_array[rows_for_img-1][0] = [0.0, 0.0, 0.0]
    convoluted_array[rows_for_img-1][columns_for_img-1] = [0.0, 0.0, 0.0]
    """
    for k in range(1, rows_for_img-1):
        for h in range(1, columns_for_img-1):

            convolution_val = (ff[0][0]*img[k-1][h-1]) + (ff[0][1]*img[k-1][h]) + (ff[0][2]*img[k-1][h+1]) + (ff[1][0]*img[k][h-1]) + (ff[1][2]*img[k][h+1]) + (ff[2][0]*img[k+1][h-1]) + (ff[2][1]*img[k+1][h]) + (ff[2][2]*img[k+1][h+1])
            convoluted_array[k][h] = convolution_val

    return convoluted_array


def combine_edges(horizontal_edge_strength, vertical_edge_strength, filter_function):

    edge_detected_array = np.zeros(horizontal_edge_strength.shape)

    rows_for_img = len(horizontal_edge_strength[:,0])
    columns_for_img = len(horizontal_edge_strength[0,:])

    if filter_function.lower() == 'prewitt':
        first_val = 255 * 3
        squared = np.square(first_val)
        double = squared * 2
        normalization_factor = np.sqrt(double)

    elif filter_function.lower() == 'sobel':
        first_val = 255 * 4
        squared = np.square(first_val)
        double = squared * 2
        normalization_factor = np.sqrt(double)  

    for i in range(rows_for_img):
        for j in range(columns_for_img):
            g_y = horizontal_edge_strength[i][j]
            g_x = vertical_edge_strength[i][j]

            addition_of_squares = np.square(g_y) + np.square(g_x)
            square_root = np.sqrt(addition_of_squares)
            normalized = (square_root / normalization_factor)*255.0


            edge_detected_array[i][j] = normalized
    return edge_detected_array      


def edge_thinning(edge_detected_array):
    rows_for_img = len(edge_detected_array[:,0])
    columns_for_img = len(edge_detected_array[0,:])
    thinned_edge = np.zeros(edge_detected_array.shape)

    for i in range(1, rows_for_img - 1):
        for j in range(1, columns_for_img - 1):
            current_pixel_val = edge_detected_array[i][j]
            # left_pixel_val = edge_detected_array[i][j-1]
            # right_pixel_val = edge_detected_array[i][j+1]
            up_pixel_val = edge_detected_array[i-1][j]
            down_pixel_val = edge_detected_array[i+1][j]

            #max_value_horizontal = max(current_pixel_val, left_pixel_val, right_pixel_val)
            max_value_vertical = max(current_pixel_val, up_pixel_val, down_pixel_val)
            if current_pixel_val == max_value_vertical:
                thinned_edge[i][j] = edge_detected_array[i][j]
            else:
                thinned_edge[i][j] = 0.0
                # up_pixel_val = edge_detected_array[i-1][j]
                # down_pixel_val = edge_detected_array[i+1][j]

                # max_value_vertical = max(current_pixel_val, up_pixel_val, down_pixel_val)

                # if current_pixel_val == max_value_vertical:
                #     thinned_edge[i][j] = edge_detected_array[i][j]
                # else:
                #     #thinned_edge[i][j] = [0.0, 0.0, 0.0]
                #     thinned_edge[i][j] = 0.0
    return thinned_edge