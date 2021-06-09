import os
import re
from flask import Flask, json, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random



from models import Question, Category,setup_db, db
import sys 
from random import randrange # to get a random number
from werkzeug.exceptions import HTTPException # used to determine if an error was generated by an abort

QUESTIONS_PER_PAGE = 10


  
  
  # create and configure the app

app = Flask(__name__)

setup_db(app)
CORS(app)

'''
@TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
'''
cors = CORS(app, resources={r"/*": {"origins": "*"}})  # Gotta check this later?





'''
@TODO: Use the after_request decorator to set Access-Control-Allow
'''
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

'''
@TODO: 
Create an endpoint to handle GET requests 
for all available categories.
'''

def get_all_categories(): # this is a helper method that is used to get all categories 
    results = Category.query.all()
    categories = []
    for result in results:
        categories.append({'id':result.id,'type':result.type})
    return categories


@app.route('/categories')
def get_categories():

  try:      
    categories =get_all_categories() # calling the helper method to fetch all categories
    return jsonify(categories)

  except:
    print(sys.exc_info())
    abort(500)



@app.route('/categories/<int:id>/questions')
def get_specific_categories(id):
  try:      
    
    result = Question.query.filter(Question.category==id).all()
    category = Category.query.get(id)
    
    if category ==  None:
      abort(404)

    questions =[]
    for question in result:
        questions.append(question.format())

    response = {
      'questions':questions,
      'totalQuestions':len(questions),
      'current_category':category.type,
      'success':True
    }

    return jsonify(response)

  except Exception as e:  #aborting inside a try get caught here, so I have to abort here again so that it the error handler gets called
    if isinstance(e, HTTPException):  
          abort(e.code)


    print(sys.exc_info())
    abort(400)
  
    
  
'''
@TODO: 
Create an endpoint to handle GET requests for questions, 
including pagination (every 10 questions). 
This endpoint should return a list of questions, 
number of total questions, current category, categories. 

TEST: At this point, when you start the application
you should see questions and categories generated,
ten questions per page and pagination at the bottom of the screen for three pages.
Clicking on the page numbers should update the questions. 
'''

@app.route('/questions')
def get_questions():
  
  try:
    page = request.args.get('page',1,type=int)
    
    question_results = Question.query.all()

    questions = []
    
    for question in question_results:
      questions.append(question.format())


    categories = get_all_categories()

    start = (page-1)*QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE;
    currnet_quetions = questions[start:end]

    if len(currnet_quetions) == 0: # in case current page has not questions
        abort(404)


    response = {
      'questions':currnet_quetions,
      'total_questions':len(questions),
      'categories':categories,
      'current_category ':'History', ## what is this suppose to mean? I send back many questions from different categorires --
      'success':True
    }
    return jsonify(response)

  except Exception as e:
    if isinstance(e, HTTPException):  #aborting inside a try get caught here, so I have to abort here again so that it the error handler gets called
          abort(e.code)
    print(sys.exc_info())
    abort(422)

'''
@TODO: 
Create an endpoint to DELETE question using a question ID. 

TEST: When you click the trash icon next to a question, the question will be removed.
This removal will persist in the database and when you refresh the page. 
'''
@app.route('/questions/<int:id>',methods=['DELETE'])
def delete_question(id):
    
    try:
      question = Question.query.get(id)

      if question is None:
        abort(404)

      db.session.delete(question)
      db.session.commit()


    except Exception as e:
      if isinstance(e, HTTPException):  #aborting inside a try get caught here, so I have to abort here again so that it the error handler gets called
          abort(e.code)

      db.session.rollback()
      db.session.close()
      abort(422)  
    finally:
      db.session.close()
    return jsonify({'success':True})

    
'''
@TODO: 
Create an endpoint to POST a new question, 
which will require the question and answer text, 
category, and difficulty score.

TEST: When you submit a question on the "Add" tab, 
the form will clear and the question will appear at the end of the last page
of the questions list in the "List" tab.  
'''

