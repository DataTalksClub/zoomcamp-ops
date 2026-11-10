#!/usr/bin/env python3
"""Turn identity evidence into one enrichment row per author (enrichment-all.csv).

Evidence hierarchy (README.md, "Identity matching rules"):
  confirmed  self_submitted_linkedin (CMP)  > github_declared_linkedin (own GitHub / personal site)
  signal     github_profile (self-declared company/bio on the author's own account)
  signal     domain_signal (corporate email domain; company only, never an identity link)
  candidate  name_search (Treg by name) -> medium only with corroboration, else low and flagged
Rows with confidence low/rejected are written but excluded from aggregates.
"""
from collections import Counter
import csv
import json
from pathlib import Path
import re
import unicodedata

try:
    import geonamescache
    _GC = geonamescache.GeonamesCache()
except ImportError:  # optional; country then comes from LinkedIn or explicit country names only
    _GC = None

MONTHS = {m: i for i, m in enumerate(['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'], 1)}
COURSE_WINDOW = {'start_month': 1, 'end_month': 4}  # cohort runs Jan..Apr; override per course in README

FREELANCE_RE = re.compile(r'\b(freelanc\w*|self[- ]employed|independent (?:data )?(?:consultant|contractor|engineer)|contractor|own (?:consultancy|company)|consulting (?:owner|founder)|upwork|fiverr|toptal|malt\b)', re.I)
FREELANCE_TYPES = {'freelance', 'self-employed', 'contract', 'self employed'}
STUDENT_RE = re.compile(r"\b(student|undergrad\w*|b\.?sc\.? candidate|m\.?sc\.? candidate|ph\.?d\.? (?:candidate|student)|master'?s (?:student|candidate)|studying|estudiante|étudiant|graduate student|pursuing (?:a )?(?:bachelor|master|degree))\b", re.I)
SEEKER_RE = re.compile(r'\b(open to (?:work|opportunit\w+|new roles?)|seeking|looking for (?:a |new |my )?(?:\w+ )?(?:opportunit\w+|roles?|jobs?|positions?)|job seeker|career (?:change|switch|transition)\w*|transitioning (?:in)?to|aspiring|unemployed|available for hire|actively looking)\b', re.I)
LEAD_RE = re.compile(r'\b(lead|head of|principal|staff|director|vp|vice president|chief|cto|ceo|cdo|founder|co-founder|cofounder|owner|manager|architect|partner)\b', re.I)
SENIOR_RE = re.compile(r'\b(senior|sr\.?|sênior|expert|specialist ii|iii)\b', re.I)
JUNIOR_RE = re.compile(r'\b(junior|jr\.?|intern(?:ship)?|trainee|graduate|apprentice|entry[- ]level|associate)\b', re.I)
ROLE_RULES = [
    ('analytics eng', re.compile(r'analytics engineer', re.I)),
    ('DE', re.compile(r'data engineer|data engineering|etl|elt developer|data platform|big data|dataops|data architect|data integration|pipeline|databricks engineer|data warehouse|dwh|data ops|bi engineer|data infrastructure', re.I)),
    ('DS/ML', re.compile(r'data scien|machine learning|\bml\b|mlops|\bai\b engineer|ai/ml|deep learning|\bnlp\b|computer vision|research scientist|applied scientist|statistician|quant', re.I)),
    ('DA', re.compile(r'data analyst|\bbi\b|business intelligence|power ?bi|tableau|reporting|insights? analyst|business analyst|analyst|analytics', re.I)),
    ('SWE', re.compile(r'software|backend|back-end|frontend|front-end|full[- ]?stack|developer|devops|\bsre\b|site reliability|cloud engineer|platform engineer|programmer|engineer|dba|database admin', re.I)),
]
COUNTRY_ALIASES = {'usa': 'United States', 'us': 'United States', 'u.s.': 'United States', 'united states of america': 'United States',
                   'uk': 'United Kingdom', 'england': 'United Kingdom', 'scotland': 'United Kingdom', 'wales': 'United Kingdom',
                   'uae': 'United Arab Emirates', 'deutschland': 'Germany', 'türkiye': 'Turkey', 'turkiye': 'Turkey', 'brasil': 'Brazil',
                   'españa': 'Spain', 'méxico': 'Mexico', 'the netherlands': 'Netherlands', 'holland': 'Netherlands', 'korea': 'South Korea',
                   'república dominicana': 'Dominican Republic', 'perú': 'Peru', 'ksa': 'Saudi Arabia', 'czechia': 'Czech Republic',
                   'nyc': 'United States', 'viet nam': 'Vietnam', 'russian federation': 'Russia', 'republic of korea': 'South Korea',
                   "cote d'ivoire": 'Ivory Coast', 'czech republic': 'Czech Republic', 'nederland': 'Netherlands', 'italia': 'Italy',
                   'polska': 'Poland', 'india.': 'India', 'bengaluru': 'India', 'bangalore': 'India', 'london': 'United Kingdom',
                   'lagos': 'Nigeria', 'nairobi': 'Kenya', 'cairo': 'Egypt', 'berlin': 'Germany', 'munich': 'Germany', 'paris': 'France',
                   'toronto': 'Canada', 'sao paulo': 'Brazil', 'são paulo': 'Brazil', 'madrid': 'Spain', 'barcelona': 'Spain', 'lisbon': 'Portugal',
                   'amsterdam': 'Netherlands', 'singapore': 'Singapore', 'dubai': 'United Arab Emirates', 'istanbul': 'Turkey', 'mumbai': 'India',
                   'delhi': 'India', 'new delhi': 'India', 'hyderabad': 'India', 'pune': 'India', 'chennai': 'India', 'karachi': 'Pakistan',
                   'lahore': 'Pakistan', 'jakarta': 'Indonesia', 'manila': 'Philippines', 'ho chi minh city': 'Vietnam', 'hanoi': 'Vietnam',
                   'kyiv': 'Ukraine', 'warsaw': 'Poland', 'mexico city': 'Mexico', 'bogota': 'Colombia', 'bogotá': 'Colombia', 'buenos aires': 'Argentina',
                   'santiago': 'Chile', 'lima': 'Peru', 'accra': 'Ghana', 'johannesburg': 'South Africa', 'cape town': 'South Africa', 'sydney': 'Australia',
                   'melbourne': 'Australia', 'tokyo': 'Japan', 'seoul': 'South Korea', 'beijing': 'China', 'shanghai': 'China', 'riyadh': 'Saudi Arabia',
                   'san francisco': 'United States', 'new york': 'United States', 'seattle': 'United States', 'chicago': 'United States', 'sf': 'United States', 'bay area': 'United States', 'remote': '', 'earth': '', 'worldwide': ''}
