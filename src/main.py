from config import configs
import get_domain_txt
import bot_user_dataset
import embedding
import clustering
import labelling

get_domain_txt.get_domain_dataset()
print("got dataset for the domain")
bot_user_dataset.seperate_bot_user()
# seperated bot and user utterances
print("got bot and user utterances")
embedding.get_embeddings(configs['embedding_bot'])
embedding.get_embeddings(configs['embedding_user'])
# got embeddings for bot and user utterances
print("got embeddings for bot and user utterances")
clustering.hac_clustering(configs['clustering_bot'])
clustering.hac_clustering(configs['clustering_user'])
# got clusters for bot and user utterances
print("got clusters for bot and user utterances")
labelling.get_labels_file(configs['labeling_bot'])
labelling.get_labels_file(configs['labeling_user'])
# got labels for bot and user utterances
print("got labels for bot and user utterances")
print("done: clusters and labels in output folder")
merge_cluster.get_lemmatised_sentence()
merge_cluster.get_similar_clusters()
merge_cluster.get_replaced_clusters()
print("merged labels")
schema.get_schema()
