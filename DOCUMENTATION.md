# VoyageurDeCommerce
Tool to solve the travelling salesman problem.

## Dependencies
The code is made to run on Python 3.

The library libVoyageur.py has the following dependencies :
- math
- numpy
- array
- copy

## Assumptions
The library is based on the following assumptions:
- the distance between two towns can simply be computed as the euclidian distance between their canonical coordinates,
- the starting point can be any town,
- the end point can be any town,
- the path must contain every town once and only one.

## Input
The input must be a list of towns.

Towns are defined as a list of two numerical values.

## Output
The loop does not provide output.

The outcome of the optimization is the state of the object of class Loop.

The main values that can be fetched are :
- loop.reference.etapes.indices, which is a list of the indices of the towns of the input, sorted to provide an optimized path
- loop.referenceLongueur, is the length of the optimized path.