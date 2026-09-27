import os
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import google.generativeai as genai

app = FastAPI()

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>EduGenie</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:Arial;background:#eef2ff;padding:20px}
.box{background:white;max-width:600px;margin:auto;padding:20px;border-radius:15px;box-shadow:0 4px 10px rgba(0,0,0,0.1)}
h1{text-align:center;color:#4F46E5}
input{width:100%;padding:12px;margin-top:15px;box-sizing:border-box;border:1px solid #ccc;border-radius:8px}
button{width:100%;padding:12px;background:#4F46E5;color:white;border:none;border-radius:8px;margin-top:10px;font-size:16px}
.ans{margin-top:15px;background:#f5f3ff;padding:12px;border-radius:8px;white-space:pre-wrap}
</style>
</head>
<body>
<div class="box">
<h1>EduGenie 🧠✨</h1>
<p style="text-align:center">Your AI Study Buddy</p>
<form method="post">
<input name="question" placeholder="Ask anything... What is AI?" required>
<button type="submit">Get Answer</button>
</form>
{result}
</div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE.format(result="")

@app.post("/", response_class=HTMLResponse)
def ask(question: str = Form(...)):
    try:
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            return HTML_PAGE.format(result="<div class='ans'>ERROR: GEMINI_API_KEY not set in Render Environment</div>")
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        r = model.generate_content(question)
        return HTML_PAGE.format(result=f"<div class='ans'><b>Answer:</b><br>{r.text}</div>")
    except Exception as e:
        return HTML_PAGE.format(result=f"<div class='ans'>Error: {e}</div>")
