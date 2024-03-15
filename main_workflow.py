import click
import os
import pandas as pd
import loading_parsing_functions as lpf
import model_workflows as Model_wf
import EDA_workflows as EDA_wf


@click.command()
@click.option('--json_zip_path', default='data/t20s_json.zip', help='Path to the input JSON zip file.')
@click.option('--parquet_output_folder', default='data/t20_parquet', help='Output folder for parquet files.')
@click.option('--cricket_main_parquet', default='data/cricket_main.parquet', help='Merged main parquet file path.')
@click.option('--train_data_csv', default='./data/data_for_quarto/train_data.csv', help='Path to save the training data CSV.')
@click.option('--hyperparams_csv', default='./data/data_for_quarto/Hyperparameter.csv', help='Path to save the hyperparameters CSV.')
@click.option('--image_folder', default='images', help='Folder path for saving images.')
def main(json_zip_path, parquet_output_folder, cricket_main_parquet, train_data_csv, hyperparams_csv, image_folder):
    # Ensure necessary directories exist
    for path in [parquet_output_folder, os.path.dirname(train_data_csv), os.path.dirname(hyperparams_csv), image_folder]:
        os.makedirs(path, exist_ok=True)

    # Loading data and combining into a master file
    lpf.process_cricket_jsons(json_zip_path, parquet_output_folder)
    lpf.merge_parquet_files(parquet_output_folder, cricket_main_parquet)

    # Split into training and testing
    X_train, X_test, y_train, y_test = Model_wf.split_data_from_parquet(cricket_main_parquet)

    # Save Training Data
    train_data = Model_wf.save_training_data(X_train, y_train, train_data_csv)

    # EDA Plots
    EDA_wf.var_distribution_plot(train_data, f'{image_folder}/chart1.png')
    EDA_wf.var_distribution_plot2(train_data, f'{image_folder}/chart2.png')
    EDA_wf.get_correlation_heatmap(train_data, f'{image_folder}/chart3.png')
    EDA_wf.wicket_by_over_barchart(train_data, f'{image_folder}/chart4.png')
    EDA_wf.wicket_per_over_bar(train_data, f'{image_folder}/chart5.png')
    EDA_wf.wicket_density_histogram(train_data, f'{image_folder}/chart6.png')

    # Model Building and Evaluation
    Model_wf.tune_and_save_hyperparams(X_train, y_train, hyperparams_csv)
    final_pipe = Model_wf.prepare_chosen_model(X_train, y_train, C=10**0.5)
    Model_wf.evaluate_final_model(final_pipe, X_test, y_test, f'{image_folder}/chart7.png')

if __name__ == '__main__':
    main()
