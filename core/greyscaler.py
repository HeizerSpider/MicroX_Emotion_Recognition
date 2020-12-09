import argparse
import sys
import glob
import os

from preprocessor import preprocessor

def main():
    argparser = argparse.ArgumentParser(
        description=__doc__)
    argparser.add_argument(
        '-d', '--dataFolder',
        default=None,
        type=str,
        help='input folder for all data (default: None)')
    args = argparser.parse_args()

    churn = preprocessor()

    dataFolder = args.dataFolder

    print("---------Greyscaling the images---------")
    churn.transformer(dataFolder)
    print("---------Splitting of frames complete---------")

if __name__=="__main__":
    main()