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
        return f"Error: {str(e)} Please wait 30 seconds and try again."

app = FastAPI()

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>EduGenie - AI Study Buddy</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { font-family: Arial, sans-serif; background: #f0f4ff; padding: 20px; }
.card { background: white; max-width: 650px; margin: auto; padding: 25px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
h1 { text-align: center; color: #4F46E5; margin-bottom: 5px; }
p.sub { text-align:center; color: #666; margin-top: 0; }
input { width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #ccc; margin-top: 15px; box-sizing: border-box; }
button { width: 100%; padding: 12px; background: #4F46E5; color: white; border: none; border-radius: 8px; margin-top: 12px; font-size: 16px; cursor: pointer; }
.answer { margin-top: 20px; background: #EEF2FF; padding: 15px; border-radius: 8px; white-space: pre-wrap; border-left: 4px solid #4F46E5; }
</style>
</head>
<body>
<div class="card">
<h1>EduGenie 🧠✨</h1>
<p class="sub">Your AI Study Buddy</p>
<form method="post">
<input type="text" name="question" placeholder="Ask anything... What is AI?" required>
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
    ans = ask_ai(question)
    result_html = f'<div class="answer"><b>Answer:</b><br>{ans}</div>'
    return HTML_PAGE.format(result=result_html)
