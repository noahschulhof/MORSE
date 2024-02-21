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


if not args.match:
    raise Exception('No match string provided.')


if not args.output_filepath:
    args.output_filepath = f'{args.match}_sols.csv'

sols = pd.DataFrame()

for file in os.listdir(args.sols_dir):
    if args.match in file:
        if args.sols_dir:
            filepath = os.path.join(args.sols_dir, file)
        else:
            filepath = file

        try:
            sol = pd.read_csv(filepath)
        except:
            print(f'Omitting matched file {filepath} - invalid file format')
            continue
            
        try:
            pivoted = pd.DataFrame([sol['Value'].tolist()], columns = sol['VarName'].tolist())

            sols = pd.concat([sols, pivoted])
        except:
            print(f'Omitting matched file {filepath} - inconsistent variable names')
            continue

        if args.cleanup:
            os.remove(filepath)

if args.var_names:
    sols.to_csv(args.output_filepath, index = False)
else:
    sols.to_csv(args.output_filepath, header = False, index = False)