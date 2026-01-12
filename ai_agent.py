def compute_score(text, links, keywords, themes):
    score = 0.0

    for k in keywords:
        if k in text:
            score += 0.1

    for t in themes:
        if t.lower() in text:
            score += 0.15

    for l in links:
        if any(x in l for x in ["webcast", "event", "listen"]):
            score += 0.2

    return min(score, 1.0)


def classify(score):
    if score >= 0.85:
        return "VERY HIGH"
    if score >= 0.7:
        return "HIGH"
    if score >= 0.5:
        return "MEDIUM"
    return "LOW"
