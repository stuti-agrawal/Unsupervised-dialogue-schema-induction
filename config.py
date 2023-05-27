domain_name = "ordering_pizza"

domain_label = "ordering pizza"

domain = "ORDERING_PIZZA"



args_embedding_bot = {
    'dataset': 'meta_woz',
    'df_file_name' : 'data\df_bot.txt',
    'output_file_name' : 'embedded_sent_bot.csv',
    'output_dir': 'output\sent'
}

args_embedding_user = {
    'dataset': 'meta_woz',
    'df_file_name' : 'data\df_user.txt',
    'output_file_name' : 'embedded_sent_user.csv',
    'output_dir': 'output\sent'
}

args_clustering_bot = {
    'data_path': 'output\sent\embedded_sent_bot.csv',
    'embeddings_path': 'output\sent\embeddings_sent_bot.json',
    'clusters_path': 'output\sent\clusters_sent_bot.json',
    'cluster_dict_path': 'output\sent\sent_bot_dict_bot.json',
    'distance_threshold': 10.0,
    'centroids_path': 'output\sent\centroids_sent_bot.json',
    'closest_utterance_indices_path': 'output\sent\closest_utterance_indices_sent_bot.json',
    'closest_utterances_path': 'output\closest_utterances_sent_bot.json',

}
args_clustering_user = {
    'data_path': 'output\sent\embedded_sent_user.csv',
    'embeddings_path': 'output\sent\embeddings_sent_user.json',
    'clusters_path': 'output\sent\clusters_sent_user.json',
    'cluster_dict_path': 'output\sent\sent_user_dict_user.json',
    'distance_threshold': 10.0,
    'centroids_path': 'output\sent\centroids_sent_user.json',
    'closest_utterance_indices_path': 'output\sent\closest_utterance_indices_sent_user.json',
    'closest_utterances_path': 'output\closest_utterances_sent_user.json',

}

args_labeling_bot = {
    "user_instruction":   f'You are given a set of utterances of a task-oriented bot interacting with a user for {domain_label}. You need to output a high-level dialog action that the bot intends in the given utterances.\n\nThe dialog action you output must satisfy these constraints:\n1) It should be a short phrase\n2) It should not have any specific entity names\n3)Begin with Dialog Action:\nUtterances:\n',
    "output_labels": 'output\chatgpt_response_sent_bot.json',
    "closest_utterances_file": 'output\closest_utterances_sent_bot.json'
}

args_labeling_user = {
    "user_instruction":  f'You are given a set of utterances of a user interacting with a task-oriented bot for {domain_label}. You need to output a high-level dialog action that the user intends in the given utterances.\n\nThe dialog action you output must satisfy these constraints:\n1) It should be a short phrase\n2) It should not have any specific entity names\n3)Begin with Dialog Action:\nUtterances:\n',
    "output_labels": 'output\chatgpt_response_sent_user.json',
    "closest_utterances_file": 'output\closest_utterances_sent_user.json',
}

configs = {
    'embedding_bot': args_embedding_bot,
    'embedding_user': args_embedding_user,
    'clustering_bot': args_clustering_bot,
    'clustering_user': args_clustering_user,
    'labeling_bot': args_labeling_bot,
    'labeling_user': args_labeling_user,
     'domain': domain,
    'domain_name': domain_name,
}
