import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class IntentEngine:
    """
    Semantic Intent Detection using TF-IDF Vectorization + Cosine Similarity.
    Replaces keyword/regex matching with genuine statistical NLP.
    """
    def __init__(self):
        self.wards = ["Diva", "Kalwa", "Mumbra", "Wagle Estate", "Naupada-Kopri",
                       "Majiwada-Manpada", "Vartak Nagar", "Uthalsar", "Lokmanya-Savarkar Nagar"]

        self.intent_corpus = {
            "Emergency": [
                "which ward requires immediate attention",
                "what is the most urgent area right now",
                "where is the emergency situation",
                "which area is currently most vulnerable",
                "what should we do immediately",
                "urgent action needed where",
                "where should we focus right now",
                "critical situation which ward",
                "highest priority ward",
                "which zone needs urgent help",
            ],
            "City-Wide": [
                "give me city summary",
                "city wide overview of all wards",
                "overall situation across the city",
                "all wards status report",
                "complete city analysis",
                "how is the entire city doing",
                "summarize all ward conditions",
                "full municipal status",
                "total city risk assessment",
            ],
            "Recommendation": [
                "what should officers do today",
                "where should officers focus",
                "recommend actions for the team",
                "what actions should we take",
                "operational recommendations",
                "suggest next steps for disaster response",
                "advise field teams on priorities",
                "where should i focus resources today",
            ],
            "Forecast": [
                "forecast incidents for next week",
                "how many incidents expected",
                "predict future disaster events",
                "what will happen in next days",
                "expected incident volume",
                "future disaster prediction",
                "upcoming risk forecast",
            ],
            "Resource": [
                "how many pumps should we deploy",
                "boat allocation needed",
                "resource shortage analysis",
                "deploy equipment to ward",
                "send more rescue teams",
                "resource demand for flood area",
                "what equipment is needed",
                "deploy pumps to mumbra",
                "need more boats for rescue",
                "resource gap in ward",
            ],
            "Building": [
                "which buildings need evacuation",
                "dangerous building assessment",
                "structural risk of buildings",
                "building collapse probability",
                "old buildings at risk",
                "building safety audit results",
                "evacuation candidates",
                "risky building",
                "buildings at risk",
                "unsafe building"
            ],
            "Ward Risk": [
                "which ward has highest risk",
                "ward vulnerability ranking",
                "ward risk score comparison",
                "most at risk ward",
                "compare ward danger levels",
            ],
            "Flood": [
                "flood risk prediction",
                "water logging probability",
                "rain flood likelihood",
                "monsoon flood forecast",
                "flooding chance in ward",
            ],
        }

        # Build TF-IDF model from corpus
        all_texts = []
        all_labels = []
        for intent, examples in self.intent_corpus.items():
            for ex in examples:
                all_texts.append(ex.lower())
                all_labels.append(intent)

        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        self.tfidf_matrix = self.vectorizer.fit_transform(all_texts)
        self.labels = all_labels

    def extract_ward(self, query):
        for w in self.wards:
            if w.lower() in query.lower():
                return w
        return None

    def detect_intent(self, query):
        q_lower = query.lower().strip()

        # Vectorize the query and compute cosine similarity against all training examples
        query_vec = self.vectorizer.transform([q_lower])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]

        best_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_idx])
        best_intent = self.labels[best_idx]

        # Out-of-Domain detection: empirically tuned threshold
        # Legitimate queries score >= 0.50, OOD queries score 0.38-0.47
        if best_score < 0.50:
            return {
                "primary_intent": "Unknown",
                "all_intents": ["Unknown"],
                "target_ward": None,
                "similarity_score": round(best_score, 4)
            }

        # Aggregate scores per intent to find all relevant intents
        intent_scores = {}
        for i, label in enumerate(self.labels):
            if label not in intent_scores or similarities[i] > intent_scores[label]:
                intent_scores[label] = similarities[i]

        # Sort intents by score
        sorted_intents = sorted(intent_scores.items(), key=lambda x: x[1], reverse=True)
        detected_intents = [intent for intent, score in sorted_intents if score > 0.08]

        if not detected_intents:
            detected_intents = [best_intent]

        extracted_ward = self.extract_ward(query)

        return {
            "primary_intent": best_intent,
            "all_intents": detected_intents,
            "target_ward": extracted_ward,
            "similarity_score": round(best_score, 4)
        }
