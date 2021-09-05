import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', help='single channel', default='./red.tif')
parser.add_argument('--output', help='output path', default='./dark_removed.tif')
args = parser.parse_args()

img = cv2.imread(args.input)
grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
h, w = grey.shape
MAX = 255

edges = cv2.Canny(grey, 40, 115)
lines = cv2.HoughLinesP(edges,1,np.pi / 225, 10, minLineLength=1, maxLineGap=100)

# mask used to separate dark part of the image
blank = np.zeros((h, w), dtype=img.dtype)

# draw the edges from canny on blank
for line in lines:
    x1,y1,x2,y2 = line[0]
    cv2.line(blank,(x1,y1),(x2,y2),(255,255,255),1)

# generate column indices, to find the first occurence of non-zero value in each row
indices = np.indices((h, w))[1]
edge_indices = indices.copy()
edge_indices[blank==0] = h * w
first_edges = np.amin(edge_indices, axis=1)

# fill the mask with white until first occurence of edges and 0 elsewhere
before_edge = indices.T <= first_edges.T
blank[before_edge.T] = 255
blank[np.logical_not(before_edge.T)] = 0

# separate the dark part
shadow = cv2.bitwise_and(img, img, mask=blank)
shadow = cv2.cvtColor(shadow, cv2.COLOR_BGR2GRAY)

# brighten the dark part
gamma = 0.66

table = np.empty((MAX), np.uint8)
for i in range(MAX):
    table[i] = np.clip(pow(i / (MAX - 1), gamma) * (MAX - 1), 0, MAX - 1)

shadow = table[shadow]

# replace dark part in the original image with brighter one
grey[before_edge.T] = shadow[before_edge.T]

cv2.imwrite(args.output, grey)
