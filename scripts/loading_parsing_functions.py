
import os
import pandas as pd
import json  # Make sure to import json
import pyarrow
import zipfile
import click
from collections import defaultdict
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.loading_parsing_functions import * 

@click.command()
@click.option('--input_folder', type=str,default='../data/t20_parquet', help='Path to the parquet folder')
@click.option('--output_file', default='../data/cricket_main.parquet', help='Merged main parquet file path.')

def main(input_folder, output_file):
    """
    Merges all Parquet files in the specified input folder into a single Parquet file,
    using a majority vote on data types from the first 20 files.

    Args:
    - input_folder: Path to the folder containing Parquet files to merge.
    - output_file: Full path and name of the output Parquet file.
    """

    #convert json files into Parquest file 
    process_cricket_jsons("data/t20s_json.zip", input_folder)

    # Ensure the input folder exists
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)  # This creates the input_folder if it does not exist
    
    # Ensure the output directory (for the output_file) exists
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    parquet_files = [f for f in os.listdir(input_folder) if f.endswith('.parquet')]
    
    # Step 1: Determine the majority data type for each column
    dtype_mapping = determine_majority_dtypes(parquet_files, input_folder)
    
    # Step 2: Apply data types and concatenate all files
    merged_df = apply_dtypes_and_concatenate(parquet_files, input_folder, dtype_mapping)
    
    if not merged_df.empty:
        # Save the merged DataFrame to the specified output Parquet file
        merged_df.to_parquet(output_file, index=False)
        print(f"Merged Parquet file saved as: {output_file}")
    else:
        print("Failed to merge Parquet files.")

if __name__ == '__main__':
    main()