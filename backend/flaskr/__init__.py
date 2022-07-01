import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
categories = Category.query.order_by(Category.id)

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1)*QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    question_page = [question.format() for question in selection]
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
        query_categories = Category.query.order_by(Category.type).all()
        if len(query_categories) ==0:
            abort(404)
        
        return jsonify({
            "Success": True,
            "Categories":   Category.type,

        })

    
    #TODO:
   
    #Retrieve questions and group them in pages of 10 questions to a page
    @app.route("/questions")
    def get_paginated_questions():
        selection = Question.query.order_by(Question.id).all()
        questions_view = paginate_questions(request, selection)

        if len(questions_view) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "Questions": questions_view,
                "Number of Questions": len(Question.query.all()),
                "Current Category":Question.category,
                "Categories": categories,
            }
        )
    
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
                    "Success": True,
                    "Deleted": question_id,
                    "Questions": questions_view,
                    "Total Number of Books": len(Question.query.all()),
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
                "Success": True,
                "Created": questions.id,
                "Questions": questions_view,
                "Total Number of Questions": len(Question.query.all()),
                }
            )

        except:
            abort(422)
    
    #TODO:
   
    #Search for specific question
    #Partials strings have been implemented
    @app.route('/questions/search')
    def search_questions():
        searh_term = request.args.get("question")
        questions = Question.query.filter(Question.question.ilike(f"%{searh_term}%")).all()
        results =[]

        for quest in questions:
            results.append({
                "Question No:": quest.id,
                "Questions:": quest.question,
            })
        return jsonify(results)

 
    #TODO:
        
    #Query questions based on categories
    @app.route('/categories/<str:category_type>/question', methods=['GET'])
    def filter_questions_by_categroy(category_type):
        try:
            filter_questions = Question.query.filter(Question.category==category_type).all()
            if filter_questions is None:
                abort(404)
            filtered = paginate_questions(request, filter_questions)
            return jsonify({
                "Success": True,
                "Category": category_type,
                "QUestions": filtered,
                "Number of Questions": len(filter_questions),
            })
        except:
            abort(422)
        

   
    #TODO:
    
    #Play Quizzes
    @app.route('/quizzes')
    def play_quizzes():
        try:
            data = request.get_json()
            quiz_category= data.get('quiz_category')
            category = Category.query.get( quiz_category)
            previous_questions = data.get('previous_questions')
            if not 'previous_question' and 'quiz_category' in data:
                abort(422)
            if category['type'] =='click':
                next_question = Question.query.filter_by(Question.id.notin_(previous_questions)).all()
            else:
                next_question = Question.query.filter(category['id']).filter(~Question.id.notin_(previous_questions)).all()
            return jsonify({
                "success": True,
                "Question": random.choice(next_question).format() if next_question else None, 
            })

        except:
            abort(422)
 
    #TODO:
    
    #Handlers to for Errors
    #Resource Not Found
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "Success": False,
            "Error": 404,
            "Message": "Resource Not Found"
        }), 404
    #Catch unprocessable errors
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "Success": False,
            "Error": 422,
            "Message": "Unprocessable Request"
        }), 422
    #Bad Request error
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "Success": False,
            "Error": 400,
            "Message": "Bad Request"
        }), 400
    #Catch Method not allowed errors
    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "Success": False,
            "Error": 405,
            "Message": "Method Not Allowed"
        }), 405
    #Request Timeout
    @app.errorhandler(408)
    def request_timeout(error):
        return jsonify({
            "Success": False,
            "Error": 408,
            "Message": "Request Timeout"
        }), 408

    
    return app

