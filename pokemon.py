import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast
def bar_show(columnname,ascending:bool,xlabel:str,ylabel:str,rotation:int,text:str,color:str='blue',filter_flag:bool=False):
    counts=useful_csv[columnname].value_counts()
    
    ranks=counts.rank(ascending=ascending)
    ranks_df=pd.DataFrame({xlabel:ranks.index,ylabel:ranks.values})
    if filter_flag:
       ranks_df=ranks_df.head(10)
       plt.bar(counts.head(10).index,counts.head(10).values,color=color)
    else:
       plt.bar(counts.index,counts.values,color=color)
    print(ranks_df.to_string(index=False))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if rotation:
      plt.xticks(rotation=rotation)
    if text:
       ax = plt.gca()
       xpos = ax.get_xlim()[1] + (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.05
       ypos = ax.get_ylim()[1] * 0.5
       plt.text(xpos, ypos, text, va='center')
    plt.show()
pokemon_csv=pd.read_csv("E:\\DataScience\\Kaggle\\Datasets\\pokemon.csv")
#Get Pokemon Descriptive Statistics
csv_count=pokemon_csv['pokedex_number'].nunique()
ty1,nty1=pokemon_csv['type1'].unique(),pokemon_csv['type1'].nunique()
ty2_,nty2_=pokemon_csv['type2'].unique(),pokemon_csv['type2'].nunique()
ty2=ty2_[~pd.isnull(ty2_)]
nty2=ty2.size
ty1.sort()
ty2.sort()
null_column=pokemon_csv.isnull().sum()[pokemon_csv.isnull().any()]
useless_column=['classfication','base_egg_steps','base_happiness','pokedex_number','japanese_name','percentage_male']
null_column=null_column[~null_column.index.isin(useless_column)]
useful_csv=pokemon_csv.drop(columns=useless_column)
#Process the capture_rate column and convert its type to the numeric type
useful_csv['capture_rate'].replace('30 (Meteorite)255 (Core)',np.nan,inplace=True)
useful_csv['capture_rate'] = useful_csv.apply(lambda x: np.nan if pd.isna(x['capture_rate']) else ast.literal_eval(x['capture_rate']), axis=1)
#Data Processing and Data Visualization
#1. The number of occurrences and rankings of each type
bar_show('type1',False,'Type','Counts',60,None)
#2. How many new pokémon are there per generation?
bar_show('generation',False,'Generation','Counts',None,None,color='darkred')
#3. What about secondary types?
pokemon_without_secondary=useful_csv['type2'].isnull().sum()
type2_text='Pokémon with type2:{:.2%}\nPokémon with only type1:{:.2%}'.format((csv_count-pokemon_without_secondary)/csv_count,pokemon_without_secondary/csv_count)
bar_show('type2',False,'Type2','Counts',60,type2_text,color='darkblue')
type_df=pd.concat([useful_csv['type1'].value_counts(),useful_csv['type2'].value_counts()],axis=1)
bars1 = plt.bar(type_df.index, type_df['type1'])
bars2 = plt.bar(type_df.index, type_df['type2'], bottom=type_df['type1'])

for bar in bars1:
    height = bar.get_height()
    plt.annotate(f'{height}',
                 xy=(bar.get_x() + bar.get_width() / 2, height / 2),
                 xytext=(0, 0),
                 textcoords="offset points",
                 ha='center', va='center')
for bar in bars2:
    height = bar.get_height()
    plt.annotate(f'{height}',
                 xy=(bar.get_x() + bar.get_width() / 2,
                     bar.get_y() + height / 2),
                 xytext=(0, 0),
                 textcoords="offset points",
                 ha='center', va='center')
plt.xticks(rotation=60)
plt.show()
#4. What are the most common type combinations?
type_combinations=useful_csv['type1']+'_'+useful_csv['type2']
useful_csv['type_combinations']=type_combinations
bar_show('type_combinations',False,'Type Combination','Counts',60,None,color='darkgreen',filter_flag=True)
#5. What are the most common types of legendary pokémon?
useful_csv['type_legendary']=useful_csv['type1'][useful_csv['is_legendary']==1]
bar_show('type_legendary',False,'Legendary Type','Counts',60,None,color='yellow')
#6. How does primary type vary across generations?
Generation_type=useful_csv['type1'][useful_csv['generation']==useful_csv['generation'].min()].value_counts()
Generation_type.name='Generation 1'
for i in range(useful_csv['generation'].min()+1,useful_csv['generation'].max()+1):
   temp=useful_csv['type1'][useful_csv['generation']==i].value_counts()
   temp.name='Generation'+str(i)
   Generation_type=pd.concat([Generation_type,temp],axis=1)
Generation_type.replace(np.nan,0,inplace=True)