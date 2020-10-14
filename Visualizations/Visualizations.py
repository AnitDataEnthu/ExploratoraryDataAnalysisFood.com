import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def average_rating(rawData):
    fig8,ax=plt.subplots(1,figsize=(10,6))
    plt.style.use('seaborn-darkgrid')
    cmap_list=plt.get_cmap('viridis').colors

    n,bins,patches=ax.hist(rawData['mean_rating'],alpha=0.7)

    # apply the same color for each class to match the map
    idx=0
    for c,p in zip(bins,patches):
        plt.setp(p,'facecolor',cmap_list[idx])
        idx+=12

    ax.set(xlabel='Average Rating',ylabel='Frequency',title="Average Rating histogram",yscale="log")
    plt.savefig('Plots/average_rating_histogram.png',bbox_inches='tight')
    plt.show()

def Review_frequency(rawData):
    fig8,ax=plt.subplots(1,figsize=(10,6))
    plt.style.use('seaborn-deep')
    cmap_list=plt.get_cmap('cividis').colors

    n,bins,patches=ax.hist(rawData['review_count'],alpha=0.7)

    # apply the same color for each class to match the map
    idx=0
    for c,p in zip(bins,patches):
        plt.setp(p,'facecolor',cmap_list[idx])
        idx+=25

    ax.set(xlabel='Number of Reviews',ylabel='Frequency',title="Review Frequency histogram",yscale="log")
    plt.savefig('Plots/Review_frequency_histogram.png',bbox_inches='tight')
    plt.show()

def boxplots(rawData,numeric_cols):
    plt.style.use('ggplot')
    fig,axis=plt.subplots(2,5,figsize=(14,10))
    axis=axis.ravel()
    colors=plt.get_cmap('Set1',15).colors
    for i,ax in enumerate(axis):
        sns.boxplot(data=rawData[numeric_cols[i]],color=colors[i + 1],ax=ax)
        ax.set(title=numeric_cols[i])
    plt.tight_layout()
    plt.savefig('Plots/boxplots_for_outlier_detection.png')
    plt.show()


def minute_transformation(rawData,state):
    fig8,ax=plt.subplots(1)
    plt.style.use('seaborn-deep')
    cmap_list=plt.get_cmap('plasma').colors

    n,bins,patches=ax.hist(rawData['minutes'],alpha=0.7)

    # apply the same color for each class to match the map
    idx=0
    for c,p in zip(bins,patches):
        plt.setp(p,'facecolor',cmap_list[idx])
        idx+=6

    if state==0:
        ax.set(xlabel='Minutes',ylabel='Frequency',title="Histogram for Minutes before Pre-processing",yscale="log")
        plt.savefig('Plots/minutes_before.png',bbox_inches='tight')
        plt.show()
    elif state==1:
        ax.set(xlabel='Minutes',ylabel='Frequency',title="Histogram for Minutes after Pre-processing",yscale="log")
        plt.savefig('Plots/minutes_after.png',bbox_inches='tight')
        plt.show()

def check_correlations(RAW_recipes):
    fig,ax=plt.subplots(1,figsize=(14,8))
    sns.heatmap(RAW_recipes[["minutes","mean_rating","n_steps","n_ingredients","review_count"]].corr(),vmin=-1,vmax=1,
                center=0,annot=True,cmap=plt.get_cmap('RdBu'),square=True,ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(),rotation=45,horizontalalignment='right')
    ax.set_yticklabels(ax.get_yticklabels(),rotation=0)
    plt.savefig('Plots/correlation_heat_map.png',bbox_inches='tight')
    plt.tight_layout()


def cuisine_Distribution(df_R):
    gb_interactions=df_R.groupby('cuisine')['cuisine']
    df_cusine=pd.concat([gb_interactions.count()],axis=1)
    df_cusine.rename(columns={'cuisine':'cuisine_count'},inplace=True)
    df_cusine=df_cusine.reset_index()

    fig8,ax=plt.subplots(1,figsize=(13,6))
    ax.bar(color=sns.color_palette('GnBu_r',21),x=df_cusine['cuisine'],height=df_cusine['cuisine_count'],width=1)
    ax.set(xlabel='Cuisine',ylabel='No of Recipies',title="Recipies per cuisine")
    plt.xticks(rotation=65)
    plt.savefig('Plots/cuisine_Distribution.png',bbox_inches='tight')
    plt.show();

def avg_num_of_min_per_cuisine(df_R):
    score=[]
    for cusine in df_R['cuisine'].unique():
        df_per_cuisine=df_R[df_R['cuisine'] == cusine]
        average=df_per_cuisine['minutes'].sum() / df_per_cuisine['minutes'].count()
        score.append({"cuisine":cusine,"average":average.round(2)})

    avg_min_per_cuisine=pd.DataFrame(score)
    avg_min_per_cuisine=avg_min_per_cuisine.drop(avg_min_per_cuisine[avg_min_per_cuisine.average > 500].index)
    avg_min_per_cuisine
    fig8,ax=plt.subplots(1,figsize=(13,6))
    ax.bar(color=sns.color_palette('GnBu_r',21),x=avg_min_per_cuisine['cuisine'],height=avg_min_per_cuisine['average'],
           width=1)
    ax.set(xlabel='Cuisine',ylabel='No of Avg Minutes ',title="Avgerage Number of minutes per cuisine")
    plt.xticks(rotation=65)
    plt.savefig('Plots/avg_num_of_min_per_cuisine.png',bbox_inches='tight')
    plt.show()

def Review_count_per_cuisine(df_R):
    score=[]
    for cusine in df_R['cuisine'].unique():
        df_per_cuisine=df_R[df_R['cuisine'] == cusine]
        average=df_per_cuisine['review_count'].sum()
        score.append({"cuisine":cusine,"average":average.round(2)})

    avg_min_per_cuisine=pd.DataFrame(score)

    import matplotlib.pyplot
    fig8,ax=plt.subplots(1,figsize=(13,6))
    ax.bar(color=sns.color_palette('GnBu_r',21),x=avg_min_per_cuisine['cuisine'],height=avg_min_per_cuisine['average'],
           width=1)
    ax.set(xlabel='Cuisine',ylabel='Review Count ',title="Review Count per cuisine")
    plt.xticks(rotation=65)
    plt.savefig('Plots/Review_count_per_cuisine.png',bbox_inches='tight')
    plt.show()
