#!/usr/bin/env python3
"""Aggregate enrichment-all.csv and warehouses.csv into sponsor-safe summaries.

audience-summary.md never includes tool-usage counts from the scan (pass --hide-labels for
anything else that must stay out). Only rows with confidence high/medium and no flag count.
"""
from collections import Counter
import csv
import json
import re

BIG_BRANDS = re.compile(r'^(google|alphabet|amazon|aws|microsoft|meta|facebook|apple|netflix|airbnb|uber|lyft|ibm|oracle|sap|accenture|deloitte|pwc|ey|ernst & young|kpmg|capgemini|infosys|tcs|tata consultancy services|wipro|cognizant|hcl\w*|jpmorgan\w*|jp morgan\w*|goldman sachs|morgan stanley|citi\w*|hsbc|barclays|santander|bbva|ing|deutsche bank|allianz|axa|siemens\w*|bosch|bmw\w*|mercedes\w*|volkswagen\w*|shell|bp|unilever|nestl\w+|procter & gamble|walmart\w*|target|spotify|booking\.com|zalando|shopify|salesforce|databricks|snowflake|nvidia|intel|cisco|dell\w*|hp|hewlett\w*|samsung\w*|vodafone\w*|orange|telef[oó]nica|ericsson|nokia|philips|mckinsey\w*|boston consulting group|bcg|bain\w*|thoughtworks|epam\w*|globant|mercado ?libre|rappi|nubank|revolut|wise|stripe|paypal|visa|mastercard|american express|capital one|wells fargo|bank of america|pfizer|novartis|roche|astrazeneca|gsk|johnson & johnson|bayer|merck\w*|toyota\w*|sony|huawei|alibaba\w*|tencent|bytedance|tiktok|grab|gojek|shopee|careem|jumia|andela|safaricom|mtn\w*|flutterwave|paystack|atlassian|canva|adobe|twilio|datadog|elastic|red hat|vmware|lufthansa\w*|dhl\w*|maersk|heineken|coca-cola\w*|pepsico|l.or[eé]al|danone|amadeus|expedia\w*|wayfair|ebay|etsy|delivery hero|hellofresh|n26|klarna|adyen|abn amro|rabobank|lloyds\w*|natwest\w*|bnp paribas|soci[eé]t[eé] g[eé]n[eé]rale|ubs|zurich\w*|swiss re|munich re|generali|nhs\w*|bloomberg|reuters|thomson reuters|the economist group|bbc|linkedin|github|gitlab|intuit|ford\w*|general motors|gm|airbus|boeing|ge\b.*|general electric|honeywell|3m|nike|adidas|ikea|h&m|lidl|aldi|tesco|sainsbury\w*|carrefour|ahold\w*|mondelez|kraft\w*|anz|commonwealth bank|nab|westpac|rbc|td\b.*|scotiabank|bmo|cibc|standard chartered|emirates\w*|qatar airways|saudi aramco|aramco|petrobras|itaú\w*|itau\w*|bradesco|ambev|natura|stone|vtex|ifood|totvs|globo|ola|flipkart|swiggy|zomato|paytm|reliance\w*|airtel|jio|razorpay|phonepe|myntra|ola electric|lazada|sea|agoda|traveloka|tokopedia|bukalapak|kaspi|yandex|epam|luxoft|endava|n-ix|softserve|ciklum|grid dynamics)$', re.I)
ALIASES = {'amazon web services': 'amazon', 'amazon web services (aws)': 'amazon', 'aws': 'amazon', 'google cloud': 'google', 'meta platforms': 'meta',
           'microsoft corporation': 'microsoft', 'ibm consulting': 'ibm', 'accenture song': 'accenture', 'deloitte consulting': 'deloitte',
           'tata consultancy services': 'tcs', 'jpmorgan chase & co': 'jpmorgan chase', 'jpmorganchase': 'jpmorgan chase', 'j.p. morgan': 'jpmorgan chase',
           'ey gds': 'ey', 'ernst & young': 'ey', 'pwc acceleration centers': 'pwc', 'capgemini engineering': 'capgemini', 'capgemini invent': 'capgemini'}
