# Staff Directory

This is my coursework project for CS22002 (Modern Web Stack Development). It's a staff directory
web page that pulls random people from an external API (randomuser.me) and combines them with
made-up staff info (job title, research area, email) from my own Flask API.

## Live demo

The site is hosted on GitHub Pages here:
`https://sultan704.github.io/staff-directory/`

The backend API is also deployed (on Render), so the live site above works straight away without
needing to run anything locally:
`https://staff-directory.onrender.com`

Note: the free Render plan spins down when it's not been used for a while, so the very first
request after some idle time can take 20-30 seconds to wake back up. After that it's fast.

## What's in this repo

```
staff-directory/
├── backend/
│   ├── app.py              -> the Flask API
│   ├── test_app.py         -> tests for the API
│   ├── requirements.txt    -> python packages needed
│   └── Procfile             -> tells Render how to start the app
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

## Running it locally

You don't have to run the backend yourself to use the site, since it's already live on Render
(see above). But if you want to run everything locally instead (e.g. to make changes):

### 1. Start the backend

```bash
cd backend
pip3 install -r requirements.txt
python3 app.py
```

This runs at `http://127.0.0.1:5000`.

If you're running it locally, you'll also need to change the `API_BASE_URL` value near the top
of `frontend/script.js` back to `http://127.0.0.1:5000` instead of the live Render URL.

### 2. Start the frontend

In a separate terminal:

```bash
cd frontend
python3 -m http.server 5500
```

Then open `http://127.0.0.1:5500` in your browser.

Don't just double click index.html to open it directly, some browsers block fetch requests from
local files. Running it through the command above avoids that.

### 3. Run the tests (optional)

```bash
cd backend
pytest test_app.py -v
```

14 tests, checking all endpoints and error cases.

## My API

Interactive docs (Swagger UI):
`https://staff-directory.onrender.com/apidocs`

**GET /staff**
Returns the whole list of staff as JSON.

Optional filter: `/staff?area=AI` — matches either the short code (like "AI") or part of the full
name (like "cyber" for Cyber Security). Not case sensitive. Sending an empty or very long value
returns an error instead.

**GET /staff/<id>**
Returns one staff member by ID, e.g. `/staff/1`. Returns a 404 with a message if that ID doesn't
exist.

**GET /**
Shows the API is running and lists the available routes.

## Tools used

- HTML, CSS, JavaScript, Bootstrap for the frontend
- Python, Flask, Flask-CORS for the backend
- Flasgger for the auto-generated API docs
- pytest for testing
- Hosted on GitHub Pages (frontend) and Render (backend)

## A few notes

- The staff data is hardcoded in a list in app.py rather than a real database, since that's all
  this assignment needed.
- If staff cards ever don't load and there's a CORS error in the browser console, it's sometimes
  a browser extension (like an ad blocker) blocking the request rather than an actual bug. Worth
  checking in Incognito mode if that happens.
