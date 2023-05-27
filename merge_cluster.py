import spacy
import json
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

def get_counts_bot_user():
    with open("output\sent\clusters_sent_bot.json") as f:
        bot_clusters = json.load(f)
    with open("output\sent\clusters_sent_user.json") as f:
        user_clusters = json.load(f)
    return Counter(bot_clusters), Counter(user_clusters)
    
    
    
def get_lemmatised_sentence():
    with open('output\chatgpt_response_sent_bot.json') as f:
        bot_label_dict = json.load(f)

    with open('output\chatgpt_response_sent_user.json') as f:
        user_label_dict = json.load(f)

    # # lemmatise all the labels and store in a dict
    nlp = spacy.load("en_core_web_md")
    # lemmatise "request for dog's breed"
    # doc = nlp("request for dog's breed")
    # lemmatized_sentence = ' '.join([token.lemma_ for token in doc])
    # print(lemmatized_sentence)
    bot_lemmatised = []
    user_lemmatised = []

    bot_label_dict_lemmatized = {}
    user_label_dict_lemmatized = {}
    for key, value in bot_label_dict.items():
        doc = nlp(value)
        lemmed = ' '.join([token.lemma_ for token in doc])
        bot_label_dict_lemmatized[key] =  lemmed.lower()
        bot_lemmatised.append(lemmed.lower())
    for key, value in user_label_dict.items():
        doc = nlp(value)
        lemmed = ' '.join([token.lemma_ for token in doc])
        user_label_dict_lemmatized[key] = lemmed.lower()
        user_lemmatised.append(lemmed.lower())

    # store the lemmatised labels in a file
    with open('output\chatgpt_response_sent_bot_lemmatized.json', 'w') as fp:
        json.dump(bot_label_dict_lemmatized, fp, indent=4)
    with open('output\chatgpt_response_sent_user_lemmatized.json', 'w') as fp:
        json.dump(user_label_dict_lemmatized, fp, indent=4)
    return bot_lemmatised, user_lemmatised



    
def get_similar_clusters():
    # find all the sentences that are similar by cosine similarity and store similar cluster labels in a dict
    # load the labels from file
    with open('output\chatgpt_response_sent_bot_lemmatized.json') as f:
        bot_label_dict = json.load(f)
    with open('output\chatgpt_response_sent_user_lemmatized.json') as f:
        user_label_dict = json.load(f)

    nlp = spacy.load("en_core_web_md")
    similar_bot_clusters = {}
    similar_user_clusters = {}
    threshold = 0.75
    intersection_threshold = 0.5

    bot_labels, user_labels = list(bot_label_dict.values()), list(user_label_dict.values())
    # put all same clusters together and choose the representative cluster label based on counts
    bot_counts, user_counts = get_counts_bot_user() 

    for i in range(len(bot_labels)):
        doc1 = nlp(bot_labels[i])
        for j in range(i+1, len(bot_labels)):
            doc2 = nlp(bot_labels[j])
            similarity = cosine_similarity(doc1.vector.reshape(1, -1), doc2.vector.reshape(1, -1))
            print(bot_labels[i], bot_labels[j], similarity)
            if similarity>0.85 or (similarity > threshold and min(bot_counts[bot_labels[i]],bot_counts[bot_labels[j]]) < intersection_threshold*max(bot_counts[bot_labels[i]], bot_counts[bot_labels[j]])):
                if i not in similar_bot_clusters and j not in similar_bot_clusters:
                    similar_bot_clusters[i] = [j]
                    similar_bot_clusters[j] = i
                elif i not in similar_bot_clusters and j in similar_bot_clusters:
                    if type(similar_bot_clusters[j]) == list:
                        similar_bot_clusters[i] = j
                        similar_bot_clusters[j].append(i)
                    elif type(similar_bot_clusters[j]) == int:
                        similar_bot_clusters[similar_bot_clusters[j]].append(i)
                        similar_bot_clusters[i] = similar_bot_clusters[j]
                elif i in similar_bot_clusters and type(similar_bot_clusters[i]) == list:
                    if j not in similar_bot_clusters[i]:
                        similar_bot_clusters[i].append(j)
                    similar_bot_clusters[j] = i
                elif i in similar_bot_clusters and type(similar_bot_clusters[i]) == int:
                    if j not in similar_bot_clusters[similar_bot_clusters[i]]:
                        similar_bot_clusters[similar_bot_clusters[i]].append(j)
                    similar_bot_clusters[j] = similar_bot_clusters[i]
    for i in range(len(user_labels)):
        doc1 = nlp(user_labels[i])
        for j in range(i+1, len(user_labels)):
            doc2 = nlp(user_labels[j])
            similarity = cosine_similarity(doc1.vector.reshape(1, -1), doc2.vector.reshape(1, -1))
            print(user_labels[i], user_labels[j], similarity)
            if similarity >0.85 or (similarity > threshold and min(user_counts[user_labels[i]],user_counts[user_labels[j]]) < intersection_threshold*max(user_counts[user_labels[i]], user_counts[user_labels[j]])):
                if i not in similar_user_clusters:
                    similar_user_clusters[i] = [j]
                    similar_user_clusters[j] = i
                elif i in similar_user_clusters and type(similar_user_clusters[i]) == list:
                    if j not in similar_user_clusters[i]:
                        similar_user_clusters[i].append(j)
                    similar_user_clusters[j] = i
                elif i in similar_user_clusters and type(similar_user_clusters[i]) == int:
                    if j not in similar_user_clusters[similar_user_clusters[i]]:
                        similar_user_clusters[similar_user_clusters[i]].append(j)
                    similar_user_clusters[j] = similar_user_clusters[i]

    # store the similar clusters in a file
    with open('output\chatgpt_response_sent_bot_similar_clusters.json', 'w') as fp:
        json.dump(similar_bot_clusters, fp, indent=4)
    with open('output\chatgpt_response_sent_user_similar_clusters.json', 'w') as fp:
        json.dump(similar_user_clusters, fp, indent=4)

