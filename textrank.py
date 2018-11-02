# https://rare-technologies.com/text-summarization-with-gensim/

import glob
import os

import re

from gensim.summarization import summarize

os.chdir('data')
for text_file in glob.glob('*.txt'):
    with open(text_file) as f:
        # Read
        text = f.read()
        # Clean
        text = text.strip()
        text = re.sub(r'\[[0-9]*\]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        # Summarize
        print(summarize(text))
