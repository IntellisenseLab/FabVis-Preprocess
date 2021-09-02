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

### Total Defects

| Defect      | Count |
| :---------: | :---: |
| Abrasion    |  1    |
| Crease line |  614  |
| Dead Cotton |  3    |
| Hole        |  7    |
| Snag        |  6    |
| Laddering   |  2    |
| Slub        |  9    |
| Stain       |  374  |

<br>

### Unannotated Defects

| Defect      | Image Number |
| :---------: |  :---------: |
| Abrasion    |   1          |
| Dead Cotton |   88, 89, 90 |