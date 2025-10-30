from dotenv import load_dotenv
load_dotenv()  # load variables from .env into os.environ

import os
import re
import requests
from flask import Flask, request, jsonify
# working fine
app = Flask(__name__)

# ── API setup ───────────────────────────────────────────────────────────────
API_URL      = "https://router.huggingface.co/novita/v3/openai/chat/completions"
HF_API_TOKEN = os.getenv('HF_API_TOKEN', '').strip()
HEADERS      = {"Authorization": f"Bearer {HF_API_TOKEN}"}

# ── MODEL choices (router-side) ──────────────────────────────────────────────
MODEL = "google/gemma-3-27b-it"

def fetchQuizFromLlama(student_topic):
    print(">>> HITTING URL:", API_URL)
    print(">>> OUTBOUND HEADERS:", HEADERS)
    print("Fetching quiz for topic:", student_topic)
    payload = {
        "model": MODEL,
        "messages": [
            {"role":"user","content":(
                f"Generate a quiz with 1 question on “{student_topic}”. "
                "Each question should have 4 options (A–D) and exactly one correct answer. "
                "Format:\n"
                "**QUESTION 1:** ...\n"
                "**OPTION A:** ...\n"
                "**OPTION B:** ...\n"
                "**OPTION C:** ...\n"
                "**OPTION D:** ...\n"
                "**ANS:** A\n\n"
                # repeat for Q2 and Q3 if desired
            )}
        ],
        "max_tokens": 500,
        "temperature": 0.7,
        "top_p": 0.9
    }
    resp = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
    if resp.status_code != 200:
        raise Exception(f"API request failed: {resp.status_code} - {resp.text}")
    return resp.json()["choices"][0]["message"]["content"]

def process_quiz(quiz_text):
    pattern = re.compile(
        r'\*\*QUESTION \d+:\*\* (.+?)\n'
        r'\*\*OPTION A:\*\* (.+?)\n'
        r'\*\*OPTION B:\*\* (.+?)\n'
        r'\*\*OPTION C:\*\* (.+?)\n'
        r'\*\*OPTION D:\*\* (.+?)\n'
        r'\*\*ANS:\*\* (.+?)(?=\n|$)', re.DOTALL
    )
    questions = []
    for q,a,b,c,d,ans in pattern.findall(quiz_text):
        questions.append({
            "question": q.strip(),
            "options": [a.strip(), b.strip(), c.strip(), d.strip()],
            "correct_answer": ans.strip()
        })
    return questions

@app.route('/getQuiz', methods=['GET'])
def get_quiz():
    topic = request.args.get('topic')
    if not topic:
        return jsonify(error="Missing topic"), 400
    try:
        raw = fetchQuizFromLlama(topic)
        parsed = process_quiz(raw)
        if not parsed:
            return jsonify(error="Parse failed", raw=raw), 500
        return jsonify(quiz=parsed)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/test', methods=['GET'])
def test():
    return jsonify(quiz="test")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
