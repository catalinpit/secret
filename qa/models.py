import math
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.html import mark_safe
from markdown import markdown

'''
Code written by myself following the tutorial: https://simpleisbetterthancomplex.com/series/beginners-guide/1.11/
'''

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    # get the answers for each question in a specific topic
    def answers_count(self):
        return Answer.objects.filter(question__topic = self).count()

    # count the questions for each topic
    def questions_count(self):
        return Question.objects.filter(topic = self).count()

    # return the latest answer for each question in a specific topic
    def latest_answer(self):
        return Answer.objects.filter(question__topic = self).order_by('-created_at').first()

class Question(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, related_name='questions', on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject

    # count the number of answers
    # return the number of pages
    def get_page_count(self):
        count = self.answers.count()
        pages = count / 5
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def get_last_ten_answers(self):
        return self.answers.order_by('-created_at')[:10]

class Answer(models.Model):
    message = models.TextField(max_length=4000)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return (Truncator(self.message)).chars(30)

    def message_to_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