def get_replaced_clusters():
    with open('output\chatgpt_response_sent_bot_similar_clusters.json') as f:
        bot_similar_clusters = json.load(f)
    with open('output\chatgpt_response_sent_user_similar_clusters.json') as f:
        user_similar_clusters = json.load(f)
    # get clusters
    with open("output\sent\clusters_sent_bot.json") as f:
        bot_clusters = json.load(f)
    with open("output\sent\clusters_sent_user.json") as f:
        user_clusters = json.load(f)

    bot_counts, user_counts = get_counts_bot_user()
    print(bot_counts, user_counts)
    bot_replabel_dict = {}
    user_replabel_dict = {}
    for key, value in bot_similar_clusters.items():
        val = [int(key)]
        if type(value) == list:
            # find which cluster has the highest count including the key
            max_count = bot_counts[int(key)]
            max_cluster = key
            for i in value:
                val.append(i)
                if bot_counts[i] > max_count:
                    max_count = bot_counts[i]
                    max_cluster = i
            bot_replabel_dict[max_cluster] = val
    for key, value in user_similar_clusters.items():
        if type(value) == list:
            val = [int(key)]
            # find which cluster has the highest count including the key
            max_count = user_counts[key]
            max_cluster = int(key)
            for i in value:
                val.append(i)
                if user_counts[i] > max_count:
                    max_count = user_counts[i]
                    max_cluster = i
            user_replabel_dict[max_cluster] = val

    for key, value in bot_replabel_dict.items():
        print(key, value)
        bot_clusters = [int(key) if x in value else x for x in bot_clusters]
    for key, value in user_replabel_dict.items():
        user_clusters = [int(key) if x in value else x for x in user_clusters]

    # store the replaced clusters in a file
    with open('output\sent\clusters_sent_bot_replaced.json', 'w') as fp:
        json.dump(bot_clusters, fp, indent=4)
    with open('output\sent\clusters_sent_user_replaced.json', 'w') as fp:
        json.dump(user_clusters, fp, indent=4)


def sample_similarity():
    #   "request information about the user 's dog .", "request Dog Information"
    # nlp = spacy.load("en_core_web_sm")
    # doc1 = nlp("request information about the user 's dog .")
    # doc2 = nlp("request Dog Information")
    # similarity = cosine_similarity(doc1.vector.reshape(1, -1), doc2.vector.reshape(1, -1))
    # print(similarity)
    nlp = spacy.load('en_core_web_md')

    # Define the two strings to compare
    string1 = "request user's dog information"
    string2 = "request Dog Information"

    # Lemmatize the strings
    lemmatized_string1 = ' '.join([token.lemma_ for token in nlp(string1)])
    lemmatized_string2 = ' '.join([token.lemma_ for token in nlp(string2)])

    # Compute the cosine similarity between the vectors of the two strings
    similarity = cosine_similarity(nlp(lemmatized_string1).vector.reshape(1,-1), nlp(lemmatized_string2).vector.reshape(1,-1))

    print(f"The cosine similarity between '{string1}' and '{string2}' is: {similarity[0][0]}")


if __name__ == '__main__':
    print(get_counts_bot_user())
    get_lemmatised_sentence()
    get_similar_clusters()
    get_replaced_clusters()





