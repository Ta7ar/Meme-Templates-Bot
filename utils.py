import os
from skimage.metrics import structural_similarity as ssim 
import urllib
import numpy as np
import cv2
from typing import List, Tuple

def best_match(targetImage: np.ndarray)->Tuple[str,str]:
    '''
    Takes in a target image and returns the name of image with the highest similarity.
        Parameters:
            targetImage(np.ndarray): A 2D Array greyscale representation of the target image.
        Returns:
            Tuple[str,float]: Link to best matching image from the images folder and percentage match
    '''
    if not os.path.exists("images"):
        raise FileNotFoundError
    imgNamesArr: List[str] = os.listdir("images")
    bestMatchImg: str = None
    bestMatchSsim: float = -1
    for imgName in imgNamesArr:
        imgPath: str = os.path.join(os.getcwd(),"images",imgName)
        bestMatchCandidate: np.ndarray = cv2.imread(imgPath,cv2.IMREAD_GRAYSCALE)
        #resize the larger image to the match the dimensions of the smaller image
        smallerDimensions: Tuple[int] = targetImage.shape if targetImage.shape[0]*targetImage.shape[1] < bestMatchCandidate.shape[0]*bestMatchCandidate.shape[1] else bestMatchCandidate.shape

        similarityIndex: float = ssim(cv2.resize(bestMatchCandidate,smallerDimensions),cv2.resize(targetImage,smallerDimensions))
        if similarityIndex > bestMatchSsim:
            bestMatchSsim = similarityIndex
            bestMatchImg = imgName
    
    link = f'https://raw.githubusercontent.com/Ta7ar/Meme-Templates-Bot/main/images/{ bestMatchImg.replace(" ","%20")}'
    percentageMatch = f"{(100*bestMatchSsim):.3f}"
    return (link, percentageMatch)
    
def url_to_image(url: str)->np.ndarray:
    """
    Converts an image url to raw image data represented in numpy array.

        Parameters:
            url(str): URL where image is located.
        Returns:
            image(np.ndarray): image data in numpy array. 
    """
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
    return image

