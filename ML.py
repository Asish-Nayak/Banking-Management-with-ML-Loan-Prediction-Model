# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 14:14:37 2022

@author:ADBMS-LAB PROJECT GROUP (ASISH,HARIGARAN,SUSHANTA)
"""
import pandas as pd
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier




df=pd.read_csv(r'C:\Users\ADMIN\Desktop\MBA - BA II\Advanced DBMS LAB\project_ADBMS LAB\dataset\data_set.csv')
df.head()

#drop the null value
df = df.dropna()


#Exploratory data analysis (EDA)

#print no of rows and columns
df.shape


#gender
df.Gender.value_counts(dropna=False)
sns.countplot(x='Gender',data=df)

Male_count = len(df[df.Gender == 'Male'])
Female_count = len(df[df.Gender == 'Female'])
Null_count = len(df[df.Gender.isnull()])

print("Percentage of Male applicant: {:.2f}%".format((Male_count / 614*100)))
print("Percentage of Female applicant: {:.2f}%".format((Female_count / 614*100)))
print("Missing values percentage: {:.2f}%".format((Null_count / 614*100)))


# Married

df.Married.value_counts(dropna=False)
sns.countplot(x='Married',data=df)
countMarried = len(df[df.Married == 'Yes'])
countNotMarried = len(df[df.Married == 'No'])
countNull = len(df[df.Married.isnull()])

print("Percentage of married: {:.2f}%".format((countMarried / (len(df.Married))*100)))
print("Percentage of Not married applicant: {:.2f}%".format((countNotMarried / (len(df.Married))*100)))
print("Missing values percentage: {:.2f}%".format((countNull / (len(df.Married))*100)))

#education

df.Education.value_counts(dropna=False)
sns.countplot(x='Education',data=df)
countGraduate = len(df[df.Education == 'Graduate'])
countNotGraduate = len(df[df.Education == 'Not Graduate'])
countNull = len(df[df.Education.isnull()])

print("Percentage of graduate applicant: {:.2f}%".format((countGraduate / (len(df.Education))*100)))
print("Percentage of Not graduate applicant: {:.2f}%".format((countNotGraduate / (len(df.Education))*100)))
print("Missing values percentage: {:.2f}%".format((countNull / (len(df.Education))*100)))


#employed
df.Employed.value_counts(dropna=False)
sns.countplot(x='Employed',data=df)
countNo = len(df[df.Employed == 'No'])
countYes = len(df[df.Employed == 'Yes'])
countNull = len(df[df.Employed.isnull()])

print("Percentage of Not employed: {:.2f}%".format((countNo / (len(df.Employed))*100)))
print("Percentage of  employed: {:.2f}%".format((countYes / (len(df.Employed))*100)))
print("Missing values percentage: {:.2f}%".format((countNull / (len(df.Employed))*100)))


#loanstatus

df.Loan_Status.value_counts(dropna=False)
sns.countplot(x="Loan_Status", data=df)
countY = len(df[df.Loan_Status == 'Y'])
countN = len(df[df.Loan_Status == 'N'])
countNull = len(df[df.Loan_Status.isnull()])

print("Percentage of Approved: {:.2f}%".format((countY / (len(df.Loan_Status))*100)))
print("Percentage of Rejected: {:.2f}%".format((countN / (len(df.Loan_Status))*100)))
print("Missing values percentage: {:.2f}%".format((countNull / (len(df.Loan_Status))*100)))




#----------------------------------------------------------------------------------------------------------------------------------------

#Data Preprocessing

df2=pd.get_dummies(df)

df2.info()


# Drop columns
df3 = df2.drop(['Gender_Female', 'Married_No', 'Education_Not Graduate', 
              'Employed_No', 'Loan_Status_N'], axis = 1)

# Rename columns name
df3.rename(columns={'Gender_Male': 'Gender', 'Married_Yes': 'Married', 
       'Education_Graduate': 'Education', 'Self_Employed_Yes': 'Self_Employed',
       'Loan_Status_Y': 'Loan_Status'}, inplace=True)


df3.info()

x = df3.drop(["Loan_Status"], axis=1)
y = df3["Loan_Status"]


#----------------------------------------------------------------------------------------------------------------------------

#Splitting Data Set

X_train,X_test,Y_train,Y_test=train_test_split(x,y,test_size=0.2,random_state=0)

#-------------------------------------------------------------------------------------------------------------------------------------------

#Models

#Logistic Regression
lr1=LogisticRegression(max_iter=500)
lr1.fit(X_train,Y_train)
Y_pred=lr1.predict(X_test)
print('Confusion matrix')
print()
print(confusion_matrix(Y_test,Y_pred))
print()
print('Classification Report')
print(classification_report(Y_test,Y_pred))
print()
from sklearn.metrics import accuracy_score
acLR=accuracy_score(Y_test,Y_pred)
print('accuracy_score:{:.2f}%'.format(acLR*100))



#---------------------------------------------------------------------------------------------------------------------------------------------------------

#Support Vector Machine (SVM)

svc=SVC(max_iter=500)
svc.fit(X_train,Y_train)
Y_pred=svc.predict(X_test)
print('confusion matrix:\n',confusion_matrix(Y_test,Y_pred))
print('\n Classification report:\n',classification_report(Y_test,Y_pred))
from sklearn.metrics import accuracy_score
auSV=accuracy_score(Y_test,Y_pred)
print('Accuracy Score: {:2f}%'.format(auSV*100))

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Decision Tree
clf = DecisionTreeClassifier()
clf.fit(X_train,Y_train)
Y_pred = clf.predict(X_test)
print('Confusion matrix')
print(confusion_matrix(Y_test,Y_pred))
print('Classification report')
print(classification_report(Y_test,Y_pred))
acDT=accuracy_score(Y_test,Y_pred)
print("Decision Tree Accuracy: {:.2f}%".format(acDT*100))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

rf=RandomForestClassifier()
rf.fit(X_train,Y_train)
Y_pred=rf.predict(X_test)
print('Confusion matrix')
print(confusion_matrix(Y_test,Y_pred))
print('Classification report')
print(classification_report(Y_test,Y_pred))
acRF=accuracy_score(Y_test,Y_pred)
print("Random Forest Accuracy:  {:.2f}%".format(acRF*100))



#--------------------------------------------------------------------------------------------------
compare = pd.DataFrame({'Model': ['Logistic Regression','SVM','Decision Tree','Random Forest'], 
                        'Accuracy': [acLR*100,auSV*100,acDT*100,acRF*100]})
compare


#-----------------------------------------------------------------------------------------------------------------------------------------------------------

#save the model

##create a pickle file
import pickle
pickle_out =open('LG.pkl','wb')
pickle.dump(lr1,pickle_out)
pickle_out.close()






