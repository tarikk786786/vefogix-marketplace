"""
Vefogix Marketplace - Local Backend Server
Serves the Vefogix guest post & link building marketplace UI and handles REST APIs.
"""

import json
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import sys

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"

# Curated High-Authority Websites Database mirroring Vefogix Marketplace
WEBSITES_DATABASE = [
    {
        "id": "w-1",
        "domain": "manilatimes.net",
        "sample_url": "https://www.manilatimes.net/2026/10/16/tmt-newswire/plentisoft/eutrain-expands-european-rail-travel-content-to-support-international-trip-planning/2446942",
        "price": 23,
        "currency": "USD",
        "category": "News and Media",
        "categories": ["News and Media", "Business", "General"],
        "traffic_semrush": "714K",
        "traffic_ahrefs": "100.7K",
        "traffic_num": 714000,
        "dr": 80,
        "da": 73,
        "as_score": 56,
        "max_links": 2,
        "link_type": "DoFollow",
        "turnaround": "3 Days",
        "country": "Philippines",
        "country_extra": "+3 Others",
        "followed_backlinks": "694.5K",
        "nofollow_backlinks": "215.8K",
        "added_age": "1Y 2M",
        "domain_age": "28Y 9M",
        "deals_completed": 85
    },
    {
        "id": "w-2",
        "domain": "finance.yahoo.com",
        "sample_url": "https://finance.yahoo.com/small-business/articles/granite-pm-academy-announces-nationwide-133000836.html",
        "price": 71,
        "currency": "USD",
        "category": "News and Media",
        "categories": ["News and Media", "Finance", "Business"],
        "traffic_semrush": "120.8M",
        "traffic_ahrefs": "75.9M",
        "traffic_num": 120800000,
        "dr": 94,
        "da": 93,
        "as_score": 100,
        "max_links": 2,
        "link_type": "NoFollow",
        "turnaround": "3 Days",
        "country": "United States",
        "country_extra": "+4 Others",
        "followed_backlinks": "14.2M",
        "nofollow_backlinks": "5.1M",
        "added_age": "2Y 1M",
        "domain_age": "30Y 2M",
        "deals_completed": 142
    },
    {
        "id": "w-3",
        "domain": "businessinsider.com",
        "sample_url": "https://www.businessinsider.com/reviews/lifestyle",
        "price": 145,
        "currency": "USD",
        "category": "Business",
        "categories": ["Business", "Technology", "Finance"],
        "traffic_semrush": "45.2M",
        "traffic_ahrefs": "38.6M",
        "traffic_num": 45200000,
        "dr": 92,
        "da": 91,
        "as_score": 95,
        "max_links": 2,
        "link_type": "DoFollow",
        "turnaround": "4 Days",
        "country": "United States",
        "country_extra": "+5 Others",
        "followed_backlinks": "8.9M",
        "nofollow_backlinks": "2.4M",
        "added_age": "1Y 8M",
        "domain_age": "18Y 6M",
        "deals_completed": 110
    },
    {
        "id": "w-4",
        "domain": "digitaljournal.com",
        "sample_url": "https://www.digitaljournal.com/pr/news",
        "price": 35,
        "currency": "USD",
        "category": "News and Media",
        "categories": ["News and Media", "Technology", "General"],
        "traffic_semrush": "1.2M",
        "traffic_ahrefs": "650K",
        "traffic_num": 1200000,
        "dr": 83,
        "da": 79,
        "as_score": 68,
        "max_links": 3,
        "link_type": "DoFollow",
        "turnaround": "2 Days",
        "country": "Canada",
        "country_extra": "+2 Others",
        "followed_backlinks": "980K",
        "nofollow_backlinks": "320K",
        "added_age": "8M",
        "domain_age": "24Y 1M",
        "deals_completed": 95
    },
    {
        "id": "w-5",
        "domain": "techcrunch.com",
        "sample_url": "https://techcrunch.com/startups",
        "price": 280,
        "currency": "USD",
        "category": "Technology",
        "categories": ["Technology", "Startups", "AI & Software"],
        "traffic_semrush": "18.5M",
        "traffic_ahrefs": "12.3M",
        "traffic_num": 18500000,
        "dr": 93,
        "da": 92,
        "as_score": 94,
        "max_links": 1,
        "link_type": "DoFollow",
        "turnaround": "5 Days",
        "country": "United States",
        "country_extra": "Global",
        "followed_backlinks": "5.6M",
        "nofollow_backlinks": "1.8M",
        "added_age": "2Y 4M",
        "domain_age": "20Y 5M",
        "deals_completed": 64
    },
    {
        "id": "w-6",
        "domain": "apnews.com",
        "sample_url": "https://apnews.com/press-releases",
        "price": 89,
        "currency": "USD",
        "category": "News and Media",
        "categories": ["News and Media", "Global", "Press Release"],
        "traffic_semrush": "65.4M",
        "traffic_ahrefs": "42.1M",
        "traffic_num": 65400000,
        "dr": 91,
        "da": 90,
        "as_score": 96,
        "max_links": 2,
        "link_type": "NoFollow",
        "turnaround": "2 Days",
        "country": "United States",
        "country_extra": "Global",
        "followed_backlinks": "12.1M",
        "nofollow_backlinks": "3.8M",
        "added_age": "1Y 11M",
        "domain_age": "29Y 8M",
        "deals_completed": 128
    },
    {
        "id": "w-7",
        "domain": "venturebeat.com",
        "sample_url": "https://venturebeat.com/ai",
        "price": 195,
        "currency": "USD",
        "category": "Technology",
        "categories": ["Technology", "AI & Machine Learning", "Business"],
        "traffic_semrush": "8.9M",
        "traffic_ahrefs": "5.4M",
        "traffic_num": 8900000,
        "dr": 89,
        "da": 88,
        "as_score": 82,
        "max_links": 2,
        "link_type": "DoFollow",
        "turnaround": "4 Days",
        "country": "United States",
        "country_extra": "+3 Others",
        "followed_backlinks": "3.4M",
        "nofollow_backlinks": "1.1M",
        "added_age": "1Y 3M",
        "domain_age": "19Y 2M",
        "deals_completed": 76
    },
    {
        "id": "w-8",
        "domain": "globenewswire.com",
        "sample_url": "https://www.globenewswire.com/news-release",
        "price": 65,
        "currency": "USD",
        "category": "Press Release",
        "categories": ["Press Release", "Business", "News and Media"],
        "traffic_semrush": "14.2M",
        "traffic_ahrefs": "9.8M",
        "traffic_num": 14200000,
        "dr": 88,
        "da": 85,
        "as_score": 80,
        "max_links": 3,
        "link_type": "DoFollow",
        "turnaround": "1 Day",
        "country": "United States",
        "country_extra": "+6 Others",
        "followed_backlinks": "4.2M",
        "nofollow_backlinks": "1.3M",
        "added_age": "2Y 0M",
        "domain_age": "26Y 4M",
        "deals_completed": 175
    },
    {
        "id": "w-9",
        "domain": "usatoday.com",
        "sample_url": "https://www.usatoday.com/money",
        "price": 160,
        "currency": "USD",
        "category": "News and Media",
        "categories": ["News and Media", "Lifestyle", "Business"],
        "traffic_semrush": "78.2M",
        "traffic_ahrefs": "54.1M",
        "traffic_num": 78200000,
        "dr": 93,
        "da": 92,
        "as_score": 98,
        "max_links": 2,
        "link_type": "NoFollow",
        "turnaround": "3 Days",
        "country": "United States",
        "country_extra": "Global",
        "followed_backlinks": "18.4M",
        "nofollow_backlinks": "6.2M",
        "added_age": "1Y 9M",
        "domain_age": "32Y 1M",
        "deals_completed": 92
    },
    {
        "id": "w-10",
        "domain": "bignewsnetwork.com",
        "sample_url": "https://www.bignewsnetwork.com/news",
        "price": 29,
        "currency": "USD",
        "category": "News and Media",
        "categories": ["News and Media", "General", "World"],
        "traffic_semrush": "480K",
        "traffic_ahrefs": "210K",
        "traffic_num": 480000,
        "dr": 77,
        "da": 71,
        "as_score": 52,
        "max_links": 2,
        "link_type": "DoFollow",
        "turnaround": "2 Days",
        "country": "United Kingdom",
        "country_extra": "+4 Others",
        "followed_backlinks": "380K",
        "nofollow_backlinks": "120K",
        "added_age": "6M",
        "domain_age": "22Y 7M",
        "deals_completed": 68
    },
    {
        "id": "w-11",
        "domain": "forbes.com",
        "sample_url": "https://www.forbes.com/business",
        "price": 450,
        "currency": "USD",
        "category": "Business",
        "categories": ["Business", "Leadership", "Finance"],
        "traffic_semrush": "145.0M",
        "traffic_ahrefs": "92.4M",
        "traffic_num": 145000000,
        "dr": 94,
        "da": 95,
        "as_score": 100,
        "max_links": 1,
        "link_type": "NoFollow",
        "turnaround": "7 Days",
        "country": "United States",
        "country_extra": "Global",
        "followed_backlinks": "25.0M",
        "nofollow_backlinks": "8.5M",
        "added_age": "3Y 1M",
        "domain_age": "29Y 4M",
        "deals_completed": 54
    },
    {
        "id": "w-12",
        "domain": "entrepreneur.com",
        "sample_url": "https://www.entrepreneur.com/growing-a-business",
        "price": 220,
        "currency": "USD",
        "category": "Business",
        "categories": ["Business", "Marketing", "Startups"],
        "traffic_semrush": "16.8M",
        "traffic_ahrefs": "11.2M",
        "traffic_num": 16800000,
        "dr": 90,
        "da": 89,
        "as_score": 88,
        "max_links": 2,
        "link_type": "DoFollow",
        "turnaround": "5 Days",
        "country": "United States",
        "country_extra": "+5 Others",
        "followed_backlinks": "5.1M",
        "nofollow_backlinks": "1.7M",
        "added_age": "2Y 2M",
        "domain_age": "27Y 10M",
        "deals_completed": 88
    }
]

