import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginated_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in questions]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app, resources={'/': {'origins': '*'}})
    '''
  Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        """ Set Access Control """

        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS')

        return response
    '''
  Create an endpoint to handle GET requests for all available categories.
  '''
    @app.route('/categories')
    def get_categories():
        """Get categories endpoint
        This endpoint returns all categories or
        status code 500 if there is a server error
        """

        try:
            categories = Category.query.all()

            # Format categories to match front-end
            categories_dict = {}
            for category in categories:
                categories_dict[category.id] = category.type

            # return successful response
            return jsonify({
                'success': True,
                'categories': categories_dict
            }), 200
        except Exception:
            abort(500)
    '''
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
    @app.route('/questions', methods=['GET'])
    def get_question():

        questions = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.id).all()
        current_page_questions = paginated_questions(request, questions)

        if len(current_page_questions) == 0:
            abort(404)

        categories_dict = {}

        for category in categories:
            categories_dict[category.id] = category.type

        return jsonify({
            'success': True,
            'categories': categories_dict,
            'total_questions': len(questions),
            'questions': current_page_questions
        }), 200

    '''
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        try:
            question = Question.query.get(question_id)
            question.delete()

            return jsonify({
                'success': True,
                'message': "Successfully deleted question"
            }), 200
        except:
            abort(422)

    '''
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route('/questions', methods=['POST'])
    def post_question():

        question_data = request.get_json()

        question = question_data.get('question', '')
        answer = question_data.get('answer', '')
        difficulty = question_data.get('difficulty', '')
        category = question_data.get('category', '')

        if(question == '' or answer == '' or difficulty == '' or category == ''):
            abort(422)
        try:
            question = Question(
                question=question,
                answer=answer,
                difficulty=difficulty,
                category=category)

            # save question
            question.insert()

            return jsonify({
                'success': True,
                'message': 'Question added successfully',
            }), 200
        except:
            abort(422)

    '''
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    @app.route('/questions/search', methods=['POST'])
    def search_question():

        data = request.get_json()
        search_term = data.get('searchTerm')

        if search_term == '':
            abort(422)

        try:
            questions = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()

            if len(questions) == 0:
                abort(404)

            list_paginated_question = paginated_questions(request, questions)

            return jsonify({
                'success': True,
                'questions': list_paginated_question,
                'total_questions': len(list_paginated_question)
            }), 200
        except:
            abort(404)
    '''
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):

        category = Category.query.filter_by(id=category_id).one_or_none()

        if category is None:
            abort(422)

        questions = Question.query.filter_by(category=category_id).all()

        list_paginated_question = paginated_questions(request, questions)

        return jsonify({
            'success': True,
            'questions': list_paginated_question,
            'total_questions': len(questions),
            'current_questions': category.type
        }), 200

    '''
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():

        try:

            body = request.get_json()

            if not ('quiz_category' in body and 'previous_questions' in body):
                abort(400)

            category = body.get('quiz_category')
            prev_questions = body.get('previous_questions')

            if category['type'] == '':
                questions = Question.query.filter(
                    Question.id.notin_((prev_questions))).all()
            else:
                questions = Question.query.filter_by(category=category['id']).filter(
                    Question.id.notin_((prev_questions))).all()

            next_question = questions[random.randrange(
                0, len(questions))].format() if len(questions) > 0 else None

            return jsonify({
                'success': True,
                'question': next_question
            })
        except:
            abort(400)

    '''
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Error Request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Page Not Found'
        }), 404

    @app.errorhandler(422)
    def unproccessable_request(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unproccessable Request'
        }), 422

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    return app
