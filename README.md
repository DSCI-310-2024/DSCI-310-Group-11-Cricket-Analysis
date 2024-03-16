# DSCI-310-Group-11
**Project Title**: Predict the Probability of a Delivery getting a wicket in Cricket

Contributors: 

- Alex Lin
- Jackson Siemens
- Shruti Vijaykumar Seetharam
- Hanlin Zhao

## Project Summary

Our project works on predicting the probability of getting a wicket on a delivery in Cricket based off of game plays. Being avid sports fans, and wanting to explore a new sport, we looked towards Cricket and specifically T20 International matches to do our analysis. Our analysis uses ball-by-ball data from [Cricsheet](https://cricsheet.org/), downloaded in `json` format and then converted to `csv` format. 

## Dependencies

This project will be managed using the virtual containerization tool [Docker](https://www.docker.com/). The container image used for the project is based on the `quay.io/jupyter/scipy-notebook:2024-02-24` image. Other dependencies are specified in the [`Dockerfile`](https://github.com/DSCI-310-2024/DSCI-310-Group-11-Cricket-Analysis/blob/main/Dockerfile). 

## Running the analysis

### Setup

1. Install and setup [Docker Desktop](https://www.docker.com/) on your computer. Keep Docker Desktop open when running the analysis.
  
2. Clone this GitHub repository as specified below:

 `git clone https://github.com/DSCI-310-2024/DSCI-310-Group-11.git` 

**Note**: Our data is fairly large, and cloning it may give us an issue with having the data on your local. The scripts will run and still produce the correct data files needed.

### Analysis 

** Add docker run steps**

## Notes

### Working on JupyterLab

If you are working with the project on JupyterLab, follow the steps below. 

1. After doing the steps in Setup section, navigate to the root of this project on your computer as follows:

`cd DSCI-310-Group-11`

2. Enter the following command to setup the virtual container:

`docker-compose up`

3. Once the command has run, you will receive options to launch JupyterLab through different URLs. Copy and paste the one starting with ` http://127.0.0.1:8888/lab?token`. You will now be able to work in the JupyterLab IDE with all the files used in the analysis visible in the file browser pane.

4. Shut down the container after using it by typing `Ctrl + C` in the terminal.  Clean the container up by typing `docker-compose rm` in the terminal.

### Adding Dependencies

To add any other dependencies to the analysis: 

1. Create a new branch and add the dependency to the Dockerfile file.

2. Re-build the new image locally to make sure everything runs properly.
3. Push the changes to GitHub. Since we have built our GitHub actions workflow, the new image will be pushed to DockerHub automatically.
4. Update the image tag on the `docker-compose.yml` file so that it uses the new container image.
5. Open a pull request and merge the new branch with the main branch.


## Licenses
The License was derived from the MIT License.

## Dataset
The data was all sourced from [Cricsheet](https://cricsheet.org/).
