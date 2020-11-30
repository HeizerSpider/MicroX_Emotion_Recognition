import argparse
import sys
import glob
import os

from preprocessor import preprocessor
# from microX_model import net

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
    for folderName in os.listdir(dataFolder):
        if folderName == ".DS_Store":
            continue
        if folderName == "raw_csv":
            continue


        print("---------CSV being prepared...---------")
        # csv output from autoface.ai
        churn.csvCompiler(dataFolder, folderName)
        print("---------CSV ready---------")

        print("---------Splitting frames into MicroX components---------")
        framesFolder = dataFolder + "/" + folderName + "/" + folderName + "_frame"
        churn.microXMaker(dataFolder, folderName)
        print("---------Splitting of frames complete---------")

if __name__=="__main__":
    main()