from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import codecs
import re
from webdriver_manager.chrome import ChromeDriverManager

import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import time
import csv
import pandas as pd
import re
import string
import numpy as np
from sklearn.manifold import TSNE

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

import json
import joblib
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
from tabulate import tabulate
from fuzzywuzzy import fuzz


options = Options()
#options.add_argument('--headless')
driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
#driver = webdriver.Chrome(service=Service(ChromeDriverManager(version='114.0.5735.90').install()),options=options)

#finding leaf nodes
def log(*args):
    str_args = ""
    for arg in args:
        if isinstance(arg, dict) or isinstance(arg, list):
            str_args += json.dumps(arg)
        else:
            str_args += str(arg)
    #print(str_args)

def get_leaf_nodes(master, exclude_tags):
    nodes = master.find_all(True)
    leaf_nodes = [elem for elem in nodes if not elem.find(True)]
    unique_leaf_nodes = []

    for node in leaf_nodes:
        if node.name not in exclude_tags:
            unique_leaf_nodes.append(node.name)

    return list(set(unique_leaf_nodes))

#extract content from leaf nodes
def extract_elements_data(soup, element_name):
    elements_data = []

    elements = soup.find_all(element_name)
    for element in elements:
        content = element.text.strip()
        if content:  # Exclude rows where 'Content' is null
            elements_data.append({
                'Element': element.name,
                'HTML': element,
                'Content': content
            })

    return elements_data

#check input
def preprocess_text(text):
    # Check if the input is a float and convert it to a string
    if isinstance(text, float):
        text = str(text)
    
    # Check if the input is a string
    if not isinstance(text, str):
        raise ValueError("Input must be a string or float")

    # Remove extra spaces and convert to lowercase
    processed_text = ' '.join(text.split()).lower()
    
    return processed_text

# Function to extract classes from HTML
def extract_classes(input_df):
    # Initialize an empty DataFrame for the extracted classes
    extracted_classes_df = pd.DataFrame(columns=['Tag', 'Class', 'HTML'])

    for index, row in input_df.iterrows():
        html_input = row['HTML']
        element_data = row['Element']
        
        soup = BeautifulSoup(html_input, 'html.parser')
        elements_with_class = soup.find_all(class_=True)
        
        for element in elements_with_class:
            classes = element.get('class')
            if classes:
                for class_name in classes:
                    extracted_classes_df = extracted_classes_df._append({
                        'Tag': element_data,
                        'Class': class_name,
                        'HTML': str(element)
                    }, ignore_index=True)

    return extracted_classes_df


# Function to extract text content from HTML based on 'Tag' and 'Class' columns
def extract_text(row):
    tag = row['Tag']
    class_name = row['Class']
    html_input = row['HTML']
    
    soup = BeautifulSoup(html_input, 'html.parser')
    element = soup.find(tag, {'class': class_name})
    
    if element:
        text_content = element.get_text(strip=True)
        return text_content
    else:
        return None

