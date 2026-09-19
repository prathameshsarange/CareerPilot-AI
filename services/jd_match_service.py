import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def match_resume_to_jd(resume_text: str, jd_text: str, top_n: int = 20) -> dict:
    """Score how well a resume matches a job description using TF-IDF +
    cosine similarity — no Gemini call involved, so this is free and
    doesn't count against the API rate limit.

    Returns:
        match_score: 0-100 overall similarity
        matched_keywords: JD phrases (by TF-IDF weight) that also appear in the resume
        missing_keywords: JD phrases that don't appear in the resume
    """

    resume_text = (resume_text or "").strip()
    jd_text = (jd_text or "").strip()

    if not resume_text or not jd_text:
        raise ValueError("Both resume text and job description text are required.")

    # Overall similarity: unigrams only. Bigrams are too sparse for short
    # documents like resumes/JDs — two texts that are a genuinely strong
    # match on topic can still share almost no exact two-word phrases,
    # which drags a bigram-inclusive cosine score down misleadingly.
    pair_vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 1))
    pair_matrix = pair_vectorizer.fit_transform([resume_text, jd_text])
    similarity = cosine_similarity(pair_matrix[0:1], pair_matrix[1:2])[0][0]
    match_score = round(float(similarity) * 100, 1)

    # Keyword breakdown: rank JD's own vocabulary by TF-IDF weight, then check
    # which of those terms literally appear in the resume text.
    jd_vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=60)
    jd_matrix = jd_vectorizer.fit_transform([jd_text])
    jd_terms = jd_vectorizer.get_feature_names_out()
    jd_weights = jd_matrix.toarray()[0]

    ranked_terms = [
        term for weight, term in sorted(zip(jd_weights, jd_terms), reverse=True)
        if weight > 0
    ]

    resume_lower = re.sub(r"\s+", " ", resume_text.lower())
    matched, missing = [], []
    for term in ranked_terms:
        (matched if term in resume_lower else missing).append(term)

    return {
        "match_score": match_score,
        "matched_keywords": matched[:top_n],
        "missing_keywords": missing[:top_n],
    }