US_STATES = {'al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'de', 'fl', 'ga', 'hi', 'id', 'il', 'in', 'ia', 'ks', 'ky', 'la', 'me', 'md', 'ma', 'mi', 'mn',
             'ms', 'mo', 'mt', 'ne', 'nv', 'nh', 'nj', 'nm', 'ny', 'nc', 'nd', 'oh', 'ok', 'or', 'pa', 'ri', 'sc', 'sd', 'tn', 'tx', 'ut', 'vt', 'va',
             'wa', 'wv', 'wi', 'wy', 'california', 'texas', 'new york', 'florida', 'washington', 'massachusetts', 'illinois', 'virginia', 'georgia'}


def norm(s):
    return unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower().strip()


FALLBACK_COUNTRIES = '''Afghanistan,Albania,Algeria,Andorra,Angola,Argentina,Armenia,Australia,Austria,Azerbaijan,Bahamas,Bahrain,Bangladesh,Barbados,Belarus,Belgium,Belize,Benin,Bhutan,Bolivia,Bosnia and Herzegovina,Botswana,Brazil,Brunei,Bulgaria,Burkina Faso,Burundi,Cambodia,Cameroon,Canada,Cape Verde,Chad,Chile,China,Colombia,Congo,Costa Rica,Croatia,Cuba,Cyprus,Czech Republic,Denmark,Dominican Republic,Ecuador,Egypt,El Salvador,Estonia,Ethiopia,Fiji,Finland,France,Gabon,Gambia,Georgia,Germany,Ghana,Greece,Guatemala,Guinea,Haiti,Honduras,Hong Kong,Hungary,Iceland,India,Indonesia,Iran,Iraq,Ireland,Israel,Italy,Ivory Coast,Jamaica,Japan,Jordan,Kazakhstan,Kenya,Kosovo,Kuwait,Kyrgyzstan,Laos,Latvia,Lebanon,Lesotho,Liberia,Libya,Lithuania,Luxembourg,Macau,Madagascar,Malawi,Malaysia,Maldives,Mali,Malta,Mauritania,Mauritius,Mexico,Moldova,Monaco,Mongolia,Montenegro,Morocco,Mozambique,Myanmar,Namibia,Nepal,Netherlands,New Zealand,Nicaragua,Niger,Nigeria,North Macedonia,Norway,Oman,Pakistan,Palestine,Panama,Papua New Guinea,Paraguay,Peru,Philippines,Poland,Portugal,Puerto Rico,Qatar,Romania,Russia,Rwanda,Saudi Arabia,Senegal,Serbia,Sierra Leone,Singapore,Slovakia,Slovenia,Somalia,South Africa,South Korea,South Sudan,Spain,Sri Lanka,Sudan,Sweden,Switzerland,Syria,Taiwan,Tajikistan,Tanzania,Thailand,Togo,Trinidad and Tobago,Tunisia,Turkey,Turkmenistan,Uganda,Ukraine,United Arab Emirates,United Kingdom,United States,Uruguay,Uzbekistan,Venezuela,Vietnam,Yemen,Zambia,Zimbabwe'''.split(',')
_COUNTRIES, _CITIES = {norm(c): c for c in FALLBACK_COUNTRIES}, {}
if _GC:
    for c in _GC.get_countries().values():
        _COUNTRIES[norm(c['name'])] = c['name']
    names = {c['iso']: c['name'] for c in _GC.get_countries().values()}
    for city in sorted(_GC.get_cities().values(), key=lambda c: c['population']):
        for nm in [city['name']] + [a for a in city.get('alternatenames', []) if a.isascii()][:0]:
            _CITIES[norm(nm)] = names.get(city['countrycode'], '')


