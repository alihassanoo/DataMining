import bs4 as bs
import urllib.request
import re
import nltk
import streamlit as st
import pandas as pd


st.title('Article Summarizer')
st.markdown("This application is a Streamlit text summarizer that can be used "
            "create summaries 🗽💥🚗")
st.subheader('Is it magic? No its linear algebra!!')
title = st.text_input('URL', 'https://en.wikipedia.org/wiki/Artificial_intelligence')
try:
  scraped_data = urllib.request.urlopen(title)
except ValueError:
  st.error('Please enter a valid input')

st.sidebar.subheader("Motivation for this project")
st.sidebar.info("As I write this project, 1,907,223,370 websites are active on the internet and 2,722,460 emails are being sent per second. This is an unbelievably huge amount of data. It is impossible for a user to get insights from such huge volumes of data.")
st.sidebar.header("Ali Hassan")
st.sidebar.subheader("SP17-BSE-132")
article = scraped_data.read()

parsed_article = bs.BeautifulSoup(article,"html.parser")

paragraphs = parsed_article.find_all('p')

article_text = ""

for p in paragraphs:
    article_text += p.text

# Removing Square Brackets and Extra Spaces
article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)
# Removing special characters and digits
formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
sentence_list = nltk.sent_tokenize(article_text)
stopwords = nltk.corpus.stopwords.words('english')



word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1
maximum_frequncy = max(word_frequencies.values())

chart_data = pd.DataFrame({'Word Frequency':[word_frequencies],'Words':[stopwords]},index=[0])
print(chart_data)
st.line_chart(chart_data,width = 900,height=500)


for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

sentence_scores = {}
for sent in sentence_list:

  for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

import heapq
summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)


summary = ' '.join(summary_sentences)
st.info(summary)
st.balloons()
st.success("Article summarized successfully")


print(summary)

