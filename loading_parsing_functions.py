
import os
import pandas as pd
import json  # Make sure to import json
import pyarrow
import zipfile
import click
from collections import defaultdict

@click.command()
@click.option('--input_folder', type=str,default='data/t20_parquet', help='Path to the parquet folder')
@click.option('--output_file', default='data/cricket_main.parquet', help='Merged main parquet file path.')

def main(input_folder, output_file):
    def parse_cricket_json(file_content, game_id):
        data = json.load(file_content)

        innings = data['innings']
        player_registry = data['info']['registry']['people']
        season = data['info']['season']

        deliveries_data = []

        for inning in innings:
            team_name = inning['team']
            for over in inning['overs']:
                over_number = over['over']
                for delivery in over['deliveries']:
                    batter_id = player_registry.get(delivery['batter'], "Unknown")
                    bowler_id = player_registry.get(delivery['bowler'], "Unknown")
                    non_striker_id = player_registry.get(delivery['non_striker'], "Unknown")
                    wides = delivery.get('extras', {}).get('wides', 0)
                    noballs = delivery.get('extras', {}).get('noballs', 0)
                    legbyes = delivery.get('extras', {}).get('legbyes', 0)
                    byes = delivery.get('extras', {}).get('byes', 0)
                    wicket_info = delivery.get('wickets')
                    wicket = 1 if wicket_info else 0
                    player_out = wicket_info[0]['player_out'] if wicket_info else ""
                    player_out_id = player_registry.get(player_out, "Unknown") if player_out else ""
                    fielders = [wicket_info[0]['fielders'][0]['name'] if wicket_info and 'fielders' in wicket_info[0] else ""]
                    fielders_id = [player_registry.get(fielders[0], "Unknown") if fielders[0] else ""]
                    kind = [wicket_info[0]['kind'] if wicket_info else ""]

                    delivery_info = {
                        "game_id": game_id,
                        "season": season,
                        "team": team_name,
                        "over": over_number,
                        "batter": delivery['batter'],
                        "batter_id": batter_id,
                        "bowler": delivery['bowler'],
                        "bowler_id": bowler_id,
                        "non_striker": delivery['non_striker'],
                        "non_striker_id": non_striker_id,
                        "wides": wides,
                        "noballs": noballs,
                        "legbyes": legbyes,
                        "byes": byes,
                        "wicket": wicket,
                        "player_out": player_out,
                        "player_out_id": player_out_id,
                        "fielders_name": fielders[0],
                        "fielders_id": fielders_id[0],
                        "wicket_type": kind[0],
                        "runs_batter": delivery['runs']['batter'],
                        "runs_extras": delivery['runs']['extras'],
                        "runs_total": delivery['runs']['total']
                    }
                    deliveries_data.append(delivery_info)

    def process_cricket_jsons(zip_file_path, output_folder):
        """
        Reads JSON files from a zipped archive, converts each to a DataFrame using parse_cricket_json,
        and saves the DataFrame as a Parquet file in the output folder. Prints the progress status,
        and skips files that cause issues.

        Args:
        - zip_file_path: Path to the zip archive containing JSON files.
        - output_folder: Path to the folder where Parquet files should be saved.
        """
        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        with zipfile.ZipFile(zip_file_path, 'r') as z:
            json_files = [f for f in z.namelist() if f.endswith('.json')]
            total_files = len(json_files)
            processed_files = 0

            for filename in json_files:
                # Extract game_id from the filename, assuming filename format is 'game_01.json'
                game_id = filename.split('/')[-1].split('.')[0]

                try:
                    with z.open(filename) as file_content:
                        # Pass the file-like object and game_id to the parsing function
                        df = parse_cricket_json(file_content, game_id)
                        df = add_columns(df)

                        output_file_name = game_id + ".parquet"
                        output_file_path = os.path.join(output_folder, output_file_name)
                        
                        # Save the DataFrame as a Parquet file
                        df.to_parquet(output_file_path, index=False)

                except Exception as e:
                    continue 
                
                processed_files += 1
                progress_percentage = (processed_files / total_files) * 100
                print(f"Progress: {progress_percentage:.2f}%")

    def add_columns(df):

        # add the over for each team specifically
        df['team_over'] = df['team'] + "_" + df['over'].astype('str')

        # indicate which ball it is in the over
        df['over_ball'] = df.groupby('team_over').cumcount() + 1

        # list the teams in specific game
        teams = df['team'].unique() 

        # create inning column
        df['inning'] = [1 if x == teams[0] else 2 for x in df['team']]

        # calculate runs so far in innings
        df['runs_cumulative'] = df.groupby('inning')['runs_total'].cumsum()

        # check if it is powerplay 
        df['powerplay'] = [1 if x <= 5 else 0 for x in df['over']]
        
        df['powerplay'] = df['powerplay'].astype('object')
        df['inning'] = df['inning'].astype('object')
        
        return df
    
    def determine_majority_dtypes(parquet_files, input_folder):
        """
        Determine the majority data type for each column across a sample of Parquet files.
        
        Args:
        - parquet_files: List of parquet file names.
        - input_folder: Directory containing the Parquet files.
        - sample_size: Number of files to sample for determining data types.
        
        Returns:
        A dictionary mapping column names to their majority data type.
        """
        sample_size=21
        dtype_votes = defaultdict(lambda: defaultdict(int))
        
        for filename in parquet_files[:sample_size]:
            file_path = os.path.join(input_folder, filename)
            try:
                df = pd.read_parquet(file_path)
                # Corrected iteration over DataFrame dtypes
                for col, dtype in df.dtypes.items():
                    dtype_votes[col][str(dtype)] += 1
            except Exception as e:
                print(f"Error processing {filename}: {e}")
        
        # Determine majority data type for each column
        majority_dtypes = {}
        for col, votes in dtype_votes.items():
            majority_dtypes[col] = max(votes, key=votes.get)
    
        return majority_dtypes

    def apply_dtypes_and_concatenate(parquet_files, input_folder, dtype_mapping):
        """
        Apply data type mapping to DataFrames, handle specific cases, and concatenate them.
        
        Args:
        - parquet_files: List of parquet file names.
        - input_folder: Directory containing the Parquet files.
        - dtype_mapping: Data type mapping to enforce on the DataFrames.
        
        Returns:
        A single concatenated DataFrame with enforced data types.
        """
        dfs = []
        for filename in parquet_files:
            file_path = os.path.join(input_folder, filename)
            try:
                df = pd.read_parquet(file_path)
                # Apply general dtype mapping
                for col, dtype_str in dtype_mapping.items():
                    if col in df.columns:
                        df[col] = df[col].astype(dtype_str, errors='ignore')
                # Handle specific cases
                if 'season' in df.columns:
                    df['season'] = df['season'].astype(str)  # Convert 'season' to string
                dfs.append(df)
            except Exception as e:
                print(f"Skipping {filename} due to an error: {e}")
        
        if dfs:
            merged_df = pd.concat(dfs, ignore_index=True)
            # Additional specific dtype adjustments if necessary
            return merged_df
        else:
            print("No valid Parquet files were found or successfully read.")
            return pd.DataFrame()

    """
    Merges all Parquet files in the specified input folder into a single Parquet file,
    using a majority vote on data types from the first 20 files.

    Args:
    - input_folder: Path to the folder containing Parquet files to merge.
    - output_file: Full path and name of the output Parquet file.
    """

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