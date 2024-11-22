#Importing the necessary libraries
import nltk
nltk.download('punkt_tab')

nltk.download('stopwords')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import streamlit as st

# Charger le fichier texte
with open('ebook of meteorology the science of the atmosphere.txt', 'r', encoding='utf-8') as f:
    data = f.read().replace('\n', ' ')

# Tokeniser en phrases
sentences = sent_tokenize(data)

# Prétraitement global
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess(sentence):
    words = word_tokenize(sentence)
    words = [word.lower() for word in words if word.lower() not in stop_words and word not in string.punctuation]
    return [lemmatizer.lemmatize(word) for word in words]

# Prétraitez toutes les phrases une fois
preprocessed_corpus = [preprocess(sentence) for sentence in sentences]

# Calculer la similarité et trouver la phrase la plus pertinente
def get_most_relevant_sentence(query):
    query = preprocess(query)
    max_similarity = 0
    most_relevant_sentence = "Désolé, je n'ai pas trouvé de réponse pertinente."
    
    for sentence, preprocessed in zip(sentences, preprocessed_corpus):
        similarity = len(set(query).intersection(preprocessed)) / float(len(set(query).union(preprocessed)))
        if similarity > max_similarity:
            max_similarity = similarity
            most_relevant_sentence = sentence

    return most_relevant_sentence

# Fonction principale Streamlit
def main():
    st.title("Chatbot based on a book")
    st.write("Ask me a question about the book, and I'll do my best to answer it!")
    
    question = st.text_input("Vous :")
    if st.button("Envoyer"):
        response = get_most_relevant_sentence(question)
        st.write("Chatbot : " + response)

if __name__ == "__main__":
    main()
