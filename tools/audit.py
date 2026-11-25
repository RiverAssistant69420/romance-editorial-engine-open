"""Local advisory text audit. Python 3 standard library. No network, no edits."""
import argparse, collections, json, re
from pathlib import Path

def tokens(text):
    return re.findall(r"\b[\w]+(?:['’][\w]+)*", text.lower())

def audit(text, n=5, minimum=3, long=180):
    words=tokens(text)
    paras=[p for p in re.split(r'\n\s*\n', text) if p.strip()]
    counts=collections.Counter(tuple(words[i:i+n]) for i in range(len(words)-n+1))
    return {"words":len(words),"paragraphs":len(paras),"long_paragraph_candidates":[{"paragraph":i,"words":len(tokens(p))} for i,p in enumerate(paras,1) if len(tokens(p))>long],"repeated_phrase_candidates":[{"phrase":" ".join(g),"count":c} for g,c in counts.most_common(100) if c>=minimum],"note":"Advisory only. Repetition and paragraph length can be intentional."}

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("text_file",help="UTF-8 plain text with blank lines between paragraphs")
    p.add_argument("--phrase-length",type=int,default=5)
    p.add_argument("--minimum",type=int,default=3)
    p.add_argument("--long-paragraph",type=int,default=180)
    a=p.parse_args()
    if min(a.phrase_length,a.minimum,a.long_paragraph)<1: p.error("thresholds must be positive")
    print(json.dumps(audit(Path(a.text_file).read_text(encoding="utf-8-sig"),a.phrase_length,a.minimum,a.long_paragraph),ensure_ascii=False,indent=2))
