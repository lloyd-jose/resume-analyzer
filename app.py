from flask import Flask , render_template, request
from PyPDF2 import PdfReader


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')



skills_list = ["python","java","c++","sql","machine learning","data analysis","communication","teamwork","flask"]
role_skills = {
    "data": ["python", "sql", "data analysis", "excel"],
    "ml": ["python", "machine learning", "deep learning"],
    "web": ["html", "css", "javascript", "flask"]
}


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



def calculate_score(skills):
    score = len(skills)*10

    if score>100:
        score=100

    return score


def role_match(skills, role):
    required = role_skills.get(role, [])
    match = 0

    # convert resume skills to lowercase
    skills = [s.lower() for s in skills]

    for skill in required:
        if skill.lower() in skills:
            match += 1

    if len(required) == 0:
        return 0

    return int((match / len(required)) * 100)





@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['resume']
    role = request.form.get("role")

    print("ROLE VALUE:", role)

    if file:
        reader = PdfReader(file)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        

        skills = extract_skills(text)
        required = role_skills.get(role, [])
        suggestions = suggest(skills)
        score = calculate_score(skills)
        match_score = role_match(skills, role)

        if match_score < 50:
            suggestions.append("Your resume is not well aligned with this role")

        return render_template("result.html",skills=skills,suggestions=suggestions,score=score,match_score=match_score,role=role)
    
    return "No file uploaded"



if __name__ == '__main__':
    app.run(debug=True)
