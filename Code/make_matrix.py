import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

## Reading Social Network Dictionary
with open("social_network.pkl", "rb") as f:
    social_network = pickle.load(f)

## Reading ID to Name mapping Dictionary
with open('id_map.pkl', 'rb') as f:
    id_map = pickle.load(f)

NUM_NODES = len(social_network) # NUM_NODES = 411
adjacency_matrix = np.zeros((NUM_NODES, NUM_NODES), dtype=int)

## Mapping the Player ID to the Index in adjacency_matrix.
id_2_index = {j:i for i, j in enumerate(social_network.keys())}

## Reverse mapping of adjacency_matrix Index to Player ID
index_2_id = {i:j for i, j in enumerate(social_network.keys())}

## Run this below block to see an example of the mapping
#index_2_id[182]
#id_2_index[42562446]
#id_map[42562446]

## Creating directed graph using adjacency_matrix
## If [i, j] = 1 => i follows j
for id in social_network.keys():
    friends = social_network[id]
    for f in friends:
        if f in social_network.keys():
            # print "in"
            adjacency_matrix[id_2_index[id]][id_2_index[f]] = 1

## Finding No. of followers for each node.
follower_counts = np.sum(adjacency_matrix, axis = 0)

## Finding top 10 most followed nodes
top_10 = np.argsort(follower_counts)[-10:]

## Creating NetworkX graph object from adjacency_matrix
G = nx.from_numpy_array(adjacency_matrix, create_using=nx.MultiDiGraph())

# Coloring key players in RED
color_map = []
for node in G:
    if node in top_10:
        color_map.append('red')
    else:
        color_map.append('green')

## Force directed graph representation (Kamada Kawai), for visualizing network
nx.draw_kamada_kawai(G, node_size=25, node_color=color_map)
plt.savefig("social_network.png")
plt.show()

## Plot bar graph of top 10 most followed players
players = []
for i in top_10:
    # print id_map[index_2_id[i]]
    players.append(id_map[index_2_id[i]]["name"])

g = sns.barplot(range(10), follower_counts[top_10])
g.set_xticklabels(players, rotation=90)
plt.title('Top personality Follower Counts')
plt.savefig("top_players_followers.png")
plt.show()

## Plot Heatmap of adjacency_matrix
## White dotted lines denote value '1'.
sns.heatmap(adjacency_matrix)
plt.title("Heatmap of Adjacency Matrix")
plt.savefig("Heatmap.png")
plt.show()
## Saving the adjacency_matrix numpy file
np.save('social_network.npy', adjacency_matrix)
