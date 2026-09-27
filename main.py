import os
import google.generativeai as genai
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# Load API Key from Render Environment Variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def ask_ai(prompt: str):
    """Function to call Gemini AI"""
    if not GEMINI_API_KEY:
        return "ERROR: GEMINI_API_KEY is not set in Render Environment."
    try:
        # Using the stable free model
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini API Error: {str(e)}"

# Frontend HTML
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>EduGenie - AI Study Buddy</title>
<style>
body{font-family: sans-serif; background: #f4f6fb; margin: 0; padding: 10px;}
.container{max-width: 750px; margin: auto;}
.card{background: white; padding: 14px; border-radius: 12px; margin-bottom: 12px; box-shadow: 0 2px 6px #ddd;}
input, textarea{width: 95%; padding: 10px; border-radius: 8px; border: 1px solid #ccc; margin: 6px 0;}
button{background: #3b82f6; color: white; border: none; padding: 8px 14px; border-radius: 8px; font-weight: bold; cursor: pointer;}
.answer{background: #eef6ff; padding: 10px; border-radius: 8px; margin-top: 8px; white-space: pre-wrap; border-left: 4px solid #3b82f6;}
</style>
</head>
<body>
<div class="container">
<h2 style="text-align:center">EduGenie - Your AI Study Buddy</h2>

<div class="card">
<h3>a. Ask Question:</h3>
<input id="q1" placeholder="How to run python">
<button onclick="callApi('q1','a1','qna')">Get Answer</button>
<div id="a1" class="answer"></div>
</div>

<div class="card">
<h3>b. Explanation:</h3>
<input id="q2" placeholder="Enter topic to explain">
<button onclick="callApi('q2','a2','explain')">Explain</button>
<div id="a2" class="answer"></div>
</div>

<div class="card">
<h3>c. Summarize:</h3>
<textarea id="q3" placeholder="Paste text to summarize"></textarea>
<button onclick="callApi('q3','a3','sum')">Summarize</button>
<div id="a3" class="answer"></div>
</div>

<div class="card">
<h3>d. Quiz:</h3>
<input id="q4" placeholder="Enter topic for quiz">
<button onclick="callApi('q4','a4','quiz')">Create Quiz</button>
<div id="a4" class="answer"></div>
</div>

<div class="card">
<h3>e. Learning Plan:</h3>
<input id="q5" placeholder="Enter your goal">
<button onclick="callApi('q5','a5','plan')">Get Plan</button>
<div id="a5" class="answer"></div>
</div>
</div>

<script>
async function callApi(qId, aId, type){
  let q = document.getElementById(qId).value;
  let a = document.getElementById(aId);
  if(!q){ alert("Please enter text"); return; }
  a.innerHTML = "Thinking... Please wait 10 seconds...";
  let param = type=='qna'?'question=':type=='explain'?'topic=':type=='sum'?'text=':type=='quiz'?'topic=':'goal=';
  let url = '/' + type + '?' + param + encodeURIComponent(q);
  try{
    let res = await fetch(url);
    let data = await res.json();
    a.innerHTML = data.result || data.quiz || "No response";
  }catch(e){
    a.innerHTML = "Error: " + e;
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
    return {"result": ask_ai(f"Explain {topic} in simple 5 points with examples")}

@app.get("/sum")
def summ(text: str):
    return {"result": ask_ai(f"Summarize this text clearly: {text}")}

@app.get("/quiz")
def quiz(topic: str):
    return {"quiz": ask_ai(f"Create 5 MCQ quiz questions for {topic} with answers")}

@app.get("/plan")
def plan(goal: str):
    return {"result": ask_ai(f"Create a 7-day learning plan for {goal}")}
