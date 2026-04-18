"""
NLP Processor Pipeline Stub

This script will read raw messages from the database and pass them 
through the spaCy pipeline to categorize and extract job offers.

Pipeline architecture to implement later:
(nlp) 
 ├── tokenizer
 ├── TextCategorizer → determinate if it is a Job offer
 ├── EntityRuler → Rules (technologies, modality)
 ├── NER → Complex entities (company, role, experience, salary)
 ├── custom component → post-processing and normalization
"""

import spacy
import os

from dotenv import load_dotenv
load_dotenv()

def main():
    print("Starting NLP Processor setup...")
    print("Loading spaCy models...")
    
    # Load the models just to ensure they are available
    nlp_en = spacy.load("en_core_web_md")
    nlp_es = spacy.load("es_core_news_md")
    
    print("Models loaded successfully! We are ready to build the pipeline.")

if __name__ == "__main__":
    main()
