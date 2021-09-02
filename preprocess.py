import cv2
import os
import glob
import random
import PIL.Image
import numpy as np
import configparser
from collections import Counter

defects=["Slubs",
        "Barre",
        "Thick Yarn",
        "Foreign Yarn",
        "Missing Line",
        "Holes",
        "Knots",
        "Misknit",
        "Dye Spot",
        "Crease line/Crush Mark",
        "Stains/Dirty",
        "Stop marks",
        "Snagging",
        "Laddering"]

def writeStats(path, originalDatasetStat, trainDataStat, testDataStat, trainDataStatPostProcess, testDataStatPostProcess):
    config = configparser.ConfigParser()

    config["Dataset Statistics"] = originalDatasetStat
    config["Dataset Training Statistics"] = trainDataStat
    config["Dataset Testing Statistics"] = testDataStat
    config["Processed Training Statistics"] = trainDataStatPostProcess
    config["Processed Testing Statistics"] = testDataStatPostProcess

    with open(path+'statistics.ini', 'w') as configfile:
        config.write(configfile)

def bmpSave(filename, image):
	imagetemp = PIL.Image.fromarray(image.astype(np.uint8))
	imagetemp.save(filename)
	if imagetemp.mode != 'RGB':
		imagetemp=imagetemp.convert('RGB')

def checkContain(x1,y1,x2,y2,defect):
	dx,dy=defect[1],defect[2]
	dleftX,dleftY=dx-defect[3]/2,dy-defect[4]/2

	### using rectangle overlap
	newX1 = max(x1,dleftX)
	newX2 = min(x2,dleftX+defect[3])
	newY1 = max(y1,dleftY)
	newY2 = min(y2,dleftY+defect[4])
	if(newX1<newX2 and newY1<newY2):
		return 1
	return 0

def getBoxCoordinates(x1,y1,x2,y2,defect):

	### using rectangle overlap
	dx,dy=defect[1],defect[2]
	dleftX,dleftY=dx-defect[3]/2,dy-defect[4]/2
	newX1 = max(x1,dleftX)
	newX2 = min(x2,dleftX+defect[3])
	newY1 = max(y1,dleftY)
	newY2 = min(y2,dleftY+defect[4])

	boxW = newX2-newX1
	boxH = newY2-newY1
	boxX,boxY = newX1+boxW/2-x1,newY1+boxH/2-y1

	##return [defect[0],boxX,boxY,boxW,boxH]
	return [defect[0],boxX/slideWidth,boxY/slideHeight,boxW/slideWidth,boxH/slideHeight]

def cropper(imageName, slideHeight, slideWidth, jump, sourceFolder, targetFolder):
	image =  cv2.imread(sourceFolder+imageName+".bmp")
	imageH, imageW, channels = image.shape
	imageArray = []

	defects=[]
	with open(sourceFolder+imageName+".txt", 'r') as fd:
		for line in fd:
			ty,dx,dy,dw,dh=map(float,line.split())
			ty=int(ty)
			dx,dy,dw,dh=round(dx*imageW),round(dy*imageH),round(dw*imageW),round(dh*imageH)
			defects.append([ty,dx,dy,dw,dh])

	noOfFullH = int((imageH-slideHeight)/jump)
	noOfFullW = int((imageW-slideWidth)/jump)
	dCount,ndCount=0,0

	for i in range(0, noOfFullH+1):
		for j in range(0, noOfFullW+1):
			cropped = image[i*jump:(i*jump)+slideHeight, j*jump:(j*jump)+slideWidth]
			imageArray.append([cropped,[j*jump,i*jump,(j*jump)+slideWidth,(i*jump)+slideHeight]])
		if (imageW>((noOfFullW*jump)+slideWidth)):
			cropped = image[i*jump:(i*jump)+slideHeight, imageW-slideWidth:imageW]
			imageArray.append([cropped,[imageW-slideWidth,i*jump,imageW,(i*jump)+slideHeight]])

	if (imageH>((noOfFullH*jump)+slideHeight)):
		for j in range(0, noOfFullW+1):
			cropped = image[imageH-slideHeight:imageH, j*jump:(j*jump)+slideWidth]
			imageArray.append([cropped,[j*jump,imageH-slideHeight,(j*jump)+slideWidth,imageH]])

		if (imageW>(noOfFullW*slideWidth)):
			cropped = image[imageH-slideHeight:imageH, imageW-slideWidth:imageW]
			imageArray.append([cropped,[imageW-slideWidth,imageH-slideHeight,imageW,imageH]])

	for croppedImage in imageArray:
		x1,y1,x2,y2=croppedImage[1]
		flag = True
		defectCoorInCropped=[]
		for defect in defects:
			if(checkContain(x1,y1,x2,y2,defect)):
				defectCoorInCropped.append(" ".join(map(str,getBoxCoordinates(x1,y1,x2,y2,defect))))
				flag = False
		if not flag:
			nameImage = targetFolder+imageName+"_"+str(dCount)+".bmp"
			nameYolo = targetFolder+imageName+"_"+str(dCount)+".txt"
			bmpSave(nameImage,croppedImage[0])
			with open(nameYolo, 'w') as out_file:
				for newDefect in defectCoorInCropped:
						out_file.write(newDefect+"\n")
			dCount +=1		
		# else:
		# 	nameImage = sourceFolder+"/"+imageName+"_NonDiffective_"+str(ndCount)+".bmp"
		# 	#bmpSave(nameImage,croppedImage[0])
		# 	ndCount+=1

	return imageArray

