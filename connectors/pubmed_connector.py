# connectors/pubmed_connector.py
import logging
import os
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('PUBMED_API_KEY')
BASE = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'
CHUNK_SIZE = 200
logger = logging.getLogger(__name__)


def search(query, cfg, retmax=1000):
    '''Return a list of metadata dicts from PubMed (id, title, authors, year, doi, abstract, url)'''
    params = {
        'db': 'pubmed',
        'term': query,
        'retmax': retmax,
    }
    # only include API key if set (avoid passing 'None' which leads to HTTP 400)
    if API_KEY:
        params['api_key'] = API_KEY
    resp = requests.get(f"{BASE}/esearch.fcgi?{urlencode(params)}")
    resp.raise_for_status()
    from xml.etree import ElementTree as ET
    root = ET.fromstring(resp.text)
    ids = [idn.text for idn in root.findall('.//Id')]
    records = []
    if not ids:
        return records
    fetch_base = {
        'db': 'pubmed',
        'retmode': 'xml',
    }
    if API_KEY:
        fetch_base['api_key'] = API_KEY
    for idx in range(0, len(ids), CHUNK_SIZE):
        chunk = ids[idx:idx + CHUNK_SIZE]
        fetch_params = {**fetch_base, 'id': ','.join(chunk)}
        try:
            # POST keeps the payload in the body so long ID lists avoid hitting URL limits.
            r2 = requests.post(f"{BASE}/efetch.fcgi", data=fetch_params, timeout=30)
            r2.raise_for_status()
        except requests.HTTPError as exc:
            logger.warning('PubMed efetch chunk failed (%s..%s): %s', chunk[0], chunk[-1], exc)
            continue
        except requests.RequestException as exc:
            logger.warning('PubMed efetch chunk request error (%s..%s): %s', chunk[0], chunk[-1], exc)
            continue
        root2 = ET.fromstring(r2.text)
        for article in root2.findall('.//PubmedArticle'):
            try:
                title = article.find('.//ArticleTitle').text or ''
            except Exception:
                title = ''
            abstract_elems = article.findall('.//AbstractText')
            abstract = ' '.join([a.text or '' for a in abstract_elems])
            year = None
            try:
                year = article.find('.//PubDate/Year').text
            except Exception:
                pass
            doi = None
            for idv in article.findall('.//ArticleId'):
                if idv.attrib.get('IdType') == 'doi':
                    doi = idv.text
            authors = []
            for a in article.findall('.//Author'):
                lname = a.find('LastName')
                fname = a.find('ForeName')
                if lname is not None and fname is not None:
                    authors.append(f"{fname.text} {lname.text}")
            pmid = article.find('.//PMID').text
            url = f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/'
            records.append({
                'id': f'pubmed:{pmid}',
                'title': title,
                'authors': authors,
                'year': year,
                'doi': doi,
                'abstract': abstract,
                'url': url,
                'source': 'PubMed'
            })
    return records
