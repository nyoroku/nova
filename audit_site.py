import json
import re
import ssl
import statistics
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

BASE = "https://www.rafikiboatridesnaivasha.com/"
UA = "Mozilla/5.0 (compatible; RafikiTechnicalAudit/1.0)"
CTX = ssl.create_default_context()


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(request, timeout=40, context=CTX) as response:
            body = response.read()
            charset = response.headers.get_content_charset() or "utf-8"
            return response.status, response.geturl(), response.headers, body.decode(charset, "replace")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        return exc.code, exc.geturl(), exc.headers, body
    except Exception as exc:
        return 0, url, {}, f"ERROR: {exc}"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.in_h1 = False
        self.in_script = False
        self.script_type = ""
        self.title_parts = []
        self.h1_parts = []
        self.h1s = []
        self.metas = []
        self.links = []
        self.scripts = []
        self.current_script = []
        self.html_lang = ""
        self.text_parts = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        tag = tag.lower()
        if tag == "html":
            self.html_lang = attrs.get("lang", "")
        elif tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.in_h1 = True
            self.h1_parts = []
        elif tag == "meta":
            self.metas.append(attrs)
        elif tag == "link":
            self.links.append(attrs)
        elif tag == "script":
            self.in_script = True
            self.script_type = attrs.get("type", "")
            self.current_script = []
            self.skip_depth += 1
        elif tag in {"style", "noscript", "svg"}:
            self.skip_depth += 1

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
        elif tag == "h1":
            self.in_h1 = False
            self.h1s.append(" ".join("".join(self.h1_parts).split()))
        elif tag == "script":
            if self.script_type.lower() == "application/ld+json":
                self.scripts.append("".join(self.current_script))
            self.in_script = False
            self.script_type = ""
            self.current_script = []
            self.skip_depth = max(0, self.skip_depth - 1)
        elif tag in {"style", "noscript", "svg"}:
            self.skip_depth = max(0, self.skip_depth - 1)

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)
        if self.in_h1:
            self.h1_parts.append(data)
        if self.in_script:
            self.current_script.append(data)
        elif self.skip_depth == 0:
            text = " ".join(data.split())
            if text:
                self.text_parts.append(text)


def jsonld_types(values):
    result = []

    def visit(value):
        if isinstance(value, dict):
            type_value = value.get("@type")
            if isinstance(type_value, list):
                result.extend(str(v) for v in type_value)
            elif type_value:
                result.append(str(type_value))
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    for raw in values:
        try:
            visit(json.loads(raw))
        except Exception:
            result.append("INVALID_JSON_LD")
    return sorted(set(result))


def meta_values(parser, key, value):
    return [
        item.get("content", "").strip()
        for item in parser.metas
        if item.get(key, "").lower() == value.lower()
    ]


def link_values(parser, rel):
    return [
        item
        for item in parser.links
        if rel.lower() in item.get("rel", "").lower().split()
    ]


def analyze_page(url):
    status, final_url, headers, html = fetch(url)
    parser = PageParser()
    if status == 200:
        parser.feed(html)
    title = " ".join("".join(parser.title_parts).split())
    descriptions = meta_values(parser, "name", "description")
    robots = meta_values(parser, "name", "robots")
    canonical_links = link_values(parser, "canonical")
    alternates = [
        item for item in link_values(parser, "alternate") if item.get("hreflang")
    ]
    anchors = re.findall(r"<a\b[^>]*\bhref=[\"']([^\"']+)", html, flags=re.I)
    internal = {
        urljoin(final_url, href).split("#")[0]
        for href in anchors
        if href and not href.startswith(("mailto:", "tel:", "javascript:", "#"))
        and urlparse(urljoin(final_url, href)).netloc
        == urlparse(BASE).netloc
    }
    words = re.findall(r"\b[\w'-]+\b", " ".join(parser.text_parts))
    return {
        "url": url,
        "status": status,
        "final_url": final_url,
        "bytes": len(html.encode("utf-8", "replace")),
        "title": title,
        "title_len": len(title),
        "descriptions": descriptions,
        "description_len": len(descriptions[0]) if descriptions else 0,
        "robots": robots,
        "canonical": [item.get("href", "") for item in canonical_links],
        "html_lang": parser.html_lang,
        "hreflang": [(item.get("hreflang"), item.get("href")) for item in alternates],
        "h1_count": len([h for h in parser.h1s if h]),
        "h1s": parser.h1s,
        "jsonld_types": jsonld_types(parser.scripts),
        "jsonld_blocks": len(parser.scripts),
        "word_count": len(words),
        "internal_links_unique": len(internal),
        "content_type": headers.get("Content-Type", "") if headers else "",
    }


