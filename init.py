from random import randint, shuffle
from quiz import get_question_after, get_quises, check_answer
from flask import Flask, session, redirect, url_for, render_template
from flask import request



def start_quiz(quiz_id):
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['answers'] = 0
    session['total'] = 0

def end_quiz():
    session.clear()

def quiz_form():
    q_list = get_quises()
    return render_template('Quiz\start.html', q_list=q_list)

def index():
    if request.method == 'GET':
        start_quiz(-1)
        return quiz_form()
    else:
        quiz_id = request.form.get('quiz')
        start_quiz(quiz_id)
        redirect(url_for('test'))


def save_answers():
    answer = request.form.get('ans_text')
    quest_id = request.form.get('q_id')
    session['last_question'] = quest_id
    session['total'] += 1
    if check_answer(quest_id, answer):
        session['answers'] += 1


def question_form(question):
    answers_list = [
        question[2], question[3], question[4], question[5]
    ] 
    shuffle(answers_list)
    return render_template('test.html', question=question[1], question_id = question[0], answers_list=answers_list)


def test():
    if not('quiz' in session) or int(session['quiz'])<0:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            save_answers()

        result = get_question_after(session['last_question'] , session['quiz'])
        if result is None or len(result) == 0:
            return redirect(url_for('result'))
        else:
            return question_form(result)

def result():
    end_quiz()
    return render_template('result.html', right=session['answer'], total=session['total'])

import os
folder = os.getcwd()
app = Flask(__name__, template_folder=folder, static_folder=folder)
app.add_url_rule('/', 'index', index, methods=['post', 'get'])
app.add_url_rule('/test','test',test, methods=['post', 'get'])
app.add_url_rule('/result','result',result)
app.config['SECRET_KEY'] = 'LILINKO'
if __name__ == '__main__':
    app.run()