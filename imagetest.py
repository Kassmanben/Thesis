import cv2
import numpy as np


def pixel_expand():
    y=0
    x = 0
    coordinates = []
    #Horizontal lines
    while y < imageHeight:
        diff_img = np.ediff1d(img[y])
        length = 0
        if np.max(diff_img) != 0:
            start = 0
            end = 0
            for index in range(len(diff_img)):
                if diff_img[index] == 0 and index != len(diff_img)-1:
                    #print(length,start, end)
                    length += 1
                    end += 1
                else:
                    if length > imageWidth/2.5:
                        coordinates.append([(start, y), (end, y)])
                    length = 0
                    start = index
                    end = index
                #print(start,end, length, diff_img[index])
        else:
            coordinates.append([(0, y), (imageWidth, y)])
        y+=1
        #Vertical Lines
    while x< imageWidth:
        diff_img = np.ediff1d(img.transpose()[x])
        length = 0
        if np.max(diff_img) != 0:
            start = 0
            end = 0
            for index in range(len(diff_img)):
                if diff_img[index] == 0 and index != len(diff_img)-1:
                    length += 1
                    end += 1
                else:
                    if length > imageHeight/4:
                        coordinates.append([(x, start), (x, end)])
                    length = 0
                    start = index
                    end = index
                #print(start,end, length, diff_img[index])
        else:
            coordinates.append([(x, 0), (x, imageHeight)])
        x+=1

    temp_list = []
    for l in range(len(coordinates)-1):
        line_diff1 = tuple(np.subtract(coordinates[l+1][0],coordinates[l][0]))
        line_diff2 = tuple(np.subtract(coordinates[l+1][1],coordinates[l][1]))
        #print(line_diff1, line_diff2)
        if line_diff1 in [(1,0),(0,1)] or line_diff2 in [(1,0),(0,1)]:
            temp_list.append(coordinates[l])
        else:
            #print(temp_list)
            shortest_length = (np.inf, np.inf)
            if len(temp_list)>20:
                for ci in range(len(temp_list)-1):
                    length_tuple = np.subtract(temp_list[ci][1],temp_list[ci][0])
                    if length_tuple[0] != 0 and length_tuple[0]<shortest_length[0]:
                        shortest_length = (length_tuple[0], 0)
                    elif length_tuple[1] != 0 and length_tuple[1]<shortest_length[1]:
                        shortest_length = (0 , length_tuple[1])
                for c in temp_list:
                    cv2.line(img, c[0], tuple(np.add(c[0], shortest_length)), 0, 1)
            temp_list = []
    if len(temp_list) > 20:
        for ci in range(len(temp_list) - 1):
            length_tuple = np.subtract(temp_list[ci][1], temp_list[ci][0])
            if length_tuple[0] != 0 and length_tuple[0] < shortest_length[0]:
                shortest_length = (length_tuple[0], 0)
            elif length_tuple[1] != 0 and length_tuple[1] < shortest_length[1]:
                shortest_length = (0, length_tuple[1])
        for c in temp_list:
            cv2.line(img, c[0], tuple(np.add(c[0], shortest_length)), 0, 1)

    cv2.imwrite('new_page2' + str(pg_num) + '.bmp', img)



def mark_whitespace(range_limit, img_matrix, orientation):
    coordinate = img_matrix.shape[1]  # Get image width/height depending on the matrix
    white = True
    for x in range(0, range_limit):
        if white and not np.array_equal(img_matrix[x], img_matrix[x - 1]):
            if orientation == "x":
                cv2.line(img, (0, x), (coordinate, x), 0, 1)
            else:
                cv2.line(img, (x, 0), (x, coordinate), 0, 1)
            white = False
        if not white and np.array_equal(img_matrix[x], img_matrix[x - 1]):
            if orientation == "x":
                cv2.line(img, (0, x), (coordinate, x), 0, 1)
            else:
                cv2.line(img, (x, 0), (x, coordinate), 0, 1)
    cv2.imwrite('new_page2' + str(pg_num) + '.jpg', img)
for x in range(1,6):
    pg_num = x
    img = cv2.imread('S_A2-' + str(pg_num) + '.png', 0)
    #img = cv2.imread('building.jpg', 0)
    imageWidth = img.shape[1]  # Get image width
    imageHeight = img.shape[0]
    pixel_expand()