def processData(slideHeight, slideWidth, jump, sourceFolder, targetFolder, trainImageList, testImageList):
    targetFolderTrain= targetFolder+"train/"
    targetFolderTest= targetFolder+"test/"

    filesTrain = glob.glob(targetFolderTrain+"*")
    for file in filesTrain:
        os.remove(file)

    filesTest = glob.glob(targetFolderTrain+"*")
    for file in filesTest:
        os.remove(file)

    for imageName in trainImageList:
        cropper(imageName, slideHeight, slideWidth, jump, sourceFolder, targetFolderTrain)

    for imageName in testImageList:
        cropper(imageName, slideHeight, slideWidth, jump, sourceFolder, targetFolderTest)

def checkClasses(imageFolder):
    src_train = os.listdir(imageFolder+"train/")
    src_test = os.listdir(imageFolder+"test/")

    dicTrain={}
    dicTest={}

    for file_name in src_train:
        if(file_name[-3:]=="bmp"):
            with open(imageFolder+"train/"+file_name[:-3]+"txt",'r') as f:
                for line in f:
                    if(defects[int(line.split()[0])] not in dicTrain):
                        dicTrain[defects[int(line.split()[0])]]=1
                    else:
                        dicTrain[defects[int(line.split()[0])]]+=1
    
    for file_name in src_test:
        if(file_name[-3:]=="bmp"):
            with open(imageFolder+"test/"+file_name[:-3]+"txt",'r') as f:
                for line in f:
                    if(defects[int(line.split()[0])] not in dicTest):
                        dicTest[defects[int(line.split()[0])]]=1
                    else:
                        dicTest[defects[int(line.split()[0])]]+=1
    
    return dicTrain, dicTest

def writeConfig(imageFolder, configFolder):
    img_train = os.listdir(imageFolder+"train/")
    txt_train = configFolder+"train.txt"

    img_test = os.listdir(imageFolder+"test/")
    txt_test = configFolder+"test.txt"

    classFile = configFolder+"obj.names"
    dataFile = configFolder+"obj.data"

    with open(txt_train, 'w') as file:
        for file_name in img_train:
            if(file_name[-3:]=='bmp'):
                file.write("%s\n" % ("../images/train/"+file_name))

    print("\nWrote Train data into train.txt")
    
    with open(txt_test, 'w') as file:
        for file_name in img_test:
            if(file_name[-3:]=='bmp'):
                file.write("%s\n" % ("../images/test/"+file_name))

    print("\nWrote Test data into test.txt")

    with open(classFile, 'w') as file:
        for eachDefect in defects:
            file.write("%s\n" % eachDefect)

    print("\nWrote Classnames into obj.names")

    with open(dataFile, 'w') as file:
        file.write("classes = %s\n" % str(len(defects)))
        file.write("train  = ../config/train.txt\n")
        file.write("valid  = ../config/test.txt\n")
        file.write("names = ../config/obj.names\n")
        file.write("backup = ../weights/\n")

    print("\nWrote data into obj.data")

def calculateSuitability(instanceDic, totalDefects, trainDefects, trainComponent):
    suitability = 0

    for defect in defects:
        try:
            suitability += (1/totalDefects[defect])*(int(totalDefects[defect]*trainComponent) - (trainDefects[defect]+instanceDic[defect]))
        except KeyError:
            continue

    return suitability

def checkCompletion(instanceDic, totalDefects, trainComponent):
    completed = True

    for defect in defects:
        try:
            if ((int(totalDefects[defect]*trainComponent) - instanceDic[defect])>0):
                completed = False
        except KeyError:
            continue

    return completed