def country_of(location):
    if not location:
        return ''
    parts = [norm(p) for p in re.split(r'[,/|·\-–]| and ', location) if norm(p)]
    for p in reversed(parts):
        if p in COUNTRY_ALIASES:
            return COUNTRY_ALIASES[p]
        if p in _COUNTRIES:
            return _COUNTRIES[p]
        if p in US_STATES and len(parts) > 1:
            return 'United States'
    for p in parts:
        if p in _CITIES and len(p) > 3:
            return _CITIES[p]
    whole = norm(location)
    for name, canon in _COUNTRIES.items():
        if len(name) > 4 and re.search(r'\b' + re.escape(name) + r'\b', whole):
            return canon
    return ''


def parse_date(s):
    """'Dec 2025' / '2024' / 'Present' -> (year, month) or None for Present/unknown."""
    if not s or re.search(r'present|current|now', s, re.I):
        return None
    m = re.search(r'([A-Za-z]{3})\w*\s+(\d{4})', s)
    if m and m.group(1).lower() in MONTHS:
        return int(m.group(2)), MONTHS[m.group(1).lower()]
    m = re.search(r'(\d{4})', s)
    return (int(m.group(1)), 6) if m else None


def current_role(li):
    exp = li.get('experience') or []
    present = [e for e in exp if parse_date(e.get('endDate')) is None and e.get('endDate') is not None or re.search(r'present', str(e.get('endDate') or ''), re.I)]
    cur = present[0] if present else None
    if not cur and li.get('currentPosition'):
        cp = li['currentPosition'][0]
        cur = {'companyName': cp.get('companyName'), 'title': cp.get('position') or cp.get('title'), 'startDate': None, 'endDate': 'Present'}
    if not cur and exp:
        cur = dict(exp[0], _ended=True)  # most recent role, ended
    return cur


