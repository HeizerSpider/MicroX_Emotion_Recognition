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

    # def countChecker(self,dataFolder):
    #     '''
    #     Transforms all files within a single directory
    #     '''
    #     inputFolder = dataFolder
    #     # i = 0
    #     for folderName in os.listdir(inputFolder):
    #         checkList = []
    #         if folderName == ".DS_Store":
    #             continue
    #         for microX in os.listdir(os.path.join(inputFolder,folderName)):
    #             if microX == ".DS_Store":
    #                 continue
    #             fileNumber = len(os.listdir(microX))
    #             checkList.append(fileNumber)
    #             g = groupby(iterable)
    #             return next(g, True) and not next(g, False)
    #             if microX == folderName + ".csv":
    #                 continue
    #                 #insert transform here
    #                 image = cv2.imread(os.path.join(inputFolder,folderName,microX,images))
    #                 gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #                 cv2.imwrite(os.path.join(inputFolder,folderName,microX,images), gray_image)


    def transformer(self,dataFolder):
        '''
        Transforms all files within a single directory
        '''
        inputFolder = dataFolder
        # i = 0
        for folderName in [f for f in os.listdir(inputFolder) if not f.startswith('.')]:
            if folderName == ".DS_Store":
                continue
            for microX in [f for f in os.listdir(os.path.join(inputFolder,folderName)) if not f.startswith('.')]:
                if microX == ".DS_Store":
                    continue
                if microX == folderName + ".csv":
                    continue
                for images in [f for f in os.listdir(os.path.join(inputFolder,folderName,microX)) if not f.startswith('.')]:
                    if images == ".DS_Store":
                        continue
                    #insert transform here
                    image = cv2.imread(os.path.join(inputFolder,folderName,microX,images))
                    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    cv2.imwrite(os.path.join(inputFolder,folderName,microX,images), gray_image)

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

    def mainFrameDuplication(self, lastFrame, framesFolder, folderName):
        try:
            # try to see if its 2 digits
            lastFrameValue = int(lastFrame[-6:-4])
            try:
                #try to see if its 3 digits
                lastFrameValue = int(lastFrame[-7:-4])
            except:
                lastFrameValue = int(lastFrame[-6:-4])
        except:
            lastFrameValue = int(lastFrame[-5])
        
        # print(lastFrameValue)

        filenames  = [f for f in os.listdir(framesFolder) if not f.startswith('.')]
        neededFiles = [folderName + "_frame" + str(i) +".jpg" for i in range(lastFrameValue+1)]

        # print(neededFiles)
        # print(len(filenames))

        counter = 0
        numberFilesInFolder = len(filenames)

        for filename in filenames:
            if filename == ".DS_Store":
                filenames.remove(".DS_Store")
                continue
            try:
                neededFiles.remove(filename)
                counter += 1
            except:
                continue
        
        while numberFilesInFolder < lastFrameValue + 1:
            print(numberFilesInFolder, lastFrameValue)
            for remainingFile in neededFiles:
                try:
                    # try to see if its 2 digits
                    value = int(remainingFile[-6:-4])
                    print(value)
                    try:
                        #try to see if its 3 digits
                        value = int(remainingFile[-7:-4])
                        previous_filename = remainingFile[0:-7] + str(int(value) - 1) + ".jpg"
                        # print("value")
                    except:
                        value = int(remainingFile[-6:-4])
                        previous_filename = remainingFile[0:-6] + str(int(value)-1) + ".jpg"
                        print(value)
                        print(previous_filename)
                except:
                    value = int(remainingFile[-5])
                    if value == 0:
                        previous_filename = remainingFile[0:-5] + str(value+1) + ".jpg"
                    else:
                        previous_filename = remainingFile[0:-5] + str(value-1) + ".jpg"

                try:
                    print("Trying to duplicate files", previous_filename, remainingFile)
                    previous_file_directory = "{}/{}".format(framesFolder, previous_filename)
                    shutil.copyfile(previous_file_directory, "{}/{}".format(framesFolder, remainingFile))
                    neededFiles.remove(remainingFile)
                except:
                    print("Duplication failed")
                    # continue
            print([f for f in os.listdir(framesFolder) if not f.startswith('.')])
            numberFilesInFolder = len([f for f in os.listdir(framesFolder) if not f.startswith('.')])
            print(numberFilesInFolder)

    def microFrameDuplication(self, filename, filenames, microXoutput, microXcomponent):
        print("File may have errors")
        try:
            print("Duplication of {} in process".format(filename))
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
                    # print(previous_filename)
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
            print("Duplication for microX failed")
            return


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

        # print(keypoints)

        keypoints.set_index('filename', inplace=True)
        # print(keypoints)
        dim = (60, 60)
        filenames = []
        fail_counter = 0

        # duplicates for frames that are missing
        print("Checking frames")
        self.mainFrameDuplication(lastFrame, framesFolder, folderName)

        numberOfFiles = len([f for f in os.listdir(framesFolder) if not f.startswith('.')])

        for i in range(numberOfFiles):
            for j in range(6):
                filenames.append(frameName + str(i) + ".jpg")

        for micro in microX:
            while len([f for f in os.listdir(os.path.join(microXoutput,micro)) if not f.startswith('.')]) < numberOfFiles:
                # print(len(os.listdir(os.path.join(microXoutput,micro))), numberOfFiles)
                for filename in filenames:
                    image = cv2.imread(os.path.join(framesFolder,filename))
                    print(filename)

        # TODO change the y points cos we need argmin/argmax instead
            
                    for microXcomponent in microX:
                        if microXcomponent == "leftEye":
                            beginX = keypoints.loc[filename,' x_36']
                            endX = keypoints.loc[filename,' x_39']
                            beginY = keypoints.loc[filename,' y_38']
                            endY = keypoints.loc[filename,' y_40']

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
                        padding = 5
                        try:
                            cropped_image = image[int(beginY)-padding:int(endY)+padding,int(beginX)-padding:int(endX)+padding]
                            resized = cv2.resize(cropped_image,dim)
                            # gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
                            cv2.imwrite("{}/{}/{}{}".format(microXoutput,microXcomponent, microXcomponent, filename),resized) #gray_image)
                            try:
                                filenames.remove(filename)
                            except:
                                print("Unable to remove file")
                                continue
                        except:
                            print("File may have errors")
                            try:
                                print("Duplication of {} in process".format(filename))
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
                                        # print(previous_filename)
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
                                print("Duplication for microX failed")
                                fail_counter += 1

                print("fail_counter = ", fail_counter, ",number of files = ", numberOfFiles)
            # moving dataset to respective folders (completed / incomplete)
                if fail_counter >  (numberOfFiles * 6 + 300): 
                    print("____________________________FAILED DATASET MOVING FOLDER____________________________")
                    original = dataFolder + "/" + folderName
                    target = "/Users/heizer/github_repos/MicroX_Emotion_Recognition/core/incomplete_data"
                    shutil.move(original,target)
                    break 
            

        try:
            # # # if all microX folders have frames 0 - 10
            # for microXcomponent in microX:
            #     neededFiles  = []
            #     for i in range(10):
            #         checkFile = microXcomponent + frameName + str(i) + ".jpg"
            #         neededFiles.append(checkFile)
            #     checkFolder = os.listdir(os.path.join(microXoutput,microXcomponent))
            #     print(neededFiles)
            #     print(checkFolder)
            #     check = all(item in checkFolder for item in neededFiles)
            #     print(check)
            #     if check is False:
            #         print("Missing files")
            #         original = dataFolder + "/" + folderName
            #         target = "/Users/heizer/github_repos/MicroX_Emotion_Recognition/core/incomplete_data/few_frames"
            #         shutil.move(original, target)  
            original = dataFolder + "/" + folderName
            target = "/Users/heizer/github_repos/MicroX_Emotion_Recognition/core/completed_split"
            print(original, target)

            shutil.move(original, target)       
        except:
            print("Moving on to next dataset")
