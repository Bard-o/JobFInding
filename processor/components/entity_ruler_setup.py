"""
EntityRuler setup — loads tech term patterns from a JSONL file into the spaCy pipeline.

The patterns file is at: processor/data/tech_patterns.jsonl

To add a new technology, just add a new line to that file following the format:
    {"label": "TECH", "pattern": [{"LOWER": "newthing"}]}

For multi-word tech names use multiple token dicts:
    {"label": "TECH", "pattern": [{"LOWER": "google"}, {"LOWER": "cloud"}]}
"""

import os
import json
from spacy.language import Language

# Path to the patterns file (relative to the processor working directory)
PATTERNS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "tech_patterns.jsonl")


def load_patterns() -> list[dict]:
    """Read the JSONL patterns file and return a list of pattern dicts."""
    patterns = []
    with open(PATTERNS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                patterns.append(json.loads(line))
    return patterns


def add_entity_ruler(nlp: Language) -> Language:
    """
    Add an EntityRuler to the pipeline loaded with tech patterns.
    Must be called AFTER the pipeline is created but BEFORE processing docs.
    """
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    patterns = load_patterns()
    ruler.add_patterns(patterns)
    print(f"✓ EntityRuler loaded with {len(patterns)} tech patterns")
    return nlp
