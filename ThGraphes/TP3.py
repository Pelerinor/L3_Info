#graphes d'exemples (pour tests)
cycle= Graph();
cycle.add_edges([[i,(i+1)%6]for i in range(6)]);

chemin=Graph();
chemin.add_edges([[i,i+1] for i in range(5)]);

cylindre = Graph.cartesian_product(cycle,chemin);

graph1 = Graph(12);
graph1.add_edges([[0,1],[1,2],[3,4],[0,5],[1,3],[2,4],[5,6],[5,8],[6,7],[7,8],[1,9],[8,9],[9,11],[9,10]]);

graph2 = Graph(11);
graph2.add_edges([[0,1],[2,1],[1,0],[0,2],[0,3],[3,10],[4,5],[5,4],[6,5],[6,4],[3,7],[7,8],[8,9],[9,7],[10,7],[5,10]]);

TP = Graph(14)
TP.add_edges([[0,1],[1,2],[4,3],[1,4],[2,3],[3,5],[5,6],[6,8],[7,8],[5,7],[6,9],[9,10],[10,11],[11,12],[12,9],[11,13],[13,12]])

fig1 = Graph(7) # Figure 1 of the TP document
fig1.add_edges([[0,1],[1,2],[2,0],[2,3],[3,4],[4,5],[5,6],[6,2]])

fig2 = Graph(12) # Figure 2 of the TP document
fig2.add_edges([[0,1],[1,2],[2,4],[4,3],[3,1],[4,5],[5,6],[6,8],[5,7],[7,8],[6,9],[9,10],[9,12],[10,11],[11,12],[11,13],[12,13]])

art = Graph(10) # The graph in the scientific article (given as example)
art.add_edges([[0,1],[1,2],[2,3],[0,3],[0,2],[2,4],[4,5],[5,6],[6,7],[5,7],[4,8],[8,9],[4,9],[1,4]])

no_con = Graph(5)    #no connectivity
no_con.add_edges([[0,1],[1,2],[2,0],[3,4]])

def pronfondeur_recursif(G, couleur, v, L, T, C, date, d, f, DFI):
    couleur[v] = 'Gris'
    date = date+1
    d[v] = date

    if v not in L:
        L.append(v)

    for voisin in G.neighbors(v):
        # voisin déjà parcouru
        if couleur[voisin] == 'Noir':
            T.add_edges([[v, voisin, 1]])
            C.append([v, voisin,1])

        # sommet nouvellement découvert
        if couleur[voisin] == 'Blanc':
            T.add_edges([[voisin, v, 1]])
            DFI.append(voisin)
            couleur[voisin] = 'Gris'
            couleur, date, DFI = pronfondeur_recursif(G, couleur, voisin, L,T,C, date, d, f, DFI)

    couleur[v] = 'Noir'
    date = date+1
    f[v] = date
    return couleur, date, DFI

def trier_aretes(aretes, DFI):
    newList = list()

    for i in DFI:
        for arete in aretes:
            if arete[0] == i:
                newList.append(arete)

    return newList

def decomposition_en_chaine(G, T, backedges, visited, DFI, chaines):
    backedges = trier_aretes(backedges, DFI)
    print "backedges:" + str(backedges)

    for e in backedges:
        chaines.append(list())
        chaines[len(chaines)-1].append([e[0],e[1]])
        if e[0] not in visited:
            visited.append(e[0])
        decomposition_en_chaine_recursif(T, visited, DFI, e[1], chaines)

    print "visited : " + str(visited)
    return visited, chaines

def decomposition_en_chaine_recursif(T, visited, DFI, v, chaines):
    if v not in visited :
        visited.append(v)

    voisins = T.neighbors_out(v)
    for i in DFI:
        if (i in voisins) and (i not in visited):
            chaines[len(chaines)-1].append([v, i])
            decomposition_en_chaine_recursif(T, visited, DFI, i, chaines)
            return
        elif (i in voisins) and (i in visited):
            chaines[len(chaines)-1].append([v, i])
            return

# Retourne True s'il y a un cycle différent de C[0] dans C
def is_there_various_circles(chaines):
    for i in range(1, len(chaines)):
        if chaines[i][0][0] == chaines[i][len(chaines[i])-1][1]:
            return True
    return False