ORDERS_STORE = []


class VefogixHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        
        if parsed.path == "/api/websites":
            qs = urllib.parse.parse_qs(parsed.query)
            q = qs.get("q", [""])[0].lower().strip()
            cat = qs.get("category", ["all"])[0]
            min_dr = int(qs.get("min_dr", [0])[0])
            min_da = int(qs.get("min_da", [0])[0])
            max_price = int(qs.get("max_price", [9999])[0])
            link_type = qs.get("link_type", ["all"])[0]
            sort_by = qs.get("sort", ["default"])[0]

            filtered = []
            for w in WEBSITES_DATABASE:
                if q and (q not in w["domain"].lower() and not any(q in c.lower() for c in w["categories"])):
                    continue
                if cat != "all" and cat != w["category"] and cat not in w["categories"]:
                    continue
                if w["dr"] < min_dr or w["da"] < min_da:
                    continue
                if w["price"] > max_price:
                    continue
                if link_type != "all" and w["link_type"].lower() != link_type.lower():
                    continue
                filtered.append(w)

            # Sort logic
            if sort_by == "price_asc":
                filtered.sort(key=lambda x: x["price"])
            elif sort_by == "price_desc":
                filtered.sort(key=lambda x: x["price"], reverse=True)
            elif sort_by == "dr_desc":
                filtered.sort(key=lambda x: x["dr"], reverse=True)
            elif sort_by == "traffic_desc":
                filtered.sort(key=lambda x: x["traffic_num"], reverse=True)

            self._send_json({"total": len(filtered), "data": filtered})
            return

        elif parsed.path == "/api/stats":
            self._send_json({
                "registered_websites": "129,877+",
                "publishers_writers": "45,000+",
                "tasks_completed": "250,000+",
                "support": "24 X 7"
            })
            return

        elif parsed.path == "/api/orders":
            self._send_json({"orders": ORDERS_STORE, "total": len(ORDERS_STORE)})
            return

        # Default static file handling
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        if parsed.path == "/api/cart/checkout":
            order_id = f"VFX-{len(ORDERS_STORE) + 1001}"
            order = {
                "order_id": order_id,
                "items": payload.get("items", []),
                "total_usd": payload.get("total_usd", 0),
                "target_url": payload.get("target_url", ""),
                "anchor_text": payload.get("anchor_text", ""),
                "content_option": payload.get("content_option", "publisher_writes"),
                "status": "QUEUED_EDITORIAL_REVIEW"
            }
            ORDERS_STORE.append(order)
            self._send_json({"success": True, "order": order})
            return

        self.send_response(404)
        self.end_headers()

    def _send_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))


def start_server(host: str = "127.0.0.1", port: int = 8600):
    server = HTTPServer((host, port), VefogixHandler)
    print(f"[*] Vefogix Marketplace running at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    start_server()
