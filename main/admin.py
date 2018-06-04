# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django import forms
from .models import Question, Answer, Profile


class AnswerInline(admin.TabularInline):
    formset = forms.BaseInlineFormSet
    model = Answer
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Profile)
