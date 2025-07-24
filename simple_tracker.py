import cv2 as cv
import numpy as np
import time
from datetime import datetime

VIDEO_SOURCE = 0
#VIDEO_SOURCE = 'f-35.mp4'

MATCH_THRESHOLD = 0.6
TEMPLATE_SIZE = 100     # Template size in pixels 
MASK_SIZE = TEMPLATE_SIZE + 1
ROI_SIZE = TEMPLATE_SIZE * 2

# For points or pixel positions
X_AXIS = 0
Y_AXIS = 1

# Names for windows
MAIN_WINDOW_NAME = "Tracker"
MASK_WINDOW_NAME = "Mask"
ROI_WINDOW_NAME = "ROI"
CORR_WINDOW_NAME = "Correlation"

image_properties = {}
image_quadrant_limits = {}
point_selected = None # For initial point at left button mouse event
new_selection = False # Flag that indicates that a new point was selected
tracking_enabled = False # Is tracking enabled?


def mouse_callback(event, x, y, flags, param):
    """
    Callback for mouse events:
    SINGLE LEFT BUTTON DOWN -- Mask selection
    """
    #global mask_origin, mask
    global point_selected
    global new_selection
    global tracking_enabled
    
    # Handle Left-mouse-button event. Mask selection
    if(event == cv.EVENT_LBUTTONDOWN):
        print("Boton Izquierdo",x,y)
        point_selected = (x,y)
        new_selection = True
        tracking_enabled = True
        print(param)


def create_mask(img, point):
    # Find the upper-left point of the mask
    mask_origin = check_boundaries(point, MASK_SIZE)
    # Get mask pixels
    mask = img[\
        mask_origin[Y_AXIS]:mask_origin[Y_AXIS]+MASK_SIZE,\
        mask_origin[X_AXIS]:mask_origin[X_AXIS]+MASK_SIZE, :\
        ]
    return mask_origin, mask


