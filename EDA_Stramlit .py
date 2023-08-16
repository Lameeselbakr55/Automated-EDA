import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to load data
def load_data(file):
    if file is not None:
        if file.name.endswith('.csv'):
            data = pd.read_csv(file)
        elif file.name.endswith('.xls') or file.name.endswith('.xlsx'):
            data = pd.read_excel(file)
        else:
            st.error("Invalid file format. Please upload a CSV or Excel file.")
            return None
        return data

# Function to display basic statistics
def display_basic_stats(data):
    st.subheader("Basic Statistics")
    st.write(data.describe())

# Function to display data types
def display_data_types(data):
    st.subheader("Data Types")
    st.write(data.dtypes)

# Function to display missing values
def display_missing_values(data):
    st.text("Count of Missing Values")
    st.write(data.isnull().sum())
    st.text("DataFrame of Missing Values")
    st.write(data[data.isnull().any(axis=1)])
    
    
# Function to drop missing values
def drop_missing_values(data):
    st.write(data.dropna(inplace=True))
    st.text("Missing Values Dropped successfully")
    display_missing_values(data)

    
# Function to fill missing values
def fill_missing_values(data, value_to_replace):
    st.text("Missing Values filled sucessfully  ")  
    st.write(data.fillna(value_to_replace, inplace=True)) 
    display_missing_values(data)   
    
# Function to dispay duplicates in dataframe 
def display_duplicates(data):
    st.text("Duplicates in the data frame are :  ") 
    for col in data.columns:
        data[col] = data[col].duplicated()
    st.dataframe(data)

    
# Function to count duplicats in dataframe 
def count_duplicates(data):
    st.text("Sum of Duplicates in the data frame are :  ") 
    for col in data.columns:
        num_duplicates = data[col].duplicated().sum()
        st.write(col ,"  =  " ,num_duplicates )
 
 # Function to drop duplicats in dataframe 
def drop_duplicates(data):
     st.text(" Duplicates are dropped successfully ") 
     for col in data.columns:
         st.write(data.drop_duplicates(col, keep='last',inplace=True))
     count_duplicates(data)

    
# Function to display data visualizations using Matplotlib
def display_visualizations(data):
    
    st.subheader("Data Visualizations")
    st.text("Numerical columns are : ")
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    st.write(numeric_cols)
    st.text("categorical columns are : ")
    categorical_cols = data.select_dtypes(include=[object]).columns
    st.write(categorical_cols)
    
    # Allow user to select column
    selected_column = st.selectbox("Select column to visualize:", data.columns)

   # Allow user to select plot type
    plot_type = st.selectbox("Select plot type:", ["Histogram", "Bar Plot", "Pie chart"])
    
    # Histogram for numeric columns
    
    if plot_type == "Histogram":
        plt.figure(figsize=(8, 6))
        plt.hist(data[selected_column], bins=20, edgecolor='k')
        plt.xlabel(selected_column)
        plt.ylabel("Frequency")
        st.pyplot()
        
    elif plot_type == "Bar Plot":
        plt.figure(figsize=(8, 6))
        value_counts = data[selected_column].value_counts()
        plt.bar(value_counts.index, value_counts.values, edgecolor='k')
        plt.xlabel(selected_column)
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        st.pyplot()
        
    elif plot_type == "Pie chart":
        plt.figure(figsize=(8, 6))
        value_counts = data[selected_column].value_counts()
        plt.pie(value_counts,labels=value_counts.index.values.tolist())
        plt.xlabel(selected_column)
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        st.pyplot()
        
    
    

# Main function
def main():
    st.title("Automated EDA App")
    st.write("Upload a CSV or Excel file for Exploratory Data Analysis.")

    # File upload
    file = st.file_uploader("Upload a file", type=["csv", "xls", "xlsx"])

    if file is not None:
        data = load_data(file)
        if data is not None:
            display_basic_stats(data)



    # Missong values Operations                  
            st.subheader("Missing Values Operations")
            functions = ["Default","Count Missing Values", "Fill Missing Values", "Drop Missing Values","Data Visualizations"]
            selected_function = st.selectbox("Select function to apply:", functions)


            if selected_function == "Count Missing Values":
                display_missing_values(data)
            elif selected_function == "Fill Missing Values":
                fill_missing_values(data,'xf')
            elif selected_function == "Drop Missing Values":
                drop_missing_values(data)
                display_data_types(data)

    # Duplicated values Operations            
            st.subheader("Duplicated Data Operations")
            functions = ["Default", "Display Duplicated Values", "Count Duplicates in each column", "Drop Duplicates"]
            selected_function = st.selectbox("Select function to apply:", functions)


            if selected_function == "Display Duplicated Values":
                 display_duplicates(data)
            elif selected_function == "Count Duplicates in each column":
                count_duplicates(data)
            elif selected_function == "Drop Duplicates":
                drop_duplicates(data)
             
      #Data Visualiztion
            display_visualizations(data)  

              
             

if __name__ == "__main__":
    main()
