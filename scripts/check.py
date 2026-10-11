"""Best-effort collector for publicly accessible official Bari school-office pages.
Does NOT certify absence of nominations or inspect all school websites.
"""
import datetime as dt
import io
import json
import os
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'results.json'
SEEDS = ["https://www.uspbari.it/usp/?s=GPS"]
HEADERS = {"User-Agent": "GPS-Lorenzo/0.1 (public school notices research; contact via GitHub repository)"}
TIMEOUT = 18
MAX_PDFS = 15
MAX_BYTES = 12 * 1024 * 1024
KEYWORDS = re.compile(r'(?i)\b(?:AB55|AB56|chitarra|gps|nomine|bollettin[oi]|supplenz[ae]|rettific[ae])\b')
NAMES = re.compile(r'(?i)\b(?:rodio|bombacigno|schiavone)\b')
SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def get(url):
    r = SESSION.get(url, timeout=TIMEOUT, allow_redirects=True)
    r.raise_for_status()
    if len(r.content) > MAX_BYTES:
        raise ValueError('File troppo grande')
    return r


def official(url):
    host = (urlparse(url).hostname or '').lower()
    return host == 'uspbari.it' or host.endswith('.uspbari.it')


def main():
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
    previous = json.loads(OUT.read_text(encoding='utf8')) if OUT.exists() else {'documents': []}
    # Preserve historical records; remove duplicate URLs below.
    records = {d['url']: d for d in previous.get('documents', []) if d.get('url')}
    sources = []
    candidates = []
    for seed in SEEDS:
        try:
            page = get(seed)
            soup = BeautifulSoup(page.text, 'html.parser')
            sources.append({'label':'Ricerca GPS — Ambito Territoriale Bari', 'url':seed, 'status':'Pagina raggiunta', 'note':'Elenco non necessariamente esaustivo.'})
            for a in soup.find_all('a', href=True):
                href = urljoin(page.url, a['href'])
                label = a.get_text(' ', strip=True)[:180]
                if not official(href):
                    continue
                if href.lower().split('?')[0].endswith('.pdf'):
                    candidates.append((href,label or 'PDF ufficiale'))
                elif KEYWORDS.search(label) and ('2026' in label or 'gps' in label.lower()):
                    # Inspect selected article pages, not the entire site.
                    try:
                        article = get(href)
                        if 'text/html' not in article.headers.get('Content-Type','text/html'):
                            continue
                        inner = BeautifulSoup(article.text,'html.parser')
                        for b in inner.find_all('a',href=True):
                            u = urljoin(article.url,b['href'])
                            if official(u) and u.lower().split('?')[0].endswith('.pdf'):
                                candidates.append((u,b.get_text(' ',strip=True)[:180] or label))
                    except Exception as exc:
                        print('Article unavailable:',href,str(exc))
        except Exception as exc:
            sources.append({'label':'Ricerca GPS — Ambito Territoriale Bari','url':seed,'status':'Accesso fallito','note':str(exc)[:140]})
            print('Seed unavailable:',seed,str(exc))
    seen=set()
    processed=0
    for url,title in candidates:
        if url in seen or url in records or processed>=MAX_PDFS:
            continue
        seen.add(url)
        processed+=1
        try:
            response=get(url)
            pdf=PdfReader(io.BytesIO(response.content))
            text='\n'.join((p.extract_text() or '') for p in pdf.pages[:80])
            if not text.strip():
                print('No extractable text (possible scan):',url)
                continue
            # Only list documents whose extracted text indicates relevance to AB55/AB56.
            if not re.search(r'(?i)\bAB\s?5[56]\b|\bchitarra\b',text):
                continue
            matches=sorted(set(m.group(0).upper() for m in NAMES.finditer(text)))
            records[url]={'title':title or 'Documento ufficiale','url':url,'date':'Data da verificare',
                          'status':'Testo acquisito, nomina non verificata',
                          'note':'Documento pertinente per parola chiave. La presenza di un cognome non prova un incarico.',
                          'matches':matches}
        except Exception as exc:
            print('PDF unavailable:',url,str(exc))
    result={'checked_at':now,'documents':list(records.values()),'sources':sources}
    OUT.parent.mkdir(exist_ok=True,parents=True)
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Documents in archive:',len(records),'PDFs attempted:',processed)


if __name__=='__main__':
    main()
