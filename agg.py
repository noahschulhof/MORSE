import argparse
import os
import pandas as pd

argParser = argparse.ArgumentParser()

argParser.add_argument('-m', '--match', type = str, help = 'String to match solution files')
argParser.add_argument('-s', '--sols_dir', type = str, help = 'Filepath to solutions directory')
argParser.add_argument('-o', '--output_filepath', type = str, help = 'Output filepath')
argParser.add_argument('-c', '--cleanup', action = 'store_true', help = 'Flag - remove individual solution files')
argParser.add_argument('-v', '--var_names', action = 'store_true', help = 'Flag - store variable names')

args = argParser.parse_args()

# Check that string match is provided
if not args.match:
    raise Exception('No match string provided.')

# Generate output filepath name if not provided
if not args.output_filepath:
    args.output_filepath = f'{args.match}_sols.csv'

# Initialize an empty Pandas DataFrame to which solutions will later be appended
sols = pd.DataFrame()

# Iterate through files in solutions directory
for file in os.listdir(args.sols_dir):

    # Check if string match is in filepath
    if args.match in file:
        if args.sols_dir:
            filepath = os.path.join(args.sols_dir, file)
        else:
            filepath = file

        # Check that filepath/format is valid
        try:
            sol = pd.read_csv(filepath)
        except:
            print(f'Omitting matched file {filepath} - invalid file format')
            continue

        # Check that variable names are consistent with the aggregated DataFrame     
        try:
            pivoted = pd.DataFrame([sol['Value'].tolist()], columns = sol['VarName'].tolist())

            sols = pd.concat([sols, pivoted])
        except:
            print(f'Omitting matched file {filepath} - inconsistent variable names')
            continue
        
        # Remove individual solution files is cleanup flag is specified
        if args.cleanup:
            os.remove(filepath)

# Write variable names to output file if var_names flag is specified
if args.var_names:
    sols.to_csv(args.output_filepath, index = False)
else:
    sols.to_csv(args.output_filepath, header = False, index = False)