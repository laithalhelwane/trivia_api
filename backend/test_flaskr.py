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
        self.database_path = "postgres://{}@{}/{}".format(
            'postgres:admin', 'localhost:5432', self.database_name)
        self.new_question = {
            'question': 'what is my name',
            'answer': 'laith',
            'difficulty': '1',
            'category': '5'
        }
        self.new_question_bad = {
            'question': 'what is my name',
            'answer': 'laith',
            'category': '5'
        }

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

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')

    def test_delete_question(self):
        question = Question(question=self.new_question['question'],
                            answer=self.new_question['answer'],
                            category=self.new_question['category'],
                            difficulty=self.new_question['difficulty'])
        question.insert()
        questions_len_before_delete = len(Question.query.all())
        question_id = question.id
        res = self.client().delete('questions/{}'.format(question_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(questions_len_before_delete,
                         len(Question.query.all()) + 1)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)

    def test_404_delete_not_exist_question(self):
        res = self.client().delete('questions/100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')

    def test_add_question(self):
        questions_len_before_add = len(Question.query.all())
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertEqual(data['total_questions'], questions_len_before_add + 1)

    def test_400_add_question(self):
        questions_len_before_add = len(Question.query.all())
        res = self.client().post('/questions', json=self.new_question_bad)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad request')
        self.assertEqual(questions_len_before_add, len(Question.query.all()))

    def test_search_question(self):
        res = self.client().post('/questions', json={'searchTerm': 'title'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/6/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(len(data['questions']), 0)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 'Sports')

    def test_404_get_questions_by_category(self):
        res = self.client().get('/categories/201/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')

    def test_get_random_questions(self):
        res = self.client().post('/quizzes',
                                 json={
                                     'previous_questions': [6],
                                     'quiz_category': {'type': 'Entertainment',
                                                       'id': '5'}
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question']['category'], 5)
        self.assertNotEqual(data['question']['id'], 6)
        self.assertTrue(data['question'])

    def test_400_get_random_questions(self):
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
