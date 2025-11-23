from flask import Flask, render_template, request, jsonify
import json
import re
from datetime import datetime
app = Flask(__name__)
PORTFOLIO_DATA = {
    "personal_info": {
        "name": "Surya Akhil Varma",
        "role": "AI/ML Enthusiast | DSA Learner",
        "email": "varmasurya394@gmail.com",
        "github":"https://github.com/P-SAV06",
        "linkedin": "https://www.linkedin.com/in/surya-akhil-varma-penmatsa-596679214/",
        "location": "India",
        "bio": "AI/ML enthusiast passionate about building practical solutions and turning data into impactful products and preparing for technical challenges."
    },
    "skills": {
        "programming": ["Python", "Java", "C"],
        "AIML": ["MachineLearning","NumPy", "Pandas", "Scikit-learn", "Regression Algorithms", "Matplotlib", "Neural Networks"],
        "backend": ["Flask"],
        "tools": ["VS Code", "Google Colab"],
        "databases": ["MySQL Basics"]
    },
    "education": [
        {
            "degree": "Bachelor of Technology",
            "institution": "CMR ENGINEERING COLLEGE",
            "duration": "2024 - 2028",
            "description": "Computer Science Engineering - CGPA: 8.7"
        },
        {
            "degree": "Intermediate (12th Grade)",
            "institution": "MPC",
            "duration": "2022 - 2024",
            "description": "Mathematics, Physics, Chemistry - Score: 925"
        },
        {
            "degree": "Secondary School (10th Grade)",
            "institution": "Triveni Talent School",
            "duration": "2022",
            "description": "SSC - CGPA: 9.7"
        }
    ],
    "projects": [
        {
            "id": 1,
            "name": "Weather Predictor",
            "description": "ML model that predicts outputs of the nextday weather on previous data",
            "tech_stack": ["Python", "TensorFlow", "Pandas", "Flask", "Chart.js"],
            "features": ["7-day forecast", "Interactive charts", "Historical data analysis"],
        },
        {
            "id": 2,
            "name": "Heart Risk Classifier",
            "description": "Machine learning pipeline for predicting heart disease risk",
            "tech_stack": ["Python", "Scikit-learn", "Pandas", "Numpy", "Matplotlib"],
            "features": ["Risk assessment", "Model explainability", "Data visualization", "Export reports"],
    },
        {
            "id": 3,
            "name": "Portfolio Website",
            "description": "Dynamic portfolio website with AI chatbot using Flask backend",
            "tech_stack": ["Python", "Flask", "JavaScript", "CSS3", "HTML5"],
            "features": ["Interactive chatbot", "Flask backend", "Dynamic content", "Contact form"],
            
        },
        {
            "id":4,
            "name":"AI-powered Artisian Hub",
            "description":"Group Project. Dynamic website for local artisians to sell their ptoducts with right market price",
            "tech_stack": ["Python","pytorch","Scikit-learn", "Flask", "JavaScript", "CSS3", "HTML5","React js","Node js"],
            "features": ["Interactive chatbot", "Responsive design", "Dynamic content", "AI powerd Image recognation","AI powered price generator",
            "AI powered product discription"],
            "database": "MySQL",
            "github": "https://github.com/P-SAV06/ArtisianHub2.git",

        },
    ],
    "certifications": [
        {
            "Internship": "Young Innovator Internship",
            "Company": "Scaler School of Technology",
            "duration": "June 2024 - September 2024",
            "description": "Gained hands-on experience with various AI tools and technologies. Developed proficiency in AI video annotations for Model training. Earned a certificate of excellence in the innovator internship."
        },
        {
            "Degree": "Minors in Artificial Intelligence and Machine Learning",
            "provider": "Indian Institute of Technology Ropar",
            "duration": "2024 - Present",
            "description": "Pursuing Minor Degree in AL/ML from IIT ropar"
        },
    ],
}
CHATBOT_KNOWLEDGE = {
    "greetings": [
        "Hello! I'm Surya's AI assistant. How can I help you know about his portfolio?",
        "Hi there! I can tell you about Surya's projects, skills, certifications, and more. What would you like to know?",
        "Hey! Welcome to Surya's portfolio. Ask me anything about his work!"
    ],
    "about": [
        f"Surya Akhil Varma is a passionate {PORTFOLIO_DATA['personal_info']['role']}. {PORTFOLIO_DATA['personal_info']['bio']}",
        f"Surya is located in {PORTFOLIO_DATA['personal_info']['location']} and specializes in AI/ML and learning Data Structures & Algorithms.",
        "Surya is currently studying Computer Science and working on practical ML projects while preparing for technical interviews."
    ],
    "Internship":[
        "If its an internship i think Surya is a perfect fit for it as has a decent knowledge on Python and Machine Learning Fundamentals."
        "He has a good knowledge on ML algorithms like Regressions, Data Visualization, NeuralNetworks."
        "He also did some realtime implementation of these ML algorithms which you can find in his projects section."
    ],
    "projects": [
        f"Surya has worked on {len(PORTFOLIO_DATA['projects'])} projects including:",
        "Here are Surya's key projects:"
    ],
    "skills": [
        f"Surya's technical skills include:",
        f"Surya is proficient in the following technologies:"
    ],
    "education": [
        f"Surya is pursuing his Bachelor of Technology in Computer Science Engineering at CMR ENGINEERING COLLEGE with a CGPA of 8.7. "
        f"He completed his Intermediate (12th Grade) in MPC with a score of 925. "
        f"He completed his schooling at Triveni Talent School with a CGPA of 9.7."
    ],
    "Additional Course's":[
        f"Surya is pursuing his Minor degree in AI/ML from IIT ropar "
        f"He had completed a Young Innovator Internship from Scaler School of Technology where he had gained hands on exprience in using AI tools efficiently"
    ],
    "contact": [
        f"You can reach Surya at {PORTFOLIO_DATA['personal_info']['email']} or connect with him on GitHub: {PORTFOLIO_DATA['personal_info']['github']}",
        f"Contact Surya via email: {PORTFOLIO_DATA['personal_info']['email']} or LinkedIn: {PORTFOLIO_DATA['personal_info']['linkedin']}"
    ]
}
def generatechatbotresponse(user_message):
    message_lower = user_message.lower()
    if any(word in message_lower for word in ["hello", "hey", "greetings"]) or message_lower.strip() in ["hi", "hi there", "hey there"]:
        return CHATBOT_KNOWLEDGE["greetings"][0]
    elif (any(word in message_lower for word in [
    "project", "projects", "work", "built", "developed", "created"]) or
    "tell me about his projects" in message_lower or 
    "tell me about surya's projects" in message_lower):
        response = CHATBOT_KNOWLEDGE["projects"][0] + "\n\n"
        for i, project in enumerate(PORTFOLIO_DATA["projects"][:3], 1):
            response += f"{i}. **{project['name']}**: {project['description']}\n"
            response += f"   Tech: {', '.join(project['tech_stack'][:3])}\n\n"
        response += "You can find more details on his Github!"
        return response
    elif (any(word in message_lower for word in ["who", "introduce"]) or 
          ("about" in message_lower and not any(word in message_lower for word in ["project", "skill", "education", "certification", "his", "surya"]))):
        return CHATBOT_KNOWLEDGE["about"][0]
    elif any(word in message_lower for word in ["skill", "technology", "programming", "languages", "tools"]):
        response = CHATBOT_KNOWLEDGE["skills"][0] + "\n\n"
        for category, skills in PORTFOLIO_DATA["skills"].items():
            response += f"**{category.title().replace('_', ' ')}**: {', '.join(skills)}\n"
        return response
    elif any(word in message_lower for word in ["certification", "certifications", "coursework", "intern", "internship", "course", "training"]):
        response = "Surya's certifications and additional coursework:\n\n"
        for cert in PORTFOLIO_DATA["certifications"]:
            response += f"**{cert['name']}**\n"
            response += f"{cert['provider']} ({cert['duration']})\n"
            response += f"{cert['description']}\n\n"
        return response
    elif any(word in message_lower for word in ["education", "degree", "university", "college", "study"]):
        response = "Surya's educational background:\n\n"
        for edu in PORTFOLIO_DATA["education"]:
            response += f"**{edu['degree']}**\n"
            response += f"{edu['institution']} ({edu['duration']})\n"
            response += f"{edu['description']}\n\n"
        return response
    elif any(word in message_lower for word in ["contact", "email", "reach", "connect", "linkedin", "github"]):
        return CHATBOT_KNOWLEDGE["contact"][0]
    else:
        return "I can help you learn about Surya's projects, skills, certifications, education, or contact information. What specific area interests you?"