def role_timing(start, course_year):
    if not start:
        return 'unknown'
    cs, ce = (course_year, COURSE_WINDOW['start_month']), (course_year, COURSE_WINDOW['end_month'])
    if start < cs:
        return 'before course'
    if start <= ce:
        return 'during course'
    return 'after course'


def seniority(title, text, open_to_work=False, has_company=True, freelance=False):
    t = title or ''
    blob = f'{t} {text or ""}'
    if STUDENT_RE.search(t) or (not has_company and STUDENT_RE.search(blob)):
        return 'student'
    if (SEEKER_RE.search(t) or (open_to_work and not has_company) or (not has_company and SEEKER_RE.search(blob))):
        return 'job seeker'
    if not t:
        return 'unknown'
    if LEAD_RE.search(t):
        return 'lead+'
    if SENIOR_RE.search(t):
        return 'senior'
    if JUNIOR_RE.search(t):
        return 'junior'
    return 'mid'


def role_family(title, text=''):
    for blob in (title or '', text or ''):
        for fam, rx in ROLE_RULES:
            if rx.search(blob):
                return fam
    return 'other' if title else 'unknown'


def clean_company(c):
    c = re.sub(r'^@+', '', (c or '').strip())
    c = re.sub(r'\s*[,·|].*$', '', c) if len(c) > 40 else c
    c = re.sub(r'\b(inc\.?|ltd\.?|llc|gmbh|s\.?a\.?|b\.?v\.?|plc|pvt\.?|limited|corp\.?|co\.)$', '', c, flags=re.I).strip(' .,-')
    return c


def bio_title_company(bio):
    """'Senior Data Engineer at Acme | ...' -> (title, company)."""
    if not bio:
        return '', ''
    first = re.split(r'[|•\n]', bio)[0].strip()
    m = re.search(r'^(.{3,80}?)\s+(?:at|@)\s+([^,.;|]{2,60})', first, re.I)
    if m:
        return m.group(1).strip(), clean_company(m.group(2))
    if ROLE_RULES and any(rx.search(first) for _, rx in ROLE_RULES) and len(first) < 80:
        return first, ''
    return '', ''


def domain_company(domain):
    if not domain:
        return ''
    base = re.sub(r'^(mail|email|corp|us|uk|de|in)\.', '', domain)
    label = base.split('.')[0]
    return label.capitalize() if len(label) > 2 else base


def name_tokens(s):
    return {t for t in re.split(r'[^a-z]+', norm(s)) if len(t) > 1}


def corroborate(author, cand):
    """Score a name-search candidate. Returns (confidence, reasons)."""
    reasons = []
    prof = author.get('github_profile') or {}
    gh_country = country_of(prof.get('location') or '')
    text = ' '.join(str(cand.get(k) or '') for k in ('headline', 'location', 'title', 'about', 'summary'))
    cand_country = country_of(cand.get('location') or '') or cand.get('country', '')
    if gh_country and cand_country and gh_country == cand_country:
        reasons.append('location country matches GitHub location')
    if re.search(r'data|analytics|bi\b|etl|engineer|scien|ml\b', text, re.I):
        reasons.append('data/engineering headline')
    comp = clean_company(prof.get('company') or '').lower()
    if comp and comp in text.lower():
        reasons.append('company matches GitHub company')
    if author.get('email_domain') and domain_company(author['email_domain']).lower() in text.lower():
        reasons.append('email domain matches')
    if re.search(r'zoomcamp|datatalks', text, re.I):
        reasons.append('mentions DE Zoomcamp/DataTalksClub')
    strong = {'company matches GitHub company', 'email domain matches', 'mentions DE Zoomcamp/DataTalksClub'}
    if strong & set(reasons) or ('location country matches GitHub location' in reasons and 'data/engineering headline' in reasons):
        return 'medium', reasons
    return 'low', reasons


