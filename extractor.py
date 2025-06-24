import re
import string
from collections import Counter
import json

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def extract_keywords(text, limit=10):
    words = clean_text(text).split()
    stopwords = set(['the', 'and', 'is', 'in', 'of', 'to', 'a', 'on', 'for', 'with', 'as', 'by', 'an', 'at'])  # add more
    keywords = [word for word in words if word not in stopwords and len(word) > 2]
    freq = Counter(keywords)
    return freq.most_common(limit)

def extract_entities(text):
    # Extract capitalized words (potential names or orgs)
    names = re.findall(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)?', text)
    orgs = [word for word in names if word.lower() not in ['The', 'A', 'In']]
    # Dates (simplified pattern)
    dates = re.findall(r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[^\n]{0,15}', text)
    return list(set(orgs)), list(set(dates))

def analyze_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    keywords = extract_keywords(text)
    orgs, dates = extract_entities(text)
    sentences = re.split(r'[.!?]', text)
    paragraphs = text.split('\n\n')

    report = {
        "Top Keywords": keywords,
        "Possible Names/Organizations": orgs,
        "Dates": dates,
        "Stats": {
            "Total Words": len(text.split()),
            "Total Sentences": len([s for s in sentences if s.strip()]),
            "Paragraphs": len([p for p in paragraphs if p.strip()])
        }
    }

    print("📄 Text Analysis Report:")
    for k, v in report.items():
        print(f"\n🔸 {k}:")
        print(v)

    # Save to JSON for output
    with open('report.json', 'w', encoding='utf-8') as out:
        json.dump(report, out, indent=4)

if __name__ == "__main__":
    analyze_text('article.txt')