# Reponses exercice 1
def Exercice1(G, visited, chaines, T):
    # Affichage des résultats obtenus.

    deconnectantes = Exercice2_arete_deconnectante(G, chaines)

    print "Exercice 1 :"
    if len(G.vertices()) != len(visited):
        print "Not a 2-EDGE-CONNECTED."
        print "Composantes 2-arêtes connexes : "
        show_2_edge_connected(G, deconnectantes)
    elif is_there_various_circles(chaines):
        print "2-EDGE-CONNECTED BUT NOT 2-CONNECTED."
        show_2_connected(chaines)
    else:
        print "2-CONNECTED."

    return deconnectantes

# Reponses exercice 2
def Exercice2(T, deconnectantes):
    print "\nExercice 2 : orientation fortement connexe."
    if len(deconnectantes) == 0:
        print "Graphe fortement connexe : "
        T.show()
    else:
         print "arete deconnectante : " + str(deconnectantes)

# Supprime les arêtes présentes dans une chaines et retourne une liste d'arêtes (= les arêtes déconnanctes du graphe)
def Exercice2_arete_deconnectante(G, chaines):
    opt_edges = G.edges()

    for C in chaines:
        for edge in C:
            e = (edge[0], edge[1], None)

            if e in opt_edges:
                opt_edges.remove(e)
            else:
                opt_edges.remove((edge[1], edge[0], None))

    return opt_edges

def show_2_edge_connected(G, deconnectantes):
    G1 = G
    G1.delete_edges(deconnectantes)
    G1.show()

def show_2_connected(chaines):
    G1 = Graph(0)
    nbCycles = 0

    for chaine in chaines:
        if is_cycle(chaine):             # Graphe non connexe
        
            nbCycles = nbCycles+1
            for i in chaine:
                v0 = vertex_name(i[0], nbCycles)
                v1 = vertex_name(i[1], nbCycles)

                G1.add_vertex(v0)
                G1.add_vertex(v1)

                G1.add_edge([v0, v1])
        else:
            for i in chaine:
                v0 = vertex_name(i[0])
                v1 = vertex_name(i[1])

                G1.add_vertex(v0)
                G1.add_vertex(v1)

                G1.add_edge([v0, v1])

    G1.show()

# vertex_name(2,2) return 2''
def vertex_name(vertex, nb_cycles=1):
    return str(vertex) + str(mult_text("'", nb_cycles-1))

# mult_text("'", 5) return '''''
def mult_text(text, n):
    newText = ""
    for i in range(0, n):
        newText = newText + text
    return newText

def is_cycle(list):
    if (list[0][0] == list[len(list)-1][1]):
        return True
    else:
        return False

def Schmidt(G):
    # Variable pour parcours pronfondeur
    depart = G.vertices()[0]
    couleurs = list()
    L = list()        # ordre du parcours en profondeur
    d = list()        # dates de debut
    f = list()        # dates de fin
    DFI = list()      # Depth First Index
    date = 0

    # Variable pour decomposition en chaines
    backedges = list()
    chaines = list()    # ensembles des chaines (C1, ..., Ck)
    visited = list()    # ordre des sommets visités

    L.append(depart)
    T = DiGraph(len(G.vertices()));     # Tree (Arbre de la décomposition en chaînes)

    for v in G.vertices(): # Initialisation
        couleurs.append('Blanc')
        d.append(-1)
        f.append(-1)

    for v in G.vertices(): # Parcours Profondeur(création de T)
        if couleurs[v]  == 'Blanc':
            DFI.append(v)
            couleurs, date, DFI = pronfondeur_recursif(G, couleurs, v, L, T, backedges, date, d, f, DFI);

        if (len(G.vertices()) != len(L)): # G non connexe
            print "G is not connected."
            return [],[], DiGraph(0)

    visited, chaines = decomposition_en_chaine(G, T, backedges, visited, DFI, chaines)
    print "chaines : " + str(chaines)
    return visited, chaines, T

G = art
print "Graphe : "
G.show()

# Calcul de l'algorithme de Schmidt, récupération de la décomposition en chaines.
visited, chaines, T = Schmidt(G)

if len(T.vertices()) != 0:
    deconnectantes = Exercice1(G, visited, chaines, T) # Exercice 1

    Exercice2(T, deconnectantes)                       # Exercice 2
