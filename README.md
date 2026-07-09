# Staff Directory

This is my coursework project for CS22002 (Modern Web Stack Development). It's a staff directory
web page that pulls random people from an external API (randomuser.me) and combines them with
made-up staff info (job title, research area, email) from my own Flask API.

## What's in this repo

```
staff-directory/
├── backend/
│   ├── app.py              -> the Flask API
│   ├── test_app.py         -> tests for the API
│   └── requirements.txt    -> python packages needed
└── frontend/
    ├── index.html
    ├── style.css
    └── script.js
```

## What it does

- Gets 10 random people (name + photo) from randomuser.me
- Gets extra staff details (job title, research area, email) from my own API
- Puts them together into one card per person
- You can search by name, job title or research area
- You can also filter using the dropdown
- Click on a card to see more details in a pop-up
- If something fails to load, it shows a message instead of just breaking
- Layout is responsive (works on phone/tablet/desktop) using Bootstrap

## How to run it

You need two things running at the same time: the backend (the API) and the frontend (the web page).

### 1. Start the backend first

Open a terminal and go into the backend folder:

```bash
cd backend
pip3 install -r requirements.txt
python3 app.py
```

Leave this terminal open. It should say it's running on `http://127.0.0.1:5000`.

### 2. Start the frontend

Open a **second** terminal (keep the first one running) and go into the frontend folder:

```bash
cd frontend
python3 -m http.server 5500
```

Then open your browser and go to `http://127.0.0.1:5500`.

Note: don't just double click index.html to open it, it might not work properly because of how
browsers handle fetch requests from local files. Running it through the command above fixes that.

### 3. (Optional) Run the tests

If you want to check the API is working correctly:

```bash
cd backend
pytest test_app.py -v
```

This runs through 14 checks on the API and they should all pass.

## My API

While the backend is running, you can see the full interactive docs at:

```
http://127.0.0.1:5000/apidocs
```

Here's a quick summary of what it does:

**GET /staff**
Gives back the whole list of staff as JSON.

You can also filter it like this: `/staff?area=AI` — this will only return staff in that
research area. It works with either the short code (like "AI") or part of the full name (like
"cyber" for Cyber Security). It's not case sensitive.

If you leave the area blank or make it too long it'll send back an error instead.

**GET /staff/<id>**
Gives back one staff member by their ID number, e.g. `/staff/1`.
If the ID doesn't exist you'll get a 404 error with a message explaining that.

**GET /**
Just shows that the API is up and lists the routes available.

## Tools used

- HTML, CSS, JavaScript for the frontend, plus Bootstrap for the layout
- Python + Flask for the backend, with Flask-CORS so the frontend can actually talk to it
- Flasgger for the auto-generated API docs
- pytest for testing

## A few notes

- The staff data is just hardcoded in a list in app.py, not a real database, since that's all
  this assignment needed.
- If the staff cards don't load and you see a CORS error in the browser console, it might be a
  browser extension (like an ad blocker) blocking local requests, not an actual bug. Try it in
  Incognito mode to check.
- Make sure the backend terminal is still running whenever you're using the site, otherwise the
  staff data won't load (only the photos from randomuser.me would, or nothing at all).
