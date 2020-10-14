from DataExploration import read_all_files,recombine_review_with_recipie
from Helper.Utils import create_list
from Helper.apyori import apriori

def read_data_MBA():
    print("Reading the food.com data: ")
    rawData1,review_data=read_all_files()
    df_Recipies=recombine_review_with_recipie(rawData1,review_data)
    Recipies=create_list(df_Recipies)
    return Recipies

def implement_apriori(Recipies):
    # TODO tune apriori parameters
    associationRules = apriori(Recipies, min_support=0.0050, min_confidence=0.6, min_lift=3, min_length=5,max_length=None)
    associationResult = list(associationRules)

    print("\n\nNumber of Rules:")
    print(len(associationResult))

    print("\n\nExample of a rule:")
    print(associationResult[0])
    print("\n\n")

    associationResult10=associationResult[0:10]

    print("Listing 10 of the rules:\n")
    for item in associationResult10:
        pair = item[0]
        items = [x for x in pair]
        print("Rule: " + items[0] + " --> " + items[1])
        print("Support: " + str(item[1]))
        print("Confidence: " + str(item[2][0][2]))
        print("Lift: " + str(item[2][0][3]))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def main():
    Recipies=read_data_MBA()
    implement_apriori(Recipies)

if __name__ == "__main__":
    main()