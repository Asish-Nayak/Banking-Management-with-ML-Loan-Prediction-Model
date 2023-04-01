# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 11:35:18 2022

@author: ADBMS-LAB PROJECT GROUP (ASISH,HARIGARAN,SUSHANTA)
"""


import streamlit as st
import mysql.connector
import pandas as pd
import pickle


st.set_page_config(layout="wide")

original_title = '<p style="font-family:Courier; color:WHITE; font-size: 50px;">BANK DATABASE SYSTEM </p>'
st.markdown(original_title, unsafe_allow_html=True)    

given =st.selectbox('Select The Role', ("select",'admin',"customer"))

if ( given == 'admin'):
 
      p=st.text_input("Enter Pawsword")
      cnx =  mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password=p,
                database="Bank_Database")
    
        
elif (given== "customer"):
       cnx =  mysql.connector.connect(
           host="localhost",
           port=3306,
           user="customer",
           password="password",
           database="Bank_Database")
      









pickle_in = open("LG.pkl","rb")
regressor=pickle.load(pickle_in)


#-----------------------------------------------------------------------------#

def openacc():
    
    n=st.text_input("Enter Name")
    ag=st.text_input("Enter your age")
    db=st.text_input("Enter DOB (dd/mm/yyyy)")
    g=st.selectbox('Select the gender', ("select","Male","Female"))
    p=st.text_input("Enter phone")
    ad=st.text_input("Enter address")
    ob=st.text_input("Enter your Opening balance")
    
    if st.button("next"):
          sql3="""select acno from personal_details ORDER BY acno desc LIMIT 1"""
          sql1= """insert into personal_details values (%s,%s,%s,%s,%s,%s,%s)"""
          sql2="""insert into account_details values (%s,%s)"""
          cur = cnx.cursor()
          cur.execute(sql3)
          num = cur.fetchone()
          if num is None :
              num = 100111
              ac = num 
          else:
              inn = int(num[0])
              ac= inn+1
          data1 = (n,ac,ag,db,g,p,ad)
          data2=(ac,ob)
          cur.execute(sql1,data1)
          cur.execute(sql2,data2)
          cnx.commit()
          return st.write("Data Enter successfully you account number is ",ac)
    
    
#-----------------------------------------------------------------------------#

def depoAmo():
    am = st.number_input("Enter amount")
    ac = st.text_input("Enter account number")
    if st.button("next"):
        sql3= "select balance from account_details where acno = %s "
        data=(ac,)
        cur = cnx.cursor()
        cur.execute(sql3,data)
        myresult = cur.fetchone()
        tam = myresult[0] + am
        sql4="update account_details set balance = %s where acno = %s"
        d = (tam,ac)
        cur.execute(sql4,d)
        cnx.commit()
        return st.write("Update successfully")
        
#-----------------------------------------------------------------------------#    
def witham():
    am =st.number_input("Enter amount")
    ac = st.text_input("Enter account number")
    if st.button("next"):
        sql5= "select balance from account_details where acno = %s "
        data=(ac,)
        cur = cnx.cursor()
        cur.execute(sql5,data)
        myresult = cur.fetchone()
        tam = myresult[0]-am
        sql6="update account_details set balance =%s where acno = %s"
        d = (tam,ac)
        cur.execute(sql6,d)
        cnx.commit()
        return st.write("Update successfully")  
    
#-----------------------------------------------------------------------------#

def balance():
    ac=st.text_input("Enter account number")
    a="select balance from account_details where acno = %s"
    data = (ac,)
    cur = cnx.cursor()
    cur.execute(a,data)
    myresult = cur.fetchone()
    if st.button("next"):
          return st.write("Balance for this Account :is",myresult[0])
        
    
    
#-----------------------------------------------------------------------------#

def dispacc():
    ac=st.text_input("Enter account number")
    a="select * from account_details where acno = %s "
    b="select name from personal_details where acno = %s"
    data =(ac,)
    cur = cnx.cursor()
    cur.execute(a,data)
    myresult=pd.DataFrame(cur.fetchall(),columns=['Account_number','Amount in acount'])
    cur.execute(b,data)
    name=pd.DataFrame(cur.fetchone(),columns = ['Name'])
    new = pd.DataFrame(columns=range(3))
    new = pd.concat ([name , myresult],join = 'outer', axis = 1)
    
    if st.button("next"):
       return st.write("details",new)
    
    
#-----------------------------------------------------------------------------#

def closeac():
    ac=st.text_input("Enter account number")
    sql1="delete from account_details where acno = %s "
    sql2="delete from personal_details where acno = %s"
    data=(ac,)
    cur = cnx.cursor()
    cur.execute(sql1,data)
    cur.execute(sql2,data)
    cnx.commit()
    if st.button("next"):
        return st.write("Account removed successfully") 
#-----------------------------------------------------------------------------#
def perdiction(a,b,c,d,e,g):
       
       if a == "Male" :
           a=1
       else:
           a=0
       if b=="Married":
           b=1
       else:
           b=0
       if c=="Graduate":
           c=1
       else:
           c=0
       if d=="Yes":
           d=1
       else:
           d=0
       data1=[[a,b,c,d,e]]
       data2=pd.DataFrame(data1,columns=[["Gender","Married","Education","Employed","salary"]])
       p=regressor.predict(data2)
       if p[0]==1:
           l = "Yes"
       else:
           l ="NO"
       data=(g,l)
       sql="""insert into loan_status values (%s,%s);"""
       cur = cnx.cursor()
       cur.execute(sql,data)
       cnx.commit()
       cur.close()
       st.write("Application successfully")
       
       
       
#-----------------------------------------------------------------------------#

def loanapp():
    ac=st.text_input("Enter Account number")
    m=st.selectbox('Marital_status', ("select","Married","Unmarried"))
    e=st.selectbox("Education_status",("select","Graduate","Ungraduate"))
    emp=st.selectbox("Are you employed",("select","Yes","No"))
    s=st.text_input("Enter your salary")
    
    data=(ac,)
    if st.button("next"):
          sql1= """insert into loan_application values (%s,%s,%s,%s,%s)"""
          sql2="""select gender from personal_details where acno = %s """
          cur = cnx.cursor()
          data2=(ac,m,e,emp,s)
          cur.execute(sql1,data2)
          cnx.commit()
          cur.close()
          cur = cnx.cursor()
          cur.execute(sql2,data)
          g=cur.fetchone()
          cur.close()
          perdiction(g,m,e,emp,s,ac)
          

#-----------------------------------------------------------------------------#      
def displon():
     ac=st.text_input("Enter account number")
     a="select * from loan_status where acno = %s "
     sql="select name from personal_details where acno = %s"
     data =(ac,)
     cur = cnx.cursor()
     cur.execute(sql,data)
     n = pd.DataFrame(cur.fetchone(),columns=['Name'])
     cur.execute(a,data)
     myresult=pd.DataFrame(cur.fetchall(),columns=['Account_number','Loan approved '])
     new = pd.concat ([n , myresult],join = 'outer', axis = 1)
     if st.button("next"):
        return st.write("details",new)
   
    
def dislist():
       a="select * from account_details  "
       b="select name from personal_details "
       cur = cnx.cursor()
       cur.execute(a)
       myresult=pd.DataFrame(cur.fetchall(),columns=['Account_number','Amount in acount'])
       cur.execute(b)
       name=pd.DataFrame(cur.fetchall(),columns = ['Name'])
       new = pd.DataFrame(columns=range(3))
       new = pd.concat ([name , myresult],join = 'outer', axis = 1)
       
       return st.write("List of Customer",new)
       
#-----------------------------------------------------------------------------#   

def admin():
     
    col1, col2, col3 = st.columns(3)
    
    with col1:
     from PIL import Image
     image = Image.open(r'C:\Users\ADMIN\Desktop\MBA - BA II\Advanced DBMS LAB\project_ADBMS LAB\img.jpeg')
     st.image(image)
    with col2:
        
     original_title = '<p style="font-family:Courier; color:WHITE; font-size: 20px;">1.OPEN NEW ACCOUNT <br> 2.DEPOSIT AMOUNT<br>3.WITHDRAW AMOUNT<br>4.BALANCE ENQUIRY<br>5.DISPLAY CUSTOMER DETAILS<br>6.CLOSE AN ACCOUNT<br>7.LOAN APPLICATION<br>8.CHECK LOAN STATUS<br>9.LIST OF CUSTOMERS DETAILS</p>'
     st.markdown(original_title, unsafe_allow_html=True)

                                       
     choice =st.selectbox('Enter task number', ("select",1,2,3,4,5,6,7,8,9))
   
   
    with col3:  
     if ( choice == 1):
            openacc()
     elif (choice == 2):
            depoAmo()
     elif (choice == 3):
            witham()
     elif (choice == 4):
             balance() 
     elif (choice == 5):
            dispacc()
     elif (choice == 6):
            closeac()
     elif (choice == 7):
            loanapp()
     elif (choice == 8):
            displon()      
     elif(choice == 9):
           dislist()
def customer():
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
     from PIL import Image
     image = Image.open(r'C:\Users\ADMIN\Desktop\MBA - BA II\Advanced DBMS LAB\project_ADBMS LAB\img.jpeg')
     st.image(image)
    with col2:
        
     original_title = '<p style="font-family:Courier; color:WHITE; font-size: 20px;">1.OPEN NEW ACCOUNT <br> 2.DEPOSIT AMOUNT<br>3.WITHDRAW AMOUNT<br>4.BALANCE ENQUIRY<br>5.DISPLAY CUSTOMER DETAILS<br>6.LOAN APPLICATION</p>'
     st.markdown(original_title, unsafe_allow_html=True)

                                       
     choice =st.selectbox('Enter task number', ("select",1,2,3,4,5,6))
   
   
    with col3:  
     if ( choice == 1):
            openacc()
     elif (choice == 2):
            depoAmo()
     elif (choice == 3):
            witham()
     elif (choice == 4):
             balance() 
     elif (choice == 5):
            dispacc()
     elif (choice == 6):
            loanapp()

def main():
    
     if (  given  == 'admin'):
            admin()
     elif (given== "customer"):
         customer()

if __name__=='__main__':
    main()