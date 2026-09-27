import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not set!")

genai.configure(api_key=api_key)

def ask_ai(prompt: str):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        res = model.generate_content(prompt)
        return res.text
    except Exception as e:
        return f"Error: {e} - Try again after 30 sec"

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """<html><body>
    <h2>EduGenie - Ready!</h2>
    <form action="/ask"><input name="q" placeholder="Ask anything"><button>Ask</button></form>
    <hr>
    <form action="/explain"><input name="topic" placeholder="Topic"><button>Explain</button></form>
    </body></html>"""

@app.get("/ask", response_class=HTMLResponse)
def ask(q: str):
    ans = ask_ai(q)
    return f"<p><b>Q:</b> {q}</p><p>{ans}</p><a href='/'>Back</a>"

@app.get("/explain", response_class=HTMLResponse)
def explain(topic: str):
    ans = ask_ai(f"Explain {topic} in simple Tamil and English")
    return f"<p><b>Topic:</b> {topic}</p><p>{ans}</p><a href='/'>Back</a>"
