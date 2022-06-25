# API Development and Documentation Final Project

## Trivia App
The Trivia App is a Udacity Practice Project for students and I did this as part of my journey in the Fullstack Nanodegree Course.

The application helps a student or any other person interested in learning about about knowledge in Art, Science and more to answer some questions. It does the following:
Display questions - both all questions and by category as well as showing the difficulty rating and question category by default.
It  offers the ability to add new questions and require that they include question and answer text and also the ability to delete questions.
One can also search for questions based on a text query string and play the quiz game, randomizing either all questions or within a specific category.

## Code Style
This project was done using the [PEP8 Style Guide](https://peps.python.org/pep-0008/)

## Getting Started
Pre-Requisite
Anyone intending to use this project must have Python3, pip and node installed on their local machines. Use the following links for guide on how to install [Python 3](https://docs.python.org/3/using/windows.html), the latest versions of [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/) and [node](https://nodejs.org/en/download/).

You can download a zip version or [Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine.

## How to Start

Environment setup
It is advised that you work on this using a virtual environment so that you can isolate the dependencies for this project and prevent inteference from other dependencies for other projects.
Use the following as guide to setting up a [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment).
These commands may come handy for quick reference.
To install the dependencies, use this:
pip install -r requirements.txt

Database
Use the following commands to 
After starting your Postgres, create a trivia database:

createbd trivia
Populate the database using the trivia.psql file provided. From the backend folder in terminal run:

psql trivia < trivia.psql

Be sure to navigate to the backend directory before running the command.
### Backend
From the backend folder run pip install requirements.txt. All required packages are included in the requirements file.

To run the application run the following commands:
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
For Windows users, use the following commands:
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run

These commands put the application in development and directs the application to use the __init__.py file in the flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. On Windows, look for the commands in the [Flask Documentation](https://flask.palletsprojects.com/en/1.0.x/tutorial/factory/).
The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.


The [backend](./backend/README.md) directory contains completed Flask and SQLAlchemy server. You are free to update the endpoints in the  `__init__.py` and can reference models.py for DB and SQLAlchemy setup. 

> View the [Backend README](./backend/README.md) for more details.

### Frontend
From the frontend folder, run the following commands to start the client:

npm install // only once to install dependencies
npm start 
By default, the frontend will run on localhost:3000.

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. You can edit the endpoints as you see reasonable for the backend you design. To be on the safer side for beginners, read through the frontend code to understand before you begin to make changes.

> View the [Frontend README](./frontend/README.md) for more details.
