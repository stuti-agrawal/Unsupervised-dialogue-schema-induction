import pandas as pd
import json
from config import domain_name  

def seperate_bot_user():
    with open(f'meta_woz_{domain_name}.txt', 'r') as f:
        dataset = []
        for line in f:
            data = json.loads(line.strip())
            dataset.append(data)


    # Create a dataframe from the datasets
    df = pd.DataFrame(dataset)
    df_user = df.copy()
    df_bot = df.copy()
    # drop utterances and roles columns
    df_user.drop(['utterances', 'roles'], axis=1, inplace=True)
    df_bot.drop(['utterances', 'roles'], axis=1, inplace=True)

    df_bot['utterances'] = ['' for i in range(len(df))]
    df_user['utterances'] = ['' for i in range(len(df))]

    for i in range(len(df)):
        bot_utterances = []
        user_utterances = []
        for j in range(len(df['utterances'][i])):
            if df['roles'][i][j] == 'BOT':
                bot_utterances.append(df['utterances'][i][j])
            else:
                user_utterances.append(df['utterances'][i][j])
        df_bot['utterances'][i] = bot_utterances
        df_user['utterances'][i] = user_utterances

    # save df_bot and df_user to txt files
    with open('df_bot.txt', 'w') as f:
        for i in range(len(df_bot)):
            f.write(json.dumps(df_bot.iloc[i].to_dict()) + '\n')

    with open('df_user.txt', 'w') as f:
        for i in range(len(df_user)):
            f.write(json.dumps(df_user.iloc[i].to_dict()) + '\n')

if "__init__" == '__main__':
    seperate_bot_user()
    
        
