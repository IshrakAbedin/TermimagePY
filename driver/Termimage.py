# Last modified: Mohammad Ishrak Abedin, 24-11-2020

import os
import argparse
from coreconnector import printImage

def main():
    impath, width, ratio = getImagePathWidthHWRatio()
    printImage(impath, width, ratio)

def nonnegative_integer(val : str, default = 120) -> int:
    '''Data conversion system for `argparse`'''
    val = int(val)
    return val if val >= 0 else default

def nonzero_float(val : str, default = 2) -> float:
    '''Data conversion system for `argparse`'''
    val = float(val)
    return val if val > 0 else default

def getImagePathWidthHWRatio():
    '''
    getImagePathWidthHWRatio()

    Parse input arguments.

    Returns
    -------
    imagePath : `str`
        Absolute path of the target image.\\
    width : `int`
        Target width of the image.\\
    ratio : `float`
        Stretch/Compression ratio of the image.
    '''
    parser = argparse.ArgumentParser(
        description="View image on the Terminal. Written by Mohammad Ishrak Abedin.")
    parser.add_argument("imagePath", help="Path of the image.")
    parser.add_argument("-w", "--width", dest="width",
                        help="Viewing Width of the image. Must be a nonnegative integer. Keep it smaller than console width. Default is 120.",
                        type=nonnegative_integer, default=120)
    parser.add_argument("-r", "--ratio", dest="ratio",
                        help="Console blocks for characters are not square. This is the stretching/compression ratio. Must be greater than 0. Default is 2.",
                        type=nonzero_float, default=2)

    parsed_inputs = parser.parse_args()

    parsed_inputs.imagePath = os.path.abspath(parsed_inputs.imagePath)
    return parsed_inputs.imagePath, parsed_inputs.width, parsed_inputs.ratio

main()