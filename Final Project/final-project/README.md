# Autostopp Challenge

#### Video Demo: https://youtu.be/5Z5151n-MHE
#### Description:
Autostopp Challenge is a web application acompanies a real world hitchhikers race. Several teams decide on a destination where they hitchhike to. The person who arrives first, wins the race. It is possible to complete additional challenges to receive time bonuses. The available challenges and related bonuses are available in this app. Users can choose from a list of challenges, complete them and share their progress with the other players.
The web app is built using Python, Flask, SQLite, SQLalchemy, JavaScript and HTML/CSS.

## Functionality

### Login and Registration

The user can register with their name, email and password. The inputted password is hashed and stored in the SQLite database. The user can then log in using their email and password.

### Challenges

The user can view the list of challenges available on the platform. The challenges are sorted by name by default, but the user can sort them by time bonus as well. The user can click on a challenge to view the description and reveal a button complete the challenge. Once they complete a challenge, they can mark it as complete by providing a location and some notes. The user cannot mark the same challenge as complete twice.

### Feed

The user can view the progress of other users in the community. The feed displays the name of the user who completed the challenge, the name of the challenge, the bonus points awarded, the location and the timestamp.

### Players

The user can view a scoreboard that displays the name of all registered users and their total bonus points. The total bonus points are calculated as the sum of bonus points awarded for all challenges completed by the user.

## Design choices

The web app is developed as a flask application which can be accessed via the browser. The web app is fully responsive and can be viewed on every device.

### Client side

For the client side the code is written in JavaScript and HTML/CSS. The bootstrap library is used to intergate several interactive design elements like Cards, Accordion, NavBar and Modal.
The repeating elements are contained in the layout.html file whereas the single pages extend this layout using jinja notation.
On the pages Feed, Challenges and Players it is possible to click on the items to get more information as a Modal.

### Server side

The server side code is written in python in two files: app.py and helpers.py. All data is stored in a SQL database. This database contains 3 tables as follows:
CREATE TABLE IF NOT EXISTS "users" (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    hash TEXT NOT NULL);
CREATE TABLE challenges (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    bonus INTEGER NOT NULL,
    link TEXT);
CREATE TABLE IF NOT EXISTS "completed_challenges" (
    id integer primary key NOT NULL,
    challenge_id integer NOT NULL,
    user_id integer NOT NULL,
    notes varchar(40) NULL,
    location varchar(40) NULL,
    timestamp timestamp NOT NULL);

The table completed_challenges joins the two tables users and challenges in case a challenge was completed.
The table challenges uses the unsplash API to store links for the images for the challenges.

To access the sqlite database the library sqlalchemy is used.



## How to run the app

1. Clone the repository to your local machine.
2. Create a virtual environment and activate it.
3. Install the dependencies using `pip install -r requirements.txt`.
4. Set the FLASK_APP environment variable to `app.py`.
5. Set the FLASK_ENV environment variable to `development`.
6. Create the database by running `flask initdb`.
7. Run the app using `flask run`.
8. Open the web app by navigating to `http://localhost:5000` in your web browser.