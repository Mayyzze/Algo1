from typing import Set
import sys, os, time
import networkx as nx


def get_voisins(g, node):
    return {int(n) for n in g.adj[node].keys()}


def dominant(g):
    """
        A Faire:         
        - Ecrire une fonction qui retourne le dominant du graphe non dirigé g passé en parametre.
        - cette fonction doit retourner la liste des noeuds d'un petit dominant de g

        :param g: le graphe est donné dans le format networkx : https://networkx.github.io/documentation/stable/reference/classes/graph.html

    """

    dominant = nx.Graph()
    while len(g.nodes) > len(dominant.nodes):
        add_dominant = set()
        for node in (set(g.nodes).difference(dominant.nodes)):
            best_nodes = get_voisins(g,str(node)).difference(dominant.nodes)
            if len(best_nodes) >= len(add_dominant):
                add_dominant = best_nodes
                best_node = int(node)
        dominant.add_edges_from([(best_node, n) for n in add_dominant])
        dominant.nodes[best_node]['is_optimal'] = True
        for node in add_dominant:
            dominant.nodes[node]['is_optimal'] = False
            
    ## A ce stade, on possède un dominant issu de l'algo glouton 
    ## qui possède plus de node que nécessaire, il faut maintenant en enlever sans perdre le caractère dominant

    node_isin_dominant = [n for n in dominant.nodes if (dominant.nodes[n]['is_optimal'] == True)]
    
    for node in node_isin_dominant:
        dominant.nodes[node]['is_optimal'] = False
        for n in dominant.nodes:
            optimal = False
            if dominant.nodes[n]['is_optimal'] == True:
                optimal = True
            else:
                for voisin in get_voisins(dominant, n):
                    if dominant.nodes[voisin]['is_optimal'] == True:
                        optimal = True
                        break
            if optimal == False:
                dominant.nodes[node]['is_optimal'] = True
                break

    final_dominant_nodes = [n for n in dominant.nodes if (dominant.nodes[n]['is_optimal'] == True)]

    return final_dominant_nodes

                    

              

    # def fin_voisins(graphe, node):  ## Détermine la quantité de noeuds voisins n'ayant qu'un voisin
    #     score = 0
    #     list_voisin = [n for n in graphe[node]]
    #     for voisins in list_voisin:
    #         if [n for n in graphe[node]] == []:
    #             score += 1
    #     return score

    # def max_neighbors_intersec(reste):
    #     max_nb_neighbors = -1
    #     best_node = 0
    #     equal_neighbors_nodes = []
    #     for node in reste:
    #         neighbors = [n for n in reste[node]]
    #         if len(neighbors) > max_nb_neighbors:
    #             max_nb_neighbors = len(neighbors)
    #             equal_neighbors_nodes = []
    #             best_node = node
    #             true_neighbors = []
    #             for i in range (len(neighbors)):
    #                 true_neighbors.append(neighbors[i])
    #         if len(neighbors) == max_nb_neighbors:
    #             equal_neighbors_nodes.append(node)
    #     if equal_neighbors_nodes != []:
    #         best_choice = -1
    #         for node in equal_neighbors_nodes:
    #             score = fin_voisins(reste, node)
    #             if score > best_choice:
    #                 best_node = node 
    #                 true_neighbors = [node for node in reste[node]]

    #     return (best_node, true_neighbors)

    # reste = g

    # while len(list(reste.nodes)) > 0 :
    #     best_node, neighbors = max_neighbors_intersec(reste)[0], max_neighbors_intersec(reste)[1]
    #     dominant.add_node(best_node)
    #     reste.remove_node(best_node)
    #     #print(best_node in neighbors_intersec)
    #     for node in neighbors :
    #         reste.remove_node(node)        


    # return dominant.nodes  # pas terrible :) mais c'est un dominant










#########################################
#### Ne pas modifier le code suivant ####
#########################################
if __name__=="__main__":
    input_dir = os.path.abspath(sys.argv[1])
    output_dir = os.path.abspath(sys.argv[2])
    
    # un repertoire des graphes en entree doit être passé en parametre 1
    if not os.path.isdir(input_dir):
	    print(input_dir, "doesn't exist")
	    exit()

    # un repertoire pour enregistrer les dominants doit être passé en parametre 2
    if not os.path.isdir(output_dir):
	    print(input_dir, "doesn't exist")
	    exit()       
	
    # fichier des reponses depose dans le output_dir et annote par date/heure
    output_filename = 'answers_{}.txt'.format(time.strftime("%d%b%Y_%H%M%S", time.localtime()))             
    output_file = open(os.path.join(output_dir, output_filename), 'w')

    for graph_filename in sorted(os.listdir(input_dir)):
        #print(graph_filename)
        # importer le graphe
        g = nx.read_adjlist(os.path.join(input_dir, graph_filename))
        
        # calcul du dominant
        D = sorted(dominant(g), key=lambda x: int(x))

        # ajout au rapport
        output_file.write(graph_filename)
        for node in D:
            output_file.write(' {}'.format(node))
        output_file.write('\n')
        
    output_file.close()
