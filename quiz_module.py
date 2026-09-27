def generate_quiz(topic: str):
    return [
        {"q": f"What is {topic}?", "options": ["Option A", "Option B", "Option C", "Correct Answer"], "answer": "Correct Answer"},
        {"q": f"Why is {topic} important?", "options": ["A", "B", "C", "D"], "answer": "B"},
        {"q": f"Give one example of {topic}", "options": ["Ex1", "Ex2", "Ex3", "Ex4"], "answer": "Ex1"}
    ]
