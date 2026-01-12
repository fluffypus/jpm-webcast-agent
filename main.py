for session in agenda["sessions"]:
    for company in session["companies"]:

        company_cfg = companies["companies"].get(company)
        if not company_cfg:
            continue

        domain = company_cfg["domain"]
        urls = [
            f"https://{domain}/{p}"
            for p in companies["defaults"]["base_paths"]
        ]

        keywords = (
            companies["defaults"]["generic_keywords"]
            + company_cfg.get("extra_keywords", [])
        )

        for url in urls:
            html = fetch_page(url)
            if not has_changed(url, html):
                continue

            text = extract_text(html)
            links = extract_links(html)

            score = compute_score(
                text, links, keywords, session["themes"]
            )

            if score >= 0.6:
                notify({
                    "company": company,
                    "session": session["name"],
                    "score": round(score, 2),
                    "confidence": classify(score),
                    "links": links
                })
