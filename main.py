from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import time
import os
from google import genai


GEMINI_API_KEY = "YOUR_API_KEY"
client = genai.Client(api_key=GEMINI_API_KEY)
app = FastAPI()


MODELS = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
]

def ask_ai(prompt: str):
    for model_name in MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "503" in error_msg or "429" in error_msg or "UNAVAILABLE" in error_msg or "404" in error_msg:
                time.sleep(1)
                continue
            continue
    return "All models are busy. Please wait 30 seconds and try again."

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>EduGenie - Gemini 3.8 Flash</title>
<style>
body{font-family:sans-serif;background:#f4f6fb;margin:0;padding:10px}
.container{max-width:750px;margin:auto}
.header{background:white;padding:15px;border-radius:15px;text-align:center;margin-bottom:12px}
.card{background:white;padding:14px;border-radius:12px;margin-bottom:10px;box-shadow:0 2px 5px #ddd}
input,textarea{width:93%;padding:10px;border:1px solid #ccc;border-radius:8px;margin:6px 0}
button{background:#3b82f6;color:white;border:none;padding:8px 14px;border-radius:8px;font-weight:bold;cursor:pointer}
.answer{background:#f0f7ff;padding:10px;border-radius:8px;margin-top:8px;border-left:3px solid #3b82f6;white-space:pre-wrap;font-size:13px}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>EduGenie - AI Learning Assistant</h1><p>Powered by Gemini 3.8 Flash</p></div>
<div class="card"><h3>a. Ask Question:</h3>
<input id="q1" placeholder="Enter your question">
<button onclick="callApi('q1','a1','qna')">Get Answer</button>
<div id="a1" class="answer" style="display:none"></div></div>
<div class="card"><h3>b. Explanation:</h3>
<input id="q2" placeholder="Enter topic to explain">
<button onclick="callApi('q2','a2','explain')">Explain</button>
<div id="a2" class="answer" style="display:none"></div></div>
<div class="card"><h3>c. Summarising:</h3>
<textarea id="q3" rows="3" placeholder="Paste text to summarize"></textarea>
<button onclick="callApi('q3','a3','sum')">Summarize</button>
<div id="a3" class="answer" style="display:none"></div></div>
<div class="card"><h3>d. Quiz:</h3>
<input id="q4" placeholder="Enter topic for quiz">
<button onclick="callApi('q4','a4','quiz')">Create Quiz</button>
<div id="a4" class="answer" style="display:none"></div></div>
<div class="card"><h3>e. Personalized Plan:</h3>
<input id="q5" placeholder="Enter your learning goal">
<button onclick="callApi('q5','a5','plan')">Get Plan</button>
<div id="a5" class="answer" style="display:none"></div></div>
</div>
<script>
async function callApi(qid, aid, type){
let q = document.getElementById(qid).value;
let a = document.getElementById(aid);
if(!q){alert("Please enter text"); return;}
a.style.display='block';
a.innerHTML='Thinking... Please wait...';
let param = type=='qna'?'question=':type=='explain'?'topic=':type=='sum'?'text=':type=='quiz'?'topic=':'goal=';
let url = '/'+type+'?'+param+encodeURIComponent(q);
try{
let r = await fetch(url);
let d = await r.json();
a.innerHTML = d.result || d.quiz;
}catch(e){
a.innerHTML = 'Server Error: ' + e;
}
}
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE

@app.get("/qna")
def qna(question: str):
    return {"result": ask_ai(question)}

@app.get("/explain")
def explain(topic: str):
    return {"result": ask_ai(f"Explain {topic} in simple 5 points")}

@app.get("/sum")
def summ(text: str):
    return {"result": ask_ai(f"Summarize this text: {text}")}

@app.get("/quiz")
def quiz(topic: str):
    return {"quiz": ask_ai(f"Create 5 MCQ quiz questions for {topic} with answers")}

@app.get("/plan")
def plan(goal: str):
    return {"result": ask_ai(f"Create a 7-day learning plan for {goal}")}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
