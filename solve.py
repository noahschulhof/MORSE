from morse import *
import argparse
import ast

argParser = argparse.ArgumentParser()

argParser.add_argument('-i', '--instance_filepath', type = str, help = 'Filepath to instance .mps file')
argParser.add_argument('-s', '--sol_filepath', type = str, default = None, help = 'Filepath to solution file')
argParser.add_argument('-r', '--random_seed', type = int, default = None, help = 'Seed for random weights (if perturbation vector is not supplied) and Gurobi')
argParser.add_argument('-p', '--perturbation_vector', type = str, default = None, help = 'Quote-enclosed iterable to be used as perturbation vector')

args = argParser.parse_args()

if args.perturbation_vector:
    try:
        args.perturbation_vector = [float(x) for x in ast.literal_eval(args.perturbation_vector)]
    except:
        raise Exception('Perturbation vector must be a quote-enclosed iterable.')

m = Morse(args.instance_filepath, args.random_seed, args.perturbation_vector)

m.solve()

if args.sol_filepath:
    m.record_sols(args.sol_filepath)