def search_candidates(result):
    """Normalize crawl4ai people-search rows."""
    if not isinstance(result, dict):
        return []
    rows = result.get('data') or result.get('results') or result.get('people') or result.get('output') or []
    if isinstance(rows, dict):
        rows = rows.get('results') or rows.get('people') or rows.get('items') or []
    return [r for r in rows if isinstance(r, dict)] if isinstance(rows, list) else []


def li_data(cache, slug):
    p = cache / f'li-full-{slug}.json'
    if not p.exists():
        return None
    d = json.loads(p.read_text() or 'null')
    if not d:
        return None
    out = d.get('output') or {}
    return out.get('data') if out.get('found') else {}


def linking_fact(a, cand):
    """A fact that ties a LinkedIn profile to this author (not just a same-name person)."""
    certs = ' '.join(c.get('title', '') + ' ' + c.get('issuedBy', '') for c in cand.get('certifications') or [])
    if re.search(r'data engineering zoomcamp', certs, re.I):
        return 'profile lists the Data Engineering Zoomcamp certificate'
    blob = json.dumps({k: cand.get(k) for k in ('about', 'projects', 'experience', 'headline')}).lower()
    if a.get('github') and re.search(r'github\.com/' + re.escape(a['github'].lower()) + r'\b', blob):
        return 'profile links the GitHub account'
    for repo in a.get('repos', []):
        name = repo.split('/', 1)[-1].lower()
        if len(name) > 8 and name in blob:
            return 'profile mentions the submitted project'
    if re.search(r'zoomcamp|datatalks', blob):
        return 'profile mentions DE Zoomcamp/DataTalksClub'
    return ''


def apply_linkedin(row, li, course_year):
    cur = current_role(li) or {}
    row['company'] = clean_company(cur.get('companyName') or '')
    row['title'] = (cur.get('title') or cur.get('position') or '').strip()
    if cur.get('_ended'):
        row['notes'] += f"Latest LinkedIn role ended {cur.get('endDate')}; "
        row['company'], row['title'] = '', ''
    start = parse_date(cur.get('startDate'))
    row['role_start'] = cur.get('startDate') or ''
    row['role_timing'] = role_timing(start, course_year) if row['company'] else 'unknown'
    row['country'] = li.get('country') or country_of(li.get('location') or '')
    certs = [c.get('title', '') for c in li.get('certifications') or []]
    row['dez_certificate'] = 'yes' if any(re.search(r'data engineering zoomcamp', c, re.I) for c in certs) else ''
    headline = li.get('headline') or ''
    emp_type = (cur.get('employmentType') or '').lower()
    m = FREELANCE_RE.search(' '.join([row['company'], row['title'], headline]))
    is_free = emp_type in FREELANCE_TYPES or bool(m)
    if is_free:
        row['freelance'] = 'contract' if emp_type == 'contract' and not m else ('self-employed' if emp_type in ('self-employed', 'self employed') else 'freelance')
    else:
        row['freelance'] = ''
    if is_free:
        row['notes'] += 'Freelance basis: ' + (f'LinkedIn employment type {emp_type}' if emp_type in FREELANCE_TYPES else f'"{m.group(0)}" in title/headline') + '; '
    nm = ' '.join(filter(None, [li.get('firstName'), li.get('lastName')])) or li.get('name')
    if nm:
        row['name'] = nm
    row['seniority'] = seniority(row['title'] or headline, headline + ' ' + (li.get('about') or '')[:300], bool(li.get('openToWork')), bool(row['company']), is_free)
    row['role_family'] = role_family(row['title'], headline)
    if not row['title'] and headline:
        row['title'] = headline[:120]
        row['notes'] += 'Title from LinkedIn headline; '


