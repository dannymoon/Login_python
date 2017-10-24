from __future__ import unicode_literals
from django.db import models
import re


emailREGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
nameREGEX = re.compile(r'^[A-Za-z]+$')
# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 1 or len(postData['last_name']) < 1 or len(postData['email']) < 1 or len(postData['password']) < 1 or len(postData['confirm_password']) < 1:
            errors["all"] = "All fields must be filled"
            return errors
        if len(postData['first_name']) < 3:
            errors["first_name"] = "First name should be more than 2 characters"
        if len(postData['last_name']) < 3:
            errors["last_name"] = "Last name should be more than 2 characters"
        if not nameREGEX.match(postData['first_name']):
            errors["first_name"] = "name fields must be letter characters only"
        if not nameREGEX.match(postData['last_name']):
            errors["last_name"] = "name fields must be letter characters only"
        if not emailREGEX.match(postData['email']):
            errors["email"] = "Email must be in proper format"
        if len(postData['password']) < 8:
            errors["password_length"] = "Password must be at least 8 characters long"
        if postData['password'] != postData['confirm_password']:
            errors["password"] = "Password must match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {} {}>".format(self.first_name, self.last_name)