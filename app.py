import json
import math
import re
import socketserver
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
INDEX_PATH = BASE_DIR / "index.html"
MODEL_PATH = BASE_DIR / "outputs" / "trustjob_pipeline.joblib"
METRICS_PATH = BASE_DIR / "outputs" / "comparaison_modeles_trustjob.csv"

PORT = 5000

RISK_TERMS = [
    "upfront fee", "processing fee", "application fee", "pay a fee",
    "wire transfer", "western union", "money order", "bank account",
    "social security number", "passport", "frais de dossier",
    "paiement préalable", "virement bancaire", "coordonnées bancaires",
    "crypto", "bitcoin", "whatsapp", "telegram",
    "no experience", "sans expérience", "urgent", "immediately", "immédiatement",
    "copy of your passport", "training kit", "processing fees",
]


def load_model():
    if not MODEL_PATH.exists():
        print(f"[!] Modèle introuvable : {MODEL_PATH}")
        print("[!] Exécutez le notebook jusqu'à la sauvegarde du modèle, puis relancez le backend.")
        sys.exit(1)
    print(f"[*] Chargement du modèle : {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)
    print("[+] Modèle chargé.")
    return model


MODEL = load_model()


def load_metrics():
    if not METRICS_PATH.exists():
        return []
    try:
        df = pd.read_csv(METRICS_PATH)
        df = df.replace({np.nan: None})
        rows = df.to_dict(orient="records")
        # Ensure plain Python types for JSON serialization
        cleaned = []
        for row in rows:
            item = {}
            for k, v in row.items():
                if isinstance(v, (np.integer,)):
                    item[k] = int(v)
                elif isinstance(v, (np.floating,)):
                    item[k] = None if np.isnan(v) else float(v)
                else:
                    item[k] = v
            cleaned.append(item)
        return cleaned
    except Exception as e:
        print(f"[!] Erreur lecture métriques : {e}")
        return []


def clamp01_100(value: float) -> float:
    return max(0.0, min(100.0, float(value)))


def risk_from_margin(margin: float) -> float:
    # Sigmoïde sur la marge de décision (LinearSVC) -> indice 0-100
    try:
        score = 100.0 / (1.0 + math.exp(-float(margin)))
    except OverflowError:
        score = 0.0 if margin < 0 else 100.0
    return round(clamp01_100(score), 1)


def detect_terms(text: str):
    lower = (text or "").lower()
    found = []
    for term in RISK_TERMS:
        pattern = r"\b" + re.escape(term.lower()) + r"\b"
        if re.search(pattern, lower):
            found.append(term)
    return found


class TrustJobHandler(BaseHTTPRequestHandler):
    server_version = "TrustJobBackend/1.0"

    def log_message(self, fmt, *args):
        print(f"[{self.log_date_time_string()}] {self.command} {self.path} -> {args[1]}")

    def _send_json(self, status: int, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            if not INDEX_PATH.exists():
                self.send_error(404, "index.html introuvable.")
                return
            data = INDEX_PATH.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        if self.path == "/api/metrics":
            self._send_json(200, load_metrics())
            return

        self.send_error(404, "Ressource introuvable.")

    def do_POST(self):
        if self.path != "/api/predict":
            self.send_error(404, "Ressource introuvable.")
            return

        try:
            length = int(self.headers.get("Content-Length", "0") or 0)
        except ValueError:
            length = 0
        raw = self.rfile.read(length) if length > 0 else b"{}"

        try:
            data = json.loads(raw.decode("utf-8") or "{}")
        except Exception:
            self._send_json(400, {"error": "JSON invalide."})
            return

        if not isinstance(data, dict):
            self._send_json(400, {"error": "Corps de requête invalide."})
            return

        text = str(data.get("text", "") or "")
        try:
            telecommuting = int(data.get("telecommuting", 0) or 0)
        except Exception:
            telecommuting = 0
        try:
            has_company_logo = int(data.get("has_company_logo", 1) if data.get("has_company_logo", None) is not None else 1)
        except Exception:
            has_company_logo = 1
        try:
            has_questions = int(data.get("has_questions", 1) if data.get("has_questions", None) is not None else 1)
        except Exception:
            has_questions = 1

        row = pd.DataFrame([{
            "text": text,
            "telecommuting": telecommuting,
            "has_company_logo": has_company_logo,
            "has_questions": has_questions,
        }])

        try:
            pred = int(MODEL.predict(row)[0])
        except Exception as e:
            self._send_json(500, {"error": f"Erreur de prédiction : {e}"})
            return

        if hasattr(MODEL, "decision_function"):
            try:
                margin = float(MODEL.decision_function(row)[0])
                risk_score = risk_from_margin(margin)
            except Exception:
                risk_score = 95.0 if pred == 1 else 10.0
        elif hasattr(MODEL, "predict_proba"):
            try:
                proba = float(MODEL.predict_proba(row)[0][1])
                risk_score = round(clamp01_100(proba * 100.0), 1)
            except Exception:
                risk_score = 95.0 if pred == 1 else 10.0
        else:
            risk_score = 95.0 if pred == 1 else 10.0

        response = {
            "prediction": pred,
            "risk_score": risk_score,
            "detected_terms": detect_terms(text),
        }
        self._send_json(200, response)


class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def run():
    server = ThreadedHTTPServer(("", PORT), TrustJobHandler)
    url = f"http://localhost:{PORT}"
    print("==============================================================")
    print("  TrustJob AI - Backend (modèle ML + interface)")
    print("==============================================================")
    print(f"[+] Interface : {url}")
    print("[*] Ctrl+C pour arrêter.")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Arrêt du serveur.")
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
