"""
CareerNova — ML Predictor
Uses KMeans clustering to classify a student as:
  Top Performer | Average | At Risk

Input: list of 5 subject marks (out of 100)
Output: cluster label string + career path suggestions
"""
import pickle
import numpy as np
import os

# Load model once at startup
_MODEL_PATH = os.path.join(os.path.dirname(__file__), "student_model.pkl")

with open(_MODEL_PATH, "rb") as f:
    _model_data = pickle.load(f)

_scaler          = _model_data["scaler"]
_kmeans          = _model_data["kmeans"]
_cluster_label_map = _model_data["cluster_label_map"]

# Career suggestions per performance tier
CAREER_SUGGESTIONS = {
    "Top Performer": [
        ("Software Engineer at FAANG",     "Your exceptional scores open doors to top-tier tech companies.",        97),
        ("Research Scientist / ML Engineer","Strong academics suit AI/ML research roles at DeepMind, OpenAI, etc.", 91),
        ("Product Manager",                "Combine technical depth with strategy for PM roles.",                   83),
    ],
    "Average": [
        ("Full Stack Developer",           "Solid foundations for building end-to-end web applications.",           74),
        ("Data Analyst",                   "Use your database and analytical skills for BI and reporting.",         68),
        ("QA / Test Engineer",             "Systematic thinking and attention to detail suit QA roles.",            61),
    ],
    "At Risk": [
        ("IT Support Specialist",          "Foundational IT skills lead to system admin and helpdesk roles.",       55),
        ("Junior Developer (with bootcamp)","Targeted upskilling can fast-track you into development roles.",       50),
        ("Technical Recruiter",            "Domain knowledge helps identify and assess technical talent.",          45),
    ],
}

# Risk level mapping
RISK_MAP = {
    "Top Performer": "Low",
    "Average":       "Medium",
    "At Risk":       "High",
}


def predict_student(subject_marks: list) -> dict:
    """
    Predict a student's performance tier from their subject marks.

    Args:
        subject_marks: list of up to 5 floats (marks out of 100).
                       Padded with subject mean (69) if fewer than 5 are given.

    Returns:
        {
          "tier":       "Top Performer" | "Average" | "At Risk",
          "risk_level": "Low" | "Medium" | "High",
          "careers":    [(title, description, match_score), ...]
        }
    """
    # Ensure exactly 5 features — pad with mean if fewer subjects
    marks = list(subject_marks)[:5]
    while len(marks) < 5:
        marks.append(69.0)   # approximate dataset mean

    features = np.array(marks).reshape(1, -1)
    scaled   = _scaler.transform(features)
    cluster  = int(_kmeans.predict(scaled)[0])
    tier     = _cluster_label_map[cluster]

    return {
        "tier":       tier,
        "risk_level": RISK_MAP[tier],
        "careers":    CAREER_SUGGESTIONS[tier],
    }
