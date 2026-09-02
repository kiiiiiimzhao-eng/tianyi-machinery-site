import re, json, io
from pathlib import Path

base = Path('E:/赵雯/独立站/Kim网站/tianyi-site')

ORG_JSON = '''{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Hubei Tianyi Machinery Co., Ltd.",
  "legalName": "Hubei Tianyi Machinery Co., Ltd.",
  "url": "https://www.tianyimachine.com/",
  "logo": "https://www.tianyimachine.com/images/logo-200.png",
  "description": "Professional manufacturer of bulk material handling equipment including belt conveyors, chain conveyors, bucket elevators, screw conveyors, apron conveyors and dust collectors.",
  "foundingDate": "2007",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "No. 25, Wangcheng Road",
    "addressLocality": "Yidu City, Yichang City",
    "addressRegion": "Hubei Province",
    "addressCountry": "CN"
  },
  "contactPoint": [
    {
      "@type": "ContactPoint",
      "telephone": "+86-13872451240",
      "contactType": "sales",
      "email": "kim@tianyi-machinery.com",
      "availableLanguage": ["English", "Chinese"]
    }
  ],
  "numberOfEmployees": "201-500"
}'''

ORG_BLOCK = '<script type="application/ld+json">\n' + ORG_JSON + '\n</script>\n'

def has_org_schema(raw):
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S):
        try:
            data = json.loads(b)
        except Exception:
            continue
        if isinstance(data, dict) and data.get('@type') == 'Organization':
            return True
        # handle @graph
        if isinstance(data, dict) and isinstance(data.get('@graph'), list):
            if any(isinstance(n, dict) and n.get('@type') == 'Organization' for n in data['@graph']):
                return True
    return False

skipped_dirs = {'.workbuddy', 'audit', 'screenshots'}
pages = []
for p in base.rglob('*.html'):
    if any(part in skipped_dirs for part in p.parts):
        continue
    pages.append(p)

injected = 0
skipped = 0
errors = []
for p in pages:
    try:
        raw = p.read_text(encoding='utf-8')
    except Exception as e:
        errors.append(f"{p}: read error {e}")
        continue
    if has_org_schema(raw):
        skipped += 1
        continue
    if '</head>' not in raw:
        errors.append(f"{p}: no </head>")
        continue
    # inject before </head>
    new_raw = raw.replace('</head>', ORG_BLOCK + '</head>', 1)
    try:
        p.write_text(new_raw, encoding='utf-8')
        injected += 1
    except Exception as e:
        errors.append(f"{p}: write error {e}")

out = io.StringIO()
out.write(f"Total HTML pages scanned (excl .workbuddy/audit): {len(pages)}\n")
out.write(f"Injected Organization schema: {injected}\n")
out.write(f"Already had Organization (skipped): {skipped}\n")
out.write(f"Errors: {len(errors)}\n")
for e in errors:
    out.write(f"  {e}\n")

Path('E:/赵雯/独立站/Kim网站/tianyi-site/.workbuddy/_org_inject.txt').write_text(out.getvalue(), encoding='utf-8')
print("DONE")
