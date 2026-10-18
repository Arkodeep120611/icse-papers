from flask import Flask, render_template, send_from_directory, abort
import os
import re

app = Flask(__name__)

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "papers")

SUBJECTS = {
    # GROUP I — LANGUAGES
    "011": "English Language",
    "012": "Literature in English",
    "021": "Assamese",
    "031": "Bengali",
    "041": "Gujarati",
    "051": "Hindi",
    "061": "Kannada",
    "071": "Khasi",
    "081": "Malayalam",
    "091": "Marathi",
    "101": "Nepali",
    "111": "Odia",
    "121": "Punjabi",
    "131": "Tamil",
    "141": "Telugu",
    "151": "Tibetan",
    "161": "Urdu",
    "171": "Mizo",
    "191": "Sanskrit",
    "201": "Lepcha",
    "221": "Arabic",
    "231": "Modern Armenian",
    "251": "Chinese",
    "261": "Dzongkha",
    "271": "French",
    "281": "German",
    "331": "Persian",
    "361": "Spanish",
    "381": "Thai",
    "401": "Garo",
    "421": "Ao-Naga",
    "431": "Portuguese",
    "471": "Tangkhul",

    # GROUP II — CORE SUBJECTS
    "501": "History & Civics",
    "502": "Geography",
    "511": "Mathematics",
    "521": "Physics",
    "522": "Chemistry",
    "523": "Biology",

    # GROUP III — ADDITIONAL SUBJECTS
    "531": "French (Group III)",
    "541": "Spanish (Group III)",
    "551": "German (Group III)",

    "581": "History, Civics & Geography (Thailand) — Paper 1",
    "582": "History, Civics & Geography (Thailand) — Paper 2",

    "601": "Art — Paper 1",
    "602": "Art — Paper 2",
    "603": "Art — Paper 3",
    "604": "Art — Paper 4",

    "631": "Commercial Studies",
    "641": "Economics",
    "651": "Technical Drawing Applications",
    "661": "Robotics & Artificial Intelligence",
    "671": "Basic Data Entry Operator",
    "681": "Home Science",
    "691": "Cookery",
    "701": "Fashion Designing",
    "711": "Dietetic Aide",
    "721": "Physical Education",
    "731": "Hospitality Management",
    "741": "Cashier",
    "751": "Early Years Physical Activity Facilitator",

    "771": "French (Group II)",
    "821": "Environmental Science",
    "841": "Yoga",
    "861": "Computer Applications",
    "871": "Economic Applications",
    "881": "Commercial Applications",
    "891": "Environmental Applications",

    # MUSIC, DANCE AND OTHER SUBJECTS
    "901": "Mass Media & Communication",
    "911": "Hindustani Music",
    "921": "Carnatic Music",
    "931": "Western Music",
    "941": "Indian Dance",
    "951": "Drama",
    "961": "Auto Service Technician",
}


def parse_filename(filename):
    name = os.path.splitext(filename)[0]

    # Extract the three-digit paper code at the beginning
    code_match = re.match(r"^\s*(\d{3})(?=\s|[-_])", name)
    code = code_match.group(1) if code_match else "N/A"

    subject = SUBJECTS.get(code, "Unknown Subject")
    improvement = "IMPROVEMENT" in name.upper()

    return {
        "filename": filename,
        "code": code,
        "subject": subject,
        "improvement": improvement,
    }


@app.route("/")
def home():
    if not os.path.isdir(BASE_DIR):
        abort(404)

    years = sorted(
        [
            folder
            for folder in os.listdir(BASE_DIR)
            if os.path.isdir(os.path.join(BASE_DIR, folder))
        ],
        reverse=True,
    )

    return render_template("index.html", years=years)


@app.route("/year/<year>")
def year_page(year):
    folder = os.path.join(BASE_DIR, year)

    if not os.path.isdir(folder):
        abort(404)

    papers = []

    for file in os.listdir(folder):
        if file.lower().endswith(".pdf"):
            papers.append(parse_filename(file))

    papers.sort(key=lambda paper: (paper["code"], paper["filename"].lower()))

    return render_template(
        "year.html",
        year=year,
        papers=papers,
    )


@app.route("/view/<year>/<path:filename>")
def view_pdf(year, filename):
    folder = os.path.join(BASE_DIR, year)

    if not os.path.isdir(folder):
        abort(404)

    # send_from_directory safely restricts file serving to this folder
    return send_from_directory(folder, filename)


if __name__ == "__main__":
    app.run(debug=True)
