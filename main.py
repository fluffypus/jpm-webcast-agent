import time
import yaml

from scraper import fetch_page, extract_text, extract_links
from diff_engine import has_changed
from ai_agent import compute_score, classify
from notifier import notify


# 🔹 Charger l'agenda
with open("agenda.yaml", "r") as f:
    agenda = yaml.safe_load(f)

# 🔹 Charger les sociétés
with open("companies.yaml", "r") as f:
    companies_cfg = yaml.safe_load(f)


def run():
    sessions = agenda.get("sessions", [])
    defaults = companies_cfg.get("defaults", {})
    companies = companies_cfg.get("companies", {})

    base_paths = defaults.get("base_paths", [])
    generic_keywords = defaults.get("generic_keywords", [])

    for session in sessions:
        session_name = session["name"]
        themes = session.get("themes", [])
        session_companies = session.get("companies", [])

        for company in session_companies:
            company_cfg = companies.get(company)
            if not company_cfg:
                continue

            domain = company_cfg.get("domain")
            extra_keywords = company_cfg.get("extra_keywords", [])

            urls = [
                f"https://{domain}/{path}"
                for path in base_paths
            ]

            keywords = generic_keywords + extra_keywords

            for url in urls:
                try:
                    html = fetch_page(url)

                    if not has_changed(url, html):
                        continue

                    text = extract_text(html)
                    links = extract_links(html)

                    score = compute_score(
                        text=text,
                        links=links,
                        keywords=keywords,
                        themes=themes
                    )

                    if score >= 0.6:
                        notify({
                            "company": company,
                            "session": session_name,
                            "confidence": classify(score),
                            "score": round(score, 2),
                            "links": links
                        })

                except Exception as e:
                    print(f"⚠️ {company} | {url} | {e}")


if __name__ == "__main__":
    run()
