import sys
import glob
import os

import cv2
import pandas as pd
import numpy as np
import shutil


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

    def csvCompiler(self, dataFolder, foldername):
        '''
        Compiles the csv into the format to use for image cropping
        '''
        inputCSV = dataFolder + "/" + "raw_csv" + "/" + foldername + "_raw.csv"
        outputCSV = dataFolder + "/" + foldername + "/" + foldername + ".csv"

        table = pd.read_csv(inputCSV)
        frames = table['frame']
        filenamearr = []

        for i in frames:
	        filename = foldername + '_frame' + str(i-1) + '.jpg' 
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

        allfeatures.to_csv(outputCSV)

    def microXMaker(self, dataFolder, folderName):
        '''
        Does the reading from csv, takes image as input, crops and scales all images/components into respective folders
        '''
        CSV = dataFolder + "/" + folderName + "/" + folderName + ".csv"
        frameName = folderName + "_frame"
        framesFolder = dataFolder + "/" + folderName + "/" + frameName
        microXoutput = dataFolder + "/" + folderName
        microX = ['leftEye', 'rightEye', 'leftBrow', 'rightBrow', 'mouth', 'nose' ]
        for directory in microX:
            try:
                os.mkdir(os.path.join(microXoutput,directory))
            except:
                print("Folders already exists")
                break
        
        keypoints = pd.read_csv(CSV)
        print(keypoints)
        keypoints.set_index('filename', inplace=True)
        print(keypoints)
        dim = (60, 60)
        filenames = []
        fail_counter = 0

        iterations = len(os.listdir(framesFolder)) 

        for i in range(iterations):
            filenames.append(frameName + str(i) + ".jpg")

        if iterations < 10:
            try:
                original = dataFolder + "/" + folderName
                target = "/Users/heizer/github_repos/MicroX_Emotion_Recognition/core/incomplete_data/few_frames"
                shutil.move(original, target)  
            except:
                print("Moving on to next dataset")
            return

        while len(filenames) > 0:
            fail_counter += 1
            print(filenames)
            for filename in filenames:
                image = cv2.imread(os.path.join(framesFolder,filename))
                print(filename)

                if keypoints.loc[filename, " success"] == 0:
                    try:
                        # filenames.remove(filename)
                        os.remove(dataFolder + "/" + folderName + "/" + folderName + "_frame/" + filename)
                        # continue
                    except:
                        print("Will have to duplicate later")

    # TODO change the y points cos we need argmin/argmax instead
        
                for microXcomponent in microX:
                    if microXcomponent == "leftEye":
                        beginX = keypoints.loc[filename,' x_36']
                        endX = keypoints.loc[filename,' x_39']
                        beginY = keypoints.loc[filename,' y_38']
                        endY = keypoints.loc[filename,' y_40']
                        # beginY = np.argmin(keypoints.loc[filename,' y_37'], keypoints.loc[filename,' y_38'])
                        # endY = np.argmax(keypoints.loc[filename,' y_40'], keypoints.loc[filename,' y_41'])

                    if microXcomponent == "rightEye":
                        beginX = keypoints.loc[filename,' x_42']
                        endX = keypoints.loc[filename,' x_45']
                        beginY = keypoints.loc[filename,' y_44']
                        endY = keypoints.loc[filename,' y_46']

                    if microXcomponent == "leftbrow":
                        beginX = keypoints.loc[filename,' x_17']
                        endX = keypoints.loc[filename,' x_21']
                        beginY = keypoints.loc[filename,' y_19']
                        endY = keypoints.loc[filename,' y_17']

                    if microXcomponent == "rightbrow":
                        beginX = keypoints.loc[filename,' x_22']
                        endX = keypoints.loc[filename,' x_26']
                        beginY = keypoints.loc[filename,' y_24']
                        endY = keypoints.loc[filename,' y_26']

                    if microXcomponent == "nose":
                        beginX = keypoints.loc[filename,' x_31']
                        endX = keypoints.loc[filename,' x_35']
                        beginY = keypoints.loc[filename,' y_27']
                        endY = keypoints.loc[filename,' y_33']

                    if microXcomponent == "mouth":
                        beginX = keypoints.loc[filename,' x_48']
                        endX = keypoints.loc[filename,' x_54']
                        beginY = keypoints.loc[filename,' y_51']
                        endY = keypoints.loc[filename,' y_57']


                    # crop and resize image
                    try:
                        cropped_image = image[int(beginX):int(endX),int(beginY):int(endY)]
                        resized = cv2.resize(cropped_image,dim)
                        cv2.imwrite("{}/{}/{}{}".format(microXoutput,microXcomponent, microXcomponent, filename), resized)
                        try:
                            filenames.remove(filename)
                        except:
                            continue
                    except:
                        print("File may have errors")
                        try:
                            print("Duplication of previous frames in process")
                            try:
                                # try to see if its 2 digits
                                value = int(filename[-6:-4])
                                try:
                                    #try to see if its 3 digits
                                    value = int(filename[-7:-4])
                                    previous_filename = filename[0:-7] + str(int(value) - 1) + ".jpg"
                                except:
                                    value = int(filename[-6:-4])
                                    previous_filename = filename[0:-6] + str(int(value)-1) + ".jpg"
                                    print(previous_filename)
                            except:
                                value = int(filename[-5])
                                if value == 0:
                                    previous_filename = filename[0:-5] + str(value+1) + ".jpg"
                                else:
                                    previous_filename = filename[0:-5] + str(value-1) + ".jpg"

                            previous_file_directory = "{}/{}/{}{}".format(microXoutput,microXcomponent, microXcomponent, previous_filename)
                            shutil.copyfile(previous_file_directory, "{}/{}/{}{}".format(microXoutput,microXcomponent, microXcomponent, filename))
                            filenames.remove(filename)
                        except:
                            continue

        moving dataset to respective folders (completed / incomplete)
            if fail_counter >  (iterations + 10): 
                print("____________________________FAILED DATASET MOVING FOLDER____________________________")
                original = dataFolder + "/" + folderName
                target = "/Users/heizer/github_repos/MicroX_Emotion_Recognition/core/incomplete_data"
                shutil.move(original,target)
                break 
        

        try:
            original = dataFolder + "/" + folderName
            target = "/Users/heizer/github_repos/MicroX_Emotion_Recognition/core/completed_split"
            shutil.move(original, target)       
        except:
            print("Moving on to next dataset")
