import numpy as np
import cv2


# Main findcontour function 
def getContours(img):
    #imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgray = img
    # Threshold white paper(background) to white pixel(255), word is actully black(0)
    #retvalth, imgthreshold = cv2.threshold(imgray, 50, 255, cv2.THRESH_BINARY)
    # We want words are white, backgournd is black, easy for opencv findcontour function
    #imgthresholdNot = cv2.bitwise_not(imgthreshold)
    # Dilation make all 6 to form a closed loop
    #kernel = np.ones((5,5), np.uint8)
    #imgdilation = cv2.dilate(imgthresholdNot, kernel, iterations=2)
    # Must use EXTERNAL outer contours, Must use CHAIN_APPROX_NONE method(not change points)
    contours, hierarchy = cv2.findContours(imgray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    max=0
    area=0
    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) > area:
            area = cv2.contourArea(contours[i])
            max = i
    if (len(contours) != 0):
        contours = [contours[max]]
    return contours

# Get complex vector of templete contour
def getTempleteCV(imgOricpy,templeteComVector):
    tpContour = getContours(imgOricpy)
    for contour in tpContour:
        x, y, w, h = cv2.boundingRect(contour)
        for point in contour:
            templeteComVector.append(complex(point[0][0]-x, (point[0][1]-y)))
    return templeteComVector

# Get complex vectors of testees contours
def getSampleCV(imgSP,sampleComVectors):
    spContours = getContours(imgSP)
    for contour in spContours:

        x, y, w, h = cv2.boundingRect(contour)
        for point in contour:
            sampleComVectors.append(complex(point[0][0]-x, (point[0][1]-y)))
    return sampleComVectors


# Calculate fourier transform of templete CV
def getempleteFD(templeteComVector):
    
    return np.fft.fft(templeteComVector)

# Calculate fourier transform of sample CVs
def getsampleFDs(sampleComVectors):
    sampleFD = np.fft.fft(sampleComVectors)
    return sampleFD

# Make fourier descriptor invariant to rotaition and start point
def rotataionInvariant(fourierDesc):
    for index, value in enumerate(fourierDesc):
        fourierDesc[index] = np.absolute(value)

    return fourierDesc    

# Make fourier descriptor invariant to scale
def scaleInvariant(fourierDesc):
    firstVal = fourierDesc[0]

    for index, value in enumerate(fourierDesc):
        fourierDesc[index] = value / firstVal

    return fourierDesc

# Make fourier descriptor invariant to translation
def transInvariant(fourierDesc):
    
    return fourierDesc[1:len(fourierDesc)]

# Get the lowest X of frequency values from the fourier values.
def getLowFreqFDs(fourierDesc):
    # frequence order returned by np.fft is (0, 0.1, 0.2, 0.3, ...... , -0.3, -0.2, -0.1)
    # Note: in transInvariant(), we already remove first FD(0 frequency)

    return fourierDesc[:5]

# Get the final FD that we want to use to calculate distance
def finalFD(fourierDesc):
    fourierDesc = rotataionInvariant(fourierDesc)
    fourierDesc = scaleInvariant(fourierDesc)
    fourierDesc = transInvariant(fourierDesc)
    fourierDesc = getLowFreqFDs(fourierDesc)

    return fourierDesc

# Core match function
def match(tpFD, spFDs):
    tpFD = finalFD(tpFD)
    # dist store the distance, same order as spContours
    dist = []
    font = cv2.FONT_HERSHEY_SIMPLEX
    spFD = finalFD(spFDs)
    res=np.linalg.norm(np.array(spFD)-np.array(tpFD))
    return res
    '''for spFD in spFDs:
        spFD = finalFD(spFD)

        # Calculate Euclidean distance between templete and testee
        dist.append(np.linalg.norm(np.array(spFD)-np.array(tpFD)) )
        print(dist)
        # Draw distance on image
        distText = str(round(dist[len(dist)-1],2))'''

# -------------------------------------------------------------------------- 
# Main loop
def countfly(imageSR,imageGT):
    res=[]
    for i in range(len(imageSR)):
    # imOricpy is for processing, imgOri is for showing
        try:
            imgOricpy = imageSR[i]
            #imgSP = cv2.imread(imageGT , 1)
            imgSP = imageGT[i]
            templeteComVector = []
            sampleComVectors = []

            # Get complex vector
            templeteComVector=getTempleteCV(imgOricpy,templeteComVector)
            sampleComVectors=getSampleCV(imgSP,sampleComVectors)
            # Get fourider descriptor
            #print(len(templeteComVector))
            tpFD = getempleteFD(templeteComVector)
            sampleFDs = getsampleFDs(sampleComVectors)
            # real match function
            res.append(match(tpFD, sampleFDs))
        except:
            res.append(1)
    res= np.mean(res)
    return res


if __name__=='__main__':
    countfly(SR,GT)
