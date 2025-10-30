# LLM-Powered-Quiz-Server

The **LLM-Powered-Quiz-Server** repository provides the server-side logic for a next-generation, LLM-driven quiz application.  
It handles question generation, user scoring, and model inference requests, exposing a secure API consumed by the companion frontend app.

---

## Overview

This backend integrates a large language model (LLM) to dynamically generate, evaluate, and explain quiz questions in real time.  
The system is designed for modularity and educational research use, allowing model prompts, evaluation logic, and scoring methods to be extended without refactoring core components.

---

## Key Features

- **Dynamic Question Generation** – Uses an LLM to produce topic-relevant, difficulty-balanced quiz questions.  
- **Automated Answer Evaluation** – Model-based semantic comparison between student answers and reference solutions.  
- **Explanatory Feedback** – Returns short concept explanations generated from the model for each question.  
- **RESTful API Architecture** – Clean GET endpoints for quiz generation and health checking.  
- **Stateless Inference Pipeline** – Handles isolated user sessions for scalability and cloud deployment.  
- **Configurable Model Gateway** – Pluggable connector supporting OpenAI, Hugging Face, or locally hosted models.

---

## Repository Context

This is the **server component** of the full LLM Quiz System.  
The corresponding **frontend** (Android client) can be found in the companion repository.

- **Frontend repo:** `LLM-Powered-Quiz-App`
- **Backend repo:** `LLM-Powered-Quiz-Server` *(this repository)*

---

## Architecture

```
Frontend (UI) ─► REST API ─► LLM-Powered-Quiz-Server
                                ├─ ModelHandler (LLM gateway)
                                ├─ QuestionGenerator
                                ├─ Evaluator
                                ├─ ScoringService
                                └─ MongoDB / LocalStorage (optional)
```

---

## Tech Stack

| Layer | Technology |
|-------|-------------|
| Language | Python 3.12 |
| Framework | Flask / FastAPI *(depending on deployment branch)* |
| AI Model | Hugging Face Router API (OpenAI-compatible) |
| Data Handling | JSON over HTTPS |
| Environment | Virtual env (`venv` / `myenv`), dotenv configuration |
| Version Control | Git / GitHub |
| OS Compatibility | macOS & Linux verified |

---

## Setup & Run

```bash
# 1. Clone the repo
git clone https://github.com/daniel-p-allen/LLM-Powered-Quiz-Server.git
cd LLM-Powered-Quiz-Server

# 2. Create environment
python3 -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pip install flask python-dotenv requests

# 4. Run the server
python main.py
```

Default server runs at `http://127.0.0.1:5000/`.

---

## Environment Variables

Create a `.env` file in the root directory:

```
HF_API_TOKEN=<your_huggingface_api_token>
MODEL_PROVIDER=huggingface
MODEL_NAME=google/gemma-3-27b-it
```

*Never commit your `.env` file.*

---

## API Endpoints

| Method | Endpoint | Params | Description |
|--------|-----------|---------|-------------|
| `GET`  | `/getQuiz` | `topic` (query) | Calls the LLM to generate a quiz question for the given topic and returns JSON. |
| `GET`  | `/test` | – | Health/check endpoint returning a dummy payload. |


---

## Deployment

The backend supports containerised deployment:

```bash
docker build -t LLM-Powered-Quiz-Server .
docker run -p 5000:5000 LLM-Powered-Quiz-Server
```

or deploy directly to platforms such as **Render**, **Railway**, or **AWS Elastic Beanstalk**.

---

## Project Structure

```
LLM-Powered-Quiz-Server/
 ├── main.py
 ├── main-pipeline.py
 ├── main-inferenceclient.py
 ├── main-directModel.py
 ├── requirements.txt
 ├── README.md
 ├── venv/  (ignored)
 └── .gitignore
```

---

## Security Notes

- No secrets are tracked; `.env`, virtual environments, and key files are excluded in `.gitignore`.  
- HTTPS and token-based authentication are recommended for production deployments.  
- Rotate API keys regularly and avoid embedding credentials in code.

---

## License

This project is released under the **MIT License** – see the `LICENSE` file for details.

---

## Acknowledgments

Developed by **Daniel Allen (DanDeakinTutors)** as part of a university and personal applied-AI project.  
Uses open-source LLM frameworks and the Python scientific ecosystem.

---
