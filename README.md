# FabVis-Preprocess
 <br>

## Setup

Clone the repository

```sh
git clone https://github.com/IntellisenseLab/FabVis-RD-Preprocess.git
```

Create a folder to hold the base dataset

```sh
mkdir dataset
```

Optionally download existing data set from [here](https://drive.google.com/drive/folders/1ydFYKZxfJdkf1DyhO2EZK7M5WZNHuHNE?usp=sharing) and extract.

 <br>

## Dataset labelling

For installing up dataset labelling software run,

```sh
pip3 install labelImg
```

For starting dataset labelling software run,

```sh
cd dataset
labelImg
```

<br>

## Dataset processing

For starting the dataset preprocessing process run,

```sh
python3 preprocess.py
```

For checking the dataset distribution after preprocessing run,

```sh
python3 checkStatistics.py
```

For checking the dataset for unannotated images run,

```sh
python3 checkDataset.py
```

<br>

## Statistics

<br>

### Annotated Defects

| Defect                 | Count |
| :-------------------:  | :---: |
| Slubs                  |  34   |
| Barre                  |  6    |
| Thick Yarn             |  0    |
| Foreign Yarn           |  3    |
| Missing Line           |  40   |
| Holes                  |  50   |
| Knots                  |  0    |
| Misknit                |  8    |
| Dye Spot               |  10   |
| Crease line/Crush Mark |  324  |
| Stains/Dirty           |  293  |
| Stop marks             |  0    |
| Snagging               |  18   |
| Laddering              |  26   |

### Dataset Distribution

![chart](https://user-images.githubusercontent.com/25496607/139519516-2ba78a12-a422-4a2f-87c7-0952b17dfba9.png)


<br>

### Unannotated Defects

| Defect      | Image Number |
| :---------: |  :---------: |
| Abrasion    |   1          |
| Dead Cotton |   88, 89, 90 |
