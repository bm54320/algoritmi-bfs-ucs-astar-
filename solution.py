import heapq
import sys
from collections import deque
from queue import PriorityQueue

args = sys.argv

def VratiSljedecuLiniju(string):
    index = args.index(string)
    index = index + 1
    return args[index]

datoteka = VratiSljedecuLiniju("--ss")


#googlo sam ovaj dio https://www.w3schools.com/python/python_file_open.asp
def CitajIzDatoteke(path):
    file = open(path , 'r',encoding="utf-8")
    return file.readlines()

linija = CitajIzDatoteke(datoteka)

if sys.argv.__contains__("--h"):
    heuristika = VratiSljedecuLiniju("--h")

    linijaHeuristika = CitajIzDatoteke(heuristika)

    heuristic_dict = {}

    for line in linijaHeuristika:
        siu = line.split(": ")
        siu[1] = siu[1].strip()
        heuristic_dict[siu[0]] = siu[1]


def print_funkcija(found_solution, states_visited, path_length, total_cost, path):
    if found_solution == True:
        print("[FOUND_SOLUTION]: yes")
        print("[STATES_VISITED]: " + states_visited.__str__())
        print("[PATH_LENGTH]: " + path_length.__str__())
        print("[TOTAL_COST]: " + str(float(total_cost)))
        print("[PATH]: " + path.__str__())
    else:
        print("[FOUND_SOLUTION]: no")

if linija[0].strip() == "#":
    linija.pop(0)
start = linija[0].strip()
finish = linija[1].strip()
dva_ciljna_stanja = finish.split(" ")
expand = []
open = []

#Splitat cemo gradove i njihove susjede u liste
gradovi = {}
for line in linija[2:]:
    susjedi = {}
    splitaj = line.split(":")
    splitaj[1] = splitaj[1].strip()
    clan = splitaj[1].split(" ")
    for clan1 in clan:
        clan2 = clan1.split(",")
        try:
            susjedi[clan2[0]] = clan2[1]
        except IndexError:
            continue
    gradovi[splitaj[0]] = susjedi



def bfs():
    print("# BFS")
     
    found_solution = False
    states_visited = 0
    total_cost = 0
    path_length = 0
    path = []
    visited = set()
    path.append(start)
    zapamti_i = 0
    zapamti_path_length = 0
    ciljnaa = set()
    for c in dva_ciljna_stanja:
        ciljnaa.add(c) 

    pocetni_rijecnik = {}
    pocetni_rijecnik[start] = 0
    open_queue = deque([(pocetni_rijecnik, [start])])

    while(open_queue):
        node, current_path = open_queue.popleft()
        key1 = list(node.keys())
        kljuc = key1[0]
        if kljuc not in visited :
            visited.add(kljuc)
            states_visited += 1
            
        if kljuc in ciljnaa:
            cost = node.get(kljuc)
            path_length = len(current_path)
            print_funkcija(True, states_visited,path_length,cost,current_path)
            return
        if kljuc in gradovi:
            novi_clan = gradovi.get(kljuc)
            for key in novi_clan:
                if key not in visited:
                    rijecnik = {}
                    nova_vrijednost = int(novi_clan[key]) + sum(node.values())
                    rijecnik[key] = nova_vrijednost
                    open_queue.append((rijecnik, current_path + [key]))


