import os
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import google.generativeai as genai

app = FastAPI()

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>EduGenie - AI Study Buddy</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:system-ui;background:#eef2ff;padding:15px;margin:0}
.card{background:white;max-width:600px;margin:30px auto;padding:25px;border-radius:20px;box-shadow:0 10px 30px rgba(0,0,0,0.1)}
h1{text-align:center;color:#4F46E5;margin:0}
p.sub{text-align:center;color:#666}
input{width:100%;padding:14px;margin-top:20px;border:1px solid #ddd;border-radius:10px;box-sizing:border-box;font-size:16px}
button{width:100%;padding:14px;background:#4F46E5;color:white;border:none;border-radius:10px;margin-top:12px;font-size:16px;font-weight:bold}
.ans{margin-top:20px;background:#f5f3ff;padding:15px;border-radius:10px;white-space:pre-wrap;line-height:1.6}
small{display:block;text-align:center;margin-top:15px;color:#999}
</style>
</head>
<body>
<div class="card">
<h1>EduGenie 🧠✨</h1>
<p class="sub">Your AI Study Buddy - Works 100%</p>
<form method="post" action="/">
<input name="q" placeholder="Ask anything... Ex: What is Photosynthesis?" required>
<button type="submit">Ask EduGenie</button>
</form>
{ans}
<small>Deployed on Render • f7364eb fixed</small>
</div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML.format(ans="")

@app.post("/", response_class=HTMLResponse)
def ask(q: str = Form(...)):
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return HTML.format(ans="<div class='ans'>⚠️ GEMINI_API_KEY is not set.<br>Go to Render > Environment > Add Variable > GEMINI_API_KEY = your key</div>")
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(q)
        text = response.text.replace("\n", "<br>")
        return HTML.format(ans=f"<div class='ans'><b>Q: {q}</b><br><br>{text}</div>")
    except Exception as e:
        return HTML.format(ans=f"<div class='ans'>Error: {e}</div>")
