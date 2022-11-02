import pandas as pd
import numpy as np
df = pd.read_excel('dataset.xlsx')
df.head(20)

dict_decode = {0:'чай',1:'кофе'}
df['мама'] = df.iloc[:,5].map(lambda x:x[0]).replace({'ч':0,'к':1})
df['папа'] = df.iloc[:,5].map(lambda x:x[1]).replace({'ч':0,'к':1})
df['К/Ч'] = df['К/Ч'].replace({'ч':0,'к':1})
df = df.drop(columns=['Родители (мама, папа) что пьют'])
df.head(20)

time_sleep = int(input('Часы сна:'))
work = int(input('Трудоустройство:'))
weight = int(input('Вес:'))
height = int(input('Рост:'))
distance = float(input('Расстояние до МИРЭА в часах:'))
mama = input('Что пьет мама:')
papa = input('Что пьет папа:')
dict_encode = {'ч':0,'к':1}

def drink_by_knn(train_df, new_object, k=5, type_norm=2):
    help_dict = {0: 'Чай', 1: 'Кофе'}

    train_df['dist'] = (np.linalg.
                                          norm(train_df.drop(columns=['К/Ч']) - new_object,
                                               ord=type_norm, axis=1))

    answer = train_df.sort_values('dist').iloc[:k]['К/Ч'].value_counts().index.tolist()[0]
    return f'Человек предпочитает {help_dict[answer]}'
test_data = np.array([time_sleep,work,weight,height,distance,
                      dict_encode[mama.lower()],dict_encode[papa.lower()]])
print(drink_by_knn(df,test_data))
print('Самое близкое расстояние',sorted(df.dist)[0])
print(df.sort_values(by='dist'))