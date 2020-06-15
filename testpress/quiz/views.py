from flask import render_template, url_for, flash, request, redirect, Blueprint
import json
from testpress import db,models
from testpress.models import qanda
import requests
import random
import datetime

quiz = Blueprint('quiz',__name__)

global score
score = 0
global start_time
start_time = datetime.datetime.now()

@quiz.route('/',methods = ['GET','POST'])
def index():
    return render_template('index.html')

@quiz.route('/quizapi',methods = ['GET','POST'])
def get_api():
    global start_time
    start_time = datetime.datetime.now()
    models.qanda.query.delete()
    uri= 'https://opentdb.com/api.php?amount=10&category=9&difficulty=easy&type=multiple'
    data = requests.get(uri)
    data = data.json()
    questions = data['results']
    i = 0
    for question in questions:
        question_str = json.dumps(question) 
        qanda_input = qanda(question = question_str,answer=None,id=i)
        db.session.add(qanda_input)
        db.session.commit()
        i = i+1
    global score
    score = 0
    return redirect(url_for('quiz.questions_display',question_id = 0))

@quiz.route('/quiz/<int:question_id>',methods = ['GET','POST'])
def questions_display(question_id):
    global start_time
    start_time.time()
    global score
    if question_id < 10:
        question_input = models.get_question(question_id)
        question = json.loads(question_input.question)
        i = question_id
        choices = question['incorrect_answers']
        choices.append(question['correct_answer'])
        random.shuffle(choices)
        return render_template('quiz.html',question = question, i = question_id, choices= choices,unhide = 0 )
    else:
        all_ques_obj = qanda.query.all()
        all_questions = []
        all_answers= []
        for i in all_ques_obj:
            question = json.loads(i.question)
            all_questions.append(question['question'])
            all_answers.append(i.answer)
        total_time = datetime.datetime.now() - start_time
        timer =  total_time.total_seconds()/60
        timer = round(timer,2)
        context = {all_questions[i]: all_answers[i] for i in range(len(all_questions))}
        
        return render_template('finish.html',context = context,score = score,timer = timer)

@quiz.route('/check_answers',methods = ['GET','POST'])
def check_answers():
    data = request.form['option'].split('+')
    selected_answer = data[0]
    question_id = int(data[1])
    question = models.get_question(question_id)
    question.answer = selected_answer
    db.session.commit()
    question = json.loads(question.question)
    choices = question['incorrect_answers']
    choices.append(question['correct_answer'])
    if question['correct_answer'] == selected_answer:
        global score
        score = score + 1
        return render_template('quiz.html',answer = 1,question= question,choices=choices, i = question_id, correct_answer = selected_answer, unhide = 1)
        #return 'correct'
    else:
        return render_template('quiz.html', answer = 0, unhide = 1,question= question,choices=choices, i = question_id)
        #return 'incorrect'


