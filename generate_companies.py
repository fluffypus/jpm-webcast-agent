import yaml
import os


def normalize_domain(company_name):
    """
    Heuristique simple pour deviner le domaine
    (modifiable plus tard)
    """
    name = company_name.lower()
    name = name.replace("&", "and")
    name = name.replace(" ", "")
    return f"{name}.com"


def load_yaml(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}


def main():
    agenda = load_yaml("agenda.yaml")
    existing = load_yaml("companies.yaml")

    sessions = agenda.get("sessions", [])

    # sociétés trouvées dans l'agenda
    companies_in_agenda = set()
    for s in sessions:
        for c in s.get("companies", []):
            companies_in_agenda.add(c)

    # structure de sortie
    output = {
        "defaults": existing.get("defaults", {
            "base_paths": ["investors", "events", "news"],
            "generic_keywords": ["webcast", "presentation", "conference", "jpm"]
        }),
        "companies": existing.get("companies", {})
    }

    for company in sorted(companies_in_agenda):
        if company not in output["companies"]:
            output["companies"][company] = {
                "domain": normalize_domain(company),
                "extra_keywords": []
            }

    with open("companies.yaml", "w") as f:
        yaml.dump(output, f, sort_keys=False)

    print(f"✅ companies.yaml mis à jour ({len(output['companies'])} sociétés)")


if __name__ == "__main__":
    main()
