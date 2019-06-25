from __future__ import unicode_literals
from django.db import models
from datetime import datetime

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        current_date = str(datetime.now())
        if len(postData['name']) < 2:
            errors['name'] = 'Name should be at least 2 characters'
        if len(postData['alias']) < 2:
            errors['alias'] = 'Alias should be at least 2 characters'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email must be of valid format'
        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters'
        if postData['date_of_birth'] == '':
            errors['date_of_birth'] = "Date of birth can't be left empty"
        # if postData['date_of_birth'] > current_date:
        #     errors['date_of_birth'] = "Date of birth can't be in the future"
        return errors

    def login_validator(self, postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email must be of valid format'
        if not User.objects.filter(email=postData['email']):
            errors['email'] = "Email address not recognized, please register if you haven't already done so."
        # if not User.objects.filter(password=postData['password']):
        #     errors['password'] = "Invalid password, please try again."
        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters'
        return errors

class QuoteManager(models.Manager):
    def contribute_validator(self, postData):
        errors = {}
        if len(postData['quoted-by']) < 3:
            errors['quoted-by'] = 'Quoted by must be at least 3 characters long.'
        if len(postData['message']) < 10:
            errors['message'] = 'Message must be at least 10 characters long.'
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_of_birth = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f"{self.id} {self.first_name} {self.last_name} {self.email}"

class Quote(models.Model):
    content = models.TextField()
    quoted_by = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name="quotes")
    favorited_by = models.ManyToManyField(User, related_name="favorite")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
