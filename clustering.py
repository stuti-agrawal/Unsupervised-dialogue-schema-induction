import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
import json
from rouge import Rouge
from config import args_clustering_bot as args_bot
from config import args_clustering_user as args_user



def get_df(args):
    df = pd.read_csv(args['data_path'])
    return df

def get_idx_utterance(args):
    # Create a dictionary of the index of the utterance and the utterance
    idx_utterance = {}
    df = get_df(args)
    count = 0
    for i in range(len(df)):
        for j in range(len(eval(df['utterances'][i]))):
            idx_utterance[count] = eval(df['utterances'][i])[j]
            count += 1
    return idx_utterance


def get_utterances_from_closest_idx(closest_utterance_indices, args):
    closest_utterances = {}
    idx_utterance = get_idx_utterance(args)
    for i, utterance_indices in closest_utterance_indices.items():
        closest_utterances[i] = []
        prev_utterance = idx_utterance[utterance_indices[0]]
        closest_utterances[i].append(prev_utterance)
        for j in utterance_indices[1:]:
            if len(closest_utterances[i]) == 15:
                break
            score = Rouge().get_scores(prev_utterance, idx_utterance[j])
            print(score)
            if score[0]['rouge-1']['f'] > 0.2:
                prev_utterance = idx_utterance[j]
                closest_utterances[i].append(idx_utterance[j])

    return closest_utterances

def make_embeddings_2dArray(args):
    df = get_df(args)

    # Create a list of all the embeddings
    embeddings = []
    for i in range(len(df)):
        embeddings += eval(df['sent_embeddings'][i])

    embeddings = np.array(embeddings)
    print(embeddings.shape)

    # save embeddings to a JSON file
    with open(args['embeddings_path'], 'w') as f:
        json.dump(embeddings.tolist(), f, indent=4)


def get_Embedding(args):
# get embeddings from JSON file
    with open(args['embeddings_path'], 'r') as f:
        embeddings = json.load(f)
        embeddings = np.array(embeddings)
    return embeddings


def make_Clusters(embeddings, args):
    distance_threshold = args['distance_threshold']

    # Perform hierarchical agglomerative clustering
    model = AgglomerativeClustering(distance_threshold=distance_threshold, n_clusters=None)
    model.fit(embeddings)

    # Get the cluster labels and centroids
    labels = model.labels_
    centroids = []
    label_centroids = {}
    for i in range(max(labels) + 1):
        centroid = np.mean(embeddings[labels == i], axis=0)
        centroids.append(centroid)
        label_centroids[i] = centroid

    print("Number of clusters:", len(centroids))
    # Get the 10 closest values in each label to each centroid
    closest_values = []
    closest_values_dict = {}
    closest_utterance_indices = {}
    for i, centroid in label_centroids.items():
        cluster_embeddings = embeddings[labels == i]
        cluster_idx = np.where(labels == i)[0]
        print(cluster_embeddings.shape)
        distances = np.linalg.norm(cluster_embeddings - centroid, axis=1)
        closest_indices = np.argsort(distances)
        closest_values.append(cluster_embeddings[closest_indices])
        closest_utterance_indices[i] = cluster_idx[closest_indices]
        closest_values_dict[i] = closest_indices.tolist()
    print("got closest values for cluster")


    closest_utterances = get_utterances_from_closest_idx(closest_utterance_indices, args)
                
    # save the closest_utterances to a JSON file
    with open(args['closest_utterances_path'], 'w') as f:
        # add the utterances to the list
        json.dump(closest_utterances, f, indent=4)

    # save the closest_embeddings to a JSON file
    with open(args['centroids_path'], 'w') as f:
        # add the utterances to the list
        for item in closest_values:
            f.write("%s\n" % item)

    # save the cluster labels to a JSON file
    with open(args['clusters_path'], 'w') as f:
        json.dump(labels.tolist(), f, indent=4)

def get_Clusters(args):
    # get clusters from JSON file
    with open(args['clusters_path'], 'r') as f:
        clusters = json.load(f)
        clusters = np.array(clusters)
    return clusters

def get_turn_count(args):
    df = get_df(args)
    turn_count = []
    for i in range(len(df)):
        turn_count.append(len(eval(df['utterances'][i])))
    return turn_count

def get_segmented_values(args):
    # Create a segmented list of the cluster labels according to the number of turns in each dialogue
    segmented_values = []

    # Loop through the counts and split the values into sublists
    start_index = 0
    turn_count = get_turn_count(args)
    clusters = get_Clusters(args)
    for count in turn_count:
        end_index = start_index + count
        segmented_values.append(clusters[start_index:end_index])
        start_index = end_index
    return segmented_values

def get_cluster_dict(args):
    # Create a new column in the DataFrame with the segmented values
    df = get_df(args)
    df['cluster_labels'] = get_segmented_values(args)
    
    # # # Create cluster dict by combining the cluster labels with the utterances
    bot_cluster_dict = {}
    for i in range(len(df)):
        utterance = eval(df['utterances'][i])
        for j in range(len(df['cluster_labels'][i])):
            if df['cluster_labels'][i][j] not in bot_cluster_dict:
                bot_cluster_dict[int(df['cluster_labels'][i][j])] = [utterance[j]]
            else:
                bot_cluster_dict[int(df['cluster_labels'][i][j])].append(utterance[j])
            
    # Save the cluster dict to a JSON file
    with open(args['cluster_dict_path'], 'w') as f:
        json.dump(bot_cluster_dict, f, indent=4)
    # save changes to the dataframe
    df.to_csv(args['data_path'], index=False)

def hac_clustering(args):
    get_df(args)
    # # append embeddings to the dataframe
    make_embeddings_2dArray(args)
    # # get embeddings from JSON file
    embeddings = get_Embedding(args)
    # # make clusters using the embeddings
    make_Clusters(embeddings, args)
    # # get utterance clusters from clustering values
    get_cluster_dict(args)


if __name__ == '__main__':
    hac_clustering(args_bot)
    hac_clustering(args_user)