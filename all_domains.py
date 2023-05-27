import os
import json
import shutil
import importlib
domains = []
with open("dataset\meta_woz_by_domain.json", "r") as file:
    data = json.load(file)
    

# get keys in file
for key in data.keys():
    domains.append(key)

for domain in domains:
    # Set the original folder path and name
    original_folder = "order_pizza"
    original_folder_name = "order_pizza"

    # Set the new folder name
    new_folder_name = domain.lower()

    # Set the path where you want to create the new folder
    path = "./"

    if not os.path.exists(os.path.join(path, new_folder_name)):
    # Use shutil.copytree() to copy the original folder to the new folder
        shutil.copytree(original_folder, os.path.join(path, new_folder_name))

        # Rename the copied folder
        # os.rename(os.path.join(path, new_folder_name, original_folder_name), os.path.join(path, new_folder_name, new_folder_name))
     
     # change the domain name in config.py of the new folder
        with open(os.path.join(path, new_folder_name, "config.py"), "r") as file:
            data = file.readlines()
        data[0] = f"domain_name = '{domain}'\n"
        with open(os.path.join(path, new_folder_name, "config.py"), "w") as file:
            file.writelines(data)

# open all folders and change the domain name in config.py
for domain in domains:
    if domain == "ORDERING_PIZZA":
        continue
    if domain == "PET_ADVICE":
        continue
    module_name = domain.lower() + ".config"
    my_module = importlib.import_module(module_name)
    my_module.domain_name = domain
    with open(os.path.join(domain.lower(), "config.py"), "w") as file:
        # write all of this
        #         domain_name = "ordering_pizza"

        # domain_label = "ordering pizza"

        # domain = "ORDERING_PIZZA"



        # args_embedding_bot = {
        #     'dataset': 'meta_woz',
        #     'df_file_name' : 'df_bot.txt',
        #     'output_file_name' : 'embedded_sent_bot.csv',
        #     'output_dir': 'output\sent'
        # }

        # args_embedding_user = {
        #     'dataset': 'meta_woz',
        #     'df_file_name' : 'df_user.txt',
        #     'output_file_name' : 'embedded_sent_user.csv',
        #     'output_dir': 'output\sent'
        # }

        # args_clustering_bot = {
        #     'data_path': 'output\sent\embedded_sent_bot.csv',
        #     'embeddings_path': 'output\sent\embeddings_sent_bot.json',
        #     'clusters_path': 'output\sent\clusters_sent_bot.json',
        #     'cluster_dict_path': 'output\sent\sent_bot_dict_bot.json',
        #     'distance_threshold': 10.0,
        #     'centroids_path': 'output\sent\centroids_sent_bot.json',
        #     'closest_utterance_indices_path': 'output\sent\closest_utterance_indices_sent_bot.json',
        #     'closest_utterances_path': 'output\closest_utterances_sent_bot.json',

        # }
        # args_clustering_user = {
        #     'data_path': 'output\sent\embedded_sent_user.csv',
        #     'embeddings_path': 'output\sent\embeddings_sent_user.json',
        #     'clusters_path': 'output\sent\clusters_sent_user.json',
        #     'cluster_dict_path': 'output\sent\sent_user_dict_user.json',
        #     'distance_threshold': 10.0,
        #     'centroids_path': 'output\sent\centroids_sent_user.json',
        #     'closest_utterance_indices_path': 'output\sent\closest_utterance_indices_sent_user.json',
        #     'closest_utterances_path': 'output\closest_utterances_sent_user.json',

        # }

        # args_labeling_bot = {
        #     "user_instruction":   f'You are given a set of utterances of a task-oriented bot interacting with a user for {domain_label}. You need to output a high-level dialog action that the bot intends in the given utterances.\n\nThe dialog action you output must satisfy these constraints:\n1) It should be a short phrase\n2) It should not have any specific entity names\n3)Begin with Dialog Action:\nUtterances:\n',
        #     "output_labels": 'output\chatgpt_response_sent_bot.json',
        #     "closest_utterances_file": 'output\closest_utterances_sent_bot.json'
        # }

        # args_labeling_user = {
        #     "user_instruction":  f'You are given a set of utterances of a user interacting with a task-oriented bot for {domain_label}. You need to output a high-level dialog action that the user intends in the given utterances.\n\nThe dialog action you output must satisfy these constraints:\n1) It should be a short phrase\n2) It should not have any specific entity names\n3)Begin with Dialog Action:\nUtterances:\n',
        #     "output_labels": 'output\chatgpt_response_sent_user.json',
        #     "closest_utterances_file": 'output\closest_utterances_sent_user.json',
        # }

        # configs = {
        #     'embedding_bot': args_embedding_bot,
        #     'embedding_user': args_embedding_user,
        #     'clustering_bot': args_clustering_bot,
        #     'clustering_user': args_clustering_user,
        #     'labeling_bot': args_labeling_bot,
        #     'labeling_user': args_labeling_user,
        #      'domain': domain,
        #     'domain_name': domain_name,
        # }

        file.write(f"domain_name = '{domain.lower()}'\n")
        file.write(f"domain_label = '{domain.lower()}'\n")
        file.write(f"domain = '{domain.upper()}'\n")
        file.write("\n")
        file.write("args_embedding_bot = {\n")
        file.write(f"\t'dataset': 'meta_woz',\n")
        file.write(f"\t'df_file_name' : 'df_bot.txt',\n")
        file.write(f"\t'output_file_name' : 'embedded_sent_bot.csv',\n")
        file.write(f"\t'output_dir': 'output\sent'\n")
        file.write("}\n")
        file.write("\n")
        file.write("args_embedding_user = {\n")
        file.write(f"\t'dataset': 'meta_woz',\n")
        file.write(f"\t'df_file_name' : 'df_user.txt',\n")
        file.write(f"\t'output_file_name' : 'embedded_sent_user.csv',\n")
        file.write(f"\t'output_dir': 'output\sent'\n")
        file.write("}\n")
        file.write("\n")
        file.write("args_clustering_bot = {\n")
        file.write(f"\t'data_path': 'output\sent\embedded_sent_bot.csv',\n")
        file.write(f"\t'embeddings_path': 'output\sent\embeddings_sent_bot.json',\n")
        file.write(f"\t'clusters_path': 'output\sent\clusters_sent_bot.json',\n")

        file.write(f"\t'cluster_dict_path': 'output\sent\sent_bot_dict_bot.json',\n")


        file.write(f"\t'distance_threshold': 10.0,\n")
        file.write(f"\t'centroids_path': 'output\sent\centroids_sent_bot.json',\n")
        file.write(f"\t'closest_utterance_indices_path': 'output\sent\closest_utterance_indices_sent_bot.json',\n")
        file.write(f"\t'closest_utterances_path': 'output\closest_utterances_sent_bot.json',\n")
        file.write("\n")

        file.write("}\n")
        file.write("\n")
        file.write("args_clustering_user = {\n")
        file.write(f"\t'data_path': 'output\sent\embedded_sent_user.csv',\n")
        file.write(f"\t'embeddings_path': 'output\sent\embeddings_sent_user.json',\n")
        file.write(f"\t'clusters_path': 'output\sent\clusters_sent_user.json',\n")
        file.write(f"\t'cluster_dict_path': 'output\sent\sent_user_dict_user.json',\n")
        file.write(f"\t'distance_threshold': 10.0,\n")
        file.write(f"\t'centroids_path': 'output\sent\centroids_sent_user.json',\n")
        file.write(f"\t'closest_utterance_indices_path': 'output\sent\closest_utterance_indices_sent_user.json',\n")
        file.write(f"\t'closest_utterances_path': 'output\closest_utterances_sent_user.json',\n")

        file.write("}\n")
        file.write("\n")
        file.write("args_labeling_bot = {\n")
        file.write(f"\t\"user_instruction\":   f'You are given a set of utterances of a task-oriented bot interacting with a user for {domain.lower()}. You need to output a high-level dialog action that the bot intends in the given utterances.\\n\\nThe dialog action you output must satisfy these constraints:\\n1) It should be a short phrase\\n2) It should not have any specific entity names\\n3)Begin with Dialog Action:\\nUtterances:\\n',\n")
        file.write(f"\t\"output_labels\": 'output\chatgpt_response_sent_bot.json',\n")
        file.write(f"\t\"closest_utterances_file\": 'output\closest_utterances_sent_bot.json',\n")
        file.write("}\n")
        file.write("\n")
        file.write("args_labeling_user = {\n")
        file.write(f"\t\"user_instruction\":  f'You are given a set of utterances of a user interacting with a task-oriented bot for {domain.lower()}. You need to output a high-level dialog action that the user intends in the given utterances.\\n\\nThe dialog action you output must satisfy these constraints:\\n1) It should be a short phrase\\n2) It should not have any specific entity names\\n3)Begin with Dialog Action:\\nUtterances:\\n',\n")
        file.write(f"\t\"output_labels\": 'output\chatgpt_response_sent_user.json',\n")
        file.write(f"\t\"closest_utterances_file\": 'output\closest_utterances_sent_user.json',\n")
        file.write("}\n")
        file.write("\n")
        file.write("configs = {\n")
        file.write("\t'embedding_bot': args_embedding_bot,\n")
        file.write("\t'embedding_user': args_embedding_user,\n")
        file.write("\t'clustering_bot': args_clustering_bot,\n")
        file.write("\t'clustering_user': args_clustering_user,\n")
        file.write("\t'labeling_bot': args_labeling_bot,\n")
        file.write("\t'labeling_user': args_labeling_user,\n")
        file.write("\t 'domain': domain,\n")
        file.write("\t'domain_name': domain_name,\n")
        file.write("}\n")
        file.write("\n")
        file.write("\n")
        file.write("\n")
        file.write("\n")
        file.write("\n")

        file.close()





    



