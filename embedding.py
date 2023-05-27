from sentence_transformers import SentenceTransformer
from datasets import load_dataset
import pandas as pd
import json
from config import args_embedding_bot as args_bot
from config import args_embedding_user as args_user


def get_df(args):
    # Read the text file into a list of dictionaries
    with open(args['df_file_name'], 'r') as f:
        dataset = []
        dataset_small = []
        i = 0
        for line in f:
            data = json.loads(line.strip())
            dataset.append(data)
            if i < 800:
                dataset_small.append(data)
            i += 1

    # Convert the list of dictionaries to a Pandas DataFrame
    # df = pd.DataFrame(dataset)
    df = pd.DataFrame(dataset_small)
    return df

def get_embedding(text, model):
   x = model.encode(text)
   return list(x)


def df_embeddings(df, args):
    model = SentenceTransformer('all-mpnet-base-v2')
    df['sent_embeddings'] = df.utterances.apply(lambda x: [get_embedding(prompt, model=model) for prompt in x])

    output_file = args['output_dir'] + '/' + args['output_file_name']
    df.to_csv(output_file, index=False)

def get_embeddings(args):
    df = get_df(args)
    df_embeddings(df, args)

if __name__ == '__main__':
    get_embeddings(args_bot)
    get_embeddings(args_user)