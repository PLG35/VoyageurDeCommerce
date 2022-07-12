# -*-coding:Latin-1 -*

# Imports
import libVoyageur as voy
import random
import copy

class testVoyageur:
    def __init__(self):
        # Initialization
        self.outputs = []
        self.villes = []
        dimh = 100
        dimv = 100
        self.n = 5
        for i in range(self.n):
            x = int(random.random() * dimh)
            y = int(random.random() * dimv)
            position = [x, y]
            self.villes.append(position)

    #########
    # Order #
    #########

    # addIndex
    def testAddIndex(self):
        test = True
        order = voy.Order(self.villes)
        order.addIndex(0)
        if(len(order.indices) != 1):
            self.outputs.append({"class":"order","method":"addIndex(ville)","result":"error","message":"order.indices n'est pas incrémenté correctement"})
            test = False
        if(len(order.remainingIndices) != self.n-1):
            self.outputs.append({"class":"order","method":"addIndex(ville)","result":"error","message":"order.remainingIndices n'est pas mis à jour correctement"})
            test = False
        order.addIndex(0)
        if(len(order.indices) != 1):
            self.outputs.append({"class":"order","method":"addIndex(ville)","result":"error","message":"order.indices n'est pas incrémenté correctement la deuxième fois"})
            test = False
        if(len(order.remainingIndices) != self.n-1):
            self.outputs.append({"class":"order","method":"addIndex(ville)","result":"error","message":"order.remainingIndices n'est pas mis à jour correctement la deuxième fois"})
            test = False
        if(test):
            self.outputs.append({"class":"order","method":"addIndex(ville)","result":"success","message":""})

    # removeIndex
    def testRemoveIndex(self):
        test = True
        order = voy.Order(self.villes)
        order.addIndex(1)
        order.removeIndex()
        if(len(order.indices) != 0):
            self.outputs.append({"class":"order","method":"removeIndex()","result":"error","message":"order.indices n'est pas décrémenté pour un indice valide"})
            test = False
        if(len(order.remainingIndices) != self.n):
            self.outputs.append({"class":"order","method":"removeIndex()","result":"error","message":"order.remainingIndices n'est pas incrémenté pour un indice valide"})
            test = False
        if(test):
            self.outputs.append({"class":"order","method":"removeIndex()","result":"success","message":""})

    # copy
    def testCopyOrder(self):
        test = True
        order = voy.Order(self.villes)
        order.addIndex(1)
        order2 = copy.copy(order)
        if(len(order.indices) != len(order2.indices)):
            self.outputs.append({"class":"order","method":"__copy__(order)","result":"error","message":"order.indices n'est pas copié correctement"})
            test = False
        if(len(order.remainingIndices) != len(order2.remainingIndices)):
            self.outputs.append({"class":"order","method":"__copy__(order)","result":"error","message":"order.remainingIndices n'est pas copié correctement"})
            test = False
        order.addIndex(2)
        if(len(order.indices) == len(order2.indices)):
            self.outputs.append({"class":"order","method":"__copy__(order)","result":"error","message":"order.indices est impacté après la copie"})
            test = False
        if(len(order.remainingIndices) == len(order2.remainingIndices)):
            self.outputs.append({"class":"order","method":"__copy__(order)","result":"error","message":"order.remainingIndices est impacté après la copie"})
            test = False
        if(test):
            self.outputs.append({"class":"order","method":"__copy__(order)","result":"success","message":""})

    ##########
    # Chemin #
    ##########

    # addEtape
    def testAddEtape(self):
        test = True
        order = voy.Order(self.villes)
        chemin = voy.Chemin(order, self.villes)
        chemin.addEtape(0)
        if(len(chemin.etapes.indices) != 1):
            self.outputs.append({"class":"chemin","method":"addEtape(ville)","result":"error","message":"chemin.etapes.indices n'est pas incrémenté correctement"})
            test = False
        if(len(chemin.etapes.remainingIndices) != self.n-1):
            self.outputs.append({"class":"chemin","method":"addEtape(ville)","result":"error","message":"chemin.etapes.remainingIndices n'est pas mis à jour correctement"})
            test = False
        chemin.addEtape(0)
        if(len(chemin.etapes.indices) != 1):
            self.outputs.append({"class":"chemin","method":"addEtape(ville)","result":"error","message":"chemin.etapes.indices n'est pas incrémenté correctement la deuxième fois"})
            test = False
        if(len(chemin.etapes.remainingIndices) != self.n-1):
            self.outputs.append({"class":"chemin","method":"addEtape(ville)","result":"error","message":"chemin.etapes.remainingIndices n'est pas mis à jour correctement la deuxième fois"})
            test = False
        if(test):
            self.outputs.append({"class":"chemin","method":"addEtape(ville)","result":"success","message":""})

    # addEtapeToFixed
    def testAddEtapeToFixed(self):
        test = True
        order = voy.Order(self.villes)
        chemin = voy.Chemin(order, self.villes)
        chemin.addEtapeToFixed(0)
        if(len(chemin.etapesFixed.indices) != 1):
            self.outputs.append({"class":"chemin","method":"addEtapeToFixed(ville)","result":"error","message":"chemin.etapesFixed.indices n'est pas incrémenté correctement"})
            test = False
        if(len(chemin.etapesFixed.remainingIndices) != self.n-1):
            self.outputs.append({"class":"chemin","method":"addEtapeToFixed(ville)","result":"error","message":"chemin.etapesFixed.remainingIndices n'est pas mis à jour correctement"})
            test = False
        chemin.addEtapeToFixed(0)
        if(len(chemin.etapesFixed.indices) != 1):
            self.outputs.append({"class":"chemin","method":"addEtapeToFixed(ville)","result":"error","message":"chemin.etapesFixed.indices n'est pas incrémenté correctement la deuxième fois"})
            test = False
        if(len(chemin.etapesFixed.remainingIndices) != self.n-1):
            self.outputs.append({"class":"chemin","method":"addEtapeToFixed(ville)","result":"error","message":"chemin.etapesFixed.remainingIndices n'est pas mis à jour correctement la deuxième fois"})
            test = False
        if(test):
            self.outputs.append({"class":"chemin","method":"addEtapeToFixed(ville)","result":"success","message":""})

    # removeEtape
    def testRemoveEtape(self):
        test = True
        order = voy.Order(self.villes)
        chemin = voy.Chemin(order, self.villes)
        chemin.addEtape(2)
        chemin.removeEtape()
        if(len(chemin.etapes.indices) != 0):
            self.outputs.append({"class":"chemin","method":"removeEtape()","result":"error","message":"chemin.etapes.indices n'est pas décrémenté pour un indice valide"})
            test = False
        if(len(chemin.etapes.remainingIndices) != self.n):
            self.outputs.append({"class":"chemin","method":"removeEtape()","result":"error","message":"chemin.etapes.remainingIndices n'est pas incrémenté pour un indice valide"})
            test = False
        if(test):
            self.outputs.append({"class":"chemin","method":"removeEtape()","result":"success","message":""})

    # __copy__
    def testCopyChemin(self):
        test = True
        order = voy.Order(self.villes)
        chemin = voy.Chemin(order, self.villes)
        chemin.addEtape(1)
        chemin2 = copy.copy(chemin)
        if(len(chemin.etapes.indices) != len(chemin2.etapes.indices)):
            self.outputs.append({"class":"chemin","method":"__copy__(chemin)","result":"error","message":"chemin.etapes.indices n'est pas copié correctement"})
            test = False
        if(len(chemin.etapes.remainingIndices) != len(chemin2.etapes.remainingIndices)):
            self.outputs.append({"class":"chemin","method":"__copy__(chemin)","result":"error","message":"chemin.etapes.remainingIndices n'est pas copié correctement"})
            test = False
        if(len(chemin.etapesFixed.indices) != len(chemin2.etapesFixed.indices)):
            self.outputs.append({"class":"chemin","method":"__copy__(chemin)","result":"error","message":"chemin.etapesFixed.indices n'est pas copié correctement"})
            test = False
        if(len(chemin.etapesFixed.remainingIndices) != len(chemin2.etapesFixed.remainingIndices)):
            self.outputs.append({"class":"chemin","method":"__copy__(chemin)","result":"error","message":"chemin.etapesFixed.remainingIndices n'est pas copié correctement"})
            test = False
        if(chemin.distance != chemin2.distance):
            self.outputs.append({"class":"chemin","method":"__copy__(chemin)","result":"error","message":"chemin.distance n'est pas copié correctement"})
            test = False
        chemin.addEtape(2)
        if(len(chemin.etapes.indices) == len(chemin2.etapes.indices)):
            self.outputs.append({"class":"chemin","method":"__copy__(chemin)","result":"error","message":"chemin.etapes.indices est impacté"})
            test = False
        if(len(chemin.etapes.remainingIndices) == len(chemin2.etapes.remainingIndices)):
            self.outputs.append({"class":"chemin","method":"__copy__(chemin)","result":"error","message":"chemin.etapes.remainingIndices est impacté"})
            test = False
        if(chemin.distance == chemin2.distance):
            self.outputs.append({"class":"chemin","method":"__copy__(chemin)","result":"error","message":"chemin.distance est impacté"})
            test = False
        if(test):
            self.outputs.append({"class":"chemin","method":"__copy__(chemin)","result":"success","message":""})

    ########
    # Loop #
    ########

    # loopDFS
    def testLoopDFS(self):
        test = True
        loop = voy.Loop(self.villes)
        loop.firstGuess()
        refLongueur = loop.referenceLongueur
        order = voy.Order(self.villes)
        chemin = voy.Chemin(order, self.villes)
        loop.loopDFS(chemin)
        if(loop.referenceLongueur >= refLongueur):
            self.outputs.append({"class":"loop","method":"loopDFS(chemin)","result":"error","message":"la longueur du chemin n'a pas été réduite par rapport au first guess"})
            test = False
        if(test):
            self.outputs.append({"class":"loop","method":"loopDFS(chemin)","result":"success","message":""})

    # __copy__
    def testCopyLoop(self):
        test = True
        loop = voy.Loop(self.villes)
        loop.firstGuess()
        loop2 = copy.copy(loop)
        if(loop.referenceLongueur != loop2.referenceLongueur):
            self.outputs.append({"class":"loop","method":"__copy__(loop)","result":"error","message":"loop.referenceLongueur n'est pas copié correctement"})
            test = False
        if(loop.order.length != loop2.order.length):
            self.outputs.append({"class":"loop","method":"__copy__(loop)","result":"error","message":"loop.order n'est pas copié correctement"})
            test = False
        if(loop.reference.etapes.length != loop2.reference.etapes.length and loop.reference.etapesFixed.length != loop2.reference.etapesFixed.length and loop.reference.distance != loop2.reference.distance):
            self.outputs.append({"class":"loop","method":"__copy__(loop)","result":"error","message":"loop.reference n'est pas copié correctement"})
            test = False
        order = voy.Order(self.villes)
        chemin = voy.Chemin(order, self.villes)
        loop.loopDFS(chemin)
        if(loop.referenceLongueur == loop2.referenceLongueur):
            self.outputs.append({"class":"loop","method":"__copy__(loop)","result":"error","message":"loop.referenceLongueur est impacté"})
            test = False
        if(loop.reference.distance == loop2.reference.distance):
            self.outputs.append({"class":"loop","method":"__copy__(loop)","result":"error","message":"loop.reference est impacté"})
            test = False
        if(test):
            self.outputs.append({"class":"loop","method":"__copy__(loop)","result":"success","message":""})

    # Display
    def launchTests(self):
        # Launch tests
        self.testAddIndex()
        self.testRemoveIndex()
        self.testCopyOrder()
        self.testAddEtape()
        self.testAddEtapeToFixed()
        self.testRemoveEtape()
        self.testCopyChemin()
        self.testLoopDFS()
        self.testCopyLoop()

        # Provide return
        return self.outputs

myTest = testVoyageur()
testResults = myTest.launchTests()
print(testResults)