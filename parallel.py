import argparse
import ast

argParser = argparse.ArgumentParser()

argParser.add_argument('-f', '--script_filepath', type = str, help = 'Filepath to parallelized script')
argParser.add_argument('-i', '--instance_filepath', type = str, help = 'Filepath to instance .mps file')
argParser.add_argument('-s', '--sol_filepath', type = str, default = None, help = 'Filepath to solution files')
argParser.add_argument('-n', '--num_runs', type = int, help = 'Number of runs to be executed')
argParser.add_argument('-e', '--executable', type = str, default = 'python3', help = 'Python executable')
argParser.add_argument('-r', '--seeds_filepath', type = str, default = None, help = 'Filepath to csv/txt/tsv file with one seed per line')
argParser.add_argument('-p', '--perturbation_filepath', type = str, default = None, help = 'Filepath to csv file with one perturbation vector per line')

args = argParser.parse_args()


# Handle missing arguments
if not args.script_filepath or not args.instance_filepath or not args.num_runs:
    missing = ', '.join([f'{short}/--{arg}' for short, arg in zip(['-f', '-i', '-n'], ['script_filepath', 'instance_filepath', 'num_runs']) if not getattr(args, arg)])

    raise Exception(f'Missing required argument(s) {missing}')


# Parse perturbations if filepath is supplied
if args.perturbation_filepath:
    try:
        with open(args.perturbation_filepath, 'r') as r:
            perturbations = r.read().split('\n')

        if '' in perturbations:
            perturbations.remove('')

        # Check that number of perturbations and number of runs are equivalent
        assert len(perturbations) == args.num_runs, f'Found {len(perturbations)} perturbation vectors in {args.perturbation_filepath}, expected {args.num_runs}.'
        
        
    except:
        raise Exception(f'Invalid perturbation file: {args.perturbation_filepath}')
    

# Parse random seeds if filepath is supplied
if args.seeds_filepath:
    try:
        with open(args.seeds_filepath, 'r') as f:
            seeds = f.read().split('\n')

        if '' in seeds:
            seeds.remove('')

        # Check that number of random seeds and number of runs are equivalent
        assert len(seeds) == args.num_runs, f'Seeds vector has length {len(seeds)}, expected length {args.num_runs}.'

    except:
        raise Exception('Seeds vector must be a quote-enclosed iterable.')


# Write parallelizable script to specified filepath
with open(args.script_filepath, 'w') as w:
    if args.sol_filepath:

        root = args.sol_filepath.split('.')[0]

        if args.perturbation_filepath:
            if args.seeds_filepath:
                w.write('\n'.join([f'{args.executable} solve.py -i {args.instance_filepath} -s {root}_{i}.csv -r {seed} -p {args.perturbation_filepath} -l {i + 1}' for i, seed in enumerate(seeds)]))
            else:
                w.write('\n'.join([f'{args.executable} solve.py -i {args.instance_filepath} -s {root}_{i}.csv -p {args.perturbation_filepath} -l {i + 1}' for i in range(len(perturbations))]))
        
        elif args.seeds_filepath:
            w.write('\n'.join([f'{args.executable} solve.py -i {args.instance_filepath} -s {root}_{i}.csv -r {seed}' for i, seed in enumerate(seeds)]))

        else:
            w.write('\n'.join([f'{args.executable} solve.py -i {args.instance_filepath} -s {root}_{i}.csv' for i in range(args.num_runs)]))

    else:
        if args.perturbation_filepath:
            if args.seeds_filepath:
                w.write('\n'.join([f'{args.executable} solve.py -i {args.instance_filepath} -r {seed} -p {args.perturbation_filepath} -l {i + 1}' for i, seed in enumerate(seeds)]))
            else:
                w.write('\n'.join([f'{args.executable} solve.py -i {args.instance_filepath} -p {args.perturbation_filepath} -l {i + 1}' for i in range(len(perturbations))]))
        
        elif args.seeds_filepath:
            w.write('\n'.join([f'{args.executable} solve.py -i {args.instance_filepath} -r {seed}' for seed in seeds]))

        else:
            w.write('\n'.join([f'{args.executable} solve.py -i {args.instance_filepath}' for i in range(args.num_runs)]))