# -*-coding:Latin-1 -*

# Imports
import math
import numpy as np
import array as arr
import copy

class Order:
    """Definition d'un ordre de villes etapes"""

    # Constructor
    def __init__(self, villes):
        self.villes = villes
        self.indices = []
        self.length = 0
        self.remainingIndices = arr.array('I', np.arange(0, len(self.villes)))

    def __copy__(self):
        newOne = Order(self.villes)
        newOne.indices = copy.copy(self.indices)
        newOne.length = self.length
        newOne.remainingIndices = copy.copy(self.remainingIndices)
        return newOne

    def fillDummy(self):
        self.indices = self.remainingIndices

    def getLastIndex(self):
        return self.indices[len(self.indices)-1]

    def addIndex(self, index):
        if(self.remainingIndices.count(index) > 0):
            self.indices.append(index)
            self.length += 1
            self.remainingIndices.remove(index)

    def removeIndex(self):
        if(len(self.indices) > 0):
            index = self.indices[len(self.indices)-1]
            self.indices.remove(index)
            self.length -= 1
            self.remainingIndices.append(index)
            self.remainingIndices = arr.array('I', sorted(self.remainingIndices))

class Chemin:
    """Definition d'un chemin reliant des villes"""

    # Constructor
    def __init__(self, order, villes):
        self.villes = villes
        self.etapesFixed = Order(self.villes)
        self.etapes = order
        self.distance = 0.0

    # Permits to copy the distance it each time a new chemin is created
    def __copy__(self):
        # Create the new orders that define the chemin
        newEtapes = copy.copy(self.etapes)
        newEtapesFixed = copy.copy(self.etapesFixed)

        # Create a new chemin and assign its orders
        newone = Chemin(newEtapes, self.villes)
        newone.etapesFixed = newEtapesFixed
        newone.distance = self.distance

        return newone

    def longueur(self):
        somme = 0.0
        
        # Loop on the etapesFixed
        for i in range(1, len(self.etapesFixed.indices)):
            ville1 = self.villes[self.etapesFixed.indices[i-1]]
            ville2 = self.villes[self.etapesFixed.indices[i]]
            dx = ville1[0] - ville2[0]
            dy = ville1[1] - ville2[1]
            buff = math.sqrt(dx * dx + dy * dy)
            somme += buff
        
        # Handle transition between etapesFixed and etapes
        if len(self.etapes.indices) > 0 and len(self.etapesFixed.indices) > 0:
            ville1 = self.villes[self.etapesFixed.indices[len(self.etapesFixed.indices)-1]]
            ville2 = self.villes[self.etapes.indices[0]]
            dx = ville1[0] - ville2[0]
            dy = ville1[1] - ville2[1]
            buff = math.sqrt(dx * dx + dy * dy)
            somme += buff
            
        # Loop on the etapes
        for i in range(1, len(self.etapes.indices)):
            ville1 = self.villes[self.etapes.indices[i-1]]
            ville2 = self.villes[self.etapes.indices[i]]
            dx = ville1[0] - ville2[0]
            dy = ville1[1] - ville2[1]
            buff = math.sqrt(dx * dx + dy * dy)
            somme += buff
            
        return somme

    def addLongueur(self):
        self.distance = self.longueur()

    def profondeur(self):
        return len(self.etapes.indices)

    def addEtape(self, etape):
        # Ajoute l'étape au chemin
        self.etapes.addIndex(etape)

        # Update la longueur du chemin
        if(len(self.etapes.indices) + len(self.etapesFixed.indices) > 1):
            i = len(self.etapes.indices) - 1
            if(i == 0):
                j = len(self.etapesFixed.indices)-1
                ville1 = self.villes[self.etapesFixed.indices[j]]
            else:
                ville1 = self.villes[self.etapes.indices[i-1]]
            ville2 = self.villes[self.etapes.indices[i]]
            dx = ville1[0] - ville2[0]
            dy = ville1[1] - ville2[1]
            buff = math.sqrt(dx * dx + dy * dy)
        
            self.distance += buff

    def addEtapeToFixed(self, etape):
        # Ajoute l'étape au chemin
        self.etapesFixed.addIndex(etape)
        if(etape in self.etapes.remainingIndices):
            self.etapes.remainingIndices.remove(etape)

        # Update la longueur du chemin
        i = len(self.etapesFixed.indices) - 1
        ville1 = self.villes[self.etapesFixed.indices[i-1]]
        ville2 = self.villes[self.etapesFixed.indices[i]]
        dx = ville1[0] - ville2[0]
        dy = ville1[1] - ville2[1]
        buff = math.sqrt(dx * dx + dy * dy)
        
        self.distance += buff

    def removeEtape(self):
        # Update la longueur du chemin
        if(len(self.etapes.indices) + len(self.etapesFixed.indices) > 1):
            i = len(self.etapes.indices) - 1
            if(i == 0):
                j = len(self.etapesFixed.indices)-1
                ville1 = self.villes[self.etapesFixed.indices[j]]
            else:
                ville1 = self.villes[self.etapes.indices[i-1]]
            ville2 = self.villes[self.etapes.indices[i]]
            dx = ville1[0] - ville2[0]
            dy = ville1[1] - ville2[1]
            buff = math.sqrt(dx * dx + dy * dy)

            self.distance -= buff

        # Ajoute l'etape au chemin
        self.etapes.removeIndex()

