# -*- coding: utf-8 -*-
"""REEVIISIII TERAKHIR REVISI FINAL-FINAL.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PHZOdZ7h11lOED_Eg1Xuc7JLvhGsh1F4
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as ss 


# install data fie yang akan diproses
from google.colab import drive
drive.mount('/content/gdrive')

path_1 = 'gdrive/My Drive/Colab Notebooks/File bahan-bahan data/application_train.csv'

dataset = pd.read_csv(path_1)
dataset

"""# INTRODUCTING TO DATA (MENGENAL DATA)"""

# cek tipe data
dataset.dtypes

# cek jumlah tipe data
dataset.info()

# cek jumlah targetnya
sns.countplot(data=dataset, x='TARGET')
plt.show()

dataset['TARGET'].value_counts()

Total = 225248 + 19032
print(19032/Total, ':' ,225248/Total)

# cek statistik numeric
dataset.describe()

# cek statistik keseluruhan termasuk kategorikal 
dataset.describe(include='all')

"""MENGHAPUS MISSING VALUE"""

# Mengecek kolum dengan null value dari masing-masing fitur

jumlah_null2 = dataset.isnull().sum()/dataset.shape[0]
jumlah_null3 = jumlah_null2[jumlah_null2>0.30]
jumlah_null4 = pd.DataFrame(jumlah_null3)  

# Mereset index dan mengganti nama fitur
jumlah_null4= jumlah_null4.rename(columns= {0: 'persentase'})
jumlah_null4.sort_values(by='persentase')
jumlah_null4 = jumlah_null4.reset_index()
jumlah_fitur_null = jumlah_null4.rename(columns={'index' : 'nama_fitur'})
jumlah_fitur_null.sort_values(by='persentase', ascending= False) # disimpan dalam fitur jumlah_fitur_null

for row in jumlah_fitur_null.iterrows():
    name_column = list(row)
    name_column = [str(i).split('\n',1)[0] for i in name_column]
    name_column = name_column[1].split()[1]
    dataset.drop([name_column],axis=1,inplace=True)

new_dataset = dataset

new_dataset

# menghapus row/baris dengan null value
new_dataset.dropna(inplace = True)
new_dataset

# cek jumlah targetnya
sns.countplot(data=new_dataset, x='TARGET')
plt.show()

new_dataset['TARGET'].value_counts()

# Melihat variabel/fitur yang berjenis kategorikal
 for col_name in new_dataset.columns:
    if new_dataset[col_name].dtypes == 'object':
      unique_col = len(new_dataset[col_name].unique())
      print("feature '{col_name}' punya {unique_col} unique categories".format(col_name=col_name, unique_col=unique_col))

# Melakukan LABEL ENCODING fitur kategori

new_dataset['NAME_CONTRACT_TYPE']= new_dataset['NAME_CONTRACT_TYPE'].astype("category").cat.codes
new_dataset['CODE_GENDER'] = new_dataset['CODE_GENDER'].astype("category").cat.codes
new_dataset['FLAG_OWN_CAR'] = new_dataset['FLAG_OWN_CAR'].astype("category").cat.codes
new_dataset['FLAG_OWN_REALTY']= new_dataset['FLAG_OWN_REALTY'].astype("category").cat.codes
new_dataset['NAME_TYPE_SUITE'] = new_dataset['NAME_TYPE_SUITE'].astype("category").cat.codes
new_dataset['NAME_INCOME_TYPE'] = new_dataset['NAME_INCOME_TYPE'].astype("category").cat.codes
new_dataset['NAME_EDUCATION_TYPE']= new_dataset['FLAG_OWN_REALTY'].astype("category").cat.codes
new_dataset['NAME_FAMILY_STATUS'] = new_dataset['NAME_TYPE_SUITE'].astype("category").cat.codes
new_dataset['NAME_HOUSING_TYPE'] = new_dataset['NAME_INCOME_TYPE'].astype("category").cat.codes



"""# Cek distribusi variabelnya. lalu merubahnya menjadi distribusi normal dengan log. dan menghapus outliersnya"""

plt.figure(figsize=(10,10))
sns.distplot(new_dataset['AMT_INCOME_TOTAL'])
plt.title("AMT_INCOME_TOTAL",size=15, weight='bold')

new_dataset['AMT_INCOME_TOTAL_log'] = np.log(new_dataset.AMT_INCOME_TOTAL+1)

plt.figure(figsize=(12,10))
sns.distplot(new_dataset['AMT_INCOME_TOTAL_log'])
plt.title("AMT_INCOME_TOTAL",size=15, weight='bold')

plt.figure(figsize=(10,10))
sns.distplot(new_dataset['AMT_CREDIT'])
plt.title("AMT_CREDIT",size=15, weight='bold')

new_dataset['AMT_CREDIT_log'] = np.log(new_dataset.AMT_CREDIT+1)