def main():
    robots_status, _, _, robots_body = fetch(urljoin(BASE, "robots.txt"))
    sm_status, _, _, sitemap_text = fetch(urljoin(BASE, "sitemap.xml"))
    root = ET.fromstring(sitemap_text)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    entries = []
    for item in root.findall("sm:url", ns):
        loc = item.findtext("sm:loc", default="", namespaces=ns)
        lastmod = item.findtext("sm:lastmod", default="", namespaces=ns)
        priority = item.findtext("sm:priority", default="", namespaces=ns)
        entries.append((loc, lastmod, priority))
    urls = [row[0] for row in entries]

    path_groups = Counter()
    for url in urls:
        parts = [p for p in urlparse(url).path.split("/") if p]
        path_groups[parts[0] if parts else "(root)"] += 1

    suspicious_re = re.compile(r"(?:volume|edition|ref)-?\d+", re.I)
    suspicious = [url for url in urls if suspicious_re.search(url)]
    long_slugs = [url for url in urls if len(urlparse(url).path) > 160]
    lastmods = Counter(row[1] or "(missing)" for row in entries)
    priorities = Counter(row[2] or "(missing)" for row in entries)

    print("SITEWIDE")
    print(json.dumps({
        "robots_status": robots_status,
        "robots_body_preview": robots_body[:300],
        "sitemap_status": sm_status,
        "sitemap_bytes": len(sitemap_text.encode("utf-8")),
        "sitemap_url_count": len(urls),
        "path_groups": path_groups,
        "suspicious_generated_slug_count": len(suspicious),
        "path_over_160_chars_count": len(long_slugs),
        "lastmod_top": lastmods.most_common(8),
        "priority_counts": priorities,
        "duplicate_exact_urls": len(urls) - len(set(urls)),
    }, indent=2, default=list))

    candidates = [
        BASE,
        urljoin(BASE, "faq/"),
        urljoin(BASE, "tours/"),
        urljoin(BASE, "destinations/"),
        urljoin(BASE, "blog/boat-rides-naivasha-complete-guide/"),
        urljoin(BASE, "blog/lake-naivasha-boat-safari-guide-for-international-visitors/"),
    ]
    candidates.extend(suspicious[:4])
    candidates.extend(long_slugs[:2])
    seen = set()
    sample_urls = [u for u in candidates if u and not (u in seen or seen.add(u))]
    print("\nPAGE SAMPLE")
    reports = []
    for url in sample_urls:
        report = analyze_page(url)
        reports.append(report)
        print(json.dumps(report, ensure_ascii=False, indent=2))

    title_counts = Counter(r["title"] for r in reports if r["title"])
    desc_counts = Counter(
        r["descriptions"][0] for r in reports if r["descriptions"]
    )
    print("\nSAMPLE DUPLICATION")
    print(json.dumps({
        "duplicate_titles": [item for item in title_counts.items() if item[1] > 1],
        "duplicate_descriptions": [item for item in desc_counts.items() if item[1] > 1],
        "status_counts": Counter(r["status"] for r in reports),
        "jsonld_type_counts": Counter(t for r in reports for t in r["jsonld_types"]),
        "median_word_count": statistics.median(r["word_count"] for r in reports if r["status"] == 200),
    }, indent=2, default=list))

    print("\nSUSPICIOUS URL EXAMPLES")
    for url in suspicious[:10]:
        print(url)

    print("\nLONG URL EXAMPLES")
    for url in long_slugs[:10]:
        print(url)


if __name__ == "__main__":
    main()
