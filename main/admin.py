# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django import forms
from .models import Question, Answer, Profile


class AnswerInlineFormset(forms.BaseInlineFormSet):
    """Custom inline formset for Answer model."""

    def clean(self):
        """Make sure only one answer is selected as correct."""
        super(AnswerInlineFormset, self).clean()
        checked_count = 0
        for form in self.forms:
            if form.instance.is_correct:
                checked_count += 1
        if checked_count != 1:
            raise forms.ValidationError(
                "One answer must be selected as correct one."
            )


class AnswerInline(admin.TabularInline):
    formset = AnswerInlineFormset
    model = Answer
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Profile)
