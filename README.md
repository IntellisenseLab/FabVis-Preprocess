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

Optionally download existing data set from [here](https://drive.google.com/drive/folders/1Dux7qifXWn168jbo7LxX8lborTtgrAGl?usp=sharing) and extract.

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
| Slubs                  |  44   |
| Barre                  |  7    |
| Thick Yarn             |  0    |
| Foreign Yarn           |  3    |
| Missing Line           |  64   |
| Holes                  |  68   |
| Knots                  |  0    |
| Misknit                |  8    |
| Dye Spot               |  12   |
| Crease line/Crush Mark |  423  |
| Stains/Dirty           |  380  |
| Stop marks             |  0    |
| Snagging               |  34   |
| Laddering              |  26   |

### Dataset Distribution

![chart]()

<br>

### Unannotated Defects

| Defect      | Image Number |
| :---------: |  :---------: |
| Abrasion    |   1          |
| Dead Cotton |   88, 89, 90 |
