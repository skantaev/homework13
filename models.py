# -*- coding: utf-8 -*-

from datetime import datetime
from guest_book_improved.app import db


# Таблица для записей
class GuestBookItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Поле автор
    author = db.Column(db.String(30), nullable=False)
    # Поле содержимое
    content = db.Column(db.String(3000), nullable=False)

    # Дата создания
    date_created = db.Column(db.DateTime, default=datetime.now)
    # Поле "обновлено"
    updated_at = db.Column(db.DateTime, default=datetime.now)

    # Поле "удалено", для видимости записи
    deleted = db.Column(db.Boolean, default=False, nullable=False)

    def __str__(self):
        return '<Author %r, id %s>'.format(self.author, self.id)

    # Преобразование в словарь
    def to_dict(self):
        return {
            'id': self.id,
            'author': self.author,
            'content': self.content,
            'date created': self.date_created,
            'updated at': self.updated_at,
            'deleted': self.deleted
        }
