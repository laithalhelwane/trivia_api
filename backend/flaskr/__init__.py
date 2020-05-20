import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# function for paginating questions
def paginate(request, questions):
    page_index = request.args.get('page', 1, type=int)
    start = (page_index - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions_formatted = [question.format() for question in questions]
    questions_formatted = questions_formatted[start:end]
    return questions_formatted


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # Initialize CORS
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        # Set Access-Control-Allow Headers
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Method',
                             'GET, POST, DELETE, PATCH, OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        # Handle GET requests for all available categories
        categories = Category.query.all()
        data = {}
        for category in categories:
            data[category.id] = category.type
        # Return Categories and success message to the view
        return jsonify({
            'success': True,
            'categories': data
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():
        '''
        handle GET requests for questions,
        including pagination (every 10 questions)
        '''
        questions = Question.query.all()
        # Paginate the Questions
        questions_formatted = paginate(request, questions)
        if len(questions_formatted) == 0:
            abort(404)
        # Get All Categories
        categories = Category.query.all()
        data = {}
        for category in categories:
            data[category.id] = category.type
        '''
        Return Questions ,Categories,
        total questions and success message to the view
        '''
        return jsonify({
            'success': True,
            'questions': questions_formatted,
            'total_questions': len(questions),
            'categories': data,
        })

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        # Handler to DELETE question using a question ID
        question = Question.query.filter(Question.id == id).one_or_none()
        if question is None:
            abort(404)  # The question is Not Found
        else:
            try:

                question.delete()
                # Return Success message and the id of deleted question.
                return jsonify({
                    'success': True,
                    'deleted': id
                })
            except Exception:
                abort(422)  # unprocessable --> problem in deleting question.

    @app.route('/questions', methods=['POST'])
    def add_question():
        # Handler to POST a new question
        form = request.get_json()
        # if searchTerm is present
        if form.get('searchTerm') is not None:
            search = form.get('searchTerm')
            # get questions that match search Term
            questions_search_result = Question.query.filter(
                Question.question.ilike(f'%{search}%')).all()
            questions_formatted = paginate(request, questions_search_result)
            # Return Success message, search result and total questions.
            return jsonify({
                'success': True,
                'questions': questions_formatted,
                'total_questions': len(Question.query.all())
            })
        else:
            question_text = form.get('question')
            question_answer = form.get('answer')
            question_difficulty = form.get('difficulty')
            question_category = form.get('category')
            '''
            The question and answer text, category,
             and difficulty score are required.
            '''
            if (question_text is None
                    or question_answer is None
                    or question_difficulty is None
                    or question_category is None):
                abort(400)  # Bad request
                # Create and insert a new question
            try:
                question = Question(question=question_text,
                                    answer=question_answer,
                                    category=question_category,
                                    difficulty=question_difficulty)
                question.insert()
                '''
                Return success Massage,
                the id of the new added question and total questions.
                '''
                return jsonify({
                    'success': True,
                    'created': question.id,
                    'total_questions': len(Question.query.all())
                })
            except Exception:
                abort(422)

    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def get_questions_by_category(id):
        # Handel get request to get questions based on category.
        # id is the id of the selected Category
        category = Category.query.filter_by(id=id).one_or_none()
        # if the category dose not exist
        if category is None:
            abort(404)
        # get questions that match with selected category
        questions = Question.query.filter(
            Question.category == str(category.id)).all()

        # paginate questions
        questions_formatted = paginate(request, questions)
        # return Success massage and the results
        return jsonify({
            'success': True,
            'questions': questions_formatted,
            'total_questions': len(Question.query.all()),
            'current_category': category.type
        })

    @app.route('/quizzes', methods=['POST'])
    def get_random_questions():
        # Handles POST request to get questions to play the quiz
        form = request.get_json()
        previous_questions = form.get('previous_questions')
        quiz_category = form.get('quiz_category')
        # if the quiz_category or previous_questions isn't found
        if previous_questions is None or quiz_category is None:
            abort(400)
        else:
            # if no category selected get all questions
            if quiz_category['id'] == 0:
                questions = Question.query.all()
            # get questions in the given category
            else:
                questions = Question.query.filter(
                    Question.category == quiz_category['id']).all()
            # get all unused questions
            not_played_before_questions = []
            for question in questions:
                in_previous = False
                for p in previous_questions:
                    if question.id == p:
                        in_previous = True
                if not in_previous:
                    not_played_before_questions.append(question)
            # if there is no unused question
            if len(not_played_before_questions) == 0:
                return jsonify({
                    'success': True
                })
            else:
                # select random question from the unused questions
                question = random.randrange(
                    0, len(not_played_before_questions), 1)
                # return success massage and the question
                return jsonify({
                    'success': True,
                    'question': not_played_before_questions[question].format()
                })

    # error Handler
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Un processable'
        }), 404

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    return app
