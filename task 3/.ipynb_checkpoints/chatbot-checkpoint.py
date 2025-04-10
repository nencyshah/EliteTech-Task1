import os
import json
import datetime
import csv
import nltk
import ssl
import random
import streamlit as st
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Fix SSL issue for nltk
ssl._create_default_https_context = ssl._create_unverified_context
nltk.download('punkt')

# Load intents from JSON file
file_path = os.path.join(os.getcwd(), "intents.json")
with open(file_path, "r", encoding="utf-8") as file:
    intents = json.load(file)

# Create the vectorizer and classifier
vectorizer = TfidfVectorizer()
clf = LogisticRegression(random_state=0, max_iter=10000)

# Preprocess the data
tags = []
patterns = []
for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        tags.append(intent["tag"])
        patterns.append(pattern)

# Train the model
x = vectorizer.fit_transform(patterns)
y = tags
clf.fit(x, y)

# Web Scraping Function to Get Financial Data (Example: FD Rates)
def get_fd_rates(bank_name):
    """Fetch the latest FD rates from the internet"""
    search_url = f"https://www.google.com/search?q={bank_name}+fixed+deposit+rates+India"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        result = soup.find("div", class_="BNeawe").text
        return f"The latest FD rate for {bank_name} is {result}."
    except:
        return "Sorry, I couldn't find the FD rates at the moment."

# Chatbot function
def chatbot(input_text):
    input_text_vector = vectorizer.transform([input_text])
    tag = clf.predict(input_text_vector)[0]

    # Check if user asks for real-time financial data
    if "fd_rate" in tag:
        bank_name = input_text.split()[-1]  # Extract bank name from input
        return get_fd_rates(bank_name)

    # Normal intent response
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

    return "I'm sorry, I didn't understand that."

# Streamlit UI
counter = 0

def main():
    global counter
    st.title("💰 Finance Chatbot with NLP")
    st.write("Ask me about budgeting, investments, credit scores, or latest FD rates!")

    # Sidebar menu
    menu = ["Home", "Conversation History", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Home
    if choice == "Home":
        st.subheader("💬 Chat with the Finance Bot")
        
        # Initialize chat log file
        if not os.path.exists('chat_log.csv'):
            with open('chat_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['User Input', 'Chatbot Response', 'Timestamp'])

        counter += 1
        user_input = st.text_input("You:", key=f"user_input_{counter}")

        if user_input:
            response = chatbot(user_input)
            st.text_area("Chatbot:", value=response, height=120, max_chars=None, key=f"chatbot_response_{counter}")

            # Log conversation
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('chat_log.csv', 'a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([user_input, response, timestamp])

            if response.lower() in ['goodbye', 'bye']:
                st.write("Thank you for chatting! Have a great day! 😊")
                st.stop()

    # Conversation History
    elif choice == "Conversation History":
        st.header("📜 Conversation History")
        with open('chat_log.csv', 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                st.text(f"🧑 User: {row[0]}")
                st.text(f"🤖 Chatbot: {row[1]}")
                st.text(f"📅 Timestamp: {row[2]}")
                st.markdown("---")

    # About Section
    elif choice == "About":
        st.subheader("🔍 About This Finance Chatbot")
        st.write("""
        - 💡 **Purpose**: This chatbot helps users with financial queries like budgeting, investments, and FD rates.
        - 🧠 **NLP Model**: Uses TfidfVectorizer & Logistic Regression for intent recognition.
        - 🌐 **Live Financial Data**: Fetches real-time FD rates from Google.
        - 🚀 **Built With**: Python, Streamlit, NLP, Web Scraping.
        """)

if __name__ == '__main__':
    main()
