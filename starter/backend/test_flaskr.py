import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres:postgres@{}/{}".format('localhost:5432', self.database_name)
       
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()



        self.new_question = {
            'question':'what is my name?',
            'answer':'I don;t know',
            'difficulty':3,
            'category':1
        }

        
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def testing_categories_true(self):
        res = self.client().get('/categories')
        data =res.get_data()
        self.assertEqual(res.status_code,200)
        self.assertTrue(data)


    def testing_categories_questions_true(self):
        res = self.client().get('/categories/1/questions')
        data =res.get_json()
    
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['current_category'],'Science')

    def testing_categories_questions_false(self):
        res = self.client().get('/categories/44/questions')
        data =res.get_json()
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)

    
    def testing_questions_true(self):
        res = self.client().get('/questions?page=1')
        data =res.get_json()

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])

    def testing_questions_false(self):
        res = self.client().get('/questions?page=1444')
        data =res.get_json()

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        

    def testing_add_question_true(self):
        res = self.client().post('/questions',json=self.new_question)

        self.assertEqual(res.status_code,200)
        self.assertEqual(res.get_json()['success'],True)    

    def testing_add_question_false(self):
        res = self.client().post('/questions')

        self.assertEqual(res.status_code,400)
        self.assertEqual(res.get_json()['success'],False)


    def testing_search_true(self):
        res = self.client().post('/questions/search',json={'searchTerm':'what'})

        self.assertEqual(res.status_code,200)
        self.assertEqual(res.get_json()['success'],True)


    def testing_search_false(self):
        res = self.client().post('/questions/search')

        self.assertEqual(res.status_code,400)
        self.assertEqual(res.get_json()['success'],False)


    def testing_quiz_true(self):
        res = self.client().post('/quizzes',json={'quiz_category':{'id':1,'type':'Science'},'previous_questions':[]})

        self.assertEqual(res.status_code,200)
        self.assertEqual(res.get_json()['success'],True)

    def testing_quiz_false(self):
        res = self.client().post('/quizzes')

        self.assertEqual(res.status_code,400)
        self.assertEqual(res.get_json()['success'],False)







# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()