def ucs():
    found_solution = False
    states_visited = 0
    total_cost = 0
    path_length = 100
    current_path = []
    visited = set()
    path = []
    path.append(start)
    zapamti_i = 0
    queue = PriorityQueue()
    queue.put((0, start, [start]))
    visited.add(start)

    if len(dva_ciljna_stanja) == 1:
        while not queue.empty():
            priority, element, path_to_node = queue.get()
            if element not in visited:
                visited.add(element)
            if element == dva_ciljna_stanja[0]:
                states_visited = len(visited)
                cost = priority
                path_length = len(path_to_node) 
                current_path = path_to_node 
                print_funkcija(True, states_visited, path_length, cost, current_path)
                return
            if element in gradovi:
                novi_clan = gradovi.get(element)
                for key in novi_clan:
                    if key not in visited:
                        nova_vrijednost = int(novi_clan[key]) + priority
                        nova_putanja = path_to_node + [key]
                        queue.put((nova_vrijednost, key, nova_putanja))
    else:
        for finish in dva_ciljna_stanja:
            while not queue.empty():
                priority, element, path_to_node = queue.get()
                if element not in visited:
                    visited.add(element)
                if element == finish:
                    temporery_path_length = path_length
                    path_length = len(current_path)
                    if path_length < temporery_path_length:
                        states_visited = len(visited)
                        cost = priority
                        path_length = len(path_to_node) 
                        current_path = path_to_node 

                if element in gradovi:
                    novi_clan = gradovi.get(element)
                    for key in novi_clan:
                        if key not in visited:
                            nova_vrijednost = int(novi_clan[key]) + priority
                            nova_putanja = path_to_node + [key]
                            queue.put((nova_vrijednost, key, nova_putanja))

        print_funkcija(True, states_visited, path_length, cost, current_path)

def nadi_cijenu(start,finish,lista):
    
    cijena = 0
    k = range(len(lista))[::-1] #googlao sam ovo za reversed for loop
    for i in k:
        if i == 0:
            return cijena
        if lista[i] in gradovi:
            nova_lista = gradovi.get(lista[i])
            for key in nova_lista:
                if key == lista[i - 1]:
                    cijena = cijena + int(nova_lista.get(key))

def nadi_cijenu1(start,finish,lista, gradovi):
    cijena = 0
    for i in range(len(lista)):
        if i == len(lista) - 1:
            return cijena
        nova_lista = gradovi.get(lista[i])
        for key in nova_lista:
            if key == lista[i + 1]:
                cijena += int(nova_lista[key])

    
def astar():
    print("# A-STAR " + heuristika )
    found_solution = False
    states_visited = 0
    total_cost = 0
    path_length = 0
    current_path = []
    visited = set()
    path = []
    path.append(start)
    zapamti_i = 0
    queue = PriorityQueue()
    queue.put((57,0, start, [start]))
    visited.add(start)

    while not queue.empty():
        priority,cijena, element, path_to_node = queue.get()
        #print(priority,cijena, element, path_to_node)
        
        priority = priority - int(heuristic_dict.get(element))
        if element not in visited:
            visited.add(element)
        if len(dva_ciljna_stanja) > 1:
            if element == dva_ciljna_stanja[0] or element == dva_ciljna_stanja[1]: 
                states_visited = len(visited)
                if element == dva_ciljna_stanja[0]:
                    cost = nadi_cijenu1(start,dva_ciljna_stanja[0],path_to_node, gradovi)
                else:
                    cost = nadi_cijenu1(start,dva_ciljna_stanja[1],path_to_node, gradovi)
                path_length = len(path_to_node) 
                current_path = path_to_node 
                print_funkcija(True, states_visited, path_length, cost, current_path)
                return
        elif element == dva_ciljna_stanja[0]:
            states_visited = len(visited)
            cost = nadi_cijenu(start,finish,path_to_node) 
            path_length = len(path_to_node) 
            current_path = path_to_node 
            print_funkcija(True, states_visited, path_length, cost, current_path)
            return
        if element in gradovi:
            novi_clan = gradovi.get(element)
            for key in novi_clan:
                if key not in visited:
                    nova_vrijednost = int(novi_clan[key]) + priority + int(heuristic_dict.get(key))
                    cijena = int(novi_clan[key]) + priority 
                    nova_putanja = path_to_node + [key]
                    queue.put((nova_vrijednost,cijena, key, nova_putanja))

def checkConsistent():
    check = True
    expression = "OK"
    brojac = 0
    print("# HEURISTIC-CONSISTENT "+heuristika)
    for key in heuristic_dict:
        try:
            for sljedeceMjesto,udaljenost in reversed(gradovi[key].items()):
                if int(heuristic_dict[key]) > (int(heuristic_dict[sljedeceMjesto]) + int(udaljenost)):
                    check = False
                    brojac = 1
                else:
                    check = True     
                if check == False:
                    expression = "ERR"
                else:
                    expression = "OK"    
                print("[CONDITION]: ["+expression+"] h(" + key+") <= h("+sljedeceMjesto+") + c: "+str(float(heuristic_dict[key]))+" <= "+str(float(heuristic_dict[sljedeceMjesto]))+" + " + str(float(udaljenost)))    
        except Exception:
            break
    
    if brojac == 0:
        print("[CONCLUSION]: Heuristic is consistent.")
    else:
        print("[CONCLUSION]: Heuristic is not consistent.")