plt.figure(figsize=(12,10))
sns.distplot(new_dataset['AMT_CREDIT_log'])
plt.title("AMT_CREDIT_TOTAL",size=15, weight='bold')

plt.figure(figsize=(10,10))
sns.distplot(new_dataset['AMT_ANNUITY'])
plt.title('AMT_ANNUITY',size=15, weight='bold')

new_dataset['AMT_ANNUITY_log'] = np.log(new_dataset.AMT_ANNUITY+1)

plt.figure(figsize=(12,10))
sns.distplot(new_dataset['AMT_ANNUITY_log'])
plt.title('AMT_ANNUITY_TOTAL',size=15, weight='bold')

new_dataset = new_dataset.drop(columns=['AMT_INCOME_TOTAL',	'AMT_CREDIT',	'AMT_ANNUITY'])

plt.figure(figsize=(40, 30))
corrMatrix = new_dataset.corr()
sns.heatmap(corrMatrix)
plt.show()

pd.set_option('display.max_rows', None)
corrMatrix[['TARGET']].sort_values(by='TARGET', ascending=False)

df1 = pd.DataFrame(data=new_dataset, columns=['SK_ID_CURR', 'TARGET', 'DAYS_BIRTH', 'REGION_RATING_CLIENT_W_CITY', 'REGION_RATING_CLIENT', 'DAYS_LAST_PHONE_CHANGE',  'CODE_GENDER',
                   'REG_CITY_NOT_WORK_CITY', 'DAYS_ID_PUBLISH', 'NAME_HOUSING_TYPE', 'NAME_INCOME_TYPE', 'FLAG_EMP_PHONE', 'REG_CITY_NOT_LIVE_CITY',   
                   'FLAG_DOCUMENT_3', 'DAYS_REGISTRATION', 'LIVE_CITY_NOT_WORK_CITY', 'DEF_30_CNT_SOCIAL_CIRCLE', 'AMT_INCOME_TOTAL_log', 'AMT_CREDIT_log',
                  'CNT_FAM_MEMBERS', 'AMT_ANNUITY_log'])

df1.head(15)

# membuat fitur baru

df1['INCOME_CREDIT_PERC'] = new_dataset['AMT_INCOME_TOTAL_log'] / new_dataset['AMT_CREDIT_log']
df1['INCOME_PER_PERSON'] = new_dataset['AMT_INCOME_TOTAL_log'] / new_dataset['CNT_FAM_MEMBERS']
df1['ANNUITY_INCOME_PERC'] = new_dataset['AMT_ANNUITY_log'] / new_dataset['AMT_INCOME_TOTAL_log']
df1['PAYMENT_RATE'] = new_dataset['AMT_ANNUITY_log'] / new_dataset['AMT_CREDIT_log']

df1.head(10)

total = df1.isnull().sum().sort_values(ascending=False)
percent_1 = df1.isnull().sum()/df1.isnull().count()*100
percent_2 = (round(percent_1, 1)).sort_values(ascending=False)
missing_data = pd.concat([total, percent_2], axis=1, keys=['Total', '%'])
missing_data.head(23)

data_train = df1.drop("SK_ID_CURR")
data_test = df1.drop("TARGET", axis=1)

X_train = data_train.drop("TARGET", axis=1)
y_train = data_train["TARGET"]
X_test  = data_test.drop("SK_ID_CURR", axis=1).copy()

X_test

from imblearn.over_sampling import SMOTE

undersample = SMOTE()
X_train, y_train = undersample.fit_resample(X_train, y_train)

pd.Series(y_train).value_counts()

"""# Model Algoritma KNN"""

X_train = df1.drop(['TARGET', 'SK_ID_CURR'],1)
y_train = df1["TARGET"]
X_test  = df1.drop(['TARGET', 'SK_ID_CURR'],1)

from imblearn.over_sampling import SMOTE

undersample = SMOTE()
X_train, y_train = undersample.fit_resample(X_train, y_train)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.25, random_state=777)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()

X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

from sklearn.neighbors import  KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

y_test_pred = knn.predict(X_test)
y_test_pred

from sklearn.metrics import accuracy_score
accuracy_score(y_test, y_test_pred)

y_train_pred = knn.predict(X_train)
y_train_pred

accuracy_score(y_train, y_train_pred)

"""# Decision Tree"""

X_train = df1.drop(['TARGET', 'SK_ID_CURR'],1)
y_train = df1["TARGET"]
X_test  = df1.drop(['TARGET', 'SK_ID_CURR'],1)

from imblearn.over_sampling import SMOTE

undersample = SMOTE()
X_train, y_train = undersample.fit_resample(X_train, y_train)

pd.Series(y_train).value_counts()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size = 0.25, random_state = 0)

from sklearn.tree import DecisionTreeClassifier
dectree = DecisionTreeClassifier(random_state = 5, max_depth=15)
dectree.fit(X_train, y_train)

y_test_pred = dectree.predict(X_test)
accuracy_score(y_test, y_test_pred)

