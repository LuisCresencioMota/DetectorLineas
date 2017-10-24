#importing some useful packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

import moviepy.editor as mpy
import tempfile

#%matplotlib inline
import os
path = ("./test_images/")
os.listdir(path)
#os.listdir("./test_images/")
# Import everything needed to edit/save/watch video clips
from moviepy.editor import VideoFileClip
from IPython.display import HTML
def process_image(image):    
    # NOTE: The output you return should be a color image (3 channel) for processing video below
    # TODO: put your pipeline here,
    gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    #print('This image is ', type(image), ' with dimensions', image.shape)
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
    vertices = np.array([[(0,imshape[0]),(imshape[1]*1/4, imshape[0]*9/16), (imshape[1]*3/4, imshape[0]*9/16), (imshape[1],imshape[0])]], dtype=np.int32)
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    edges = cv2.bitwise_and(edges, mask)
    #plt.imshow(edges)
    #plt.show()
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
            slope = (float (y2)- float(y1))/(float(x2)-float(x1))
            #print(slope)
            if ( slope > slope_threshold or slope < -slope_threshold):
                cv2.line(image2show,(x1,y1),(x2,y2),(0,0,255),3)
                cv2.line(edges,(x1,y1),(x2,y2),(0,0,0),3)



    result = image2show
    return result
    # Create a "color" binary image to combine with line image
    #color_edges = np.dstack((edges, edges, edges)) 
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
    lines_dotted = []
    lines_dotted = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)
    # Iterate over the output "lines" and draw lines on a blank image
    if not lines_dotted is None:
        #print(lines_dotted)
        #if true
        for line in lines_dotted:
            for x1,y1,x2,y2 in line:
                slope = (y2-y1)/(x2-x1)
                #print slope
                if ( slope > slope_threshold or slope < -slope_threshold):
                    cv2.line(image2show,(x1,y1),(x2,y2),(0,0,0),3)
    # Create a "color" binary image to combine with line image
    #color_edges = np.dstack((edges, edges, edges)) 
    # Draw the lines on the edge image
    #lines_edges = cv2.addWeighted(color_edges, 0.8, line_image, 1, 0) 
    #plt.imshow(image2show)
    #plt.show()
    # you should return the final output (image where lines are drawn on lanes)
    result = image2show
    return result
white_output = './test_videos_output/challenge_.mp4'
## To speed up the testing process you may want to try your pipeline on a shorter subclip of the video
## To do so add .subclip(start_second,end_second) to the end of the line below
## Where start_second and end_second are integer values representing the start and end of the subclip
## You may also uncomment the following line for a subclip of the first 5 seconds
##clip1 = VideoFileClip("test_videos/solidWhiteRight.mp4").subclip(0,5)
clip1 = VideoFileClip("./test_videos/challenge.mp4")
white_clip = clip1.fl_image(process_image) #NOTE: this function expects color images!!
white_clip.write_videofile(white_output, audio=False)
