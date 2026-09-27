import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.generativeai as genai

app = FastAPI()

# Static and templates iruntha mount pannum, illa na skip pannum
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

templates = None
if os.path.exists("templates"):
    templates = Jinja2Templates(directory="templates")

# Un modules - error vantha kooda app crash aagathu
try:
    import qna
except: qna = None
try:
    import quiz_module
except: quiz_module = None
try:
    import summary_module
except: summary_module = None
try:
    import explanation_module
except: explanation_module = None
try:
    import learning_path
except: learning_path = None

HTML_FALLBACK = """
<!DOCTYPE html>
<html>
<head><title>EduGenie</title><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:system-ui;background:#eef2ff;padding:15px}
.card{background:white;max-width:700px;margin:30px auto;padding:25px;border-radius:20px}
h1{text-align:center;color:#4F46E5}
input,textarea{width:100%;padding:14px;border:1px solid #ddd;border-radius:10px;box-sizing:border-box;margin-top:10px}
button{width:100%;padding:14px;background:#4F46E5;color:white;border:none;border-radius:10px;margin-top:12px;font-weight:bold}
.ans{margin-top:20px;background:#f5f3ff;padding:15px;border-radius:10px;white-space:pre-wrap}
</style>
</head>
<body>
<div class="card">
<h1>EduGenie 🧠✨</h1>
<p style="text-align:center">Your AI Study Buddy is Live!</p>
<form method="post" action="/">
<textarea name="q" placeholder="Ask anything..." required rows="3"></textarea>
<button type="submit">Ask</button>
</form>
{ans}
</div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # templates la index.html iruntha atha kaatum
    if templates and os.path.exists("templates/index.html"):
        return templates.TemplateResponse("index.html", {"request": request})
    return HTML_FALLBACK.format(ans="")

@app.post("/", response_class=HTMLResponse)
async def ask(request: Request, q: str = Form(...)):
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return HTML_FALLBACK.format(ans="<div class='ans'>⚠️ Add GEMINI_API_KEY in Render > Environment</div>")
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        res = model.generate_content(q)
        return HTML_FALLBACK.format(ans=f"<div class='ans'><b>Q:</b> {q}<br><br>{res.text}</div>")
    except Exception as e:
        return HTML_FALLBACK.format(ans=f"<div class='ans'>Error: {e}</div>")
