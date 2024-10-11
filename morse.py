import gurobipy as gp
from gurobipy import GRB, quicksum
import random as rm
import pandas as pd
from collections.abc import Iterable

class Morse():
    def __init__(self, instance, seed = None, weights = None):
        self.instance = instance

        self.orig_model = gp.read(instance)
        self.orig_obj = self.orig_model.getObjective()
        self.orig_obj_coeffs = [self.orig_obj.getCoeff(i) for i in range(self.orig_obj.size())]

        self.model = self.orig_model.copy()
        self.obj_function = self.model.getObjective()
        self.obj_vars = [self.obj_function.getVar(i) for i in range(self.obj_function.size())]
        self.obj_coeffs = [self.obj_function.getCoeff(i) for i in range(self.obj_function.size())]

        self.contains_continuous = any([var.vtype == 'C' for var in self.obj_vars])
        self.integer_coeffs = all([int(coeff) == coeff for coeff in self.obj_coeffs])

        if seed:
            assert isinstance(seed, int), 'Seed must be an integer.'

        self.seed = seed
        

        if weights:
            assert not isinstance(weights, str), 'Perturbation vector must be a non-string iterable'
            assert isinstance(weights, Iterable), 'Perturbation vector is not iterable.'
            assert len(weights) == len(self.obj_vars), f'Perturbation vector has length {len(weights)}, expected length {len(self.obj_vars)}.'
            assert all(isinstance(x, (int, float)) for x in weights), 'Perturbation vector elements must be float or int'
        
        self.weights = weights
    

    def generate_epsilon(self) -> float:
        ''' Generate value of epsilon.
        
        Returns:
        -------
            epsilon: value of epsilon to be used for the perturbation
        '''

        # Define S as the sum of max(abs(upper bound), abs(lower bound)) for all binary/integer variables in the objective function
        S = sum([abs(coeff) * max(abs(var.ub), abs(var.lb)) for coeff, var in zip(self.obj_coeffs, self.obj_vars) if var.vtype != 'C'])

        # Define epsilon as 1/2S - note that this is a more 'conservative' value of epsilon than is used in the proof in the manuscript
        return 1 / (2 * S)


    def parse_objective(self, epsilon) -> None:
        ''' Apply perturbation to objective function and update model's objective.
        
        Args:
        -------
            epsilon: value of epsilon
        '''
        if not self.weights:
            if self.seed:
                rm.seed(self.seed)

            # Generate random weights for binary/integer variables, generate uniform weights of 1 for continuous variables
            self.weights = [rm.uniform(1 - epsilon, 1 + epsilon) if var.vtype != 'C' else 1 for var in self.obj_vars]

        # Map weights to coefficients in the objective function, set new model objective
        self.model.setObjective(quicksum(weight * coeff * var for weight, coeff, var in zip(self.weights, self.obj_coeffs, self.obj_vars)))
    

    def solve(self) -> None:
        ''' Generate and apply perturbation to the model, optimize the resulting instance.
        '''

        if self.seed:
            # Set Gurobi seed
            self.model.setParam('Seed', self.seed)

        # Generate value of epsilon for perturbation
        epsilon = self.generate_epsilon()

        # Apply perturbation to model objective function
        self.parse_objective(epsilon)

        # Optimize the perturbed model
        self.model.optimize()

        # If the objective function contains continuous variables, check that the solution found with MORSE is optimal for the original problem
        if self.contains_continuous or not self.integer_coeffs:
            self.orig_model.optimize()
            orig_obj_val = self.orig_model.ObjVal

            morse_obj_val = sum([var.X * coeff for var, coeff in zip(self.obj_vars, self.orig_obj_coeffs)])
            
            relative_diff = abs(morse_obj_val - orig_obj_val) / abs(orig_obj_val)

            if relative_diff > self.orig_model.Params.OptimalityTol:
                raise Exception('MORSE solution is not optimal for the original problem.')
    

    def record_sols(self, filepath: str) -> None:
        ''' Write objective function variables, values, and weights to csv file.

        Args:
        -------
            filepath: filepath to csv file
        '''

        # Raise error if the model is not optimized
        if not self.model.status == GRB.OPTIMAL:
            raise Exception('Model is not optimized')

        # Write dataframe with variable names, values, and weights, to csv at user's specified filepath
        pd.DataFrame({'VarName': [v.VarName for v in self.obj_vars],
                      'Value': [round(v.X) if v.vtype != 'C' else v.X for v in self.obj_vars],
                      'Weight': self.weights}).to_csv(filepath, index = False)