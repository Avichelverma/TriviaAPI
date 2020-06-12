# Full Stack Trivia API Backend

Trivia APIs are RESTful API that allows people to play the game of trivia by have their own frontend but fetching questions and categories from the API services.

The api allows:
    1. Display list of questions and categories.
    2. Delete Questions
    3. Add questions to the database
    4. Search for questions in the database using string query.
    5. Play a game of quiz, random questions on the basis of category.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Run the Frontend script

The frontend app is built on React. In order to run the app use ```npm start```.

Open ```localhost:3000``` to view the frontend in the browser.

## API Reference Guide

### Getting Started

- Frontend URL: ```http://localhost:3000/```
- Backend URL : ```http://127.0.0.1:5000/ or localhost:5000/```

No Authentication or API keys are required for this project.

### Endpoints

#### GET/categories

- Returns list of categories with id and type.
- Sample command : ```curl -X GET localhost:5000/categories```
```
{
  "categories": {
    "1": "Science",       
    "2": "Art",
    "3": "Geography",     
    "4": "History",       
    "5": "Entertainment", 
    "6": "Sports"
  },
  "success": true
}
```
#### GET/questions

- Returns a list of all questions
- Questions are paginated
- Individual pages could be requested using query string ```?pages=1```

- Sample command : ```curl -X GET localhost:5000/categories```
```
{
  "categories": {
    "1": "Science",       
    "2": "Art",
    "3": "Geography",     
    "4": "History",       
    "5": "Entertainment", 
    "6": "Sports"
  },
  "success": true
}

C:\Users\avich\Desktop\FullStack NanoDegree\TriviaAPI\starter>curl -X GET localhost:5000/questions     
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 20
}
```

#### DELETE /questions/<int:question_id>

- Deletes a question with question_id from URL parameters

- Sample command : ```curl -X DELETE localhost:5000/questions/5```
```
{
  "message": "Successfully deleted question",
  "success": true
}
```

#### POST /questions

- Creates a new question and inserts the payload in the database
- Request body : {question:string, answer:string, difficult:string, category:string}
```
{
    'success': True,
    'message': 'Question added successfully'
}
```

#### POST /question/search

- Fetches all questions where substring matches to the seach-term (case-insensitive)
- Request body : { searchTerm:string }



#### GET /categories/<int:category_id>/questions

- Fetches a dictionary of questions for a specific category

Sample Command: ```curl -X GET localhost:5000/categories/6/questions```
```
{
  "current_questions": "Sports",
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "France",
      "category": 6,
      "difficulty": 3,
      "id": 30,
      "question": "Who won lastest World cup in Fifa?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

#### POST /quizzes

- Fetches a random question in a specific category which is not previously asked.(no-repeated questions)

### Error Handling

- 200 - Success Code

- Following errors are handled with their status codes:
  - 400 - Bad Error Request
  - 404 - Page Not Found
  - 422 - Unproccessable Request
  - 500 - Internal Server Error

- Errors are returned in json format.
```
{
    'success': False,
    'error': 422,
    'message': 'Unproccessable Request'
}
```

### Author
- Avichel Verma developed the following APIs; Successfully tested the APIs
- Udacity for providing Starter files for Frontend and Backend