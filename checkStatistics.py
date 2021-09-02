import configparser
import os

config = configparser.ConfigParser()

config.read(os.path.dirname(os.path.abspath(__file__))+"/../config/statistics.ini")

originalDatasetStat = config["Dataset Statistics"]
trainDataStat = config["Dataset Training Statistics"]
testDataStat = config["Dataset Testing Statistics"]
trainDataStatPostProcess = config["Processed Training Statistics"]
testDataStatPostProcess = config["Processed Testing Statistics"]

print("\n Dataset Distribution : ")
print(sorted(originalDatasetStat))

print("\n Training Defect set Distribution : ")
print(sorted(trainDataStat))

print("\n Testing Defect set Distribution : ")
print(sorted(testDataStat))

print("\n Processed training set Distribution : ")
print(sorted(trainDataStatPostProcess))

print("\n Processed testing set Distribution : ")
print(sorted(testDataStatPostProcess))