def check_boundaries(center, size):
    global image_quadrant_limits

    x_pos = center[X_AXIS]
    y_pos = center[Y_AXIS]

    # Check the limit in Y axis
    if(y_pos < image_quadrant_limits['UPPER']):
        upper = max(0, y_pos-size//2)
        #bottom = upper + size      
    else:
        bottom = min(y_pos+size//2, image_quadrant_limits['BOTTOM'])
        upper = bottom - size
    
    # Check the limit in X axis
    if(x_pos < image_quadrant_limits['LEFT']):
        left = max(0, x_pos-size//2)
        #right = left + size
    else:
        right = min(image_quadrant_limits['RIGHT'], x_pos+size//2)
        left = right - size

    return (int(left),int(upper))
    

def update_mask(img, roi_pos, ul_match, old_mask):
    """
    Find the absolut upper-left pixel position of the new detection into 
    the original image.
    As the template matching is executed into a ROI, its position is 
    relative to it.

    Keyword Arguments:
    img -- Original image
    roi_pos -- Upper-left pixel position of the ROI
    ul_match -- Upper-left pixel position for new detection relative to ROI
        position
    """
    # Find absolute position of upper-left point of new detection
    orig_new_detection = (\
        roi_pos[X_AXIS] + ul_match[X_AXIS],\
        roi_pos[Y_AXIS] + ul_match[Y_AXIS]\
        )
    # Get new match pixels
    new_detection = img[\
        orig_new_detection[Y_AXIS]:orig_new_detection[Y_AXIS]+MASK_SIZE,\
        orig_new_detection[X_AXIS]:orig_new_detection[X_AXIS]+MASK_SIZE,:\
        ]

    new_mask = (new_detection * 0.1) + (old_mask * 0.9) 

    return orig_new_detection, new_mask.astype('uint8')


#def updateROIOrigin(frame, mask_origin):
def update_ROI(frame, mask_origin):
    """
    Find the upper-left pixel position of the ROI based on the location
    of the current detection, and the pixels for new ROI

    Keyword Arguments:
    frame -- Image from where the new ROI pixels will be obtained
    mask_origin -- The position of the current match in the image
    """
    # Find the central pixel of the mask
    mask_center = (\
        mask_origin[X_AXIS]+MASK_SIZE//2,\
        mask_origin[Y_AXIS]+MASK_SIZE//2\
        )
    # Computes the upper-left point of the ROI for next iteration
    new_roi_origin = check_boundaries(mask_center, ROI_SIZE)

    # Get pixels of the ROI for next iteration
    new_roi = frame[\
        new_roi_origin[Y_AXIS]:new_roi_origin[Y_AXIS]+ROI_SIZE,\
        new_roi_origin[X_AXIS]:new_roi_origin[X_AXIS]+ROI_SIZE,:\
        ]

    return new_roi_origin, new_roi


if __name__=='__main__':
#def main():
    # global point_selected
    # global new_selection
    # global tracking_enabled
    # Create an empty variable for frame reference. 
    # It's neccessary for mouse callback parameter
    frame = None
    matching_success = False

    # Create empty windows
    cv.namedWindow(MAIN_WINDOW_NAME)
    cv.moveWindow(MAIN_WINDOW_NAME, 0,0)

    # Create an instance for video capturing
    cap = cv.VideoCapture(VIDEO_SOURCE)
 
    # Get properties of camera source
    video_fps = cap.get(cv.CAP_PROP_FPS)
    video_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    print("FPS: {}\tWidth: {}\tHeight: {}".format(video_fps, video_width, video_height))

    # Open video codec
    fourcc = cv.VideoWriter_fourcc(*'H265')
    # Get current datetime for video naming
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    # GStreamer pipeline for video output
    gst_pipe = "appsrc ! 'video/x-raw format=RGB,width=640,height=480,framerate=30/1' ! jpegenc ! matroskamux ! filesink location="
    # Video Writers for video recording
    tracking_video = cv.VideoWriter("{}tracking_{}.mkv".format(gst_pipe,now), cv.CAP_GSTREAMER, fourcc,\
        video_fps, (video_width, video_height), True)
    output_video = cv.VideoWriter("{}output_{}.mkv".format(gst_pipe,now), cv.CAP_GSTREAMER, fourcc,\
        video_fps, (video_width, video_height), True)

    # Image quadrants for boundaries check
    image_properties.update([('Width', video_width),('Height',video_height)])
    image_quadrant_limits.update([
        ('UPPER', video_height//2),
        ('BOTTOM', video_height),
        ('LEFT', video_width//2),
        ('RIGHT', video_width),
        ])

    # Check status of the camera connection
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    # Configure mouse callbacks 
    cv.setMouseCallback(MAIN_WINDOW_NAME, mouse_callback)

    # Run forever
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        # If frame is read correctly, ret is True
        if not ret:
            print("Can't receive frame. Exiting ...")
            break
        
        # Time measurement
        e1 = cv.getTickCount()

        # Get a copy of the frame for processing
        img = frame.copy()

        # Image processing will be executed only if a mask was selected
        if (tracking_enabled):
            # Check if new target was selected
            if(new_selection):
                mask_origin, mask = create_mask(frame, point_selected)
                # Turn new selection flag False
                new_selection = False
                # Create empty windows for tracking
                cv.namedWindow(ROI_WINDOW_NAME)
                cv.moveWindow(ROI_WINDOW_NAME, video_width,0)
                cv.namedWindow(MASK_WINDOW_NAME)
                cv.moveWindow(MASK_WINDOW_NAME, video_width, ROI_SIZE+50)
                cv.namedWindow(CORR_WINDOW_NAME)
                cv.moveWindow(CORR_WINDOW_NAME, video_width, ROI_SIZE+MASK_SIZE+50)
                       
            # Display mask
            cv.imshow(MASK_WINDOW_NAME, mask)
            # Get ROI
            roi_origin, roi = update_ROI(frame, mask_origin)

            # Display ROI
            cv.imshow(ROI_WINDOW_NAME, roi)

            # Compute template matching
            temp_matching = cv.matchTemplate(roi, mask, cv.TM_CCOEFF_NORMED)

            # Show template matching result
            cv.imshow(CORR_WINDOW_NAME, temp_matching)

            # Get minimum and maximum values and their locations realtive to 
            # ROI position
            (minValue,maxValue, minLoc, maxLoc) = cv.minMaxLoc(temp_matching)
            print(minValue,maxValue, minLoc, maxLoc)
            
            # Threshold the maximum value for matching template
            if(maxValue <= MATCH_THRESHOLD):
                matching_success = False
                print("Tracking Error")
            else: 
                matching_success = True

                # Update mask origin
                mask_origin, mask = update_mask(frame, roi_origin, maxLoc, mask)
                
                # Get the difference between the center of the mask and the 
                # center of the image, in X and Y axis
                img_center_x = int(video_width//2)
                img_center_y = int(video_height//2)
                mask_center_x = mask_origin[X_AXIS] + int(MASK_SIZE//2)
                mask_center_y = mask_origin[Y_AXIS] + int(MASK_SIZE//2)
                img_mask_diff = (img_center_x-mask_center_x,\
                    img_center_y-mask_center_y) 
                print("Error: {}".format(img_mask_diff))
                
                # Draw line for diff
                cv.line(img, (img_center_x, img_center_y), (mask_center_x,\
                    mask_center_y), color=(255,0,0), thickness=1)

                # Draw a rectangle for detected object
                cv.rectangle(img, mask_origin,\
                    (mask_origin[X_AXIS]+MASK_SIZE, mask_origin[Y_AXIS]+MASK_SIZE),\
                    color=(0,0,255), thickness=1)
                
                #Draw a rectangle for ROI
                cv.rectangle(img, roi_origin, (roi_origin[X_AXIS] + ROI_SIZE,\
                    roi_origin[Y_AXIS] + ROI_SIZE), color=(0,255,0), thickness=1)
       
        # Wait for keypress
        key = cv.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('x'):
            tracking_enabled = False
            cv.destroyWindow(ROI_WINDOW_NAME)
            cv.destroyWindow(MASK_WINDOW_NAME)
            cv.destroyWindow(CORR_WINDOW_NAME)
            
        # Display tracking result
        cv.imshow(MAIN_WINDOW_NAME, img)
        tracking_video.write(img)
        output_video.write(frame)

        # Display the resulting frame
        e2 = cv.getTickCount()
        fps = 1/((e2-e1)/cv.getTickFrequency())
        print("FPS: {:1f}".format(fps))
        
    # When everything done, release the capture
    cap.release()
    tracking_video.release()
    output_video.release()
    cv.destroyAllWindows()