def ucs_za_optimistic(start,finish):
    found_solution = False
    states_visited = 0
    total_cost = 0
    path_length = 100
    current_path = []
    visited = set()
    path = []
    path.append(start)
    zapamti_i = 0
    queue = PriorityQueue()
    queue.put((0, start, [start]))
    visited.add(start)

    if len(dva_ciljna_stanja) == 1:
        while not queue.empty():
            priority, element, path_to_node = queue.get()
            if element not in visited:
                visited.add(element)
            if element == dva_ciljna_stanja[0]:
                states_visited = len(visited)
                cost = priority
                path_length = len(path_to_node) 
                current_path = path_to_node 
                #print_funkcija(True, states_visited, path_length, cost, current_path)
                return cost
            if element in gradovi:
                novi_clan = gradovi.get(element)
                for key in novi_clan:
                    if key not in visited:
                        nova_vrijednost = int(novi_clan[key]) + priority
                        nova_putanja = path_to_node + [key]
                        queue.put((nova_vrijednost, key, nova_putanja))
    else:
        for finish in dva_ciljna_stanja:
            while not queue.empty():
                priority, element, path_to_node = queue.get()
                if element not in visited:
                    visited.add(element)
                if element == finish:
                    temporery_path_length = path_length
                    path_length = len(current_path)
                    if path_length < temporery_path_length:
                        states_visited = len(visited)
                        cost = priority
                        path_length = len(path_to_node) 
                        current_path = path_to_node 

                if element in gradovi:
                    novi_clan = gradovi.get(element)
                    for key in novi_clan:
                        if key not in visited:
                            nova_vrijednost = int(novi_clan[key]) + priority
                            nova_putanja = path_to_node + [key]
                            queue.put((nova_vrijednost, key, nova_putanja))
        try:
            return cost
        except UnboundLocalError:
            cost = 0
            return cost
def provjeriGresku(heuristikaGrada, cijenaOdGradaHeuristikeDoCilja, brojac) :
    pretvoriInt = int(heuristikaGrada)
    if pretvoriInt > cijenaOdGradaHeuristikeDoCilja :
        brojac = 1
        return "[ERR]", brojac
    else :
        return "[OK]", brojac
    
def checkOptimistic():
    brojac = 0

    for line in linijaHeuristika :
        line = line.strip()

        zavrsnoStanje = dva_ciljna_stanja

        imeGrada, heuristikaGrada = line.split(":")
        heuristikaGrada = heuristikaGrada.strip()
        cijenaOdGradaHeuristikeDoCilja = ucs_za_optimistic(imeGrada, zavrsnoStanje)
        # if int(heuristikaGrada) > cijenaOdGradaHeuristikeDoCilja :
        #     vrijednost = "[ERR]"
        #     brojac = 1
        # else :
        #     vrijednost = "[OK]"
        vrijednost, brojac1 = provjeriGresku(heuristikaGrada, cijenaOdGradaHeuristikeDoCilja, brojac)
        print("[CONDITION]: " + vrijednost + " h(" + imeGrada + ") <= h*: " + str(float(heuristikaGrada)) + " <= " + str(float(cijenaOdGradaHeuristikeDoCilja)))
        if brojac1 == 1:
            brojac = brojac1

    if brojac == 0 :
        print("[CONCLUSION]: Heuristic is optimistic.")
    else :
        print("[CONCLUSION]: Heuristic is not optimistic.")


if args.__contains__("--alg"):
    sejvajSljedeci = VratiSljedecuLiniju("--alg")

    if sejvajSljedeci == "bfs":
        bfs()
    elif sejvajSljedeci == "ucs":
       ucs()
    else:
        astar()
elif args.__contains__("--check-optimistic"):
    checkOptimistic()
elif args.__contains__("--check-consistent"):
    checkConsistent()