NOT_COMPANY = re.compile(r'^(self[- ]employed|freelanc\w*|independent|none|n/?a|-|unemployed|student|open to work|looking for.*|myself|personal|home|retired|confidential|stealth.*|various)$', re.I)


def pct(n, d):
    return f'{(100 * n / d):.0f}%' if d else '-'


def table(headers, rows):
    def c(x):
        return str(x).replace('|', '/').replace('\n', ' ')
    return '\n'.join(['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |'] + ['| ' + ' | '.join(map(c, r)) + ' |' for r in rows])


SUFFIX_WORDS = {'systems', 'group', 'technologies', 'technology', 'consulting', 'digital', 'india', 'us', 'usa', 'uk', 'se', 'ag', 'gmbh',
                'inc', 'ltd', 'llc', 'plc', 'corporation', 'company', 'services', 'solutions', 'global', 'international', 'labs', 'ai', 'jsc', 'sa'}


def company_key(c):
    k = re.sub(r'\s+', ' ', (c or '').strip().lower())
    k = re.split(r'\s+(?:via|through|for|@|\(|-|–|\|)\s*', k)[0].strip(' .,')
    k = ALIASES.get(k, k)
    words = k.split()
    while len(words) > 1 and words[-1].strip('.,') in SUFFIX_WORDS:
        words = words[:-1]
    k = ' '.join(words)
    return ALIASES.get(k, k)


def load(output):
    rows = list(csv.DictReader((output / 'enrichment-all.csv').open()))
    return rows, [r for r in rows if r['enriched'] == 'yes' and not r['flag']]


def homework_counts(output):
    out = {}
    for p in sorted((output / 'cache').glob('homework-*.json')):
        _, year, slug = p.stem.split('-', 2)
        out.setdefault(year, {})[slug] = len({r['student_id'] for r in json.loads(p.read_text())['submissions']})
    return out


def warehouse_summary(output):
    rows = list(csv.DictReader((output / 'warehouses.csv').open()))
    years = sorted({r['year'] for r in rows})
    counts = {y: Counter(t for r in rows if r['year'] == y for t in r['warehouses'].split(';')) for y in years}
    labels = sorted({t for c in counts.values() for t in c} - {'none', 'unknown'}, key=lambda t: -sum(c[t] for c in counts.values()))
    scanned = {y: sum(r['year'] == y and r['status'] == 'scanned' for r in rows) for y in years}
    total = {y: sum(r['year'] == y for r in rows) for y in years}
    hw = homework_counts(output)
    fp = {}
    for p in (output / 'cache').glob('submissions-*.json'):
        fp.setdefault(p.stem.split('-')[1], set()).update(r['student_id'] for r in json.loads(p.read_text())['submissions'])
    md = ['# Final-project data warehouse usage', '',
          'Static scan of the submitted commit of every distinct final-project repository (all three attempts), same method as the orchestrator audit. '
          'A label means executable code/config/dependency evidence (imports, dbt profile `type:`, Terraform resources, connection URIs, dlt destinations, operators). '
          'README/markdown mentions do not count. Labels overlap: one project can use several warehouses.', '',
          table(['Warehouse'] + years, [[t] + [f"{counts[y][t]} ({pct(counts[y][t], scanned[y])})" for y in years] for t in labels]
                + [['none detected'] + [counts[y]['none'] for y in years], ['unknown (not scannable)'] + [counts[y]['unknown'] for y in years],
                   ['repositories (scanned)'] + [f'{total[y]} ({scanned[y]})' for y in years]]), '',
          'Percentages are of scanned repositories. Postgres is high because module 1 teaches a local Postgres ingestion stack, and many projects keep it as a staging/source database; BigQuery is the course warehouse in module 3.', '',
          '## Module 3 (Data Warehousing) homework', '',
          table(['Year', 'HW3 unique submitters', 'HW1 unique submitters', 'Final-project unique submitters'],
                [[y, hw.get(y, {}).get('hw3', '-'), hw.get(y, {}).get('hw1', '-'), len(fp.get(y, ())) or '-'] for y in years]), '']
    return md, counts, hw


