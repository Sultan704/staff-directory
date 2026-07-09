from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
CORS(app)  
swagger = Swagger(app)  


STAFF = [
    {"id": 1, "job_title": "Research Fellow",       "research_area": "Artificial Intelligence", "area_code": "AI",   "email": "a.fellow@dundee.ac.uk"},
    {"id": 2, "job_title": "Lecturer",               "research_area": "Cyber Security",          "area_code": "CSEC", "email": "b.lecturer@dundee.ac.uk"},
    {"id": 3, "job_title": "Senior Lecturer",        "research_area": "Human-Computer Interaction", "area_code": "HCI",  "email": "c.senior@dundee.ac.uk"},
    {"id": 4, "job_title": "Professor",              "research_area": "Data Science",            "area_code": "DSCI", "email": "d.prof@dundee.ac.uk"},
    {"id": 5, "job_title": "Postdoctoral Researcher","research_area": "Artificial Intelligence", "area_code": "AI",   "email": "e.postdoc@dundee.ac.uk"},
    {"id": 6, "job_title": "Teaching Fellow",        "research_area": "Software Engineering",    "area_code": "SWE",  "email": "f.teach@dundee.ac.uk"},
    {"id": 7, "job_title": "Lecturer",               "research_area": "Cyber Security",          "area_code": "CSEC", "email": "g.lect@dundee.ac.uk"},
    {"id": 8, "job_title": "Research Assistant",     "research_area": "Data Science",            "area_code": "DSCI", "email": "h.assist@dundee.ac.uk"},
    {"id": 9, "job_title": "Senior Lecturer",        "research_area": "Human-Computer Interaction", "area_code": "HCI",  "email": "i.senior@dundee.ac.uk"},
    {"id": 10, "job_title": "Professor",             "research_area": "Software Engineering",    "area_code": "SWE",  "email": "j.prof@dundee.ac.uk"},
]

VALID_AREA_CODES = {s["area_code"] for s in STAFF}
MAX_QUERY_LENGTH = 50  


@app.route("/")
def home():
    """
    Landing route with a summary of available endpoints.
    ---
    responses:
      200:
        description: API status and endpoint list
    """
    return jsonify({
        "message": "Staff Directory API is running.",
        "endpoints": ["/staff", "/staff/<id>"],
        "docs": "/apidocs"
    })


@app.route("/staff", methods=["GET"])
def get_all_staff():
    """
    Get all staff, optionally filtered by research area.
    ---
    parameters:
      - name: area
        in: query
        type: string
        required: false
        description: Filters by area code (e.g. "AI") or partial area name (e.g. "cyber")
    responses:
      200:
        description: A list of staff members
      400:
        description: The area query parameter was invalid
    """
    area = request.args.get("area")

    if area is not None:
        # Input validation: reject empty, whitespace-only, or excessively long values
        area = area.strip()
        if area == "":
            return jsonify({"error": "The 'area' query parameter cannot be empty."}), 400
        if len(area) > MAX_QUERY_LENGTH:
            return jsonify({"error": f"The 'area' query parameter must be under {MAX_QUERY_LENGTH} characters."}), 400

        area_lower = area.lower()
        filtered = [
            s for s in STAFF
            if area_lower == s["area_code"].lower()
            or area_lower in s["research_area"].lower()
        ]
        return jsonify(filtered), 200

    return jsonify(STAFF), 200


@app.route("/staff/<int:staff_id>", methods=["GET"])
def get_staff_by_id(staff_id):
    """
    Get a single staff member by ID.
    ---
    parameters:
      - name: staff_id
        in: path
        type: integer
        required: true
        description: The numeric ID of the staff member
    responses:
      200:
        description: The matching staff member
      404:
        description: No staff member found with that ID
    """
    person = next((s for s in STAFF if s["id"] == staff_id), None)
    if person is None:
        return jsonify({"error": f"No staff member found with id {staff_id}"}), 404
    return jsonify(person), 200


@app.errorhandler(404)
def handle_not_found(e):
    """Catches any unmatched route (e.g. typos in the URL) with a clean JSON error."""
    return jsonify({"error": "Resource not found. See /apidocs for available endpoints."}), 404


@app.errorhandler(500)
def handle_server_error(e):
    """Catches unexpected server errors with a clean JSON error instead of an HTML stack trace."""
    return jsonify({"error": "An unexpected server error occurred."}), 500


if __name__ == "__main__":
    
    app.run(debug=True, port=5000)