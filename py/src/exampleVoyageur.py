# -*-coding:Latin-1 -*

# Imports
import libVoyageur as voy
import threading as thr
import random
import time
import json
import copy

# Generate town with coordinates
dimh = 100
dimv = 100
villes = []
for i in range(6):
    x = int(random.random() * dimh)
    y = int(random.random() * dimv)
    position = [x, y]
    villes.append(position)

###############
# MONO-THREAD #
###############

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

################
# MULTI-THREAD #
################

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

# Create vector of threads
results = []
numberOfThreads = len(chemin.etapes.remainingIndices)
threads = [thr.Thread() for i in range(numberOfThreads)]
for i in range(numberOfThreads):
   newChemin = copy.copy(chemin)
   newChemin.addEtapeToFixed(chemin.etapes.remainingIndices[i])
   newLoop = copy.copy(loop)
   threads[i] = thr.Thread(None, newLoop.loopDFSmultithread, args=(newChemin, results, ))

# Launch threads
for thread in threads:
   thread.start()

# Join threads
for thread in threads:
   thread.join()

# Compare the results of different threads
optimum = results[0]
for result in results:
    if result[1] < optimum[1]:
        optimum = result

end = time.monotonic() # Time of the end of the computation of the optimum

# Provide result in JSON format for the multithread run
outputs = json.dumps({"villes":villes,"timingFirstGuess":str(round(middle-start, 3)),"firstGuess":firstGuess,"lengthFirstGuess":lengthFirstGuess,"timeOfExploration":str(round(end-middle, 3)),"optimum":optimum[0],"lengthOptimum":optimum[1]})
print(outputs)
