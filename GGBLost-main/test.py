# importing the module
import cv2
import matplotlib.pyplot as plt
   
# function to display the coordinates of
# of the points clicked on the image 
def click_event(event, x, y, flags, params):
  
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
  
        # displaying the coordinates
        # on the Shell
        print(x, y)
  
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.circle(img, (x,y), 10, (255, 0, 0), -1)
        cv2.imshow('image', img)
  
    # checking for right mouse clicks     
    if event==cv2.EVENT_RBUTTONDOWN:
  
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
  
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        cv2.putText(img, str(b) + ',' +
                    str(g) + ',' + str(r),
                    (x,y), font, 1,
                    (255, 255, 0), 2)
        cv2.imshow('image', img)
  
# driver function
if __name__=="__main__":
    img = cv2.imread('ggbl_1.png', 1)

    plt.imshow(img)

    
    points = plt.ginput(n=0, timeout=0)
    print(points)

    plt.show()

    

    

    # cv2.setMouseCallback('image', click_event)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()