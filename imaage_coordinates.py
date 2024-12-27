import cv2
# function to display the coordinates of
#font(font size & thickness)
# of the points clicked on the image
def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Calculate coordinates in terms of original image
        x_original = int(x * width_ratio)
        y_original = int(y * height_ratio)
        print(x_original, ' ', y_original)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x_original) + ',' +
                    str(y_original), (x,y), font,
                    0.5, (255, 0, 0), 2)
        cv2.imshow('image', img)
if __name__=="__main__":
    img = cv2.imread('/home/link-lap-24/Downloads/base/4.png', 1)
    # Save original dimensions
    original_height, original_width = img.shape[:2]
    # Resize the image
    scale_percent = 60 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(img, dim)
    # Calculate ratios
    width_ratio = original_width / width
    height_ratio = original_height / height
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    # close the window
    cv2.destroyAllWindows()