def scrape(page_source):
    soup = BeautifulSoup(page_source,features="html.parser")


    #finding leaf nodes
    exclude_elements = ['script', 'style', 'link', 'footer', 'nav', 'button','footer',
    'nav', 'slidebar', 'blurb', 'promo', 'ad','img']

    # Get unique leaf nodes excluding specified elements
    unique_leaf_nodes = get_leaf_nodes(soup, exclude_elements)

    # Create a DataFrame to store the data
    data = {'Element': [], 'HTML': [],'Content': []}

    # Extract data for each unique leaf node and add to the DataFrame
    for node in unique_leaf_nodes:
        elements_data = extract_elements_data(soup, node)
        for element_data in elements_data:
            data['Element'].append(element_data['Element'])
            data['HTML'].append(element_data['HTML'])
            data['Content'].append(element_data['Content'])

    # Ensure 'Element' is in column 1 and 'Content' is in column 2
    df = pd.DataFrame(data, columns=['Element','HTML','Content'])

    df = df.dropna(subset=['Content'])  # Drop rows where 'Content' is null
    df.to_csv('Train_data.csv', index=False)

    #log("Data saved to predict")


    #Predicting the data
    svm_classifier = joblib.load(r'C:\Users\User\Desktop\FYP\Webscraper\FYP2_model1.pkl')
    tfidf_vectorizer = joblib.load(r'C:\Users\User\Desktop\FYP\Webscraper\FYP2_vectorizer1.pkl')

    # Load the test CSV file
    test_df = pd.read_csv('Train_data.csv', encoding='unicode_escape')
    # Apply the same text preprocessing to the 'Content' column
    test_df['Content'] = test_df['Content'].apply(preprocess_text)
    # Transform the test data using the same TF-IDF vectorizer
    X_test_tfidf = tfidf_vectorizer.transform(test_df['Content'].values.astype('U'))
    # Predict the classes using the trained SVM classifier
    predictions = svm_classifier.predict(X_test_tfidf)
    # Add the predicted classes to the test DataFrame
    test_df['Predicted_Class'] = predictions
    # Save the updated DataFrame to a new CSV file
    test_df.to_csv('Data_predictions.csv', index=False)

    # Filter rows with predicted class 'Tender'
    tender_rows = test_df[test_df['Predicted_Class'] == 'Tender']

    # List to store classes
    #classes_list = []

    # Dictionary to store data
    #data = {'Tag': [], 'Class': []}

    # Assuming 'test_predictions.csv' contains the output with 'Predicted_Class' column
    test_predictions_df = pd.read_csv('data_predictions.csv')

    # Filter rows with predicted class 'Tender'
    tender_rows = test_predictions_df[test_predictions_df['Predicted_Class'] == 'Tender']

    # Iterate over each row in 'tender_rows' and apply the extract_classes function
    #data1 = {'Tag': [], 'Class': []}
    #for index, row in tender_rows.iterrows():
     #   html_input = row['HTML']
      #  element_data = row['Element']
       # extract_classes(html_input, element_data)

    # Print the list of unique classes
    #for class_name in classes_list:
        #print(class_name)

    # Convert the dictionary to a DataFrame
    class_data_df = extract_classes(tender_rows)
    class_data_df = class_data_df.drop_duplicates()

    class_data_df.to_csv('class_data.csv', index=False)

    # Apply the extract_text function to create a new 'Text' column
    class_data_df['Content'] = class_data_df.apply(extract_text, axis=1)

    # Drop rows where 'Text' column is empty
    class_data_df = class_data_df.dropna(subset=['Content'])

    # Save the updated DataFrame to a new CSV file
    class_data_df.to_csv('class_data_with_text.csv', index=False)

    TenderResult = {'Tag': [], 'Class': [],'Final': []}
    for index, row in class_data_df.iterrows():

        # Find all elements based on the tag and class
        Tenderlist = soup.find_all(row['Tag'], class_=row['Class'])

        # Extract text content from the found elements
        TenderCleaned = [Tender.text.strip() for Tender in Tenderlist]

        # Do something with TenderCleaned, for example, print it
        #print(TenderCleaned)
        
        for v in TenderCleaned:
            TenderResult['Tag'].append(row['Tag'])
            TenderResult['Class'].append(row['Class'])
            TenderResult['Final'].append(v)
            #print(v)
            #print("\n")
            
        
        #print("\n")
    
    TenderResult_df = pd.DataFrame(TenderResult)
    TenderResult_df = TenderResult_df.drop_duplicates()
    TenderResult_df.to_csv('TenderResult.csv', index=False)

    return TenderResult_df

# Prompt user for URL
val = sys.argv[1]

#val = input('Enter a URL: ')  # Prompt the user enter  URL
wait = WebDriverWait(driver, 10)
driver.get(val)
get_url = driver.current_url
wait.until(EC.url_to_be(val))

time.sleep(5)
if get_url == val:
    page_source = driver.page_source

tender_df = scrape(page_source)


# Ask user if they want to scrape more pages
#continue_scraping = input("Do you want to scrape from other pages? (yes/no): ")
continue_scraping = sys.argv[2]
if continue_scraping.lower() == 'yes':
    error_handler = True
    #next_button_xpath = input("Enter the XPath for the 'Next' button: ")
    next_button_xpath = sys.argv[3]
    #disabled_class = input("Enter the class name when the 'Next' button is disabled: ")
    disabled_class = sys.argv[4]
    page_number = 1

    start_time = time.time()#HERE TIME
    #next_button = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
    while True:
        #HERE TIME
        if time.time() - start_time > 600:  # 600 seconds = 10 minutes
            #print("Time limit reached (10 minutes). Exiting the loop.")
            #print(f"Reached the last page: Page {page_number}")
            break

        try:
            next_button = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
            next_button_disabled = driver.find_elements(By.XPATH, f"{next_button_xpath}/ancestor::li[contains(@class, '{disabled_class}')]")
            if next_button_disabled:
                #print(f"Reached the last page: Page {page_number}")
                break
        
            next_button.click()
            error_handler = False
            time.sleep(3)
            page_source = driver.page_source
            current_page = scrape(page_source)
            tender_df = pd.concat([tender_df, current_page], ignore_index=True)
            #initial_data = pd.concat([initial_data, page_data], ignore_index=True)
            
            
            page_number += 1
            #print(page_number)
            #time.sleep(2)
        except NoSuchElementException:
            #print(f"Element not found on page: Page {page_number}")
            break
        except TimeoutException:
            if(error_handler):
                print(f"Timeout occurred on page: Page {page_number}. Check your Xpath Value.")
                print("")
            break

