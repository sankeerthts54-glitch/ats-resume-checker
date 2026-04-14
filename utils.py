import fitz

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)

def get_match_score(resume_text, jd_text):
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score * 100, 1)

def get_missing_keywords(resume_text, jd_text, top_n=15):
    stop = set(stopwords.words("english"))
    def keywords(text):
        words = text.lower().split()
        return set(w.strip(".,()[]") for w in words
                   if w not in stop and len(w) > 3)
    missing = keywords(jd_text) - keywords(resume_text)
    return sorted(list(missing))[:top_n]