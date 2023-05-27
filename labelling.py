import openai
import json
from config import args_labeling_bot as args_bot
from config import args_labeling_user as args_user



def get_closest_utterances(args):
        # get closest utterances from output\sent\closest_utterances_sent_bot.json
        with open(args['closest_utterances_file']) as f:
            closest_utterances = json.load(f)
        return closest_utterances

def get_user_instruction(closest_utterance_list, args):
        user_instruction = args['user_instruction']
        # user_instruction = "You are given a set of utterances from a bot replying to a task oriented dialog system for movie listings. You need to output a high-level dialog action that the bot intends in the given utterances.\n\nThe dialog action you output must satisfy these constraints:\n1) It should be a short phrase\n2) It should not have any specific entity names\n3)end prompt with Dialog Action:\nUtterances:\n"
        # user_instruction = "You are given a set of utterances from a user talking to a task oriented dialog system for movie listings. You need to output a high-level dialog action that the user intends in the given utterances.\n\nThe dialog action you output must satisfy these constraints:\n1) It should be a short phrase\n2) It should not have any specific entity names\n3) end prompt with Dialog Action:\nUtterances:\n"
        
        for i in range(len(closest_utterance_list)):
            user_instruction += "\t\""+closest_utterance_list[i]+"\",\n"
        return user_instruction
        
    


def get_combined_chatgpt_response(args):
        openai.api_key = OPEN-AI-KEY
        label_to_instruction_dict = {}
        # user_instruction = "You are given a set of utterances from a user talking to a task oriented dialog system for movie listings. You need to output a high-level dialog action that the user intends in the given utterances.\n\nThe dialog action you output must satisfy these constraints:\n1) It should be a short phrase\n2) It should not have any specific entity names\n\nUtterances:\n\t\"okay thank you\",\n\t\t\"okay thank you\",\n\t\t\"okay thank you\",\n\t\t\"Okay thank you\",\n\t\t\"ok thank you\",\n\t\t\"Ok thank you\",\n\t\t\"ok thank you\",\n\t\t\"ok thank you\",\n\t\t\"ok thank you\",\n\t\t\"Okay thanks for the information.\",\n\t\t\"Okay .Thank you for the information\",\n\t\t\"ok great, thank you\",\n\t\t\"Ok great, thank you\",\n\t\t\"Okay thanks for the information\",\n\t\t\"Okay. Thanks\",\n\t\t\"Okay. Thanks\",\n\t\t\"Okay, thanks\",\n\t\t\"Okay, thanks\",\n\t\t\"Okay. Thanks for the info\",\n\t\t\"OK, thanks\"\n"
        closest_utterances_dict = get_closest_utterances(args)
        for key,closest_utterance_list  in closest_utterances_dict.items():
            user_instruction = get_user_instruction(closest_utterance_list, args)
            chatgpt_output = openai.ChatCompletion.create(
                                model="gpt-3.5-turbo",
                                messages = [
                                    {"role": "system", "content": ""},
                                    {"role": "user", "content": user_instruction}
                                ],
                                temperature=0.0,
                                max_tokens=200,
                                top_p=0.9,
                                frequency_penalty=0,
                                presence_penalty=0
                            )
            
            full_response = chatgpt_output["choices"][0]["message"]["content"].strip()
            gpt3_response  = full_response.split("Dialog Action:")[1].strip()
            label_to_instruction_dict[key] = gpt3_response
        
        return label_to_instruction_dict

def write_to_file(label_to_instruction_dict, args):
    with open(args['output_labels'], 'w') as fp:
        json.dump(label_to_instruction_dict, fp, indent=4)
    return

def get_labels_file(args):
    label_to_instruction_dict = get_combined_chatgpt_response(args)
    write_to_file(label_to_instruction_dict, args)

if __name__ == "__main__":
    get_labels_file(args_bot)
    get_labels_file(args_user)