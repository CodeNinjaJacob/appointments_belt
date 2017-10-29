from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django import forms
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):

    def validate_reg(self, postData):

        errors = []

        if len(postData['name']) < 2:
            errors.append("Please enter a name longer than 2 characters")

        if len(postData['alias']) < 2:
            errors.append("Please enter an alias longer than 2 characters")

        if len(postData['password']) < 8:
            errors.append("Please enter a password with at least 8 characters")

        if not re.match(EMAIL_REGEX, postData['email']):
            errors.append("Please enter your email in a valid format")
        
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors.append("This email is already in use")

        if postData['password'] != postData['password_confirm']:
            errors.append("Your password and its confirmation do not match")

        # current_date = datetime.datetime.strptime(str(datetime.date.today()),'%Y-%m-%d')
        # user_birthday = datetime.datetime.strptime(postData['birthday'], '%Y-%m-%d')

        # if user_birthday > current_date:
        #         errors.append("Please ensure that your entered birthdate does not lie in the future")

        # if user_bday == "":
        #     errors.append("Please enter a birthdate")

        if not errors:
            hashed = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(5))
            user = self.create(name = postData['name'] , alias = postData['alias'] , email = postData['email'] , password = hashed, birthday = postData['birthday'])
            return user

        return errors



    def validate_log(self, postData):

        errors = []

        if len(self.filter(email=postData['email'])) > 0:

            user = self.filter(email=postData['email'])[0]
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors.append("Please enter the correct password associated with this account")

        else:
            errors.append("Please enter your email in a valid format")

        if errors:
            return errors

        return user



class AppointmentManager(models.Manager):

    def validate_appointment(self, postData):

        errors = []

        if len(postData['task']) < 1:
            errors.append("Please fill all of the input fields")

        if not postData('date'):
            errors.append("Please fill all of the input fields")

        if not postData('task'):
            errors.append("Please fill all of the input fields")

        if not postData('time'):
            errors.append("Please fill all of the input fields")

        if datetime.strptime(postData['date'], '%Y-%m-%d').date() < datetime.today().date():
            errors.append("Please enter current and future appointments only")

        return errors

            







class User(models.Model):

    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    birthday = models.DateField()

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

class Appointment(models.Model):
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length = 255)
    task = models.CharField(max_length = 255)
    user = models.ForeignKey(User, related_name='appointments', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = AppointmentManager()