def analyzeDefectCount(datasetPath, trainComponent):
    completion = False
    src_files = os.listdir(datasetPath)
    trainImageNames=[]
    testImageNames=[]

    totalDefects={}
    trainDefects={}

    random.shuffle(src_files)

    # calculate total defects availble in the data set

    for file_name in src_files:
        if(file_name[-3:]=="bmp"):
            try:
                with open(datasetPath+file_name[:-3]+"txt",'r') as f:
                    for line in f:
                        if(defects[int(line.split()[0])] not in totalDefects):
                            totalDefects[defects[int(line.split()[0])]]=1
                        else:
                            totalDefects[defects[int(line.split()[0])]]+=1
            except FileNotFoundError:
                continue

    # Process to identify and divide images among train and test

    while(not completion):
        maxSuitability = float('-inf')
        selectedName = ""

        for file_name in src_files:
            if((file_name[-3:]=="bmp") and (file_name[:-4] not in trainImageNames)):
                trainDefectsProjection = {}

                try:
                    with open(datasetPath+file_name[:-3]+"txt",'r') as f:
                        for line in f:
                            if(defects[int(line.split()[0])] not in trainDefectsProjection):
                                trainDefectsProjection[defects[int(line.split()[0])]]=1
                            else:
                                trainDefectsProjection[defects[int(line.split()[0])]]+=1
                except FileNotFoundError:
                    continue

                suitability = calculateSuitability(trainDefectsProjection, totalDefects, trainDefects, trainComponent)

                if suitability>maxSuitability:
                    maxSuitability = suitability
                    selectedName = file_name

        else:
            trainImageNames.append(selectedName[:-4])

            with open(datasetPath+selectedName[:-3]+"txt",'r') as f:
                for line in f:
                    if(defects[int(line.split()[0])] not in trainDefects):
                        trainDefects[defects[int(line.split()[0])]]=1
                    else:
                        trainDefects[defects[int(line.split()[0])]]+=1

            completion = checkCompletion(trainDefects, totalDefects, trainComponent)
    else:
        for file_name in src_files:
            if((file_name[-3:]=="bmp") and (file_name[:-4] not in trainImageNames)):
                testImageNames.append(file_name[:-4])

    return trainImageNames, testImageNames, totalDefects, trainDefects, Counter(totalDefects)-Counter(trainDefects)


print("\n-------------------------- Creating Folder structure -------------------------")

try: 
    os.makedirs(os.path.dirname(os.path.abspath(__file__))+"/../images/test")
    print(os.path.dirname(os.path.abspath(__file__))+"/../images/test"+" created")
except FileExistsError: 
    print(os.path.dirname(os.path.abspath(__file__))+"/../images/test"+" already exist")

try: 
    os.makedirs(os.path.dirname(os.path.abspath(__file__))+"/../images/train")
    print(os.path.dirname(os.path.abspath(__file__))+"/../images/train"+" created") 
except FileExistsError: 
    print(os.path.dirname(os.path.abspath(__file__))+"/../images/train"+" already exist")  

try: 
    os.makedirs(os.path.dirname(os.path.abspath(__file__))+"/../config/")
    print(os.path.dirname(os.path.abspath(__file__))+"/../config/"+" created")
except FileExistsError: 
    print(os.path.dirname(os.path.abspath(__file__))+"/../config/"+" already exist")

try: 
    os.makedirs(os.path.dirname(os.path.abspath(__file__))+"/../weights/")
    print(os.path.dirname(os.path.abspath(__file__))+"/../weights/"+" created")
except FileExistsError: 
    print(os.path.dirname(os.path.abspath(__file__))+"/../weights/"+" already exist")

datasetPath = os.path.dirname(os.path.abspath(__file__))+"/dataset/"
imageWritePath = os.path.dirname(os.path.abspath(__file__))+"/../images/"
configWritePath = os.path.dirname(os.path.abspath(__file__))+"/../config/"

print("\n------------------------ Requesting input -------------------------")

slideHeight = int(input("Enter image height (should be divisable by 32) : "))
slideWidth = int(input("Enter image width (should be divisable by 32) : "))
jump = int(input("Enter number of pixel to have inbetween images (better to be similar to height or width) : "))
trainRatio = float(input("Enter train set component (suggested 0.75) : "))

print("\n------------------------ Processing Images ------------------------")

trainImageList, testImageList, originalDatasetStat, trainDataStat, testDataStat = analyzeDefectCount(datasetPath, trainRatio)

processData(slideHeight, slideWidth, jump, datasetPath, imageWritePath, trainImageList, testImageList)

trainDataStatPostProcess, testDataStatPostProcess = checkClasses(imageWritePath)

print("\n---------------------- Creating config files-----------------------")

writeConfig(imageWritePath, configWritePath)

writeStats(configWritePath, originalDatasetStat, trainDataStat, testDataStat, trainDataStatPostProcess, testDataStatPostProcess)
