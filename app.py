from flask import Flask, render_template, send_from_directory, abort
import os
import re

app = Flask(__name__)

BASE_DIR = "papers"

SUBJECTS = {

    # GROUP 1 LANGUAGES

    "011": "English Language",
    "012": "English Literature",
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
    "231": "Armenian",
    "251": "Chinese",
    "261": "Dzongkha",
    "271": "French",
    "281": "German",
    "351": "Russian",
    "361": "Spanish",
    "381": "Thai",

    # GROUP 2

    "401": "Classical Guitar",
    "402": "Anglo-Indian Studies",
    "421": "English for Academic Purposes",
    "431": "Portuguese",
    "441": "Korean",
    "471": "Tangkhul",

    "501": "History & Civics",
    "502": "Geography",
    "511": "Mathematics",
    "521": "Physics",
    "522": "Chemistry",
    "523": "Biology",

    # GROUP 3

    "531": "French (Group III)",
    "541": "Spanish (Group III)",
    "551": "German (Group III)",

    "581": "History Elective",
    "582": "Geography Elective",

    "601": "Art Paper 1",
    "602": "Art Paper 2",
    "603": "Art Paper 3",
    "604": "Art Paper 4",

    "631": "Computer Applications",
    "641": "Economics",
    "651": "Technical Drawing Applications",
    "661": "Cookery",
    "671": "Fashion Designing",

    "681": "Home Science",
    "691": "Cookery & Bakery",

    "701": "Fashion Designing",
    "711": "Design & Technology",
    "721": "Physical Education",
    "731": "Hospitality Management",
    "741": "Computer Hardware",
    "751": "Performing Arts",

    "761": "Sanskrit (Group II)",
    "771": "French (Group II)",

    "821": "Environmental Science",
    "841": "Yoga",

    "861": "Commercial Applications",
    "871": "Economic Applications",
    "881": "Commercial Studies",

    "891": "Environmental Applications",

    "901": "Mass Media & Communication",
    "911": "Instrumental Music - Hindustani",
    "921": "Instrumental Music - Carnatic",
    "931": "Western Music Studies",
    "941": "Indian Dance",
    "951": "Drama",
    "961": "Art & Sculpture"
}


def parse_filename(filename):

    name = filename.replace(".pdf", "")

    code_match = re.search(r"\b(\d{3})\b", name)

    code = code_match.group(1) if code_match else "N/A"

    subject = SUBJECTS.get(code, "Unknown Subject")

    improvement = "IMPROVEMENT" in name.upper()

    return {
        "filename": filename,
        "code": code,
        "subject": subject,
        "improvement": improvement
    }


@app.route("/")
def home():

    years = sorted(os.listdir(BASE_DIR), reverse=True)

    return render_template(
        "index.html",
        years=years
    )


@app.route("/year/<year>")
def year_page(year):

    folder = os.path.join(BASE_DIR, year)

    if not os.path.exists(folder):
        abort(404)

    papers = []

    for file in os.listdir(folder):

        if file.endswith(".pdf"):

            papers.append(parse_filename(file))

    papers.sort(key=lambda x: x["code"])

    return render_template(
        "year.html",
        year=year,
        papers=papers
    )


@app.route("/view/<year>/<path:filename>")
def view_pdf(year, filename):

    return send_from_directory(
        os.path.join(BASE_DIR, year),
        filename
    )


if __name__ == "__main__":
    app.run(debug=True)