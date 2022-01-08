import os

sourcefolderpath = os.path.dirname(os.path.abspath(__file__))+"/dataset/"

src_files = os.listdir(sourcefolderpath)

unannotatedImages = 0

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

dic={}

for file_name in src_files:
    if(file_name[-3:]=="bmp"):
        try:
            with open(sourcefolderpath+file_name[:-3]+"txt",'r') as f:
                for line in f:
                    if(defects[int(line.split()[0])] not in dic):
                        dic[defects[int(line.split()[0])]]=1
                    else:
                        dic[defects[int(line.split()[0])]]+=1
        except FileNotFoundError:
            unannotatedImages += 1

print("\nAll data distribution")
print(dic)
print("\nNumber of Images to be annotated : "+ str(unannotatedImages))