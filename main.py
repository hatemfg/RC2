__author__ = 'hatem'
import xml.etree.ElementTree as ET
import copy

fichier = raw_input('Veuillez entrer le fichier XML contenant le reseau ')
M1 = raw_input("Veuillez entrer le noeud M1 ")
M2 = raw_input("Veuillez entrer le noeud M2 ")
relation = raw_input("Veuillez entrer la relation entre les noeuds ")

inputXML = list()
XMLdict = dict()
tree = ET.parse(fichier)
for node in tree.iter():
    inputXML.append(node)


resultDict = dict()

for i in range(1, len(inputXML)):
    resultDict[inputXML[i].tag] = None
resultDictBuffer = copy.deepcopy(resultDict)
for key in resultDict:
    resultDict[key] = copy.deepcopy(resultDictBuffer)

for i in range( 0, len(inputXML)):
    if 'parent' in inputXML[i].attrib and 'lien' in inputXML[i].attrib:
        if inputXML[i].attrib['sens'] == '-':
            resultDict[inputXML[i].tag][inputXML[i].attrib['parent']] = inputXML[i].attrib['lien']
        else:
            resultDict[inputXML[i].attrib['parent']][ inputXML[i].tag] = inputXML[i].attrib['lien']


def find_solution(resultDict,already_marked,relation):
    printed = False
    for key1 in resultDict:
        for key2 in resultDict[key1]:
            if resultDict[key1][key2] == relation and already_marked[key1][1] == 1 and already_marked[key2][0] == 1:
                print key2,relation,key1
                printed = True
    if not printed:
        print "La relation demandee n\'a pas pu etre deduite"


def propagation_algorithm(node1,node2,relation,resultDict):

    already_marked = dict()
    for key in resultDict:
        already_marked[key] = [0,0]

    if (node1 not in resultDict) or (node2 not in resultDict):
        return False
    else:
        propagation = list()
        already_marked[node1][0] = 1
        already_marked[node2][1] = 1
        Modified1 = True
        Modified2 = True
        while Modified1 or Modified2 :
            Modified1 = False
            Modified2 = False
            propagation = [node1,node2]

            for element in propagation:
                Modified1 = False
                for key in resultDict[element]:
                    if (resultDict[element][key] == 'is_a') and (already_marked[key][0] == 0) :
                        already_marked[key][0] = 1
                        Modified1 = True
                        propagation.append(key)

                Modified2 = False
                for key in resultDict[element]:
                    if (resultDict[element][key] == 'is_a') and (already_marked[key][1] == 0):
                        already_marked[key][1] = 1
                        Modified2 = True
                        propagation.append(key)

            find_solution(resultDict,already_marked,relation)

propagation_algorithm(M1,M2,relation,resultDict)
