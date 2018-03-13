# -*- coding: utf-8 -*-
from wtforms_alchemy import ModelForm
from wtforms.fields import StringField
from wtforms.validators import Length
from guest_book_improved.models import GuestBookItem


# Полная форма, принимаются все поля кроме deleted
class ItemFullForm(ModelForm):
    class Meta:
        model = GuestBookItem
        exclude = ['deleted']

    content = StringField(validators=[Length(min=6, max=3000)])


# Форма для изменения только содержимого записи
class ItemPatchForm(ModelForm):
    class Meta:
        model = GuestBookItem
        only = ['content']

    content = StringField(validators=[Length(min=6, max=3000)])