def aggregate(output, hide_labels=()):
    rows, good = load(output)
    n, g = len(rows), len(good)
    conf = Counter(r['confidence'] for r in rows)
    flagged = [r for r in rows if r['flag']]
    sen = Counter(r['seniority'] for r in good)
    known_sen = sum(v for k, v in sen.items() if k != 'unknown')
    fam = Counter(r['role_family'] for r in good)
    known_fam = sum(v for k, v in fam.items() if k != 'unknown')
    ctry = Counter(r['country'] for r in good if r['country'])
    known_ctry = sum(ctry.values())
    free = [r for r in good if r['freelance']]
    free_kind = Counter(r['freelance'] for r in free)
    comp = Counter()
    disp = {}
    for r in good:
        if r['company'] and not NOT_COMPANY.match(r['company'].strip()) and r['freelance'] not in ('freelance', 'self-employed'):
            k = company_key(r['company'])
            comp[k] += 1
            disp.setdefault(k, re.split(r'\s+(?:via|through)\s+', r['company'])[0])
    brands = sorted([(disp[k], v) for k, v in comp.items() if BIG_BRANDS.match(k) or BIG_BRANDS.match(disp[k])], key=lambda x: (-x[1], x[0].lower()))
    multi = sorted([(disp[k], v) for k, v in comp.items() if v >= 2], key=lambda x: (-x[1], x[0].lower()))
    timing = Counter(r['role_timing'] for r in good if r['role_timing'] != 'unknown')
    ev = Counter(r['evidence_type'] or 'none' for r in rows)
    by_year = {y: sum(y in r['years'].split(';') for r in rows) for y in sorted({y for r in rows for y in r['years'].split(';')})}
    sj = sen['student'] + sen['job seeker']
    md = ['# DE Zoomcamp final-project authors: audience profile', '',
          f'Snapshot 2026-11-10. Population: every distinct final-project submitter (CMP student id) in the 2025 and 2026 cohorts: '
          f"{n} people ({', '.join(f'{k}: {v}' for k, v in by_year.items())}; people in both cohorts are counted once). "
          'Identities come from data the authors published themselves first (LinkedIn links they submitted in CMP, their own GitHub profile, '
          'their personal site), then paid lookups by that LinkedIn URL, then corroborated name matches. Unconfirmed or rejected matches are excluded.', '',
          '## Coverage', '',
          table(['Measure', 'Authors', 'Share'], [
              ['Total authors', n, '100%'], ['Enriched (used in aggregates)', g, pct(g, n)],
              ['High confidence (self-declared/self-submitted)', conf['high'], pct(conf['high'], n)],
              ['Medium confidence (corroborated match or company domain only)', conf['medium'], pct(conf['medium'], n)],
              ['Flagged (low-confidence or rejected, excluded)', len(flagged), pct(len(flagged), n)],
              ['No usable public data', conf['none'], pct(conf['none'], n)]]), '',
          table(['Evidence type (strongest per author)', 'Authors'], sorted(ev.items(), key=lambda x: -x[1])), '',
          '## Seniority', '', f'Share of the {known_sen} enriched authors with a known seniority.', '',
          table(['Seniority', 'Authors', 'Share'], [[k, sen[k], pct(sen[k], known_sen)] for k in ['student', 'job seeker', 'junior', 'mid', 'senior', 'lead+']]), '',
          f'Students and job seekers together: {sj} of {known_sen} ({pct(sj, known_sen)}). Everyone else is employed or self-employed.', '',
          '## Freelancers, contractors and consultants', '',
          f'{len(free)} enriched authors ({pct(len(free), g)} of enriched) work as freelancers, contractors, independent consultants or are self-employed. '
          'They are a separate segment: they act as the technical lead for their clients and choose the platform the client adopts.', '',
          table(['Type (LinkedIn employment type or title)', 'Authors'], [[k, free_kind[k]] for k in ['freelance', 'self-employed', 'contract']]), '',
          '`contract` means a fixed-term contract role at a client company; `freelance` and `self-employed` are independent.', '']
    if free:
        notable = [r for r in free if r['freelance'] in ('freelance', 'self-employed') and r['role_family'] in ('DE', 'analytics eng', 'DS/ML', 'DA', 'SWE')]
        md += ['Notable independent (freelance / self-employed) data practitioners:', '',
               table(['Author', 'Type', 'Title / positioning', 'Country'],
                     [[f"[{r['name'] or r['github']}]({r['github_url']})", r['freelance'], (r['title'] or r['company'])[:90], r['country']]
                      for r in sorted(notable, key=lambda r: (r['seniority'] not in ('lead+', 'senior'), r['name'].lower()))[:40]]), '']
    md += ['## Role family', '', f'Share of the {known_fam} enriched authors with a known role.', '',
           table(['Role family', 'Authors', 'Share'], [[k, fam[k], pct(fam[k], known_fam)] for k in ['DE', 'analytics eng', 'DA', 'DS/ML', 'SWE', 'other']]), '',
           '## Country', '', f'Top countries among {known_ctry} enriched authors with a known location (LinkedIn country, else GitHub location).', '',
           table(['Country', 'Authors', 'Share'], [[k, v, pct(v, known_ctry)] for k, v in ctry.most_common(20)]), '',
           f'{len(ctry)} countries in total.', '',
           '## Notable companies', '', 'Current employers that are well-known brands (author count per company):', '',
           table(['Company', 'Authors'], brands) if brands else '_none_', '',
           'All employers with two or more authors:', '', table(['Company', 'Authors'], multi) if multi else '_none_', '',
           '## Current role vs course timing', '',
           'For authors whose LinkedIn role has a start date: started before the cohort (Jan), during it (Jan to Apr), or after it.', '',
           table(['Timing', 'Authors'], [[k, timing[k]] for k in ['before course', 'during course', 'after course']]), '',
           'Roles started after the course are post-course jobs (for example a first data role after finishing the project).', '',
           '## Method', '',
           '- Population: CMP final-project exports (all attempts); one author per CMP student id; GitHub handle = owner of the submitted repo.',
           '- Evidence order: self-submitted LinkedIn in CMP (learning-in-public posts and opt-in public profile) > LinkedIn on the author\'s own GitHub profile or personal site > self-declared GitHub company/bio > corporate email domain (company only, labelled domain signal) > name-search candidate with corroboration.',
           '- Seniority, role family and freelance status are rule-based on title/headline; freelance includes self-employed, contract and independent consultant roles.',
           '- No emails are stored or shown; the per-author CSV uses GitHub handles and CMP ids.', '']
    text = '\n'.join(md) + '\n'
    for label in hide_labels:
        # Tool usage counts for hidden labels must never appear (a person's job title may mention the tool).
        bad = re.search(r'\|\s*' + re.escape(label) + r'[^|\n]*\|\s*\d|' + re.escape(label) + r'\W{0,3}\d+\s*(?:projects?|repos|repositories|%)', text, re.I)
        assert not bad, f'{label} usage numbers must not appear in audience summary'
    (output / 'audience-summary.md').write_text(text)
    wmd, counts, hw = warehouse_summary(output)
    (output / 'warehouses-summary.md').write_text('\n'.join(wmd) + '\n')
    stats = {'authors': n, 'enriched': g, 'confidence': dict(conf), 'flagged': len(flagged), 'seniority': dict(sen), 'freelance': len(free),
             'role_family': dict(fam), 'countries_top': ctry.most_common(15), 'brands': brands, 'multi': multi[:30], 'timing': dict(timing),
             'evidence': dict(ev), 'warehouses': {y: dict(c) for y, c in counts.items()}, 'homeworks': hw}
    (output / 'audience-stats.json').write_text(json.dumps(stats, indent=1))
    return json.dumps(stats, indent=1)