svm_classifier = joblib.load(r'C:\Users\User\Desktop\FYP\Webscraper\FYP2_model1.pkl')
tfidf_vectorizer = joblib.load(r'C:\Users\User\Desktop\FYP\Webscraper\FYP2_vectorizer1.pkl')

    # Load the test CSV file LOOK HEREeeeeeeeeeeeeeeeeeeeee
    #test_df = pd.read_csv('pagination_data.csv', encoding='unicode_escape')

    # Apply the same text preprocessing to the 'Content' column
tender_df['Final'] = tender_df['Final'].apply(preprocess_text)

    # Transform the test data using the same TF-IDF vectorizer
X_test_tfidf = tfidf_vectorizer.transform(tender_df['Final'].values.astype('U'))

    # Predict the classes using the trained SVM classifier
predictions = svm_classifier.predict(X_test_tfidf)

    # Add the predicted classes to the test DataFrame
tender_df['Predicted_Class'] = predictions

    # Save the updated DataFrame to a new CSV file
tender_df.to_csv('TenderResult_Predicted.csv', index=False)

data = tender_df  # Replace with your file path

# Grouping the data by 'Tag' and 'Class'
grouped_data = data.groupby(['Tag', 'Class'])

# Filtering groups where more than 50% of 'Predicted_Class' is 'Tender'
filtered_groups = []
for name, group in grouped_data:
    if (group['Predicted_Class'] == 'Tender').mean() >= 0.5:
        filtered_groups.append(group)

# Creating a new DataFrame with the filtered results
filtered_data = pd.concat(filtered_groups)

filtered_data = filtered_data[filtered_data['Predicted_Class'] == 'Tender']
filtered_data = filtered_data.drop_duplicates()
# Correcting the code to handle non-string entries in the 'Final' column
filtered_data = filtered_data[filtered_data['Final'].apply(lambda x: len(str(x).split()) <= 50)]

# Displaying the first few rows of the updated dataframe
filtered_data.to_csv('temp.csv', index=False)

if continue_scraping.lower() == 'no':
    # Convert the 'Final' column to a list
    final_list = filtered_data['Final'].tolist()

    # Create an empty list to store elements that do not meet the condition
    non_matching_pairs = []

    # Loop to compare elements
    for i in range(len(final_list)):
        for j in range(i + 1, len(final_list)):
            val = fuzz.partial_ratio(final_list[i], final_list[j])
            if val < 40 or val > 80:
                non_matching_pairs.append((final_list[i], final_list[j]))

    # Find elements repeated more than twice
    #from collections import Counter
    elements = [item for pair in non_matching_pairs for item in pair]
    

    # Filtering the DataFrame
    filtered_df = filtered_data[filtered_data['Final'].isin(elements)]

    # Retrieving the corresponding 'class' values
    class_values = filtered_df['Class'].tolist()

    class_values = list(set(class_values))

    # Proceed only if there are more than one unique classes
    if len(class_values) > 1:
        # Count the frequency of each class in the DataFrame
        class_counts = filtered_data['Class'].value_counts()

        # Find the class with the minimum frequency in class_values
        min_freq_class = min(class_values, key=lambda x: class_counts.get(x, float('inf')))

        # Remove rows with this class
        filtered_data = filtered_data[filtered_data['Class'] != min_freq_class]


Final_tender_list = filtered_data[['Final']]
Final_tender_list = Final_tender_list.drop_duplicates()



Final_tender_list['Final'] = Final_tender_list['Final'].apply(lambda x: x.capitalize())



# Iterating and printing
i = 0
for index, row in Final_tender_list.iterrows():
    i = i+1
    print(f"{i}. {row['Final']}")
      

print('\n','IT_TENDER','\n')

# Read keywords from keywords.txt
with open(r'C:\Users\User\Desktop\FYP\Webscraper\IT_keywords.txt', 'r') as file:  # Replace with your keywords file path
    keywords = [line.strip().lower() for line in file]

# Function to check if any keyword is in the text
def contains_keyword(text):
    for keyword in keywords:
        if keyword in text.lower():
            return True
    return False

# Checking each row in the 'Final' column for IT keywords
IT_tender = [tender for tender in Final_tender_list['Final'] if contains_keyword(tender)]

Final_tender_list['Label'] = Final_tender_list['Final'].apply(lambda x: 'IT_tender' if x in IT_tender else '')
Final_tender_list.to_csv(r'C:\Users\User\Desktop\FYP\Webscraper\webscraper-ui\storage\app\public\download\Final_tender_list.csv', index=False)

# Print each item with its index
for i, tender in enumerate(IT_tender, start=1):
    print(f"{i}) {tender}\n")


driver.quit()