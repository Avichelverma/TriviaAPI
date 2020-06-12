import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'password', 'localhost:5432', self.database_name)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):

        # Test to get dictionary of categories and have a success code of 200
        response = self.client().get('/categories')
        data = json.loads(response.data)

        # Assertion Declarations
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)

    def test_paginated_questions(self):

        # Test to get dictionary of questions in a specific category and have a success code of 200
        response = self.client().get('/questions')
        data = json.loads(response.data)

        # Assertion Declarations
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), 10)

    def test_page_error_bound(self):

        # Test to page bound error and have a status code of 404
        response = self.client().get('/questions?page=100')
        data = json.loads(response.data)

        # Assertion Declarations
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Page Not Found')

    def test_create_question(self):

        # Test to post a question and have a status code of 200
        question_data = {
            'question': 'This is a test question',
            'answer': 'Answer',
            'difficulty': 1,
            'category': 1
        }

        response = self.client().get('/questions', json=question_data)
        data = json.loads(response.data)

        # Assertion Declarations
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_empty_question_data(self):

        # Test to post a empty question and have a status code of 422
        question_data = {
            'question': '',
            'answer': '',
            'difficulty': 1,
            'category': 1,
        }

        response = self.client().post('/questions', json=question_data)
        data = json.loads(response.data)

        # Assertion Declarations
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unproccessable Request')

    def test_delete_question(self):

        # Test to delete a question and have a status code of 200
        response = self.client().delete('/questions/21')
        data = json.loads(response.data)

        # Assertion Declarations
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Successfully deleted question')

    def test_delete_question_id_notexist(self):

        # Test to delete a question with invalid id and have a status code of 422
        response = self.client().delete('/questions/100')

        data = json.loads(response.data)

        # Assertion Declarations
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unproccessable Request')

    def test_search_questions(self):

        # Test to seach a substring in dictionary of questions and have a status code of 200
        request_data = {
            'searchTerm': 'title'
        }

        response = self.client().post('/questions/search', json=request_data)
        data = json.loads(response.data)

        # Assertion Declarations
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_question_notFound(self):

        # Test to seach a substring in dictionary of questions and have a status code of 404
        request_data = {
            'searchTerm': 'zcaer'
        }
        response = self.client().post('/questions/search', json=request_data)
        data = json.loads(response.data)

        # Assertion Declarations
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Page Not Found')

    def test_get_question_by_category(self):

        # Test to get question by categories and get status code of 200
        response = self.client().get('/categories/3/questions')
        data = json.loads(response.data)

        # Assertion Declarations
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(len(data['questions']), 0)
        self.assertEqual(data['current_questions'], 'Geography')

    def test_invalid_category(self):

        # Test to get question by categories with invalid category_id and get status code of 422
        response = self.client().get('/categories/10/questions')
        data = json.loads(response.data)

        # Assertion Declarations
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unproccessable Request')

    def test_play_quiz(self):

        # Test to play quiz and get status code of 200
        request_data = {
            'previous_questions': [2, 4],
            'quiz_category': {
                'type': 'Entertainment',
                'id': 5
            }
        }

        response = self.client().post('/quizzes', json=request_data)
        data = json.loads(response.data)

        # Assertion Declarations
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_quiz_invalid(self):

        # Test to play quiz without any data and get status code of 400

        response = self.client().post('/quizzes', json={})
        data = json.loads(response.data)

        # Assertion Declarations
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Error Request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
