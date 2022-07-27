import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
#categories = Category.query.order_by(Category.id)

def paginate_questions(request, question_selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    question_page = [question.format() for question in question_selection]
    questions_view = question_page[start:end]

    return questions_view

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    #Setting up Cross Origin Resource Sharing | CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

  

    
    #@TODO: 
    
    
    #Response Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    
    #TODO:
    
    #Retrieve all categories
    @app.route('/categories')
    def get_categories():
        query_categories = Category.query.order_by(Category.id).all()
        if len(query_categories) ==0:
            abort(404)
        
        return jsonify({
            'success': True,
            'categories': [category.type for category in query_categories],

        })

    
    #TODO:
   
    #Retrieve questions and group them in pages of 10 questions to a page
    @app.route("/questions")

    def get_paginated_questions():
        categories = Category.query.order_by(Category.id).all()
        questions_selection = Question.query.order_by(Question.id).all()
        questions_view = paginate_questions(request, questions_selection)
        
        if len(questions_view) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "questions": questions_view,
            "total_questions": len(questions_selection),
            "categories": {category.id: category.type for category in categories},
            "current_category":None,
        })
    
    #TODO:
    
    #Delete a question
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            questions_view = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": questions_view,
                    "total_questions": len(Question.query.all()),
                }
            )

        except:
            abort(422)

    #TODO:
   
    #Add new questions
    @app.route("/questions", methods=["POST"])
    def add_question():
        body = request.get_json()

        add_question = body.get("question", None)
        add_answer = body.get("answer", None)
        add_category = body.get("category", None)
        add_difficulty = body.get("difficulty", None)

        try:
            questions = Question(question=add_question, answer=add_answer, category=add_category, difficulty=add_difficulty)
            questions.insert()

            selection = Question.query.order_by(Question.id).all()
            questions_view = paginate_questions(request, selection)

            return jsonify(
                {
                "success": True,
                "created": questions.id,
                "questions": questions_view,
                "total_qestions": len(Question.query.all()),
                }
            )

        except:
            abort(422)
    
    #TODO:
   
    #Search for specific question
    #Partials strings have been implemented
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        data = request.get_json()
        search_term = data.get('searchTerm', None)
        results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        if search_term:
            show_results = paginate_questions(request, results)
            return jsonify({
                "success": True,
                "questions": show_results,
                "total_questions": len(results),
                #"current_category": None,
            })
           
 
    #TODO:
        
    #Query questions based on categories
    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def filter_questions_by_categroy(id):
        category = Category.query.filter_by(id=id).one_or_none()
        try:
            filter_questions = Question.query.filter_by(category=str(id)).all()
            if filter_questions is None:
                abort(404)
            filtered = paginate_questions(request, filter_questions)
            return jsonify({
                "success": True,
                #"Category": Category.type,
                "questions": filtered,
                "total_questions": len(filter_questions),
                "current_category": category.type,
            })
        except:
            abort(422)
        

   
    #TODO:
    
    #Play Quizzes
    @app.route('/quizzes', methods=['POST'])
    def play_quizzes():
        try:
            data = request.get_json()

            quiz_category = data.get('quiz_category')
            previous_questions = data.get('previous_questions')

            if quiz_category['type'] == 'click':
                questions = Question.query.filter(Question.id.not_in((previous_questions))).all()
            else:
                questions = Question.query.filter_by(
                    category=quiz_category['id']).filter(Question.id.not_in((previous_questions))).all()

            # randomly select next question from available questions
            next_question = questions[random.randrange(0, len(questions))].format() if len(questions) > 0 else None

            return jsonify({
                'success': True,
                'question': next_question
            })
        except:
            abort(422)
 
    #TODO:
    
    #Handlers to for Errors
    #Resource Not Found
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404
    #Catch unprocessable errors
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Request"
        }), 422
    #Bad Request error
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400
    #Catch Method not allowed errors
    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405
    #Request Timeout
    @app.errorhandler(408)
    def request_timeout(error):
        return jsonify({
            "success": False,
            "error": 408,
            "message": "Request Timeout"
        }), 408

    
    return app

