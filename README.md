# DSCI-310-Group-11
**Project Title**: Predict the Probability of a Delivery getting a wicket in Cricket

Contributors: 

- Alex Lin
- Jackson Siemens
- Shruti Vijaykumar Seetharam
- Hanlin Zhao

## Project Summary

Our project works on predicting the probability of getting a wicket on a delivery in Cricket based off of game plays. Being avid sports fans, and wanting to explore a new sport, we looked towards Cricket and specifically T20 International matches to do our analysis. Our analysis uses ball-by-ball data from [Cricsheet](https://cricsheet.org/), downloaded in `json` format and then converted to `csv` format. 

## How to run analysis

1. Clone the repository using on the command line.

`git clone https://github.com/DSCI-310-2024/DSCI-310-Group-11.git`

2. Create the environment (if it is the first time setting it up). If the environment is set up, move on to the next step.

`conda env create -f environment.yaml` 

3. Activate the environment

`conda activate dsci310_group11`

4. Open JupyterLab and run the notebook `cricket_wicket_probability_prediction.ipynb`.

   **Note**: Some cells may take upto 4 minutes to run as our dataset is large, and we are performing hyperparameter optimization.

**Dependencies needed**:
- JupyterLab
- Python and Python Packages:
    - `numpy`
    - `pandas`
    - `altair`
    - `scikit-learn`
    - `matplotlib`
    - `vegafusion`
    - `vl-convert-python`

## Licenses
The License was derived from the MIT License.

## Dataset
The data was all sourced from [Cricsheet](https://cricsheet.org/).
