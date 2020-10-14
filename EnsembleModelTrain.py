from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,accuracy_score
from sklearn.model_selection import train_test_split,GridSearchCV

from Helper.Data import read_data_json
from DataExploration import read_all_files,recombine_review_with_recipie
from sklearn.feature_extraction.text import TfidfVectorizer
from Visualizations.Visualizations import cuisine_Distribution,Review_count_per_cuisine,avg_num_of_min_per_cuisine

def read_data_to_train():
    data_path="Data/"
    print("Reading the train data: ")
    train_data_location= data_path+"train.json"
    train=read_data_json(train_data_location)

    print("Reading the test data: ")
    test_data_location= data_path+"test.json"
    test=read_data_json(test_data_location)

    print("Reading the food.com data: ")
    rawData1,review_data=read_all_files()
    df_R=recombine_review_with_recipie(rawData1,review_data)
    return train, test, df_R


def train_the_model(train,param_grid):
    print("creating the splits from the train data")
    train['ingredient_list'] = [','.join(z).strip() for z in train['ingredients']]
    ingredients = train['ingredient_list']
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix= vectorizer.fit_transform(ingredients).todense()
    cuisines = train['cuisine']

    print("TF-IDF Matrix looks like below :\n",tfidf_matrix,"\n")
    print("Cuisine looks like below :\n",cuisines.head(),"\n")

    X_train, X_test, y_train, y_test = train_test_split(tfidf_matrix, cuisines, test_size=0.2)
    #param_grid = {'n_estimators': [1]}
    grid = GridSearchCV(RandomForestClassifier(), param_grid, cv=5)

    print("training the model from the grid search")
    grid.fit(X_train,y_train)

    print("best param",grid.best_params_)
    print("best score",grid.best_score_)
    print("best estimator",grid.best_estimator_)

    print("model score : ",grid.score(X_test, y_test))
    y_pred = grid.predict(X_test)
    print("model accuracy : ",accuracy_score(y_test, y_pred))
    cuisines = train['cuisine'].value_counts().index
    print(classification_report(y_test, y_pred, target_names=cuisines))
    return vectorizer,grid


# test['ingredient_list'] = [','.join(z).strip() for z in test['ingredients']]
# test_ingredients = test['ingredient_list']
# test_tfidf_matrix = vectorizer.transform(test_ingredients)
# test_cuisines = grid.predict(test_tfidf_matrix)
# test['cuisine'] = test_cuisines
# test.iloc[7:8,:]
def transfer_learning(vectorizer,grid,df_R):
    print("Using pretrained model to predict the cusine in the food.com data")
    df_R['ingredient_list'] = [''.join(z).strip() for z in df_R['ingredients']]
    df_R_ingredients = df_R['ingredient_list']
    df_R_tfidf_matrix = vectorizer.transform(df_R_ingredients)
    df_R_cuisines = grid.predict(df_R_tfidf_matrix)
    df_R['cuisine'] = df_R_cuisines
    df_R.head()
    return df_R


def exploration_with_cusisine(df_R):
    cuisine_Distribution(df_R)
    avg_num_of_min_per_cuisine(df_R)
    Review_count_per_cuisine(df_R)

def main():
    train,test,df_R=read_data_to_train()
    vectorizer,grid=train_the_model(train)
    df_R=transfer_learning(vectorizer,grid,df_R)
    exploration_with_cusisine(df_R)
if __name__ == "__main__":
    main()
