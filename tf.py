# https://towardsdatascience.com/text-summarization-96079bf23e83

import glob
import os

import nltk
import re

import heapq

from collections import Counter

stop_words = set(nltk.corpus.stopwords.words('english'))
stop_words.add('figure')
max_sentence_length = 30
max_summary_sentences = 3

os.chdir('data')
for text_file in glob.glob('*.txt'):
    with open(text_file, 'r', encoding='windows-1252') as f:
        # Read
        text = f.read()
        # Clean
        text = text.strip()
        text = re.sub(r'\[[0-9]*\]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        word_stream = text.lower()
        word_stream = re.sub(r'\W', ' ', word_stream)
        word_stream = re.sub(r'\d', ' ', word_stream)
        word_stream = re.sub(r'\s+', ' ', word_stream)
        # Count words
        word_stream = filter(lambda word: word not in stop_words, nltk.word_tokenize(word_stream))
        word_count = Counter(word_stream)
        max_count = max(word_count.values())
        word_count = Counter({word: count / max_count for word, count in word_count.items()})
        # Rank sentences
        raw_sentences = nltk.sent_tokenize(text)
        tokenized_sentences = filter(
            lambda words: len(words) <= max_sentence_length,
            map(lambda sentence: nltk.word_tokenize(sentence.lower()), raw_sentences)
        )
        sentence_score = {}
        for sentence, words in zip(raw_sentences, tokenized_sentences):
            for word in words:
                if sentence not in sentence_score:
                    sentence_score[sentence] = 0
                sentence_score[sentence] -= word_count[word] # because min heap
        # Print top sentences
        summary_sentences = heapq.nlargest(
            max_summary_sentences, sentence_score, key=sentence_score.get)
        print(f.name)
        print(' '.join(summary_sentences))
        print()
