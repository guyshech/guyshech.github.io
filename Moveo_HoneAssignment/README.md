# Project Name

Grouping Patent Texts

## Intro

This project aims to analyze patent claims in the mobile communications sector, grouping them into topics using various methods, culminating in the development of an interactive web application that allows users to select the number of groups they want to view, displaying the titles of the groups along with the number of claims in each group as output.

## Installation

I used python 3.9 version

To install the project, you need to use pip:
  <pre>
pip install sklearn // pip install scikit-learn
pip install scipy
pip install collections
pip install bs4
pip install requests
pip install csv
pip install streamlit
pip install google
pip install pandas 
</pre> 
  

## Task 1

You can change the URL of the patent if you want to take another claims from other patent.
You can also use : 'https://worldwide.espacenet.com/advancedSearch?locale=en_EP' to find patent related to mobile communication. 

## Task 2

The default num of group is 3, you can change this number in the code if you want.
I select LDA model.

## Task 3

Make sure you have Streamlit installed. You can install it via pip:
<pre> pip install streamlit </pre>
Run the Streamlit app using the following command:
<pre>streamlit run Task3_App.py</pre>

Make sure to replace:
<pre> 'genai.configure(api_key='YOUR_API_KEY') </pre>
with your api-key

![Streamlit Logo](https://github.com/guyshech/guyshech.github.io/blob/main/Moveo_HoneAssignment/streamlit_app.JPG)






