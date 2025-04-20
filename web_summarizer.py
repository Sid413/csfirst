"""
Web-based Text Summarization Tool using Streamlit
- Supports NLTK and spaCy extractive summarization
- Runs in the browser, no X11 required
"""
import streamlit as st
import nltk
import spacy
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from string import punctuation

# Download required NLTK data if not present
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Load spaCy model
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    from spacy.cli import download
    download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

st.set_page_config(page_title="Text Summarizer", layout="wide")

st.title("Text Summarization Tool")

METHODS = ["NLTK Extractive", "spaCy Extractive", "TextRank (Sumy)"]

if 'method' not in st.session_state:
    st.session_state['method'] = METHODS[0]
if 'summary_percent' not in st.session_state:
    st.session_state['summary_percent'] = 30
if 'min_sent_length' not in st.session_state:
    st.session_state['min_sent_length'] = 20

with st.sidebar:
    st.header("Summarization Settings")
    method = st.radio("Summarization Method", METHODS, key="method")
    if method == "NLTK Extractive":
        st.info("Uses NLTK for sentence and word tokenization. Ranks sentences by frequency of non-stopword words. Simple, fast, and interpretable.")
    elif method == "spaCy Extractive":
        st.info("Uses spaCy for advanced NLP (lemmatization, tokenization). Ranks sentences by lemmatized word frequency. Handles linguistic nuance.")
    elif method == "TextRank (Sumy)":
        st.info("Uses the TextRank algorithm (sumy library), a graph-based ranking model inspired by PageRank. Popular and effective for extractive summarization.")
    summary_percent = st.slider("Summary Length (% of sentences)", 10, 90, st.session_state['summary_percent'], 1, key="summary_percent")
    min_sent_length = st.slider("Minimum Sentence Length (chars)", 5, 100, st.session_state['min_sent_length'], 1, key="min_sent_length")

uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

# Set up session state for text input
if 'text_input' not in st.session_state:
    st.session_state['text_input'] = ""

# If a file is uploaded, update the text area value
if uploaded_file is not None:
    uploaded_text = uploaded_file.read().decode("utf-8")
    st.session_state['text_input'] = uploaded_text

text_input = st.text_area("Or paste your text here:", value=st.session_state['text_input'], height=200, key="text_input_area")
st.session_state['text_input'] = text_input
text = text_input.strip()

summary = ""

summarize_clicked = st.button("Summarize", key="summarize_btn")

# Only update summary if Summarize is clicked
if 'summary_output' not in st.session_state:
    st.session_state['summary_output'] = ''
if 'last_summary_params' not in st.session_state:
    st.session_state['last_summary_params'] = {}

# --- Summarization Methods ---
def nltk_summary(text, summary_percent=30, min_sent_length=20):
    sentences = sent_tokenize(text)
    sentences = [s for s in sentences if len(s.strip()) >= min_sent_length]
    if not sentences:
        return ""
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english') + list(punctuation))
    words = [w for w in words if w not in stop_words]
    freq = FreqDist(words)
    ranking = {i: sum(freq[w.lower()] for w in word_tokenize(s) if w.lower() in freq) for i, s in enumerate(sentences)}
    n = max(1, int(len(sentences) * summary_percent / 100))
    top_idx = sorted(ranking, key=ranking.get, reverse=True)[:n]
    top_idx.sort()
    return ' '.join([sentences[i] for i in top_idx])

# Sumy TextRank summarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

def sumy_summary(text, summary_percent=30, min_sent_length=20):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    sentences = [str(sentence) for sentence in parser.document.sentences if len(str(sentence).strip()) >= min_sent_length]
    if not sentences:
        return ""
    n = max(1, int(len(sentences) * summary_percent / 100))
    summary_sentences = summarizer(parser.document, n)
    return ' '.join(str(sentence) for sentence in summary_sentences)

def spacy_summary(text, summary_percent=30, min_sent_length=20):
    doc = nlp(text)
    sentences = [sent for sent in doc.sents if len(sent.text.strip()) >= min_sent_length]
    if not sentences:
        return ""
    # Lemmatize words, remove stopwords and punctuation
    words = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
    freq = FreqDist(words)
    ranking = {
        i: sum(freq[token.lemma_.lower()] for token in sent if not token.is_stop and not token.is_punct)
        for i, sent in enumerate(sentences)
    }
    n = max(1, int(len(sentences) * summary_percent / 100))
    top_idx = sorted(ranking, key=ranking.get, reverse=True)[:n]
    top_idx.sort()
    return ' '.join([sent.text for i, sent in enumerate(sentences) if i in top_idx])

# Use a dict of params to check if input has changed
current_params = {
    'method': method,
    'summary_percent': summary_percent,
    'min_sent_length': min_sent_length,
    'text': text
}

# Only recompute summary if Summarize is clicked
if summarize_clicked and text:
    if method == "NLTK Extractive":
        summary = nltk_summary(text, summary_percent, min_sent_length)
    elif method == "spaCy Extractive":
        summary = spacy_summary(text, summary_percent, min_sent_length)
    elif method == "TextRank (Sumy)":
        summary = sumy_summary(text, summary_percent, min_sent_length)
    st.session_state['summary_output'] = summary
    st.session_state['last_summary_params'] = current_params.copy()

if st.session_state['summary_output']:
    st.subheader("Summary")
    summary_edited = st.text_area("Summary Output", value=st.session_state['summary_output'], height=200, key="summary_output_area")
    st.session_state['summary_output'] = summary_edited
    st.write(f"Input Words: {len(text.split())} | Summary Words: {len(summary_edited.split())}")
    # Download button
    st.download_button(
        label="Download Summary as .txt",
        data=summary_edited,
        file_name="summary.txt",
        mime="text/plain"
    )
elif not summarize_clicked:
    st.info("Upload a text file or paste text above, then click Summarize.")
