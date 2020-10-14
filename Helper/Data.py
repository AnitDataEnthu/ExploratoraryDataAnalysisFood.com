import pandas as pd
import re

from sklearn.feature_extraction.text import TfidfVectorizer


def read_data(file_name):
    recipeDataUrl=file_name
    df=pd.read_csv(recipeDataUrl,low_memory=False)
    data=df.columns
    print("List of columns: ",[x for x in data])
    print("Number of columns: ",len(data))
    return df

def column_types(data):
    if type(data)==pd.DataFrame:
        print(data.dtypes)

def get_list(x):
    strlistF = []
    strlist = eval(x)
    for item in strlist:
        if len(item) > 2 and not re.search("[^a-zA-Z\s]",item):
            temp1 = item.strip()
            temp2 = temp1.replace(" ","_")
            strlistF.append(temp2)

    return(" ".join(strlistF))

def read_data_json(file_name):
    df=pd.read_json(file_name)
    data=df.columns
    print("List of columns: ",[x for x in data])
    print("Number of columns: ",len(data))
    return df

def split(train):
    # splitting descriptive features and target feature
    train['ingredient_list']=[','.join(z).strip() for z in train['ingredients']]
    ingredients=train['ingredient_list']
    vectorizer=TfidfVectorizer(stop_words='english')
    tfidf_matrix=vectorizer.fit_transform(ingredients).todense()
    cuisines=train['cuisine']
    return tfidf_matrix,cuisines