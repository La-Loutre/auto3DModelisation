import math
import numpy
import cv2
import Image
import matplotlib.pyplot as plt

def openCVToPIL(cv2Img):
    cv2Img2 = cv2.cvtColor(cv2Img,cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(cv2Img2)
    return pil_img

def PILToOpenCV(pilImg):
    open_cv_image = numpy.array(pilImg)
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.cv.CV_BGR2RGB)
    return open_cv_image

def distanceX(alpha,beta,width,dY):
    print(alpha,beta,width)
    #if(alpha*beta >0 ):
    return (dY*float(math.tan(alpha))+dY*float(math.tan(beta)))/float(2)
   # return (-dY*float(alpha)+dY*float(math.tan(beta))+width)/float(2)
    
def distanceY(alpha,beta,width):
    print(alpha,beta,width)
    print(math.tan(alpha),math.tan(beta))
    if(alpha*beta >0 ):
        return abs(float(width)/float((math.tan(alpha)-math.tan(beta))))
    return abs(float(width)/float((math.tan(alpha)+math.tan(beta))))


def cascadeClassifierDetection(img,xml):
    cascadeClass = cv2.CascadeClassifier(xml)
    img_cv = PILToOpenCV(img)
    img_cv_gray = cv2.cvtColor(img_cv,cv2.COLOR_BGR2GRAY)
    img_cv_gray = cv2.equalizeHist(img_cv_gray)
    detection = cascadeClass.detectMultiScale(img_cv_gray,1.1,2,0)
    detectionMax = detection[0]
    for (x,y,w,h) in detection:
        if  w*h > detectionMax[2]*detectionMax[3] :
            detectionMax=(x,y,w,h)
    
    (x,y,w,h) = detectionMax
    cv2.rectangle(img_cv,(x,y),(x+w,y+h),(255,0,0),2)
        #roi_color = img_cv[y:y+h, x:x+w]

    return openCVToPIL(img_cv)
def keypoints(img1,img2):
    img1_cv = PILToOpenCV(img1)
    img2_cv = PILToOpenCV(img2)
    
    surf=cv2.SURF(400)
    kp, des = surf.detectAndCompute(img1_cv,None)
    kp1, des1 = surf.detectAndCompute(img2_cv,None)
    
    #img1_cv=cv2.drawKeypoints(img1_cv,kp,None,(255,0,0),4)
    #img2_cv=cv2.drawKeypoints(img2_cv,kp1,None,(255,0,0),4)

    # create BFMatcher object
    bf = cv2.BFMatcher()

    # Match descriptors.
    matches = bf.match(des,des1)

    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)


    # Draw first 10 matches.
    img3 = drawMatches(img1_cv,kp,img2_cv,kp1,matches[:10])


    
def drawMatches(img1, kp1, img2, kp2, matches):
    """
    My own implementation of cv2.drawMatches as OpenCV 2.4.9
    does not have this function available but it's supported in
    OpenCV 3.0.0

    This function takes in two images with their associated 
    keypoints, as well as a list of DMatch data structure (matches) 
    that contains which keypoints matched in which images.

    An image will be produced where a montage is shown with
    the first image followed by the second image beside it.

    Keypoints are delineated with circles, while lines are connected
    between matching keypoints.

    img1,img2 - Grayscale images
    kp1,kp2 - Detected list of keypoints through any of the OpenCV keypoint 
              detection algorithms
    matches - A list of matches of corresponding keypoints through any
              OpenCV keypoint matching algorithm
    """

    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    

    for mat in matches:

        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # x - columns
        # y - rows
        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt

        # Draw a small circle at both co-ordinates
        # radius 4
        # colour blue
        # thickness = 1
        cv2.circle(img1, (int(x1),int(y1)), 4, (255, 0, 0), 1)   
        cv2.circle(img2, (int(x2),int(y2)), 4, (255, 0, 0), 1)
        # Draw a line in between the two points
        # thickness = 1
        # colour blue
        #cv2.line(img1, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0,0), 1)

    # Show the image
    cv2.imshow('Matched Features', img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    
def angle(widthImg,posXPoint,cameraAngle):
#    r=90-(camera0BlindSpot+(width-posYPoint)*camera0Angle/widthImg)

    return (posXPoint*cameraAngle/float(widthImg)-cameraAngle/float(2)) * math.pi/float(180)
        
