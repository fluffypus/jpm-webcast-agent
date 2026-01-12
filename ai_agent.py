from urllib.parse import urlparse


def compute_score(text, links, keywords, themes):
    score = 0.0

    for k in keywords:
        if k in text:
            score += 0.1

    for t in themes:
        if t.lower() in text:
            score += 0.15

    for l in links:
        if any(x in l for x in ["webcast", "event", "listen", "on24"]):
            score += 0.25

    return min(score, 1.0)


def extract_domains(links):
    domains = set()
    for l in links:
        if l.startswith("http"):
            parsed = urlparse(l)
            if parsed.netloc:
                domains.add(parsed.netloc.lower())
    return domains


def classify(score, company_domain, links):
    """
    Classification avec règle anti faux-positifs :
    - HIGH seulement si lien cohérent avec le domaine société
    """

    detected_domains = extract_domains(links)

    # domaines acceptables pour un vrai webcast
    allowed_domains = {
        company_domain.lower(),
        f"www.{company_domain.lower()}",
        "event.webcasts.com",
        "events.webcasts.com",
        "on24.com",
        "zoom.us"
    }

    domain_match = any(
        d in allowed_domains or d.endswith(company_domain.lower())
        for d in detected_domains
    )

    if score >= 0.85 and domain_match:
        return "HIGH"

    if score >= 0.6:
        return "MEDIUM"

    return "LOW"