def classify_author(a, cache, rechecks):
    prof = a.get('github_profile') or {}
    course_year = int(max(a['years']))
    row = {'student_key': f"cmp-{a['student_id']}", 'github': a['github'], 'github_url': f"https://github.com/{a['github']}" if a['github'] else '',
           'years': ';'.join(a['years']), 'name': prof.get('name') or a.get('cmp_display_name') or '',
           'company': '', 'title': '', 'seniority': 'unknown', 'role_family': 'unknown', 'country': '', 'freelance': '',
           'role_timing': 'unknown', 'role_start': '', 'confidence': 'none', 'evidence_type': '', 'source': '', 'source_url': '',
           'linkedin_url': '', 'domain_signal': '', 'dez_certificate': '', 'flag': '', 'notes': ''}
    gh_text = ' '.join(filter(None, [prof.get('bio'), a.get('cmp_about_me')]))
    gh_company = clean_company(prof.get('company') or '')
    bio_title, bio_company = bio_title_company(prof.get('bio') or a.get('cmp_about_me') or '')
    li_slug = (a['self_submitted_linkedin'] or a['github_declared_linkedin'] or [''])[0]
    li = li_data(cache, li_slug) if li_slug else None
    if li_slug:
        row['linkedin_url'] = f'https://www.linkedin.com/in/{li_slug}'
        row['evidence_type'] = 'self_submitted_linkedin' if a['self_submitted_linkedin'] else 'github_declared_linkedin'
        row['source'] = a.get('self_submitted_linkedin_source') or a.get('github_declared_linkedin_source')
    if li:
        apply_linkedin(row, li, course_year)
        row['confidence'] = 'high'
        row['source_url'] = row['linkedin_url']
        if row['evidence_type'] == 'self_submitted_linkedin' and li.get('publicIdentifier') and li['publicIdentifier'].lower() != li_slug.lower():
            row['notes'] += 'LinkedIn id redirected; '
    elif li_slug:
        row['notes'] += 'Confirmed LinkedIn link but profile not readable (private/unavailable); '
    # Public GitHub profile (author's own statement) fills gaps.
    if not row['company'] and (gh_company or bio_company):
        row['company'] = gh_company or bio_company
        row['source'] = row['source'] or 'github_profile'
        row['evidence_type'] = row['evidence_type'] or 'github_profile'
        row['source_url'] = row['source_url'] or row['github_url']
        row['confidence'] = 'high' if row['confidence'] in ('none', 'high') else row['confidence']
    if not row['title'] and bio_title:
        row['title'] = bio_title
    if row['confidence'] != 'high' or not li:
        is_free = bool(FREELANCE_RE.search(' '.join([row['company'], row['title'], gh_text])))
        row['freelance'] = row['freelance'] or ('freelance' if is_free else '')
        if row['seniority'] == 'unknown':
            row['seniority'] = seniority(row['title'], gh_text, bool(prof.get('hireable')) and False, bool(row['company']), is_free)
        if row['role_family'] == 'unknown':
            row['role_family'] = role_family(row['title'], gh_text)
        if row['confidence'] == 'none' and (row['title'] or row['seniority'] in ('student', 'job seeker')):
            row['confidence'] = 'high'
            row['evidence_type'] = row['evidence_type'] or 'github_profile'
            row['source'] = row['source'] or 'github_profile'
            row['source_url'] = row['source_url'] or row['github_url']
    if not row['country']:
        row['country'] = country_of(prof.get('location') or '')
    # Corporate email domain: separate evidence type, company signal only.
    if a.get('email_domain_kind') == 'corporate':
        row['domain_signal'] = a['email_domain']
        if not row['company']:
            row['company'] = domain_company(a['email_domain'])
            row['evidence_type'] = row['evidence_type'] or 'domain_signal'
            row['source'] = row['source'] or 'cmp_email_domain'
            row['confidence'] = 'medium' if row['confidence'] == 'none' else row['confidence']
            row['notes'] += 'Company from corporate email domain only (domain signal); '
    elif a.get('email_domain_kind') == 'academic':
        row['domain_signal'] = 'academic domain'
        if row['seniority'] == 'unknown' and not row['company']:
            row['seniority'] = 'student'
            row['confidence'] = 'medium' if row['confidence'] == 'none' else row['confidence']
            row['evidence_type'] = row['evidence_type'] or 'domain_signal'
            row['notes'] += 'Student inferred from academic email domain; '
    # Name-search candidates (Treg), only when no LinkedIn link was published by the author.
    rc = rechecks.get(a['github'].lower()) if a['github'] else None
    if not li_slug:
        from treg_enrich import candidate_slugs
        slugs = candidate_slugs(cache.parent, a)
        if rc and rc['status'] == 'confirmed' and rc.get('candidate_linkedin'):
            slugs = [rc['candidate_linkedin']]
        picked = None
        for slug in slugs:
            cand = li_data(cache, slug)
            if not cand:
                continue
            link = linking_fact(a, cand)
            if rc and rc['status'] == 'confirmed' and slug == rc.get('candidate_linkedin'):
                link = link or rc['outcome']
            conf, reasons = corroborate(a, {'headline': cand.get('headline'), 'location': cand.get('location'), 'country': cand.get('country'),
                                            'about': cand.get('about')})
            if link:
                picked = (slug, cand, 'high', 'linking fact: ' + link)
                break
            if conf == 'medium' and not picked and row['confidence'] in ('none', 'medium'):
                picked = (slug, cand, 'medium', 'corroborated: ' + ', '.join(reasons))
        if picked:
            slug, cand, conf, why = picked
            keep = {k: row[k] for k in ('company', 'title')} if not (cand.get('experience') or cand.get('currentPosition')) else {}
            apply_linkedin(row, cand, course_year)
            row.update({k: v for k, v in keep.items() if v and not row[k]})
            row.update(linkedin_url=f'https://www.linkedin.com/in/{slug}', source_url=f'https://www.linkedin.com/in/{slug}',
                       evidence_type='name_search_confirmed' if conf == 'high' else 'name_search_corroborated',
                       source='treg:crawl4ai+anyapi', confidence=conf)
            row['notes'] += why + '; '
        elif slugs:
            if row['confidence'] == 'none':
                row['flag'] = 'low-confidence'
                row['confidence'] = 'low'
            row['notes'] += f'{len(slugs)} name-search candidate(s) without a linking fact or corroboration; not used; '
    if rc:
        row['notes'] += 'Re-check: ' + rc['outcome'] + '; '
        if rc['status'] == 'rejected' and row['evidence_type'] == 'name_search_confirmed':
            rc['status'], rc['outcome'] = 'confirmed', 'new linking fact from name search: ' + row['notes']
        elif rc['status'] == 'rejected' and row['confidence'] in ('none', 'low', 'medium') and row['evidence_type'] in ('', 'name_search_corroborated'):
            row['flag'] = 'rejected'
            row['confidence'] = 'rejected'
    if row['confidence'] in ('low',):
        row['flag'] = row['flag'] or 'low-confidence'
    row['enriched'] = 'yes' if row['confidence'] in ('high', 'medium') and (row['company'] or row['title'] or row['seniority'] != 'unknown') else ''
    return row


