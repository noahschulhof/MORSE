import random
import statistics

def compute_average_hamming(current_sol, other_sols):
    return(statistics.mean([len([x for x, y in zip(current_sol, other_sol) if x != y]) for other_sol in other_sols]))

def choose_greedy(solution_list, subset_size):
    random.seed(23456)
    
    chosen_sols = [solution_list.pop(random.randint(0, len(solution_list) - 1))]
    for i in range(subset_size - 1):
        hamming_averages = []
        for sol in solution_list:
            hamming_averages.append(compute_average_hamming(sol, chosen_sols))
        chosen_sols.append(solution_list.pop(hamming_averages.index(max(hamming_averages))))
    return(chosen_sols)