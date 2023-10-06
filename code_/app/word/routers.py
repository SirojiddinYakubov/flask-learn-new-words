import datetime
import random
from datetime import date, timedelta

from flask import Blueprint, render_template, Request, request, flash, redirect, url_for
# from flask_apispec import marshal_with, use_kwargs
from sqlalchemy import func, or_
from sqlalchemy.orm import load_only, noload
from flask_login import login_required, current_user
from app.core.database import db
from app.core.utils import date_filter
from app.models import Word

# from code_.app.schemas.word_schema import ReadWordSchema, CreateWordSchema, UpdateWordSchema

word_blueprint = Blueprint('word', __name__)


@word_blueprint.route('/', methods=['GET'])
# @marshal_with(ReadWordSchema(many=True))
@date_filter
@login_required
def main(start, end):
    db_question = db.session.query(Word).filter(Word.created_at.between(start, end)).order_by(
        func.random()).first()
    columns = ["title_uz", "title_en", "title_ru"]
    question_titles = {c: getattr(db_question, c) for c in columns}
    question_key = random.choice(list(question_titles.keys()))
    question_title = question_titles[question_key]

    db_answers = db.session.query(Word).filter(Word.id != db_question.id).limit(3).all()
    columns.remove(question_key)
    answer_key = "title_en" if question_key != "title_en" else random.choice(columns)
    answers = [{c: getattr(obj, c) for c in ["id", answer_key]} for obj in db_answers]
    answers.append({"id": db_question.id, answer_key: question_titles[answer_key]})
    random.shuffle(answers)
    ctx = {
        "question": {
            "id": db_question.id,
            "title": question_title
        },
        "answers": answers
    }
    return render_template('word/main.html', **ctx)


@word_blueprint.route('/check-writing-word', methods=['GET', 'POST'])
@date_filter
@login_required
def check_writing_word(start, end):
    db_question = db.session.query(Word).filter(Word.created_at.between(start, end)).order_by(
        func.random()).first()
    columns = ["title_uz", "title_ru"]
    if db_question:
        question_titles = {c: getattr(db_question, c) for c in columns}
        question_key = random.choice(list(question_titles.keys()))
        question_title = question_titles[question_key]
        ctx = {
            "question": {
                "id": db_question.id,
                "title": question_title
            },
            "is_correct": None
        }
    else:
        ctx = {}
    if request.method == "POST":
        data = request.form
        word = data.get('word')
        question_id = data.get('question_id')
        question = db.session.query(Word).where(Word.id == question_id).first()
        excepted = question.title_en.split("[")[0].rstrip()
        ctx = {
            "question": {
                "id": question.id,
                "title": f"{question.title_en} | {question.title_ru} | {question.title_uz}"
            }
        }
        if word and str(word) == str(excepted):
            ctx.update({"is_correct": True})
        else:
            ctx.update({"is_correct": False})
        ctx.update({"word": word})
    return render_template('word/check_writing_word.html', **ctx)


@word_blueprint.route('/list/', methods=['GET'])
@date_filter
@login_required
def list_words(start, end):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    q = request.args.get('q', None, type=str)
    if q:
        pagination = Word.query.filter(
            or_(Word.title_uz.icontains(q), Word.title_ru.icontains(q), Word.title_en.icontains(q))).paginate(
            page=page, per_page=per_page)
    else:
        pagination = Word.query.filter(Word.created_at.between(start, end)).order_by(
            Word.created_at.desc()).paginate(
            page=page, per_page=per_page)

    if q:
        words = Word.query.filter(Word.created_at.between(start, end)).filter(
            or_(Word.title_uz.icontains(q), Word.title_ru.icontains(q), Word.title_en.icontains(q)))
    else:
        words = Word.query.filter(Word.created_at.between(start, end))
    words_list = [w.title_en.split("[")[0].rstrip() for w in words]
    # random.shuffle(words_list)
    # for i, w in enumerate(words_list, start=1):
    #     print(f"{i}.{w}", end=" ")
    # # -------------------------------------------------
    # iter = words.all()
    # random.shuffle(iter)
    # for w in iter:
    #     print(f"{w.title_en} - {w.title_uz} - {w.title_ru}")
    return render_template('word/word_list.html', pagination=pagination)


# @word_blueprint.route('/create', methods=['POST'])
# @use_kwargs(CreateWordSchema)
# @marshal_with(ReadWordSchema)
# def create_word(**json_data):
#     obj = Word.create(json_data)
#     return obj


@word_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_word():
    if request.method == 'POST':
        data = request.form
        Word.create(data)
        flash('Object add successfully', 'success')
        return redirect(url_for('word.list_words'))
    return render_template('word/word_create.html', )


@word_blueprint.route('/update/<int:word_id>', methods=['GET', 'POST'])
@login_required
def update_word(word_id):
    if request.method == 'POST':
        data = request.form
        Word.update(word_id, data)
        flash('Object updated successfully', 'success')
        return redirect(url_for('word.list_words'))
    word = Word.get(word_id)
    return render_template('word/word_update.html', word=word)


# @word_blueprint.route('/update/<int:word_id>', methods=['PUT'])
# @use_kwargs(UpdateWordSchema)
# @marshal_with(ReadWordSchema)
# def update_word(word_id, **json_data):
#     obj = Word.update(word_id, json_data)
#     return obj


@word_blueprint.route('/delete/<int:word_id>', methods=['GET'])
@login_required
def delete_word(word_id):
    flash('Object deleted successfully', 'success')
    Word.delete(word_id)
    return redirect(url_for('word.list_words'))
