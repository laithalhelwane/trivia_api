# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

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

## Trivia API Documentation

### Common Requirements
The following section defines the common requirements For using Trivia API.

#### Protocol and Calls
Any and all Requests sent to Trivia server must use HTTP. Trivia APIs can be called using the following:

##### Host
This application is hosted locally.
All requests must be sent to the following host: localhost:5000

##### Methods
- GET
- POST
- DELETE

### Error Handling
Code Values and Error Messages:
- 404: Not Found (the question or the category is not found)
- 422: Un processable.
- 400: Bad request (some of the required data are missing)
- Errors are returned as JSON in the following format:
```json
{
    'success': False,
    'error': 400,
    'message': 'Bad request'
}
```

### Trivia API Object
The following section details the Trivia Objects and their attributes.

####Question
- id: a **Integer**, the question's id
- question: a **String**, the question's text
- answer: a **String**, the question's answer
- category: a **String**, the question's category
- difficulty: a **String**, the question's difficulty

#### Category
- id: a **Integer**, the category's id
- type: a **String**, the category's type
### Endpoints
- GET '/categories'
- GET '/categories/id/questions'
- GET '/questions'
- POST '/questions'
- DELETE '/questions/id'
- POST '/quizzes'

####GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
- **An example URL**: 
```bash
curl -i -X "GET" "localhost:5000/categories"
```
```json
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
#### GET '/categories/id/questions'
- Fetches a list of all questions in the selected category 
- Request Arguments: id (The category's id) .
- Returns : An object with current category name, list of questions, and total questions number.
- **An example URL**: 
```bash
curl -i -X "GET" "localhost:5000/categories/3/questions"
```
```json
{
  "current_category": "Geography",
  "questions": [
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
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 18
}
```
#### GET '/questions'
- Fetches a list of all questions
- Results are paginated in groups of 10.    
- Request Arguments: None.
- Returns : An object with a 4 keys, categories, that contains a object of id: category_string key:value pairs, a list of questions and total questions number, and success message.
- **An example URL**: 
```bash
curl -i -X "GET" "localhost:5000/questions"
```
```json
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
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
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
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 18
}

```
#### POST '/questions'
- Add a new question
- Search on question(if search term is not included in request)
- Request Arguments: None.
- Returns : An object with a 3 keys, created, that contains the id of the new question total question and success message.
- **An example URL**: 
```bash
curl -i -X POST -H "Content-Type: application/json" -d '{ "question": "How many paintings did Van Gogh sell in his lifetime?", "answer": "One", "difficulty": 4, "category": "2" }' http://localhost:5000/questions
```
```json
{
  "created": 29, 
  "success": true, 
  "total_questions": 19
}
```
- **An example URL (Search)**: 
- Returns: An object with matching result.
```bash
curl http://localhost:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}'
```
```json
{
    "questions": [
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
    ],
    "success": true,
    "total_questions": 21
}
```
#### DELETE '/questions/id'
- Delete a question
- Request Arguments: id (question's id).
- Returns : An object with a 2 keys, deleted, that contains the id of the deleted question, and success message.
- **An example URL**: 
```bash
curl -i -X "DELETE" localhost:5000/questions/5
```
```json
{
  "deleted": 5,
  "success": true
}
```
#### POST '/quizzes'
- Fetch a random questions (within the given category if provided) and that is not one of the previous questions.
- Request Arguments: Category and previous question
- Returns: An object with a 2 keys, question and success message.
- **An example URL**: 
```bash
curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [16], "quiz_category": {"type": "Science", "id": "1"}}' http://localhost:5000/quizzes
```

```json
{
    "question": {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
    },
    "success": true
}

```
## Testing
To run the tests, run
```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```