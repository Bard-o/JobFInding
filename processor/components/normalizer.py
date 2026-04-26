"""
Technology name normalizer — maps variations to a single canonical name.

How to add more aliases:
    Just add entries to TECH_ALIASES below. The key is the lowercase
    version of the variation, the value is the canonical name you
    want stored in the database.

    Example:
        "fastapi": "FastAPI",
        "fast api": "FastAPI",
"""

# ══════════════════════════════════════════════════════════════
# TECH ALIASES — lowercase variation → canonical name
# Add more entries here as you discover new variations!
# ══════════════════════════════════════════════════════════════
TECH_ALIASES = {
    # JavaScript ecosystem
    "react": "React",
    "react.js": "React",
    "reactjs": "React",
    "vue": "Vue.js",
    "vue.js": "Vue.js",
    "vuejs": "Vue.js",
    "next.js": "Next.js",
    "nextjs": "Next.js",
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "javascript": "JavaScript",
    "js": "JavaScript",
    "typescript": "TypeScript",
    "ts": "TypeScript",

    # Backend languages
    "python": "Python",
    "java": "Java",
    "go": "Go",
    "golang": "Go",
    ".net": ".NET",
    "dotnet": ".NET",

    # Cloud & infrastructure
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    "aws": "AWS",
    "gcp": "GCP",
    "google cloud": "GCP",
    "azure": "Azure",
    "terraform": "Terraform",
    "ansible": "Ansible",
    "jenkins": "Jenkins",
    "gitlab": "GitLab",
    "github actions": "GitHub Actions",
    "ci/cd": "CI/CD",

    # Databases
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "mysql": "MySQL",
    "mongodb": "MongoDB",
    "redis": "Redis",
    "sql": "SQL",

    # Data & monitoring
    "power bi": "Power BI",
    "grafana": "Grafana",
    "prometheus": "Prometheus",

    # Testing & tools
    "selenium": "Selenium",
    "jira": "JIRA",
    "scrum": "Scrum",

    # Frontend
    "html": "HTML",
    "css": "CSS",
    "tailwind": "Tailwind CSS",

    # AI / ML
    "openai": "OpenAI",

    # Enterprise
    "oracle": "Oracle",

    # ──────────────────────────────────────────────────────────
    # ADD MORE ALIASES BELOW THIS LINE
    # Format:  "lowercase_variation": "Canonical Name",
    # ──────────────────────────────────────────────────────────
}


def normalize_tech_name(raw_name: str) -> str:
    """
    Given a raw technology name (e.g. from an EntityRuler match),
    return the canonical version. Falls back to the original if no alias found.
    """
    key = raw_name.lower().strip()
    return TECH_ALIASES.get(key, raw_name)


def get_normalized_techs(doc) -> list[str]:
    """
    Extract all TECH entities from a spaCy doc and return their
    normalized names as a deduplicated list.
    """
    seen = set()
    result = []
    for ent in doc.ents:
        if ent.label_ == "TECH":
            normalized = normalize_tech_name(ent.text)
            if normalized not in seen:
                seen.add(normalized)
                result.append(normalized)
    return result
