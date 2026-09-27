import os
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def ask_ai(prompt: str):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        res = model.generate_content(prompt)
        return res.text
    except Exception as e:
        return f"Server busy da, 30 sec kalichu try pannu! <br><small>{e}</small>"

app = FastAPI()

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{{background:#f0f2f9; font-family: sans-serif; padding:15px}}
.card{{background:white; border-radius:20px; padding:20px; margin-bottom:20px; box-shadow:0 4px 12px #0001}}
h1{{color:#5a23e8; text-align:center; font-size:32px}}
p.sub{{text-align:center; font-size:18px; margin-top:-10px}}
h2{{font-size:20px}}
input, textarea{{width:95%; padding:15px; border-radius:12px; border:1px solid #ccc; font-size:16px}}
button{{background:#2a7bff; color:white; border:none; padding:12px 22px; border-radius:12px; font-size:16px; font-weight:bold; margin-top:12px}}
.ans{{background:#f5f5f7; border-left:5px solid #2a7bff; border-radius:12px; padding:15px; margin-top:15px; white-space:pre-wrap}}
</style>
</head>
<body>
<div class="card"><h1>EduGenie 🧠 ✨</h1><p class="sub">Your Personal AI Learning Assistant</p></div>

<div class="card">
<h2>a. Asking questions:</h2>
<form method="post" action="/ask">
<input name="q" placeholder="What is ai" required>
<button>Get Answer</button>
</form>
{ans1}
</div>

<div class="card">
<h2>b. Explanation of any topic:</h2>
<form method="post" action="/explain">
<input name="topic" placeholder="Ex: Photosynthesis" required>
<button>Explain</button>
</form>
{ans2}
</div>

<div class="card">
<h2>c. Summarising long paragraphs:</h2>
<form method="post" action="/summarise">
<textarea name="para" rows="4" placeholder="Paste long paragraph here..." required></textarea>
<button>Summarise</button>
</form>
{ans3}
</div>
</body>
</html>
"""

def render(a1="", a2="", a3=""):
    return HTML_PAGE.format(
        ans1=f'<div class="ans">{a1}</div>' if a1 else "",
        ans2=f'<div class="ans">{a2}</div>' if a2 else "",
        ans3=f'<div class="ans">{a3}</div>' if a3 else ""
    )

@app.get("/", response_class=HTMLResponse)
def home(): return render()

@app.post("/ask", response_class=HTMLResponse)
def ask(q: str = Form(...)):
    ans = ask_ai(q)
    return render(a1=ans)

@app.post("/explain", response_class=HTMLResponse)
def explain(topic: str = Form(...)):
    ans = ask_ai(f"Explain {topic} in simple way with Tamil + English points")
    return render(a2=ans)

@app.post("/summarise", response_class=HTMLResponse)
def summarise(para: str = Form(...)):
    ans = ask_ai(f"Summarise this in 5 points: {para}")
    return render(a3=ans)
