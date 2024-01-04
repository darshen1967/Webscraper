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
    print(str_args)

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

    log("Data saved to predict")


    #Predicting the data
    svm_classifier = joblib.load('FYP2_model.pkl')
    tfidf_vectorizer = joblib.load('FYP2_vectorizer.pkl')

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

    for index, row in class_data_df.iterrows():

        # Find all elements based on the tag and class
        Tenderlist = soup.find_all(row['Tag'], class_=row['Class'])

        # Extract text content from the found elements
        TenderCleaned = [Tender.text.strip() for Tender in Tenderlist]

        # Do something with TenderCleaned, for example, print it
        print(TenderCleaned)
    print("\n","next","\n")
    #TenderCleaned = [Tender.text.strip() for Tender in Tenderlist]

# Prompt user for URL
val = input('Enter a URL: ')  # Prompt the user enter  URL
wait = WebDriverWait(driver, 10)
driver.get(val)
get_url = driver.current_url
wait.until(EC.url_to_be(val))

if get_url == val:
    page_source = driver.page_source

scrape(page_source)

# Ask user if they want to scrape more pages
continue_scraping = input("Do you want to scrape from other pages? (yes/no): ")
if continue_scraping.lower() == 'yes':
    next_button_xpath = input("Enter the XPath for the 'Next' button: ")
    disabled_class = input("Enter the class name when the 'Next' button is disabled: ")
    page_number = 1
    #next_button = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
    while True:
        try:
            next_button = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
            next_button_disabled = driver.find_elements(By.XPATH, f"{next_button_xpath}/ancestor::li[contains(@class, '{disabled_class}')]")
            if next_button_disabled:
                print(f"Reached the last page: Page {page_number}")
                break
        
            next_button.click()
            time.sleep(5)
            page_source = driver.page_source
            scrape(page_source)
            #initial_data = pd.concat([initial_data, page_data], ignore_index=True)
            
            
            page_number += 1
            print(page_number)
            #time.sleep(2)
        except NoSuchElementException:
            print(f"Element not found on page: Page {page_number}")
            break
        except TimeoutException:
            print(f"Timeout occurred on page: Page {page_number}")
            break
        

driver.quit()