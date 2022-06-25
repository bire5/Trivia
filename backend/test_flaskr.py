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
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        result = self.client().get('/questions')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['Success'], True)
        self.assertTrue(len(data['Questions']))
        self.assertTrue(len(data['Categories']))
        self.assertTrue(data['Total Number of Questions'])


    def test_404_sent_requesting_questions_beyond_valid_page(self):
        result = self.client().get('/questions?page=7456')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_get_categories(self):
        result = self.client().get('/categories')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_404_sent_requesting_non_existing_category(self):
        result = self.client().get('/categories/7456')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_delete_question(self):
        question = Question(question='new question', answer='new answer',
                            difficulty=1, category="1")
        question.insert()
        deleted_question_id = question.id

        result = self.client().delete(f'/questions/{question.id}')
        data = json.loads(result.data)
        question = Question.query.filter(Question.id == deleted_question_id).one_or_none()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], str(deleted_question_id))
        self.assertEqual(question, None)

    def test_422_sent_deleting_non_existing_question(self):
        result = self.client().delete('/questions/5000')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_add_question(self):
        new_question = {
            'question': 'add_question',
            'answer': 'add_answer',
            'difficulty': 1,
            'category': "1"
        }
        total_questions_before = len(Question.query.all())
        result = self.client().post('/questions', json=new_question)
        data = json.loads(result.data)
        total_questions_after = len(Question.query.all())

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(total_questions_after, total_questions_before + 1)

    def test_422_add_question(self):
        new_question = {
            'question': 'add_question',
            'answer': 'add_answer',
        }
        result = self.client().post('/questions', json=new_question)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")

    def test_search_questions(self):
        search_term = {'searchTerm': 'Udacourse'}
        result = self.client().post('/questions/search', json=search_term)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])

    def test_404_search_question(self):
        search_term = {
            'searchTerm': '',
        }
        result = self.client().post('/questions/search', json=search_term)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    def test_get_questions_per_category(self):
        result = self.client().get('/categories/1/questions')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_get_questions_per_category(self):
        res = self.client().get('/categories/non_existence_category/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    def test_play_quizzes(self):
        next_quiz = {
            'previous_questions': [],
            'quiz_category': {'type': 'Arts', 'id': 5},
        }

        result = self.client().post('/quizzes', json=next_quiz)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_play_quizzes(self):
        next_quiz = {'previous_questions': []}
        res = self.client().post('/quizzes', json=next_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()