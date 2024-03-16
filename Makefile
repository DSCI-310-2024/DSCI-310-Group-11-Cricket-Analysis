all:data/data_for_quarto/train_data.csv \
	images/chart1.png \
	images/chart2.png \
	images/chart3.png \
	images/chart4.png \
	images/chart5.png \
	images/chart6.png \
	data/data_for_quarto/Hyperparameter.csv \
	images/chart7.png


run_docker: 
	docker run --rm -v $(PWD):/home/jovyan dsci310_group11:latest bash

data/data_for_quarto/train_data.csv: 
	$(MAKE) run_docker
	python loading_parsing_functions.py

images/chart1.png images/chart2.png images/chart3.png images/chart4.png images/chart5.png images/chart6.png: 
	$(MAKE) run_docker
	python EDA_workflows.py

data/data_for_quarto/Hyperparameter.csv images/chart7.png: 
	$(MAKE) run_docker
	python model_workflows.py

qmd/main_report.html:
	quarto render qmd/cricket_wicket_probability_prediction.qmd --to html

qmd/main_report.pdf:
	quarto render qmd/cricket_wicket_probability_prediction.qmd --to pdf

clean:
	rm -rf data/data_for_quarto/*
	rm -rf images/*
	rm -rf qmd/main_report.html