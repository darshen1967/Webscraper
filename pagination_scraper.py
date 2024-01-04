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

# [Place your scraping functions here: log, get_leaf_nodes, extract_elements_data, scrape_page]
# Initialize the WebDriver
wait = WebDriverWait(driver, 100)

# Function to log data
def log(*args):
    str_args = ""
    for arg in args:
        if isinstance(arg, dict) or isinstance(arg, list):
            str_args += json.dumps(arg)
        else:
            str_args += str(arg)
    print(str_args)

# Function to get leaf nodes
def get_leaf_nodes(master, exclude_tags):
    nodes = master.find_all(True)
    leaf_nodes = [elem for elem in nodes if not elem.find(True)]
    unique_leaf_nodes = []

    for node in leaf_nodes:
        if node.name not in exclude_tags:
            unique_leaf_nodes.append(node.name)

    return list(set(unique_leaf_nodes))

# Function to extract elements data
def extract_elements_data(soup, element_name):
    elements_data = []

    elements = soup.find_all(element_name)
    for element in elements:
        content = element.text.strip()
        if content:
            elements_data.append({
                'Element': element.name,
                'HTML': element,
                'Content': content
            })

    return elements_data

# Main scraping function
def scrape_page(page_url):
    driver.get(page_url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, features="html.parser")
    
    exclude_elements = ['script', 'style', 'link', 'footer', 'nav', 'button', 'footer', 'nav', 'slidebar', 'blurb', 'promo', 'ad', 'img']
    unique_leaf_nodes = get_leaf_nodes(soup, exclude_elements)
    data = {'Element': [], 'HTML': [], 'Content': []}

    for node in unique_leaf_nodes:
        elements_data = extract_elements_data(soup, node)
        for element_data in elements_data:
            data['Element'].append(element_data['Element'])
            data['HTML'].append(element_data['HTML'])
            data['Content'].append(element_data['Content'])

    return pd.DataFrame(data, columns=['Element', 'HTML', 'Content'])

# Initialize the TF-IDF vectorizer and SVM classifier
svm_classifier = joblib.load('FYP2_model.pkl')
tfidf_vectorizer = joblib.load('FYP2_vectorizer.pkl')

# Function to preprocess text
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
def extract_classes(html_input, element_data):
    soup = BeautifulSoup(html_input, 'html.parser')
    # Find all elements with a 'class' attribute
    elements_with_class = soup.find_all(class_=True)
    
    # Store data in the list of dictionaries
    data_list = []
    for element in elements_with_class:
        classes = element.get('class')
        if classes:
            for class_name in classes:
                data = {
                    'Tag': element_data,
                    'Class': class_name,
                    'HTML': str(element)
                }
                data_list.append(data)
    
    return data_list


# Function to extract text content from HTML based on 'Tag' and 'Class' columns
def extract_text(row):
    tag = row['Tag']
    class_name = row['Class']
    html_input = row['HTML']
    
    soup = BeautifulSoup(html_input, 'html.parser')
    element = soup.find(tag, {'class': class_name})
    
    if element:
        text_content = str(element.get_text(strip=True))
        return text_content
    else:
        return None

# Combined function to process a single page
def process_page(url):
    # Scrape the page
    initial_data = scrape_page(url)

    # Predict using the SVM classifier
    initial_data['Content'] = initial_data['Content'].apply(preprocess_text)
    X_tfidf = tfidf_vectorizer.transform(initial_data['Content'].values.astype('U'))
    predictions = svm_classifier.predict(X_tfidf)
    initial_data['Predicted_Class'] = predictions

    # Process to class_data_df
    tender_rows = initial_data[initial_data['Predicted_Class'] == 'Tender']
    all_data = []

# Iterate over each row in your DataFrame and call extract_classes
    for index, row in tender_rows.iterrows():
        html_input = str(row['HTML'])
        element_data = row['Element']
        class_data = extract_classes(html_input, element_data)
        all_data.extend(class_data)
    
    class_data_df = pd.DataFrame(all_data)
    #class_data_df = pd.DataFrame({'Tag': [], 'Class': []})
    # [Fill class_data_df using the data from extract_classes]

    class_data_df['Content'] = class_data_df.apply(extract_text, axis=1)
    return class_data_df
#.dropna(subset=['Content'])

# Main script
val = input('Enter a URL: ')
final_data = process_page(val)

continue_scraping = input("Do you want to scrape from other pages? (yes/no): ")
if continue_scraping.lower() == 'yes':
    next_button_xpath = input("Enter the XPath for the 'Next' button: ")
    disabled_class = input("Enter the class name when the 'Next' button is disabled: ")
    page_number = 1

    while True:
        try:
            next_button = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
            next_button_disabled = driver.find_elements(By.XPATH, f"{next_button_xpath}/ancestor::li[contains(@class, '{disabled_class}')]")
            if next_button_disabled:
                print(f"Reached the last page: Page {page_number}")
                break

            next_button.click()
            time.sleep(2)
            page_number += 1
            print(f"Processing Page {page_number}")

            # Process the new page
            page_data = process_page(driver.current_url)
            final_data = pd.concat([final_data, page_data])

        except NoSuchElementException:
            print(f"Element not found on page: Page {page_number}")
            break
        except TimeoutException:
            print(f"Timeout occurred on page: Page {page_number}")
            break

# Save the final data to a CSV file
final_data.to_csv('final_output.csv', index=False)
print("Data saved to final_output.csv")
