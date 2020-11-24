import sys
import glob
import os

import cv2
import pandas as pd
import numpy as np

class preprocessor():
    def __init__(self):
        super().__init__()

    def resizer(self):
        '''
        Resizes all files within a single directory (May no longer need this)
        '''
        os.mkdir("Resized")
        inputFolder = '/Users/heizer/github_repos/MicroX_Emotion_Recognition/core/test'
        i = 0
        for filename in os.listdir(inputFolder):
            image = cv2.imread(os.path.join(inputFolder,filename))
            dim = (60, 60)
            # resize image
            resized = cv2.resize(image, dim)
            cv2.imwrite("Resized/img{}.jpg".format(i), resized)
            i += 1

    def csvCompiler(self, file):
        '''
        Compiles the csv into the format to use for image cropping
        '''
        table = pd.read_csv(file)
        frames = table['frame']
        filenamearr = []

        for i in frames:
	        filename = 'image' + str(i) + '.jpg'
	        filenamearr.append(filename)

        filenames = pd.Series(filenamearr)

        arr =[]
        arr.append(' face_id')
        arr.append(' success')
        for i in range(17,68):
	        arr.append(' x_' + str(i))
	        arr.append(' y_' + str(i))

        allfeatures = table[arr]
        allfeatures.loc[:,'filename'] = filenames

        allfeatures.to_csv('/Users/heizer/github_repos/MicroX_Emotion_Recognition/core/features.csv')

    def microXMaker(self):
        '''
        Does the reading from csv, takes image as input, crops and scales all images/components into respective folders
        '''
        inputFolder = '/Users/heizer/github_repos/MicroX_Emotion_Recognition/core/glorysmileframes'
        microX = ['leftEye', 'rightEye', 'leftBrow', 'rightBrow', 'mouth', 'nose' ]
        for directory in microX:
            os.mkdir(directory)
        
        keypoints = pd.read_csv("features.csv")
        keypoints.set_index('filename', inplace=True)
        dim = (60, 60)

        for filename in os.listdir(inputFolder):
            image = cv2.imread(os.path.join(inputFolder,filename))
            print(filename)

            if keypoints.loc[filename, " success"] == 0:
                continue

            for microXcomponent in microX:
                if microXcomponent == "leftEye":
                    beginX = keypoints.loc[filename,' x_36']
                    endX = keypoints.loc[filename,' x_39']
                    beginY = keypoints.loc[filename,' x_38']
                    endY = keypoints.loc[filename,' x_40']

                if microXcomponent == "rightEye":
                    beginX = keypoints.loc[filename,' x_42']
                    endX = keypoints.loc[filename,' x_45']
                    beginY = keypoints.loc[filename,' x_44']
                    endY = keypoints.loc[filename,' x_46']

                if microXcomponent == "leftbrow":
                    beginX = keypoints.loc[filename,' x_17']
                    endX = keypoints.loc[filename,' x_21']
                    beginY = keypoints.loc[filename,' x_19']
                    endY = keypoints.loc[filename,' x_17']

                if microXcomponent == "rightbrow":
                    beginX = keypoints.loc[filename,' x_22']
                    endX = keypoints.loc[filename,' x_26']
                    beginY = keypoints.loc[filename,' x_24']
                    endY = keypoints.loc[filename,' x_26']

                if microXcomponent == "nose":
                    beginX = keypoints.loc[filename,' x_31']
                    endX = keypoints.loc[filename,' x_35']
                    beginY = keypoints.loc[filename,' x_27']
                    endY = keypoints.loc[filename,' x_33']

                if microXcomponent == "mouth":
                    beginX = keypoints.loc[filename,' x_48']
                    endX = keypoints.loc[filename,' x_54']
                    beginY = keypoints.loc[filename,' x_51']
                    endY = keypoints.loc[filename,' x_57']

                #TODO change the y points cos we need argmin/argmax instead

                # crop and resize image
                try:
                    cropped_image = image[int(beginX):int(endX),int(beginY):int(endY)]
                    resized = cv2.resize(cropped_image,dim)
                except:
                    continue
                cv2.imwrite("{}/{}{}".format(microXcomponent, microXcomponent, filename), resized)