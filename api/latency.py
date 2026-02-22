from http.server import BaseHTTPRequestHandler
import json
import numpy as np

DATA = [
  {"region":"apac","latency_ms":161.16,"uptime_pct":99.489},
  {"region":"apac","latency_ms":183.79,"uptime_pct":99.084},
  {"region":"apac","latency_ms":103.15,"uptime_pct":98.757},
  {"region":"apac","latency_ms":187.6,"uptime_pct":98.683},
  {"region":"apac","latency_ms":223.25,"uptime_pct":98.112},
  {"region":"apac","latency_ms":118.39,"uptime_pct":98.892},
  {"region":"apac","latency_ms":147.35,"uptime_pct":97.505},
  {"region":"apac","latency_ms":195.13,"uptime_pct":97.701},
  {"region":"apac","latency_ms":135.72,"uptime_pct":98.833},
  {"region":"apac","latency_ms":162.9,"uptime_pct":99.478},
  {"region":"apac","latency_ms":123.29,"uptime_pct":99.378},
  {"region":"apac","latency_ms":166.9,"uptime_pct":97.42},
  {"region":"emea","latency_ms":209.59,"uptime_pct":97.762},
  {"region":"emea","latency_ms":206.63,"uptime_pct":98.24},
  {"region":"emea","latency_ms":178.48,"uptime_pct":98.993},
  {"region":"emea","latency_ms":188.22,"uptime_pct":98.531},
  {"region":"emea","latency_ms":132.99,"uptime_pct":98.718},
  {"region":"emea","latency_ms":156.4,"uptime_pct":99.48},
  {"region":"emea","latency_ms":202.63,"uptime_pct":98.325},
  {"region":"emea","latency_ms":125.22,"uptime_pct":98},
  {"region":"emea","latency_ms":155.01,"uptime_pct":99.118},
  {"region":"emea","latency_ms":176.64,"uptime_pct":97.729},
  {"region":"emea","latency_ms":139.97,"uptime_pct":98.789},
  {"region":"emea","latency_ms":158.88,"uptime_pct":98.475},
  {"region":"amer","latency_ms":218.88,"uptime_pct":97.464},
  {"region":"amer","latency_ms":198.13,"uptime_pct":98.619},
  {"region":"amer","latency_ms":191.19,"uptime_pct":97.236},
  {"region":"amer","latency_ms":176.52,"uptime_pct":97.258},
  {"region":"amer","latency_ms":200.74,"uptime_pct":98.811},
  {"region":"amer","latency_ms":98.63,"uptime_pct":97.555},
  {"region":"amer","latency_ms":158.81,"uptime_pct":98.494},
  {"region":"amer","latency_ms":216.21,"uptime_pct":97.418},
  {"region":"amer","latency_ms":131.48,"uptime_pct":97.325},
  {"region":"amer","latency_ms":198.61,"uptime_pct":98.784},
  {"region":"amer","latency_ms":138.38,"uptime_pct":97.26},
  {"region":"amer","latency_ms":189.4,"uptime_pct":99.442},
]

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        payload = json.loads(body)

        regions = payload.get('regions', [])
        threshold = payload.get('threshold_ms', 180)

        result = {}
        for region in regions:
            records = [d for d in DATA if d['region'] == region]
            if not records:
                continue
            latencies = [r['latency_ms'] for r in records]
            uptimes = [r['uptime_pct'] for r in records]
            result[region] = {
                'avg_latency': round(sum(latencies) / len(latencies), 4),
                'p95_latency': round(float(np.percentile(latencies, 95)), 4),
                'avg_uptime': round(sum(uptimes) / len(uptimes), 4),
                'breaches': sum(1 for l in latencies if l > threshold)
            }

        self.send_response(200)
        self._send_cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