class Loop:
    """Definition de l'algo d'exploration"""

    # Create the reference
    def __init__(self, villes):
        self.villes = villes
        self.order = Order(self.villes)
        self.reference = Chemin(self.order, self.villes)
        self.reference.etapes.fillDummy()
        self.reference.addLongueur()
        self.referenceLongueur = self.reference.distance

    def __copy__(self):
        newLoop = Loop(self.villes)
        newLoop.order = copy.copy(self.order)
        newLoop.reference = copy.copy(self.reference)
        newLoop.referenceLongueur = copy.copy(self.referenceLongueur)
        return newLoop

    def firstGuess(self):
        # Initialize quarters
        NW = []
        NE = []
        SW = []
        SE = []

        # Compute the coordinates of the problem.
        maxh = 0; minh = 0; maxv = 0; minv = 0
        for ville in self.villes:
            if ville[0] < minh:
                minh = ville[0]
            if ville[0] > maxh:
                maxh = ville[0]
            if ville[1] < minv:
                minv = ville[1]
            if ville[1] > maxv:
                maxv = ville[1]
        lh = (maxh - minh) / 2.0
        lv = (maxv - minv) / 2.0

        # Fill the quarters
        for ville in self.villes:
            if(ville[0] < lh):
                if(ville[1] < lv):
                    SW.append(ville)
                else:
                    NW.append(ville)
            else:
                if(ville[1] < lv):
                    SE.append(ville)
                else:
                    NE.append(ville)

        # Order each quarter
        firstGuess = Order(self.villes)
        indexNW = sorted(range(len(NW)), key=lambda k: NW[k][0] + NW[k][1])
        for i in indexNW:
            firstGuess.addIndex(self.villes.index(NW[i]))
        indexNE = sorted(range(len(NE)), key=lambda k: NE[k][0] - NE[k][1])
        for i in indexNE:
            firstGuess.addIndex(self.villes.index(NE[i]))
        indexSE = sorted(range(len(SE)), key=lambda k: - SE[k][0] - SE[k][1])
        for i in indexSE:
            firstGuess.addIndex(self.villes.index(SE[i]))
        indexSW = sorted(range(len(SW)), key=lambda k: - SW[k][0] + SW[k][1])
        for i in indexSW:
            firstGuess.addIndex(self.villes.index(SW[i]))
        
        # Update loop
        self.reference = Chemin(firstGuess, self.villes)
        self.referenceLongueur = self.reference.longueur()

    def loopDFS(self, chemin):
        self.endReached = False
        self.lastIndex = -1
        while(not(self.endReached)):
            self.evalDFS(chemin)

    def evalDFS(self, chemin):
        # New reference
        if(len(chemin.etapes.remainingIndices) == 0 and chemin.distance < self.referenceLongueur):
            self.reference = copy.copy(chemin)
            self.referenceLongueur = self.reference.distance

        # End of the loop
        if(len(chemin.etapes.indices) == 0 and self.lastIndex == max(chemin.etapes.remainingIndices)):
            self.endReached = True

        # Next move
        elif(len(chemin.etapes.remainingIndices) > 0 and chemin.distance < self.referenceLongueur and self.lastIndex < max(chemin.etapes.remainingIndices)):
            index = 0
            tryIndex = chemin.etapes.remainingIndices[index]
            while(tryIndex <= self.lastIndex):
                index += 1
                tryIndex = chemin.etapes.remainingIndices[index]
            chemin.addEtape(chemin.etapes.remainingIndices[index])
            self.lastIndex = -2
        else:
            self.lastIndex = chemin.etapes.getLastIndex()
            chemin.removeEtape()

    def loopDFSmultithread(self, chemin, results):
        self.loopDFS(chemin)
        bestChemin = chemin.etapesFixed.indices + self.reference.etapes.indices
        results.append([bestChemin, self.referenceLongueur])
