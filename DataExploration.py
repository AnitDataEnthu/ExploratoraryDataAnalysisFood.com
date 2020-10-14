from Helper.Data import read_data,column_types,get_list
from Helper.Utils import aggregate_by_reciepies,split_into_columns,clamp_cols
from Visualizations.Visualizations import average_rating,Review_frequency,boxplots,minute_transformation,check_correlations


def read_all_files():
    data_path="Data/"
    print("Reading the reciepies data: ")
    file_name_recipies=data_path + "RAW_recipes.csv"
    recipie_data=read_data(file_name_recipies)

    print("Reading the reviews data: ")
    file_name_reviews=data_path + "RAW_interactions.csv"
    review_data=read_data(file_name_reviews)

    print("Column data types for Recipie data")
    column_types(recipie_data)

    print("Column data types for Review data")
    column_types(review_data)

    rawData=recipie_data.astype({'id':'object','contributor_id':'object'})
    rawData['id_copy']=rawData['id']
    rawData1=rawData.set_index('id')

    print("Number of total recipes: ",rawData["id"].count())
    print("Number of contributors: ",rawData["contributor_id"].nunique())

    print("Total number of reviews: ",review_data["recipe_id"].count())
    print("Total number of contributors: ",review_data["user_id"].nunique())

    return rawData1,review_data

def recombine_review_with_recipie(rawData1,review_data):
    print("Summarize the interactions data based on recipe_id, so that we might have the mean rating for each recipe and also the number of reviews posted for each recipe.")
    ratings=aggregate_by_reciepies(review_data)
    print(ratings.head())

    #print("Combining the review and the recipie data:")
    rawData_final = rawData1.join(ratings)
    print(rawData_final.columns)
    #print(rawData_final.head(5))

    return rawData_final

#data preprocessing begins here
# 1.1
def prepocessing(rawData_final):
    rawData_final['ingr_str'] = rawData_final['ingredients'].apply(get_list)
    print("columns after the strings list ingriedients are converted to ingriedients")
    print("printing just the ingriedients")
    print(rawData_final['ingredients'].head(1))



    #flattening the number of columns
    print("Flattening the nutritional values to columns")
    allNutriList=['cal', 'totalFat', 'sugar', 'sodium', 'protein', 'satFat', 'carbs']
    rawData_final=split_into_columns(rawData_final,allNutriList)
    print("Column data types for Recipie data")
    column_types(rawData_final)
    return rawData_final

def dataExploration(rawData1,rawData_final):
    #Data Exploration
    average_rating(rawData_final)
    Review_frequency(rawData_final)
    print("Printing Boxplot to check for data outliers")
    numeric_cols = ['minutes', 'n_steps', 'n_ingredients', 'cal', 'totalFat', 'sugar', 'sodium', 'protein', 'satFat', 'carbs']
    rawData_final = rawData_final.reset_index()

    boxplots(rawData_final,numeric_cols)

    #clamping to remove ouliers
    Col_to_clamp=['n_steps','minutes','n_ingredients','cal', 'totalFat', 'sugar',   'sodium', 'protein', 'satFat', 'carbs']
    for col in Col_to_clamp:
        rawData_final=clamp_cols(col,rawData_final)

    print("checking if the transformation is applied : ")
    print("max of minutes columns BEFORE transformation: ", max(rawData1['minutes']))
    print("max of minutes columns AFTER transformation: ", max(rawData_final['minutes']))
    print("Plot for minute data before transformation: ")
    minute_transformation(rawData_final,1)
    print("Plot for minute data After transformation: ")
    minute_transformation(rawData1,0)

    #Check correlation between columns
    check_correlations(rawData_final)
    return rawData_final

def main():
    rawData1,review_data=read_all_files()
    rawData_final=recombine_review_with_recipie(rawData1,review_data)
    rawData_final=prepocessing(rawData_final)
    rawData_final=dataExploration(rawData1,rawData_final)
if __name__ == "__main__":
    main()