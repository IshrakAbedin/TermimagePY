# Last modified: Mohammad Ishrak Abedin, 25-11-2020

import ctypes
import cv2
from numpy import uint8

# Load the print method from dll
coredll = ctypes.windll.LoadLibrary("./Core.dll")
coreprint = coredll.printcolor

@ctypes.CFUNCTYPE(None, ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_uint, ctypes.c_uint)
def imageprint(r, g, b, row, col):
    '''
    imageprint(r, g, b, row, col)

    Wrapper around dll `printcolor` function from `Core.dll`.

    Parameters
    ----------
    r : `ctypes.POINTER(ctypes.c_ubyte)`
        Unsigned char pointer pointing to red array.\\
    g : `ctypes.POINTER(ctypes.c_ubyte)`
        Unsigned char pointer pointing to green array.\\
    b : `ctypes.POINTER(ctypes.c_ubyte)`
        Unsigned char pointer pointing to blue array.\\
    row : `ctypes.c_uint`
        Height of the image.\\
    col : `ctypes.c_uint`
        Width of the image
    '''
    coreprint(r, g, b, row, col)

def printImage(image_path : str, width = 120, hwratio = 2.0):
    '''
    printImage(image_path : str, width = 120, hwratio = 2.0)

    Prints the image into console with 24bit color using windows dll.

    Parameters
    ----------
    image_path : `str`
        Path of the image to be printed.\\
    width : `int`
        Target width of the image.\\
    hwratio : `float`
        Stretch/compress ratio of the image.
    '''
    img = cv2.imread(image_path)
    img = ((img / img.max()) * 255).astype(uint8)
    # DOES NOT SUPPORT ALPHA
    if(len(img.shape) == 3 or len(img.shape) == 4):
        h, w, _ = img.shape
        ratio = h / w
        height = int((width * ratio) / hwratio)
        img = cv2.resize(img, (width, height))

        r_p = (ctypes.c_ubyte * (width * height))() 
        g_p = (ctypes.c_ubyte * (width * height))() 
        b_p = (ctypes.c_ubyte * (width * height))()
        for i in range(height):
            for j in range(width):
                r_p[i * width + j] = img[i, j, 2]
                g_p[i * width + j] = img[i, j, 1]
                b_p[i * width + j] = img[i, j, 0]
        imageprint(r_p, g_p, b_p, height, width)
    else:
        h, w = img.shape
        ratio = h / w
        height = int(width * ratio) // hwratio
        img = cv2.resize(img, (width, height))

        r_p = (ctypes.c_ubyte * (width * height))() 
        for i in range(height):
            for j in range(width):
                r_p[i * width + j] = img[i, j]
        imageprint(r_p, r_p, r_p, height, width)

