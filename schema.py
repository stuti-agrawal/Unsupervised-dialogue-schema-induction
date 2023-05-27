import networkx as nx
import matplotlib.pyplot as plt
import json
import pandas as pd
import math
from collections import Counter
import textwrap

# get the bot utterances and their corresponding clusters
# get the user utterances and their corresponding clusters
# get the labels of the clusters

def get_schema():
# # load csv to dataframe
    bot_df = pd.read_csv('output\sent\embedded_sent_bot.csv')
    user_df = pd.read_csv('output\sent\embedded_sent_user.csv')
        
    with open('output\chatgpt_response_sent_bot.json') as f:
        bot_label_dict = json.load(f)

    with open('output\chatgpt_response_sent_user.json') as f:
        user_label_dict = json.load(f)

    with open('output\sent\clusters_sent_bot_replaced.json') as f:
        bot_labels = json.load(f)

    with open('output\sent\clusters_sent_user_replaced.json') as f:
        user_labels = json.load(f)

    # get the counts of each cluster
    def get_counts_bot_user():
        bot_counts = Counter(bot_labels)
        user_counts = Counter(user_labels)
        return bot_counts, user_counts


    total_len  = len(bot_df)
    print(total_len)
    # get segmented values of bot and user utterances
    bot_clusters = []
    user_clusters = []
    bot_idx = 0
    user_idx = 0
    for i in range(len(bot_df)):
        bot_ut = eval(bot_df['utterances'][i])
        user_ut = eval(user_df['utterances'][i])
        bot_clusters.append(bot_labels[bot_idx:bot_idx+len(bot_ut)])
        user_clusters.append(user_labels[user_idx:user_idx+len(user_ut)])
        bot_idx += len(bot_ut)
        user_idx += len(user_ut)



    # add all keys in bot counts and user counts to graph_dict
    bot_graph_dict = {}
    user_graph_dict = {}
    graph_dict2 = {}

    bot_counts, user_counts = get_counts_bot_user()
    for i in range(len(bot_clusters)):
        bot_clus = bot_clusters[i]
        user_clus = user_clusters[i]
        n  = len(bot_clusters[i])+len(user_clusters[i])
        prev_cluster = "b:"+bot_label_dict[str(bot_clusters[i][0])]
        # if prev_cluster not in bot_graph_dict:
        #     bot_graph_dict[prev_cluster] = {}
        for j in range(1,n):
            if prev_cluster not in graph_dict2:
                graph_dict2[prev_cluster] = {}
            if j % 2 == 0:
                k = math.ceil(j/2)
                key_val = "b:" + bot_label_dict[str(bot_clus[k])]
                if key_val not in graph_dict2[prev_cluster]:
                    graph_dict2[prev_cluster][key_val] = 1
                else:
                    graph_dict2[prev_cluster][key_val] += 1
                prev_cluster = key_val
            else:
                k = math.floor(j/2)
                key_val = "u:" + user_label_dict[str(user_clus[k])]
                if key_val not in graph_dict2[prev_cluster]:
                    graph_dict2[prev_cluster][key_val] = 1
                else:
                    graph_dict2[prev_cluster][key_val] += 1
                prev_cluster = key_val

    count_dict  = graph_dict2.copy()
    for key, val in graph_dict2.items():
        summ = sum(val.values())
        for val in graph_dict2[key]:
            graph_dict2[key][val] = round(graph_dict2[key][val]/summ, 2)

    with open('output\sent\graph_dict2.json', 'w') as f:
        json.dump(graph_dict2, f, indent = 4)


    G = nx.DiGraph()
    # add nodes all keys in graph_dict2
    for key in graph_dict2:
        # bot nodes are red in color
        if key[0] == 'b':
            G.add_node(key, color = 'red', label = key)
        else:
            G.add_node(key, color = 'yellow', label = key)
    threshold = 0.01
    for key in graph_dict2:
        for val in graph_dict2[key]:
            # G.add_edge(key, val, weight = graph_dict2[key][val])
            # if graph_dict2[key][val] > 0.5:
            #     G.add_edge(key, val, weight = graph_dict2[key][val])
            if graph_dict2[key][val] > 0:
                if key in graph_dict2[val]:
                    if graph_dict2[key][val] > graph_dict2[val][key]:
                        G.add_edge(key, val, weight = graph_dict2[key][val])
                    else:
                        G.add_edge(val, key, weight = graph_dict2[val][key])
                else:
                    G.add_edge(key, val, weight = graph_dict2[key][val])

    # draw the graph
    pos = nx.circular_layout(G)
    # beautify graph and labels
    labels = nx.get_node_attributes(G, "label")
    wrapped_labels = [textwrap.fill(label, 10) for label in labels.values()]
    colors = nx.get_node_attributes(G, 'color')
    nx.draw_networkx_nodes(G, pos, node_size=350, node_color = list(colors.values()))
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, width=1)
    nx.draw_networkx_labels(G, pos, labels=dict(zip(G.nodes(), wrapped_labels)), font_size=9, font_family="sans-serif")
    plt.savefig('output\schema.png')
    plt.show()


if __name__ == '__main__':
    get_schema()