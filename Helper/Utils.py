import pandas as pd
def aggregate_by_reciepies(reviewData):
    rating = reviewData[['recipe_id','rating']].groupby('recipe_id',as_index=False)['rating']\
        .agg(['mean','count'])\
        .rename(columns={"mean": "mean_rating", "count": "review_count"})
    return rating

def split_into_columns(rawData1,allNutriList):
    recpNutr=pd.DataFrame(rawData1['nutrition'].apply(eval).to_list(), index=rawData1.index\
                            ,columns=allNutriList)

    rawData= rawData1.join(recpNutr)
    RAW_recipes= rawData.copy()
    return RAW_recipes

def clamp_cols(col,RAW_recipes):
    IQR=RAW_recipes[col].quantile(0.75) - RAW_recipes[col].quantile(0.25)
    colmax=RAW_recipes[col].quantile(0.75) + 2.5 * IQR
    colmin=RAW_recipes[col].quantile(0.25) - 2.5 * IQR
    RAW_recipes=RAW_recipes[(RAW_recipes[col] < colmax) & (RAW_recipes[col] > colmin)]
    return RAW_recipes

def Convert_nutri(string):
    li = list(string.split('\', \''))
    return li
allIngredList=[]

def create_list(RAW_recipes):
    RAW_recipes_i=RAW_recipes.reset_index()
    for ind in range(len(RAW_recipes)):
        ss=RAW_recipes_i.loc[ ind , 'ingredients' ]
        ss=ss[2:-2]
        allIngredList.append(Convert_nutri(ss))
    records=allIngredList
    print("Showing first to list of ingredients:")
    print(records[0:2])
    return records