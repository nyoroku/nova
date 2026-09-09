import re
import ssl
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from urllib.parse import urlparse

URL = "https://www.rafikiboatridesnaivasha.com/sitemap.xml"
request = urllib.request.Request(
    URL, headers={"User-Agent": "Mozilla/5.0 (compatible; RafikiTechnicalAudit/1.0)"}
)
with urllib.request.urlopen(request, timeout=40, context=ssl.create_default_context()) as response:
    body = response.read()

root = ET.fromstring(body)
ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
rows = []
for item in root.findall("sm:url", ns):
    rows.append(
        (
            item.findtext("sm:loc", default="", namespaces=ns),
            item.findtext("sm:lastmod", default="", namespaces=ns),
            item.findtext("sm:priority", default="", namespaces=ns),
        )
    )

urls = [row[0] for row in rows]
paths = [urlparse(url).path for url in urls]
families = Counter()
for path in paths:
    if path == "/":
        families["homepage"] += 1
    elif path == "/faq/":
        families["faq_hub"] += 1
    elif path.startswith("/faq/"):
        families["faq_detail"] += 1
    elif path == "/blog/":
        families["blog_hub"] += 1
    elif path.startswith("/blog/"):
        families["blog_detail"] += 1
    elif path == "/tours/":
        families["tours_hub"] += 1
    elif path.startswith("/tours/"):
        families["tour_detail"] += 1
    elif path == "/destinations/":
        families["destinations_hub"] += 1
    elif path.startswith("/best-boat-rides-naivasha-near-"):
        families["location_best_boat_rides"] += 1
    elif path.startswith("/hippo-boat-safari-lake-naivasha-near-"):
        families["location_hippo_safari"] += 1
    elif path.startswith("/crescent-island-boat-ride-and-walking-safari-near-"):
        families["location_crescent_island"] += 1
    elif "-near-" in path:
        families["other_location_variant"] += 1
    else:
        families["other_core"] += 1

generated = sum(
    bool(re.search(r"(?:volume|edition|ref)-?\d+", path, re.I)) for path in paths
)
long_120 = sum(len(path) > 120 for path in paths)
long_160 = sum(len(path) > 160 for path in paths)
lastmods = Counter(row[1] or "(missing)" for row in rows)
priorities = Counter(row[2] or "(missing)" for row in rows)

print(f"sitemap_bytes={len(body)}")
print(f"url_count={len(urls)}")
print(f"duplicate_exact_urls={len(urls)-len(set(urls))}")
print(f"generated_ref_edition_volume={generated}")
print(f"path_over_120_chars={long_120}")
print(f"path_over_160_chars={long_160}")
print("families=" + repr(dict(families)))
print("lastmods=" + repr(dict(lastmods)))
print("priorities=" + repr(dict(priorities)))