FIELDS = ['student_key', 'github', 'github_url', 'years', 'name', 'company', 'title', 'seniority', 'role_family', 'freelance', 'country',
          'role_timing', 'role_start', 'confidence', 'enriched', 'flag', 'evidence_type', 'source', 'source_url', 'linkedin_url',
          'domain_signal', 'dez_certificate', 'notes']


def classify_all(output):
    cache = output / 'cache'
    authors = json.loads((cache / 'authors.json').read_text())
    rp = output / 'rechecks.json'
    rechecks = {k.lower(): v for k, v in json.loads(rp.read_text()).items()} if rp.exists() else {}
    rows = [classify_author(a, cache, rechecks) for a in authors]
    for r in rows:
        r['notes'] = r['notes'].strip('; ')
        assert '@' not in r['domain_signal'] and not re.search(r'[\w.+-]+@[\w-]+\.[\w.]+', ' '.join(map(str, r.values()))), 'email leaked'
    with (output / 'enrichment-all.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    return {'authors': len(rows), 'enriched': sum(r['enriched'] == 'yes' for r in rows),
            'confidence': dict(Counter(r['confidence'] for r in rows)), 'flagged': sum(bool(r['flag']) for r in rows),
            'evidence': dict(Counter(r['evidence_type'] for r in rows))}
