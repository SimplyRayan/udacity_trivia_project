
# Trivia
##### The App allows you to test your knowledge on many different categories, you can also add and delete questions!


## Running the project

#### 1.Backend
##### first you might want to create a virtual environment, after that you can run the following:  

```
pip install -r requirements.txt
```

##### Database setup:  
```
psql trivia < trivia.psql
```

##### windows users can run this instead  
 ````
psql -U postgres -f trivia.psql trivia 
 ````
 
##### Running the server :  
 ````
$env:FLASK_APP="__init__"
flask run
 ````
 
 
 
#### 1.Frontend
 ````
npm install
npm start
 ````
 
## Docs

### Error Handling
##### Error are returned as JSON 
```
{'success':False,

'message':'bad request',

'code':400}
```

#####  Error types:
##### 1. 400 : BAD REQUEST
##### 1. 404: RESOURCES NOT FOUND
##### 1. 422:  UNPROCESSABLE REQUEST
##### 1. 500: INTERNAL SERVER ERROR


### ENDPOINTS

 `curl http://127.0.0.1:5000/books?page=3 -X POST -H "Content-Type: application/json" -d '{"title":"Neverwhere", "author":"Neil Gaiman", "rating":"5"}`

#### GET /categories 
##### returns all categories
#####  Request Body: None
#####  Request arguments : None
##### Request Sample : `curl http://127.0.0.1:5000/categories `
##### Response Sample: 
```
[
{"id":1,"type":"Science"},
{"id":2,"type":"Art"},
{"id":3,"type":"Geography"},
{"id":4,"type":"History"},
{"id":5,"type":"Entertainment"},
{"id":6,"type":"Sports"}
]
```

#### GET /categories/{id}/questions
##### returns questions that are part of the specified category 
#####  Request Body: None
#####  Request arguments : `id (required): id of the category`
##### Request Sample : `curl http://127.0.0.1:5000/categories/3/questions`
##### Response Sample: 
```

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
  "totalQuestions": 3
}
```

#### GET /questions

##### returns questions
#####  Request Body: None
#####  Request arguments : `page(optinal): id of the category`
##### Request Sample : `curl http://127.0.0.1:5000/questions?page=2`
##### Response Sample: 
```
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "current_category ": "History",
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Rayan",
      "category": 1,
      "difficulty": 1,
      "id": 26,
      "question": "who made this app?"
    }
  ],
  "success": true,
  "total_questions": 18
}
```

#### POST /questions
##### adding questions to app
#####  (Required) Request Body: `{"question": question [String] ,"answer":answer [String], "category":categoryId [Integer 1..5], "difficulty":difficulty [Integer 1..5] }`
#####  Request arguments : None
##### Request Sample :  `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Is this a good documenation of the API?", "answer":"I hope so", "category":3 ,difficulty:5}`
##### Response Sample: 
```
{
'success':True,

'id':77 
}
```
###### id is the newly created question id.


#### DELETE /questions/{id}
##### delete the specified question 
#####  Request Body: None
#####  Request arguments : None
##### Request Sample : `curl http://127.0.0.1:5000/questions/14 -X DELETE `
##### Response Sample: 
```
{
'success':true
}
```

#### POST /questions/search
##### returns questions that contain strings that  match the search term
##### (Required) Request Body: `{ "searchTerm": search_term [String] }`
#####  Request arguments : None
##### Request Sample : `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "soccer"}`
##### Response Sample: 
```
{
"questions":  [
{
"answer":  "Brazil",
"category":  6,
"difficulty":  3,
"id":  10,
"question":  "Which is the only team to play in every soccer World Cup tournament?"
},
{
"answer":  "Uruguay",
"category":  6,
"difficulty":  4,
"id":  11,
"question":  "Which country won the first ever soccer World Cup in 1930?"
}
],
"success":  true
}
```

#### POST /quizzes
##### return a random questions given a category (optional), and a list of previous questions
##### (Required) Request Body: `{ "quiz_category": Category,previous_questions = [Array of questions]  }`
#####  Request arguments : None
##### Request Sample : `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"category":{"type":"Science", "id":1 },previous_questions =[{ "answer": "Uruguay", "category": 6, "difficulty": 4, "id": 11, "question": "Which country won the first ever soccer World Cup in 1930?" },] }`
##### Response Sample: 
```
{
'success:true,
'question':{
"answer":  "Brazil",
"category":  6,
"difficulty":  3,
"id":  10,
"question":  "Which is the only team to play in every soccer World Cup tournament?"
}
```

## Testing
##### in order to test the application run :  
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## References 
#### [Understanding abort() behavior inside try block](https://stackoverflow.com/questions/17746897/flask-abort-inside-try-block-behaviour) 