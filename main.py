from heapq import nlargest
from string import punctuation

import spacy
from pytube import extract
from spacy.lang.en.stop_words import STOP_WORDS
from youtube_transcript_api import YouTubeTranscriptApi

# Task 1: Get the ID of the YouTube Video
url = 'https://www.youtube.com/watch?v=I2ZK3ngNvvI'
video_id = extract.video_id(url)

# Task 2: Get a Transcript of YouTube Video
transcript = YouTubeTranscriptApi.get_transcript(video_id)
text = ""

for elem in transcript:
    text = text + " " + elem["text"]

# Task 3: Get All Available Sentences
nlp = spacy.load('en_core_web_sm')
document = nlp(text)

# Task 4: Get All Tokens from the Document
tokens = [token.text for token in document]

# Task 5: Calculate the Frequency of Tokens
word_frequencies = {}
for word in document:
    text = word.text.lower()
    if text not in list(STOP_WORDS) and text not in punctuation:
        if word not in word_frequencies.keys():
            word_frequencies[word.text] = 1
        else:
            word_frequencies[word.text] += 1

# Task 6: Normalize the Frequency of Tokens
max_frequency = max(word_frequencies.values())
for word in word_frequencies.keys():
    word_frequencies[word] = word_frequencies[word] / max_frequency

# Task 7: Calculate the Score of Sentences
sentence_tokens = [sentence for sentence in document.sents]
sentence_score = {}

for sentence in sentence_tokens:
    for word in sentence:
        if word.text.lower() in word_frequencies.keys():
            if sentence not in sentence_score.keys():
                sentence_score[sentence] = word_frequencies[word.text.lower()]
            else:
                sentence_score[sentence] += word_frequencies[word.text.lower()]

# Task 8: Generate the Summary
select_length = int(len(sentence_tokens) * 0.3)
best_sentences = nlargest(select_length, sentence_score, key=sentence_score.get)
# Create a list of tuples that contains the best sentences and their order of appearance
summary_order = [(sentence, idx) for idx, sentence in enumerate(sentence_tokens) if sentence in best_sentences]

# Sort the sentences by order of appearance and join them
summary = '\n'.join(sentence.text for sentence, idx in sorted(summary_order, key=lambda x: x[1]))

print("The summary is: ", summary)
