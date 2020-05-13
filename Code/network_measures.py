import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

## Degree Distribution Histogram
def plot_degree_hist(G):
    # Degree of each node
    degrees = [G.degree(n) for n in G.nodes()]
    sns.distplot(degrees)
    plt.xlabel("Degrees")
    plt.ylabel("Probability Distribution")
    plt.title("Degree Distribution")
    plt.savefig('Degree_Distribution.png')
    plt.show()
    return degrees

## Betweeness Centrality plot
def betweenness_centrality(G):
    bet = nx.betweenness_centrality(G)
    #sns.distplot(bet.values())
    plt.xlabel("Node Index")
    plt.ylabel("Betweenness Centrality")
    plt.title("Betweeness Centrality of all Nodes")
    plt.plot(bet.keys(), bet.values())
    plt.savefig('Betweenness_Centrality.png')
    #plt.hist(bet.values())
    plt.show()
    #print set(np.argsort(bet.values())[-10:]).intersection(top_10)


## Eigenvector_Centrality plot
def eigen_centrality(G):
    eigen = nx.eigenvector_centrality_numpy(G)
    plt.xlabel("Node Index")
    plt.ylabel("Eigenvector Centrality")
    plt.title("Eigenvector Centrality of all Nodes")
    plt.plot(eigen.keys(), eigen.values())
    plt.savefig('Eigenvector_Centrality.png')
    # plt.hist(bet.values())
    plt.show()

## Load adjacency_matrix
adjacency_matrix = np.load('social_network.npy')
## Create networkx graph object
G = nx.from_numpy_array(adjacency_matrix, create_using=nx.MultiDiGraph())

## Calling each network measure function
deg = plot_degree_hist(G)
betweenness_centrality(G)
eigen_centrality(G)


# pgrank = nx.pagerank_numpy(G)
# katz = nx.katz_centrality_numpy(G)
# closeness = nx.closeness_centrality(G)