y_train_pred = dectree.predict(X_train)
accuracy_score(y_train, y_train_pred)

y_test_pred

from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix
predictions = cross_val_predict(dectree, X_train, y_train, cv=3)
confusion_matrix(y_train, predictions)

from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix
predictions = cross_val_predict(dectree, X_test, y_test, cv=3)
confusion_matrix(y_test, predictions)

from sklearn.metrics import precision_score, recall_score

print("Precision:", precision_score(y_test, predictions))
print("Recall:", recall_score(y_test, predictions))

def search_tree(X_train, X_test, y_train, y_test, max_depths):
    acc_train = []
    acc_test = []
    for depth in max_depths:
        # Train based on tree's depth
        classifier = DecisionTreeClassifier(criterion='entropy', random_state=0,
                                            max_depth=depth)
        classifier.fit(X_train, y_train)
        
        # Predict the result
        y_train_pred = classifier.predict(X_train)
        y_test_pred = classifier.predict(X_test)
        
        # Training Performance
        score_train = accuracy_score(y_train, y_train_pred)
        acc_train.append(score_train)

        # Test Performance
        score_test = accuracy_score(y_test, y_test_pred)
        acc_test.append(score_test)

    result = pd.DataFrame({'depths': max_depths, 'acc_train': acc_train, 'acc_test': acc_test})

    plt.figure(figsize=(12, 8))
    plt.title('Decision Tree Performance')
    plt.ylabel('Accuracy')
    plt.xlabel('Max Depths')
    sns.lineplot(data=result, x='depths', y='acc_train')
    sns.lineplot(data=result, x='depths', y='acc_test')
    plt.grid()
    plt.xticks(result['depths'])
    plt.show()

search_tree(X_train, X_test, y_train, y_test, max_depths=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])

"""# Random Forest"""

total = df1.isnull().sum().sort_values(ascending=False)
percent_1 = df1.isnull().sum()/df1.isnull().count()*100
percent_2 = (round(percent_1, 1)).sort_values(ascending=False)
missing_data = pd.concat([total, percent_2], axis=1, keys=['Total', '%'])
missing_data.head(23)

X_train = df1.drop(['TARGET', 'SK_ID_CURR'],1)
y_train = df1["TARGET"]
X_test  = df1.drop(['TARGET', 'SK_ID_CURR'],1)

X_train

from imblearn.over_sampling import SMOTE

undersample = SMOTE()
X_train, y_train = undersample.fit_resample(X_train, y_train)

pd.Series(y_train).value_counts()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size = 0.25, random_state = 0)

from sklearn.ensemble import RandomForestClassifier
Random_for = RandomForestClassifier(random_state=444)
Random_for.fit(X_train,y_train)

Y_prediction = Random_for.predict(X_test)
Y_prediction

acc_random_forest = Random_for.score(X_train, y_train)
acc_random_forest

Random_for.score(X_test, y_test)

importances = pd.DataFrame({'feature':X_train.columns,'importance':np.round(Random_for.feature_importances_,3)})
importances = importances.sort_values('importance',ascending=False).set_index('feature')
importances.head(25)

importances.plot.bar()

from sklearn.model_selection import cross_val_score
random_forest = RandomForestClassifier(criterion = 'entropy', random_state = 0, max_depth=3)
result = cross_val_score(random_forest, X_train, y_train, cv=5)

result.mean()

from sklearn.model_selection import cross_val_score
random_forest = RandomForestClassifier(criterion = 'entropy', random_state = 0, max_depth=3)
result = cross_val_score(random_forest, X_test, y_test, cv=5)

result.mean()

from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix
predictions = cross_val_predict(random_forest, X_train, y_train, cv=3)
confusion_matrix(y_train, predictions)

from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix
predictions = cross_val_predict(random_forest, X_test, y_test, cv=3)
confusion_matrix(y_test, predictions)

from sklearn.metrics import precision_score, recall_score

print("Precision:", precision_score(y_train, predictions))
print("Recall:",recall_score(y_train, predictions))

from sklearn.metrics import precision_score, recall_score

print("Precision:", precision_score(y_test, predictions))
print("Recall:", recall_score(y_test, predictions))

from sklearn.metrics import precision_recall_curve

y_scores = Random_for.predict_proba(X_train)
y_scores = y_scores[:,1]

precision, recall, threshold = precision_recall_curve(y_train, y_scores)
def plot_precision_and_recall(precision, recall, threshold):
    plt.plot(threshold, precision[:-1], "r-", label="precision", linewidth=5)
    plt.plot(threshold, recall[:-1], "b", label="recall", linewidth=5)
    plt.xlabel("threshold", fontsize=19)
    plt.legend(loc="upper right", fontsize=19)
    plt.ylim([0, 1])

plt.figure(figsize=(14, 7))
plot_precision_and_recall(precision, recall, threshold)
plt.show()

