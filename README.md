# DSCI-310-Group-11
**Project Title**: Predict the Probability of a Delivery getting a wicket in Cricket

Contributors: 

- Alex Lin
- Jackson Siemens
- Shruti Vijaykumar Seetharam
- Hanlin Zhao

## Project Summary

Our project works on predicting the probability of getting a wicket on a delivery in Cricket based off of game plays. Being avid sports fans, and wanting to explore a new sport, we looked towards Cricket and specifically T20 International matches to do our analysis. Our analysis uses ball-by-ball data from [Cricsheet](https://cricsheet.org/), downloaded in `json` format and then converted to `.parquet` format. 

## Dependencies

This project will be managed using the virtual containerization tool [Docker](https://www.docker.com/). The container image used for the project is based on the `quay.io/jupyter/scipy-notebook:2024-02-24` image. Other dependencies are specified in the [`Dockerfile`](https://github.com/DSCI-310-2024/DSCI-310-Group-11-Cricket-Analysis/blob/main/Dockerfile). 

## Running the analysis

### Setup

1. Install and setup [Docker](https://www.docker.com/) on your computer. Keep Docker Desktop open when running the analysis.
2. Clone this GitHub repository as specified below:

 `git clone https://github.com/DSCI-310-2024/DSCI-310-Group-11.git` 

**Note**: Our data is fairly large, and cloning it may result in an issue with having the `.parquet` data on your local. The scripts will run and still produce the correct data files needed. 

### Analysis 

1. Clear any previous analysis done by entering the following statement on the command line.

` docker-compose run --rm analysis-env make clean` 

2. Run the analysis by entering this:

` docker-compose run --rm analysis-env make all` 

The final report can be found as `main_report.html` in the `reports` folder, the images in the `images` folder and the data in the `data` folder.

**Note**: Since the data was downloaded off of the website in `json` format, we do not have a script that reads the data off the web. The data was downloaded as the website structure does not allow for reading it off the web. 

## Additional Notes

### Working on JupyterLab

If you are working with the project on JupyterLab, follow the steps below. 

1. After doing the steps in Setup section, navigate to the root of this project on your computer as follows:

`cd DSCI-310-Group-11-Cricket-Analysis`

2. Enter the following command to setup the virtual container:

`docker-compose up`

3. Once the command has run, you will receive options to launch JupyterLab through different URLs. Copy and paste the one starting with ` http://127.0.0.1:8888/lab?token`. You will now be able to work in the JupyterLab IDE with all the files used in the analysis visible in the file browser pane.
4. Shut down the container after using it by typing `Ctrl + C` in the terminal.  Clean the container up by typing `docker-compose rm` in the terminal.

### Adding Dependencies

To add any other dependencies to the analysis: 

1. Create a new branch and add the dependency to the Dockerfile file.
2. Re-build the new image locally to make sure everything runs properly. We recommend using the tag `dsci310_group11:latest` when building.
3. Push the changes to GitHub. Since we have built our GitHub actions workflow, the new image will be pushed to DockerHub automatically.
4. Update the image tag on the `docker-compose.yml` file so that it uses the new container image.
5. Open a pull request and merge the new branch with the main branch.


## Licenses
The License was derived from the MIT License. The License and code for building the GitHub Actions Workflow for containerization was derived from the [Dockerfile Practice Repository](https://github.com/ttimbers/dsci310-dockerfile-practice/tree/main)

## Dataset
The data was all sourced from [Cricsheet](https://cricsheet.org/).
