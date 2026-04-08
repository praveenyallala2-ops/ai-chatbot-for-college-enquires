"""
app.py  –  Flask Backend for SREC AI Chatbot
─────────────────────────────────────────────────────────────────────────────
Routes:
  GET  /           → serves the HTML client
  POST /chat       → receives user message, returns AI response
  GET  /health     → health-check endpoint
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

from database import init_db, get_all_training_data, get_response_for_intent
from nlp_engine import train, save_model, load_model, predict_intent, MODEL_PATH

# ──────────────────────────────────────────────────────────────────────────────
# Initialise Flask
# ──────────────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')
CORS(app)   # allow the HTML page to call the API from any origin

# ──────────────────────────────────────────────────────────────────────────────
# Boot-up: init DB  →  train / load model
# ──────────────────────────────────────────────────────────────────────────────
print("\n[BOOT] Initialising database …")
init_db()

print("[BOOT] Loading training data …")
training_data = get_all_training_data()
phrases = [row[0] for row in training_data]
labels  = [row[1] for row in training_data]
print(f"[BOOT] {len(phrases)} training phrases across {len(set(labels))} intents.")

if os.path.exists(MODEL_PATH):
    print("[BOOT] Existing model found — loading …")
    pipeline = load_model()
else:
    print("[BOOT] Training new Naive Bayes model …")
    pipeline = train(phrases, labels)
    save_model(pipeline)

print("[BOOT] ✅ Chatbot is ready!\n")

# ──────────────────────────────────────────────────────────────────────────────
# Fallback response when confidence is too low
# ──────────────────────────────────────────────────────────────────────────────
FALLBACK = (
    "🤔 I'm not sure about that specific query.\n\n"
    "You can ask me about:\n"
    "• Admissions – eligibility, process, dates\n"
    "• Fees – branch-wise fee structure\n"
    "• Courses – B.Tech, M.Tech, MBA\n"
    "• Placements – companies, packages\n"
    "• Hostel – facilities, charges\n"
    "• Transport – bus routes\n"
    "• Contact – phone, address, email\n\n"
    "Or call us directly: +91-8514-233933 📞"
)

CONFIDENCE_THRESHOLD = 0.30   # below this → fallback


# ──────────────────────────────────────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Serve the main HTML frontend."""
    return send_from_directory(BASE_DIR, 'CLOADcollege_chatbot.html')


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "model": "Naive Bayes + TF-IDF"})


@app.route('/chat', methods=['POST'])
def chat():
    """
    Accepts JSON: { "message": "user text" }
    Returns JSON: { "response": "bot reply", "intent": "...", "confidence": 0.xx }
    """
    data = request.get_json(force=True, silent=True)
    if not data or not data.get('message', '').strip():
        return jsonify({"error": "No message provided"}), 400

    user_message = data['message'].strip()

    # ── NLP Pipeline ──────────────────────────────────────────────────────────
    intent, confidence = predict_intent(pipeline, user_message)

    if confidence >= CONFIDENCE_THRESHOLD:
        response_text = get_response_for_intent(intent)
        if not response_text:
            response_text = FALLBACK
            intent = "unknown"
    else:
        response_text = FALLBACK
        intent = "unknown"
        confidence = 0.0

    # ── Log to console ────────────────────────────────────────────────────────
    print(f"  USER : {user_message}")
    print(f"  INTENT: {intent}  (conf={confidence:.2f})")

    return jsonify({
        "response":   response_text,
        "intent":     intent,
        "confidence": round(confidence, 4)
    })


# ──────────────────────────────────────────────────────────────────────────────
# Entry-point
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
