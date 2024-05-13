import streamlit as st
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import google.generativeai as genai
import pandas as pd

# Make sure to insert your API key to run the app
genai.configure(api_key='YOUR_API_KEY')

# Function to get one-word topic from Gemini AI
def get_gemini_title_for_group(claims):
    model = genai.GenerativeModel('gemini-pro')
    claims_to_ai = 'Please give me a one word title that best describes the following claims' + '\n'.join(claims)
    response = model.generate_content(claims_to_ai)
    return response.text.strip()

# Function to run LDA clustering
def run_lda(claims, num_topics):
    # Vectorize claims text using CountVectorizer
    vectorizer = CountVectorizer()
    claims_counts = vectorizer.fit_transform(claims)

    # Apply LDA clustering
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda.fit(claims_counts)

    # Assign each claim to its corresponding topic
    topics = lda.transform(claims_counts).argmax(axis=1)

    # Group claims by topic
    grouped_claims = [[] for _ in range(num_topics)]
    for idx, topic in enumerate(topics):
        grouped_claims[topic].append(claims[idx])

    # Determine one-word topics for each group of claims
    group_topics = []
    for group_claims in grouped_claims:
        topic = get_gemini_title_for_group(group_claims)
        group_topics.append({'title': topic, 'number_of_claims': len(group_claims)})
    return group_topics

# Streamlit app
def main():
    st.title("Claim Clustering App")

    # Read the CSV file
    df = pd.read_csv('claims.csv')

    # Extract values from the 'claims' column into a list
    claims = df['Claims'].tolist()

    # Slider for selecting number of groups
    num_groups = st.slider("Select number of groups:", min_value=1, max_value=len(claims), value=3)

    # Button to run clustering
    if st.button("Run Clustering"):
        # Run KMeans clustering
        groups = run_lda(claims, num_groups)

        # Display response
        st.json({'groups': groups})

if __name__ == "__main__":
    main()