@app.route('/questions',methods=['POST'])
def add_question():
      
    result = {}
    try:
      data = request.get_json()
      
      new_question = Question(question=data['question'],answer=data['answer'],
      category=data['category'],difficulty=data['difficulty'])
      db.session.add(new_question)
      db.session.commit()
      id = new_question.id

      result ={
        'success':True,
        'id':id
      }
    except:
      # print(sys.exc_info())
      db.session.rollback()
      abort(400)

    finally:
      db.session.close()

    return jsonify(result) 

'''
@TODO: 
Create a POST endpoint to get questions based on a search term. 
It should return any questions for whom the search term 
is a substring of the question. 

TEST: Search by any phrase. The questions list will update to include 
only question that include that string within their question. 
Try using the word "title" to start. 
'''
# searchTerm
@app.route('/questions/search',methods=['POST'])
def search_questions():
    try:
      data = request.get_json()
      if data == None:
        abort(400)

      searchTerm = data['searchTerm']
     

      questions = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all() #getting question that are related to the search term

      result = []
      for question in questions:
          result.append(question.format())
    
    except Exception as e :
      if isinstance(e, HTTPException):  #aborting inside a try get caught here, so I have to abort here again so that it the error handler gets called
          abort(e.code)

      # print(sys.exc_info())
      db.session.rollback()
      abort(422)
    finally:
      db.session.close()
    
    return jsonify({
      'questions':result,
      'success':True
    })

      

'''
@TODO: 
Create a GET endpoint to get questions based on category. 

TEST: In the "List" tab / main screen, clicking on one of the 
categories in the left column will cause only questions of that 
category to be shown. 
'''
## I Think this is already implemented 
# on this endpoint: /categories/<int:id>/questions
# and the in the frontend clicking on a category shows questions related to that category

'''
@TODO: 
Create a POST endpoint to get questions to play the quiz. 
This endpoint should take category and previous question parameters 
and return a random questions within the given category, 
if provided, and that is not one of the previous questions. 

TEST: In the "Play" tab, after a user selects "All" or a category,
one question at a time is displayed, the user is allowed to answer
and shown whether they were correct or not. 
'''

@app.route('/quizzes',methods=['POST'])
def get_quiz_question():
    try:

      data = request.get_json()

      if data == None:
          abort(400)

      category = data['quiz_category']
      previous_questions = data['previous_questions']
      
      questions = []
    
      if category['id'] != 0: #when all categoires are included the frontend send 0 as an id 
        questions = Question.query.filter(Question.category==category['id'] ,~Question.id.in_(previous_questions)).all()
      else:
        questions = Question.query.filter(~Question.id.in_(previous_questions)).all()
      
      if len(questions) == 0:  # in case there was no questions to send back
            return jsonify({
        'success':True,
      })

      random_number = randrange(len(questions))  # choosing a random question from the list
      randomized_quesiton = questions[random_number].format()

      return jsonify({
        'success':True,
        'question':randomized_quesiton
      })
      
    except Exception as e:
      if isinstance(e, HTTPException):  #aborting inside a try get caught here, so I have to abort here again so that it the error handler gets called
          abort(e.code)
      # print(sys.exc_info())
      abort(422)


'''
@TODO: 
Create error handlers for all expected errors 
including 404 and 422. 
'''

@app.errorhandler(400)
def error_400_handler(e):
    return jsonify({
      'success':False,
      'message':'bad request',
      'code':400
    }),400


@app.errorhandler(404)
def error_404_handler(e):
    return jsonify({
      'success':False,
      'message':'resource not found',
      'code':404
    }),404


@app.errorhandler(422)
def error_422_handler(e):
    return jsonify({
      'success':False,
      'message':'Unprocessable',
      'code':422
    }),422

@app.errorhandler(500)
def error_500_handler(e):
    return jsonify({
      'success':False,
      'message':'Internal sever error',
      'code':500
    }),500


# if __name__ == '__main__':
#     print('Running')
#     app.run()