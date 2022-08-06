# -*-coding:Latin-1 -*

# Imports
import libVoyageur as voy
import sys
import time
import copy
import json

# Get villes from the call
villes = json.loads(sys.argv[1])

# Initialise chemin
order = voy.Order(villes)
chemin = voy.Chemin(order, villes)

# Build and launch the loop
loop = voy.Loop(villes)
start = time.monotonic() # Time of the beginning of the computation of the first guess
loop.firstGuess()
firstGuess = copy.copy(loop.reference.etapes.indices)
lengthFirstGuess = loop.referenceLongueur
middle = time.monotonic() # Time of the end of the computation of the first guess - beginning of the computation of the optimum

# Loop
loop.loopDFS(chemin)
optimum = [loop.reference.etapes.indices, loop.referenceLongueur]
end = time.monotonic() # Time of the end of the computation of the optimum

# Provide result in JSON format for the multithread run
outputs = json.dumps({"villes":villes,"timingFirstGuess":str(round(middle-start, 3)),"firstGuess":firstGuess,"lengthFirstGuess":lengthFirstGuess,"timeOfExploration":str(round(end-middle, 3)),"optimum":optimum[0],"lengthOptimum":optimum[1]})
print(outputs)