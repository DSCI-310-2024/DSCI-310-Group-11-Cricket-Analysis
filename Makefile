all: data/cricket_main.parquet \
		data/data_for_quarto/train_data.csv \
		images/chart1.png \
		images/chart2.png \
		images/chart3.png \
		images/chart4.png \
		images/chart5.png \
		images/chart6.png \
		images/chart7.png \
		reports/main_report.html


data/cricket_main.parquet: scripts/loading_parsing_functions.py data/t20_parquet
	python scripts/loading_parsing_functions.py \
		--input_folder=data/t20_parquet \
		--output_file=data/cricket_main.parquet

data/data_for_quarto/train_data.csv images/chart1.png images/chart2.png images/chart3.png images/chart4.png images/chart5.png images/chart6.png: 
	python scripts/EDA_workflows.py \
		--parquet_path=data/cricket_main.parquet \
		--save_path=images\
		--save_table_path=data/data_for_quarto

images/chart7.png:
	python scripts/model_workflows.py \
		--parquet_path=data/cricket_main.parquet \
		--save_image_path=images

reports/main_report.html:
	quarto render reports/main_report.qmd --to html

clean:
	rm -rf data/cricket_main.parquet
	rm -rf data/data_for_quarto/*
	rm -rf images/*
	rm -rf reports/main_report.html