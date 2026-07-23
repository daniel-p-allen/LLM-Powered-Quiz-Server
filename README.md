# LLM-Powered-Quiz-Server

A Flask server that asks a language model for a multiple-choice question on a topic,
parses the reply into structured JSON, and returns it to an Android client.

The companion frontend is
[LLM-Powered-Quiz-App](https://github.com/daniel-p-allen/LLM-Powered-Quiz-App).

## How it works

```
  Android client
        │  GET /getQuiz?topic=photosynthesis
        ▼
  ┌──────────────────────────────────────────┐
  │  main.py  (Flask, port 5000)             │
  │                                          │
  │   fetchQuizFromLlama()                   │
  │     builds a prompt demanding a          │
  │     fixed output format, then POSTs ─────┼──► Hugging Face Router
  │                                          │    google/gemma-3-27b-it
  │   process_quiz()                    ◄────┼──── free-form text reply
  │     regex-parses that reply into         │
  │     question / options / answer          │
  └──────────────────┬───────────────────────┘
                     │  JSON
                     ▼
   { "quiz": [ { "question": ...,
                 "options": [A, B, C, D],
                 "correct_answer": "B" } ] }
```

The interesting problem is the middle step. A language model returns prose, but an
Android client needs structured data. The prompt therefore specifies an exact output
shape, and `process_quiz()` parses it with a regular expression — if the model
deviates, parsing returns nothing and the endpoint answers `500` with the raw text
attached, rather than handing the client something malformed.

## Four ways to run the model

The repository keeps four variants of the same server, each integrating the model a
different way. They exist because "how do you actually call an LLM from a backend" has
several answers with very different trade-offs.

| File | Approach | Trade-off |
|---|---|---|
| `main.py` | HTTP POST to the Hugging Face Router, an OpenAI-compatible endpoint | Runs on any machine; needs a token and a network. **This is the one that runs.** |
| `main-inferenceclient.py` | `huggingface_hub.InferenceClient` | Same hosted inference, through an SDK rather than raw HTTP |
| `main-pipeline.py` | `transformers.pipeline()`, model running locally | No token or network, but downloads the model and wants a GPU |
| `main-directModel.py` | `AutoTokenizer` + `AutoModelForCausalLM` directly | Most control over generation, most code, same hardware cost |

`hugginginfo.md` records the Hugging Face setup — access tokens, the licence
acknowledgement the Gemma model requires, and the router configuration — with
screenshots.

## Endpoints

| Method | Path | Query | Returns |
|---|---|---|---|
| `GET` | `/getQuiz` | `topic` | A parsed question, options and answer as JSON |
| `GET` | `/test` | – | `{"quiz": "test"}`, for checking the server is reachable |

`/getQuiz` answers `400` if `topic` is missing, and `500` if the model's reply cannot be
parsed.

## Running it

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

echo "HF_API_TOKEN=your_token_here" > .env

python main.py                    # http://127.0.0.1:5000
```

A Hugging Face access token is required, and the Gemma model's licence must be
acknowledged on your Hugging Face account first — `hugginginfo.md` shows where.

The other three variants need heavier dependencies (`transformers`, `torch`,
`huggingface_hub`), deliberately kept out of `requirements.txt` because they pull in
several gigabytes and are not needed to run the server.

## Layout

```
main.py                    the server that runs
main-inferenceclient.py    the same, via the huggingface_hub SDK
main-pipeline.py           the same, with the model running locally
main-directModel.py        the same, driving the model directly
hugginginfo.md             Hugging Face setup notes and screenshots
requirements.txt           what main.py needs
```

## Known limitations

- **One question per request.** The prompt asks for a single question; the format
  supports more, but nothing requests them yet.
- **Parsing is brittle by design.** The model is asked for an exact format and the reply
  is matched against it. A model that ignores the format produces a `500` rather than a
  guess — safer for the client, but output quality depends on the prompt holding.
- **No tests.** Unlike my other repositories, this one has no automated suite. The
  parser and the endpoint behaviour are both straightforward to test, and that is the
  obvious next step.
- **No authentication.** The endpoints are open. Fine on localhost, not for deployment.
- **Not deployed.** It runs locally, against the Android emulator at `10.0.2.2:5000`.

## Security

`.env` holds the Hugging Face token and is excluded by `.gitignore`. No secrets are
tracked.

## License

MIT — see [`LICENSE`](LICENSE).

## Development notes

Built by me as part of a university applied-AI project. The July 2026 documentation pass
was carried out with the assistance of an AI coding assistant (Claude); the code, the
design decisions, and the review of the result are my own.
