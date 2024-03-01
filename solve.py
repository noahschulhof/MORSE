from morse import *
import argparse

argParser = argparse.ArgumentParser()

argParser.add_argument('-i', '--instance_filepath', type = str, help = 'Filepath to instance .mps file')
argParser.add_argument('-s', '--sol_filepath', type = str, default = None, help = 'Filepath to solution file')
argParser.add_argument('-r', '--random_seed', type = int, default = None, help = 'Seed for random weights (if perturbation vector is not supplied) and Gurobi')
argParser.add_argument('-p', '--perturbation_filepath', type = str, default = None, help = 'Filepath to csv file with one perturbation vector per line')
argParser.add_argument('-l', '--perturbation_line', type = int, default = 1, help = 'Line in perturbation file on which the perturbation is found [default=1].')

args = argParser.parse_args()


if args.perturbation_filepath:
    # Read in perturbation file
    try:
        with open(args.perturbation_filepath, 'r') as f:
            perturbations = f.read().split('\n')
    except:
        raise Exception('Invalid perturbation file.')
    
    # Slice specified line from perturbation file
    try:
        pert = perturbations[args.perturbation_line - 1]
    except:
        raise Exception(f'Specified line {args.perturbation_line} not found in perturbation file.')
    
    # Convert perturbation string to iterable
    try:
        pert = pert.split(',')
    except:
        raise Exception('Invalid perturbation file format, expected comma-separated values.')
    
    # Cast perturbation values to float
    try:
        pert = [float(x) for x in pert]
    except:
        raise Exception('Perturbation entries must be float or int.')
    
else:
    pert = None


# Create an instance of the MORSE class
m = Morse(args.instance_filepath, args.random_seed, pert)

# Solve the MORSE instance
m.solve()

if args.sol_filepath:
    # Record optima to solutions filepath
    m.record_sols(args.sol_filepath)