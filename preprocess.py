from datasets import load_dataset
import json
from config import domain_name, domain

dataset = load_dataset("meta_woz")

train_dataset = dataset["train"]
test_dataset = dataset["test"]

file_name = f'data/meta_woz_{domain_name}.txt'

def getDTCNFormat(dialogue_instance, file_name):
    dialog_dict = {}
    print(dialogue_instance)
    dialog_dict["session_id"] = dialogue_instance["id"]
    dialog_dict["domain"] = dialogue_instance["domain"]
    dialog_dict["task"] = domain
    dialog_dict["utterances"] = dialogue_instance["turns"]
    roles = []
    is_bot = True
    for i in range(len(dialogue_instance["turns"])):
        if is_bot:
            roles.append("BOT")
            is_bot = False
        else:
            roles.append("USER")
            is_bot = True
    dialog_dict["roles"] = roles


    with open(file_name, "a") as file:
    # Convert the dictionary to a string
        dict_string = json.dumps(dialog_dict)
        # Write the string to the file
        file.write(dict_string + "\n")


def list_to_turns(convo_list):
    is_user = True
    conversation = []
    turn_dict = {}
    for turn in convo_list:
        if is_user:
            turn_dict["utterance"] = turn
            is_user = False
        else:
            turn_dict["response"] = turn
            conversation.append(turn_dict)
            turn_dict = {}
            is_user = True
    return conversation

def get_domain_dataset():
    prev_domain = 'AGREEMENT_BOT'
    movies = []
    domain_to_convos = {prev_domain: []}
    for i in range(len(train_dataset)):
        if train_dataset[i]['domain'] == domain:
            getDTCNFormat(train_dataset[i], file_name)


if __name__ == '__main__':
    get_domain_dataset()
