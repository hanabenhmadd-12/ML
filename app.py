import csv
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import math
from pathlib import Path
import re
import socketserver
import sys
import threading
import time
import webbrowser

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "outputs" / "trustjob_pipeline.joblib"
METRICS_PATH = BASE_DIR / "outputs" / "comparaison_modeles_trustjob.csv"
STATIC_INDEX = BASE_DIR / "static" / "index.html"

PORT = 5000

RISK_TERMS = [
    "upfront fee", "processing fee", "application fee", "pay a fee",
    "wire transfer", "western union", "money order", "bank account",
    "social security number", "passport", "frais de dossier",
    "paiement préalable", "virement bancaire", "coordonnées bancaires",
    "crypto", "bitcoin", "travail à domicile sans expérience"
]

print("=================================================================")
print("  TrustJob AI • Serveur d'Inférence & Interface Web")
print("=================================================================")
print(f"[*] Chargement du modèle de Machine Learning depuis : {MODEL_PATH}")

if not MODEL_PATH.exists():
    print(f"[!] ERREUR : Le modèle {MODEL_PATH} est introuvable.")
    sys.exit(1)

model = joblib.load(str(MODEL_PATH))
print("[+] Modèle SVM Linéaire chargé avec succès !")


class TrustJobRequestHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        # Format propre des logs HTTP
        print(f"[{self.log_date_time_string()}] {self.command} {self.path} -> {args[1]}")

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            if STATIC_INDEX.exists():
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(STATIC_INDEX, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "Fichier d'interface introuvable.")
        elif self.path == "/api/metrics":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()

            rows = []
            if METRICS_PATH.exists():
                try:
                    df = pd.read_csv(METRICS_PATH)
                    rows = df.fillna("").to_dict(orient="records")
                except Exception as e:
                    print(f"[!] Erreur lecture métriques : {e}")

            self.wfile.write(json.dumps(rows, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_error(404, "Page non trouvée.")

    def do_POST(self):
        if self.path == "/api/predict":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body.decode("utf-8"))
            except Exception:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "JSON invalide"}')
                return

            text = data.get("text", "")
            telecommuting = int(data.get("telecommuting", 0))
            has_company_logo = int(data.get("has_company_logo", 1))
            has_questions = int(data.get("has_questions", 1))

            df_input = pd.DataFrame([{
                "text": text,
                "telecommuting": telecommuting,
                "has_company_logo": has_company_logo,
                "has_questions": has_questions
            }])

            # Prédiction ML
            pred = int(model.predict(df_input)[0])

            # Score de risque (sigmoïde sur margin LinearSVC)
            if hasattr(model, "decision_function"):
                margin = float(model.decision_function(df_input)[0])
                risk_score = round(100.0 / (1.0 + math.exp(-margin)), 1)
            else:
                risk_score = 95.0 if pred == 1 else 10.0

            # Détection lexicale
            full_text_lower = text.lower()
            found_terms = [
                term for term in RISK_TERMS
                if re.search(r"\b" + re.escape(term) + r"\b", full_text_lower)
            ]

            response_payload = {
                "prediction": pred,
                "verdict": "FRAUDULENT" if pred == 1 else "LEGITIMATE",
                "risk_score": risk_score,
                "detected_terms": found_terms,
                "status": "success"
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(response_payload, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_error(404, "Route API inconnue.")


class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def run_server():
    server_address = ("", PORT)
    httpd = ThreadedHTTPServer(server_address, TrustJobRequestHandler)
    url = f"http://localhost:{PORT}"
    print(f"[+] Interface disponible sur : {url}")
    print("[*] Ouverture automatique du navigateur...")

    # Ouverture du navigateur après un court délai
    threading.Thread(target=lambda: (time.sleep(0.8), webbrowser.open(url))).start()

    print("[*] Appuyez sur Ctrl+C pour arrêter le serveur.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Arrêt du serveur TrustJob AI.")
        httpd.server_close()


if __name__ == "__main__":
    run_server()
