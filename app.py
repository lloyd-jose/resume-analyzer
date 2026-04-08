from flask import Flask , render_template, request
from PyPDF2 import PdfReader


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')



skills_list = ["python","java","c++","sql","machine learning","data analysis","communication","teamwork","flask"]

def extract_skills(text):
    found_skills = []

    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)
    
    return found_skills




def suggest(skills):
    suggestions = []

    if "python" not in skills:
        suggestions.append("Consider adding Python skills")

    if "sql" not in skills:
        suggestions.append("Learn SQL for data handling")

    if "machine learning" not in skills:
        suggestions.append("Explore Machine Learning basics")

    if len(skills) < 3:
        suggestions.append("Add more technical skills to strengthen your resume")

    if not suggestions:
        suggestions.append("Great resume! Keep it up")

    return suggestions






@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['resume']

    if file:
        reader = PdfReader(file)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        skills = extract_skills(text)
        suggestions = suggest(skills)

        return render_template("result.html",skills=skills,suggestions=suggestions)
    
    return "No file uploaded"



if __name__ == '__main__':
    app.run(debug=True)
