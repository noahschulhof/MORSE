import argparse
import ast

argParser = argparse.ArgumentParser()

argParser.add_argument('-f', '--script_filepath', type = str, help = 'Filepath to parallelized script')
argParser.add_argument('-i', '--instance_filepath', type = str, help = 'Filepath to instance .mps file')
argParser.add_argument('-s', '--sol_filepath', type = str, default = None, help = 'Filepath to solution files')
argParser.add_argument('-n', '--num_runs', type = int, help = 'Number of runs to be executed')
argParser.add_argument('-e', '--executable', type = str, default = 'python3', help = 'Python executable')
argParser.add_argument('-r', '--random_seeds', type = str, default = None, help = 'Quote-enclosed iterable of random seeds')
argParser.add_argument('-p', '--perturbation_filepath', type = str, default = None, help = 'Filepath to csv file with one perturbation vector per line')

args = argParser.parse_args()

if not args.script_filepath or not args.instance_filepath or not args.num_runs:
    raise Exception('Missing required argument')

if args.perturbation_filepath:
    try:
        with open(args.perturbation_filepath, 'r') as f:
            perturbations = f.read().split('\n')

        if '\n' in perturbations:
            perturbations.remove('\n')

        assert len(perturbations) == args.num_runs, f'Found {len(perturbations)} perturbation vectors in {args.perturbation_filepath}, expected {args.num_runs}.'
        
        
    except:
        raise Exception(f'Invalid perturbation file: {args.perturbation_filepath}')
    
if args.random_seeds:
    try:
        seeds = ast.literal_eval(args.random_seeds)
        assert len(seeds) == args.num_runs, f'Seeds vector has length {len(seeds)}, expected length {args.num_runs}.'
    except:
        raise Exception('Seeds vector must be a quote-enclosed iterable.')

with open(args.script_filepath, 'w') as f:
    if args.sol_filepath:

        root = args.sol_filepath.split('.')[0]

        if args.perturbation_filepath:
            if args.random_seeds:
                f.write('\n'.join([f'{args.executable} solve.py -i {args.instance_filepath} -s {root}_{i}.csv -r {seed} -p "{weights}"' for i, (seed, weights) in enumerate(zip(seeds, perturbations))]))
            else:
                f.write('\n'.join([f'{args.executable} solve.py -i {args.instance_filepath} -s {root}_{i}.csv -p "{weights}"' for i, weights in enumerate(perturbations)]))
        
        elif args.random_seeds:
            f.write('\n'.join([f'{args.executable} solve.py -i {args.instance_filepath} -s {root}_{i}.csv -r {seed}' for i, seed in enumerate(seeds)]))

        else:
            f.write('\n'.join([f'{args.executable} solve.py -i {args.instance_filepath} -s {root}_{i}.csv' for i in range(args.num_runs)]))

    else:
        if args.perturbation_filepath:
            if args.random_seeds:
                f.write('\n'.join([f'{args.executable} solve.py -i {args.instance_filepath} -r {seed} -p "{weights}"' for seed, weights in zip(seeds, perturbations)]))
            else:
                f.write('\n'.join([f'{args.executable} solve.py -i {args.instance_filepath} -p "{weights}"' for weights in perturbations]))
        
        elif args.random_seeds:
            f.write('\n'.join([f'{args.executable} solve.py -i {args.instance_filepath} -r {seed}' for seed in seeds]))

        else:
            f.write('\n'.join([f'{args.executable} solve.py -i {args.instance_filepath}' for i in range(args.num_runs)]))

    f.close()