@app.route('/')
def My_Portfolio():
    return render_template("index.html", 
                         portfolio_data=PORTFOLIO_DATA)
@app.route('/My_Profile')
def My_Profile():
    return render_template("profile.html", 
                         portfolio_data=PORTFOLIO_DATA)
@app.route('/My_Education')
def My_Education():
    return render_template("education.html", 
                         portfolio_data=PORTFOLIO_DATA)
@app.route('/certifications')
def certifications():
    return render_template("certifications.html", 
                         portfolio_data=PORTFOLIO_DATA)
@app.route('/projects')
def projects():
    return render_template("projects.html", 
                         portfolio_data=PORTFOLIO_DATA)
@app.route('/contact')
def contact():
    return render_template("contact.html", 
                         portfolio_data=PORTFOLIO_DATA)
@app.route('/chatbot')
def chatbot():
    return render_template("chatbot.html", 
                         portfolio_data=PORTFOLIO_DATA)
@app.route('/api/chat', methods=['POST'])
def chat_api():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        response = generatechatbotresponse(user_message)
        return jsonify({"answer": response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/projects')
def api_projects():
    return jsonify(PORTFOLIO_DATA["projects"])

@app.route('/api/skills')
def api_skills():
    return jsonify(PORTFOLIO_DATA["skills"])

if __name__ == "__main__":
    app.run(debug=True, port=8000)
    