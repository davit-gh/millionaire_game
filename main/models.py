# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@python_2_unicode_compatible
class Question(models.Model):
    """
    Model for questions.

    :param text: the question text
    :param points: points assigned to a question
    :validators: Validates that 5 < points < 20
    """

    text = models.TextField()
    points = models.IntegerField(
        validators=[MinValueValidator(5), MaxValueValidator(20)]
    )

    def __str__(self):
        return self.text[:40]


@python_2_unicode_compatible
class Answer(models.Model):
    """
    Model for answers.

    :param text: the answer text
    :param is_correct: designates whether an answer is correct
    :param question: Foreign key to Question model
    """

    text = models.CharField(max_length=100)
    is_correct = models.BooleanField()
    question = models.ForeignKey(Question, related_name="answers")

    def __str__(self):
        return self.text


class Profile(models.Model):
    """User profile for storing earned points."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.first_name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a new profile when.

    Called after a new user instance is created
    """
    if created:
        Profile.objects.create(user=instance)
