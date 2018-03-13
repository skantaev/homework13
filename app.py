# -*- coding: utf-8 -*-

from flask import Flask, request, flash, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

import guest_book_improved.config as config

app = Flask(__name__, template_folder='templates')
app.config.from_object(config)

db = SQLAlchemy(app)


@app.route('/items', methods=['GET', 'POST', 'PUT'])
def index():
    from guest_book_improved.models import GuestBookItem
    from guest_book_improved.forms import ItemFullForm

    # Создание новой записи
    if request.method == 'POST':
        form = ItemFullForm(request.form)

        if form.validate():
            item = GuestBookItem(**form.data)
            db.session.add(item)
            db.session.commit()

            flash('Запись добавлена.')

            # Возвращаем код 201 после создания поста
            resp = make_response(jsonify(item.to_dict()), 201)
            # В заголовке Location выдаем адрес созданной страницы
            resp.headers['Location'] = '/items/{}'.format(item.id)
            return resp

        else:
            flash('Форма не валидна! Запись не была добавлена.')
            flash(str(form.errors))

    # Удаление всех записей
    if request.method == 'PUT':
        # Записи удаляются, если клиент передал пустое тело запроса
        if not request.form:
            GuestBookItem.query.delete()
            db.session.commit()

    items = GuestBookItem.query.all()

    # Вывод всех записей в формате JSON
    return jsonify([i.to_dict() for i in items])


# Маршрутизация для доступа к конкретной записи по id
@app.route('/items/<int:item_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def show_item(item_id):
    from guest_book_improved.forms import ItemFullForm, ItemPatchForm
    from datetime import datetime

    # Получение записи по id из базы данных
    item = GuestBookItem.query.filter_by(id=item_id).first()

    # Если по такому id записи нет, то возвращаем код 204 или 404 в зависимости от метода
    if item is None:
        if request.method != 'DELETE':
            return 'Запись не найдена.', 404
        else:
            return 'Запись не найдена.', 204

    # Редактирование содержания конкретной записи
    if request.method == 'PATCH':
        form = ItemPatchForm(request.form)

        if form.validate():
            # Изменение содержания
            item.content = request.form['content']
            # Обновление поля updated at
            item.updated_at = datetime.now()

            db.session.commit()
            flash('Запись изменена.')

        else:
            flash('Форма не валидна! Запись не была изменена.')
            flash(str(form.errors))

    # Полная замена записи, сохраняется только id
    if request.method == 'PUT':
        form = ItemFullForm(request.form)

        if form.validate():
            item.author = request.form['author']
            item.content = request.form['content']
            item.date_created = datetime.now()
            item.updated_at = datetime.now()
            item.deleted = False

            db.session.commit()

            flash('Запись заменена.')

        else:
            flash('Форма не валидна! Запись не была заменена.')
            flash(str(form.errors))

    # "Удаление" записи, изменяются параметры видимости
    if request.method == 'DELETE':
        item.deleted = True
        db.session.commit()

    # Вывод конкретной записи
    return jsonify(item.to_dict())


if __name__ == '__main__':
    from guest_book_improved.models import *
    db.create_all()

    app.run()
