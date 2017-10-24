import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
# Read in grayscale the image
image = mpimg.imread('ejemplo.jpg')

gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)

print('This image is ', type(image), ' with dimensions', image.shape)

# First, do a gaussian filtering to remove noise
kernel_size = 9;
blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)

# Then, do Canny edge detection
low_threshold = 50
high_threshold = 150
edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

# Next we'll create a masked edges image using cv2.fillPoly()
mask = np.zeros_like(edges)   
ignore_mask_color = 255   

# This time we are defining a four sided polygon to mask
imshape = image.shape

vertices = np.array([[(0,imshape[0]),(imshape[1/4], imshape[0]*9/16), (imshape[3/4], imshape[0]*9/16), (imshape[1],imshape[0])]], dtype=np.int32)
cv2.fillPoly(mask, vertices, ignore_mask_color)
edges = cv2.bitwise_and(edges, mask)

plt.imshow(edges)
plt.show()

slope_threshold = 0.5;

# Define the Hough transform parameters for large lines

# Make a blank the same size as our image to draw on
rho = 2 # distance resolution in pixels of the Hough grid
theta = np.pi/180 # angular resolution in radians of the Hough grid
threshold = 70    # minimum number of votes (intersections in Hough grid cell)
min_line_length = 50 #minimum number of pixels making up a line
max_line_gap = 5    # maximum gap in pixels between connectable line segments
#line_image = np.copy(image)*0 # creating a blank to draw lines on

# Run Hough on edge detected image
# Output "lines" is an array containing endpoints of detected line segments
lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)

# Iterate over the output "lines" and draw lines on a blank image
#remove detected lines from edges

image2show = np.copy(image)
for line in lines:
    for x1,y1,x2,y2 in line:

        slope = (y2-y1)/(x2-x1)
        #print(slope)
        if ( slope > slope_threshold or slope < -slope_threshold):
            cv2.line(image2show,(x1,y1),(x2,y2),(0,0,255),3)
            cv2.line(edges,(x1,y1),(x2,y2),(0,0,0),3)

# Define the Hough transform parameters for dotted lines

# Make a blank the same size as our image to draw on
rho = 2 # distance resolution in pixels of the Hough grid
theta = np.pi/180 # angular resolution in radians of the Hough grid
threshold = 50    # minimum number of votes (intersections in Hough grid cell)
min_line_length = 100 #minimum number of pixels making up a line
max_line_gap = 50    # maximum gap in pixels between connectable line segments
#line_image = np.copy(image)*0 # creating a blank to draw lines on

# Run Hough on edge detected image
# Output "lines" is an array containing endpoints of detected line segments
lines_dotted = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)
# Iterate over the output "lines" and draw lines on a blank image
for line in lines_dotted:
    for x1,y1,x2,y2 in line:
        slope = (float (y2)- float(y1))/(float(x2)-float(x1))
        #print(slope)
        if ( slope > slope_threshold or slope < -slope_threshold):
            cv2.line(image2show,(x1,y1),(x2,y2),(0,255,255),3)

# Draw the lines on the edge image
#lines_edges = cv2.addWeighted(color_edges, 0.8, line_image, 1, 0) 
plt.imshow(image2show)
plt.show()

