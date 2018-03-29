# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import datetime
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^[a-zA-Z0-9]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z ]+$')

class UserManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        if len(postData['name'])<2:
            errors['name']= 'name should be more than 2 characters'
        if not NAME_REGEX.match(postData['name']):
            errors['name_re']= 'name should not contain numbers or simbols'
        if len(postData['username'])<2:
            errors['username']= 'username should be more than 2 characters'
        if not NAME_REGEX.match(postData['username']):
            errors['username_re']= 'username should not contain numbers or simbols'
        if len(postData['password'])<8:
            errors['password']= 'password should be more than 8 characters'
        if not PASSWORD_REGEX.match(postData['password']):
            errors['password_re']= 'password should contain on numbers and characters'
        if postData['password'] != postData['conf_password']:
            errors['conf_password']= 'password should match confirmation password'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_re']= 'Invalid email'

        return errors
    def login_validator(self,postData):
        errors = {}
        user = User.objects.filter(username= postData['username'])
        if len(user)>0:
            user = User.objects.get(username= postData['username'])
            password = user.password
            if not bcrypt.checkpw(postData['password'].encode(), password.encode()):
                errors['password'] = 'Incorrect Password'
        else:
            errors['username']= 'Incorrect username'
        return errors

class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    birth_date  = models.DateField(null= True, blank = True)
    pokes = models.ManyToManyField('self', related_name='pokes_with')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()
# Create your models here.
